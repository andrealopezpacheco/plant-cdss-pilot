import streamlit as st

st.set_page_config(page_title='Implant CDSS | Tooth 16', page_icon='🦷',layout='wide',initial_sidebar_state='expanded')

CSS='''<style>
.stApp, [data-testid="stAppViewContainer"] {background:#FFFFFF;color:#273246;}
[data-testid="stSidebar"] {background:#f9fbfb;border-right:1px solid #e6eded;}
[data-testid="stHeader"] {background:#FFFFFF;}
h1,h2,h3 {color:#435881 !important;letter-spacing:-.02em;}
h1{font-size:2.1rem!important;} h2{font-size:1.42rem!important;}
[data-testid="stMarkdownContainer"] p {line-height:1.55;}
.stButton > button[kind="primary"]{background:#C7CF58;color:#263246;border:0;border-radius:10px;font-weight:700;}
.stButton > button{border-radius:10px;border-color:#489595;color:#435881;}
[data-testid="stMetric"]{background:#f6f9f9;border:1px solid #e6eded;padding:15px;border-radius:12px;}
[data-testid="stAlert"]{border-radius:12px;}
div[data-testid="stVerticalBlockBorderWrapper"]{border-radius:14px;}
a {color:#327e80!important;}
.topline{height:6px;border-radius:10px;background:linear-gradient(90deg,#C7CF58 0 30%,#489595 30% 72%,#435881 72%);margin:4px 0 20px;}
.hero{padding:18px 22px;border:1px solid #e4ebeb;border-radius:16px;background:#fff;margin-bottom:16px;}
.eyebrow{color:#489595;font-size:.72rem;font-weight:750;letter-spacing:.13em;}
.pill{display:inline-block;padding:4px 9px;border-radius:20px;background:#f1f6d5;color:#455217;font-size:.76rem;font-weight:600;}
.choice{border-left:5px solid #489595;background:#f8fbfb;padding:12px 16px;border-radius:8px;margin:8px 0;}
.note{background:#fbfcf4;border-left:4px solid #C7CF58;padding:12px 15px;border-radius:8px;}
</style>'''
st.markdown(CSS, unsafe_allow_html=True)

STEPS=['Case Type','Esthetic Involvement','Patient-Related Factors','Patient Treatment Priority','Prosthetic Factors','Surgical Feasibility','Implant Selection','Surgical Planning','Restorative Planning','Decision Summary']
if 'step' not in st.session_state: st.session_state.step=0

def go(x): st.session_state.step=max(0,min(9,x))
def unfilled(k): return st.session_state.get(k) in [None,'Not assessed','Unknown','Not recorded']
def v(k,default=None):return st.session_state.get(k,default)
def flag(text):st.warning(text,icon='⚠️')
def ref(title,url):st.markdown(f'📖 [{title}]({url})')
def refs(section):
    with st.expander('Evidence & manufacturer references · illustrative, not individualized recommendations',expanded=False):
        if section==7:
            ref('Straumann BLX implant system — official technical catalogue (diameters / lengths)','https://www.straumann.com/content/dam/media-center/straumann/en/documents/brochure/technical-information/450.006-en_low.pdf')
            ref('Straumann Standard Plus tissue-level implant — manufacturer overview','https://www.straumann.com/en/dental-professionals/dental-implants/tissue-level-implant-line/standard-plus-implant.html')
        elif section==8:
            ref('Thoma et al., 2024 — 10-year RCT, 6-mm implants vs 11–15-mm implants with sinus elevation','https://doi.org/10.1111/jcpe.13954')
            ref('Yan et al., 2019 — systematic review, short implants versus sinus floor elevation','https://bmjopen.bmj.com/content/9/10/e029826')
            ref('Aghaloo et al., 2023 — guided and navigation implant surgery, systematic review','https://pubmed.ncbi.nlm.nih.gov/37436945/')
        else:
            ref('Straumann Variobase for Crown AS — angled screw channel, manufacturer information','https://www.straumann.com/content/dam/media-center/straumann/en/documents/brochure/product-information/490.288-en_low.pdf')
            ref('Ashurko et al., 2023 — connective tissue graft and collagen matrix, systematic review','https://doi.org/10.1186/s12903-023-03475-0')

def missing():
    names={'ridge_height':'Residual bone height','ridge_width':'Ridge width','md_bone':'Mesiodistal bone space','interocclusal':'Interocclusal space','supracrestal':'Supracrestal tissue height','mouth_opening':'Mouth opening','sinus':'Sinus assessment'}
    return [val for key,val in names.items() if unfilled(key)]

st.markdown('<div class="topline"></div>',unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="eyebrow">CLINICAL DECISION SUPPORT · RESEARCH PROTOTYPE</div><h1 style="margin:5px 0">Single Implant Planning Explorer</h1><span class="pill">Tooth 16 · Maxillary right first molar</span> &nbsp; <span class="pill">Illustrative evidence rules · V2</span></div>',unsafe_allow_html=True)

with st.sidebar:
    st.markdown('### Case navigation')
    st.caption('Select any module to review or update the case.')
    selected=st.radio('Module',options=list(range(10)),format_func=lambda i:f'{i+1:02d} · {STEPS[i]}',index=st.session_state.step,label_visibility='collapsed')
    if selected!=st.session_state.step: go(selected);st.rerun()
    st.divider()
    st.caption('Educational prototype only · No patient-identifying information · Independent academic concept, not endorsed by ITI or Straumann.')
    if st.button('Reset case',use_container_width=True):
        for k in list(st.session_state.keys()):
            if k!='step': del st.session_state[k]
        go(0);st.rerun()

step=st.session_state.step
st.progress((step+1)/10,text=f'Step {step+1} of 10 — {STEPS[step]}')
st.subheader(f'{step+1:02d}. {STEPS[step]}')

if step==0:
    st.markdown('Choose the extent of tooth replacement. **This pilot evaluates one single implant restoration at tooth 16.**')
    options=['Single Tooth','Short Span (≤ 3 teeth)','Extended Span (> 3 teeth)','Partially edentulous — removable','Edentulous — Maxilla','Edentulous — Mandible']
    st.radio('Case type',options,key='case_type',index=0)
    with st.expander('Case type definitions',expanded=True):
        st.markdown('''- **Single Tooth:** one missing tooth planned to be replaced by an implant-supported crown.\n- **Short Span:** up to three missing teeth; number of implants and pontic design depend on the case.\n- **Extended Span:** more than three missing teeth; implant distribution and prosthesis design require individualized planning.\n- **Partially edentulous — removable:** implant-assisted or implant-retained removable options in a partially dentate arch.\n- **Edentulous — Maxilla:** fully edentulous upper arch requiring assessment for fixed or removable rehabilitation.\n- **Edentulous — Mandible:** fully edentulous lower arch requiring assessment for fixed or removable rehabilitation.''')
    if v('case_type')!='Single Tooth':flag('This category is captured for future expansion. The clinical comparison in this pilot remains restricted to a single missing tooth (16).')
    st.text_input('Tooth designation (FDI)',value='16',disabled=True)
    st.selectbox('Site status',['Healed edentulous ridge','Failing tooth / extraction planned','Fresh extraction socket'],key='site_status')

elif step==1:
    st.radio('Does this case involve an esthetic concern?',['No relevant esthetic concern','Yes — patient-visible esthetic concern','Uncertain / needs evaluation'],key='esthetic')
    st.multiselect('Possible reasons for esthetic priority',['Smile line','Gingival margin discrepancy','Soft-tissue contour deficiency','Immediate implant consideration','Need for provisional / interim restoration','Patient-reported esthetic concern'],key='esthetic_reasons')
    st.info('Esthetic concern can modify the need for provisionalization, soft-tissue management, implant timing and restorative design. It does not automatically indicate immediate implant placement.')

elif step==2:
    st.markdown('For today, these ten categories are recorded at a screening level. Detailed subquestions and evidence rules can be added later.')
    categories=['Medical Fitness','Medications','Radiation Treatment','Growth Status','Oral Hygiene','Compliance','Periodontal Status','Access','Pathology Near Implant Site','Previous Surgeries at Planned Implant Site']
    for i,name in enumerate(categories):
        a,b=st.columns([3,2]);a.write(name)
        with b:st.selectbox(f'{name} level',['Not assessed','Low concern','Requires review','Potential high concern'],key=f'risk_{i}',label_visibility='collapsed')
    flag('A screening label does not establish medical or surgical clearance. High-concern findings trigger formal assessment, not automated approval or denial.')

elif step==3:
    st.radio('Primary patient preference',['No preference yet','Avoid additional surgery','Shorter treatment time','Long-term predictability','Minimize cost'],key='priority')
    st.multiselect('Other considerations',['Fewer appointments','Reduced postoperative discomfort','Esthetics','Retrievability','Easy hygiene and maintenance','Avoid donor-site surgery'],key='secondary_priorities')
    st.slider('Importance of avoiding additional surgery',0,10,5,key='surgery_importance')
    st.caption('Preferences influence comparative trade-offs, not whether a medically contraindicated procedure becomes acceptable.')

elif step==4:
    st.markdown('Enter measurements from the prosthetically driven diagnostic plan. **All numerical fields may be left blank.**')
    a,b=st.columns(2)
    with a:
        st.number_input('Interocclusal / restorative space (mm)',min_value=0.0,max_value=30.0,value=None,step=.5,key='interocclusal')
        st.number_input('Mesiodistal prosthetic space (mm)',min_value=0.0,max_value=30.0,value=None,step=.5,key='md_prosthetic')
        st.selectbox('Gingival margin relative to planned restoration',['Not assessed','Acceptable','Vertical soft-tissue deficiency','Excess / discrepancy'],key='gingival')
        st.selectbox('Contour relative to diagnostic wax-up',['Not assessed','Adequate','Concave ridge defect','Convex / overcontoured anatomy'],key='ridge_contour')
    with b:
        st.selectbox('Occlusal scheme',['Not assessed','Canine guidance','Group function','Other / complex'],key='occlusion')
        st.selectbox('Parafunction',['Unknown','None reported','Possible','Confirmed'],key='parafunction')
        st.selectbox('Antagonist',['Not assessed','Natural tooth','Fixed restoration','Implant-supported restoration','Removable prosthesis'],key='antagonist')
        st.selectbox('Operator restorative experience',['Not assessed','Limited','Intermediate','Advanced'],key='operator_exp')
    st.markdown('**Interpretive prompts**')
    if v('md_prosthetic') is not None and v('md_prosthetic')<7:flag('Restricted mesiodistal prosthetic space: assess neighboring tooth contours, orthodontic space management and crown feasibility. The 7-mm flag is an illustrative review trigger, not a validated threshold.')
    if v('interocclusal') is not None and v('interocclusal')<6:flag('Limited interocclusal clearance: assess restorative material thickness, prosthetic component dimensions and possible space creation. Review trigger only.')
    if v('gingival')=='Vertical soft-tissue deficiency' or v('ridge_contour')=='Concave ridge defect':st.info('Discuss whether soft-tissue volume augmentation (e.g., CTG) is relevant, and whether simultaneous or staged management is preferable.')

elif step==5:
    st.markdown('Measurements should be related to the **planned prosthetically driven implant position**, not merely the narrowest arbitrary CBCT slice.')
    a,b=st.columns(2)
    with a:
        st.number_input('Residual bone height below sinus (mm)',min_value=0.0,max_value=30.0,value=None,step=.5,key='ridge_height')
        st.number_input('Ridge width at proposed implant site (mm)',min_value=0.0,max_value=30.0,value=None,step=.5,key='ridge_width')
        st.number_input('Mesiodistal bone space between adjacent roots (mm)',min_value=0.0,max_value=30.0,value=None,step=.5,key='md_bone')
        st.number_input('Vertical supracrestal soft-tissue height (mm)',min_value=0.0,max_value=12.0,value=None,step=.5,key='supracrestal')
        st.number_input('Measured maximal mouth opening (mm)',min_value=0.0,max_value=75.0,value=None,step=1.,key='mouth_opening')
    with b:
        st.selectbox('Sinus assessment',['Not assessed','No evident disease on initial review','Possible sinus pathology','Previously treated sinus condition'],key='sinus')
        st.selectbox('Adjacent tooth pathology',['Not assessed','None identified','Present / requires evaluation'],key='adjacent_pathology')
        st.selectbox('Horizontal bony defect',['Unknown','None apparent','Present / suspected'],key='horizontal_defect')
        st.selectbox('Vertical bony deficiency',['Unknown','None apparent','Present / suspected'],key='vertical_defect')
        st.selectbox('Residual facial defect after ideal straight-axis placement',['Not assessed','None anticipated','Potential dehiscence / concavity','Potential fenestration'],key='facial_defect')
        st.selectbox('Could implant angulation reduce graft requirements?',['Unknown','Potentially — to be evaluated','Not appropriate based on prosthetic plan'],key='angulation_option')
        st.selectbox('Soft-tissue volume deficiency',['Unknown','No obvious volume deficiency','Present'],key='soft_deficiency')
    st.caption('The system does not auto-clear guided surgery or sinus elevation. Mouth opening, guide stack and drill access must be assessed for the specific system.')

elif step==6:
    st.markdown('### Straumann-based comparison — illustrative candidate systems')
    st.caption('Examples are manufacturer families, **not an exhaustive catalogue** or a product-specific suitability determination. Confirm each diameter–length–connection combination in the current regional Straumann catalogue and instructions for use.')
    height=v('ridge_height');width=v('ridge_width');md=v('md_bone');soft=v('supracrestal')
    a,b=st.columns(2)
    with a:
        with st.container(border=True):
            st.markdown('#### A · Tissue-level candidate')
            st.markdown('**Straumann Standard Plus / tissue-level family**')
            st.write('✅ Transmucosal collar can move the restorative interface away from the bone crest, subject to positioning and tissue architecture.')
            st.write('⚠️ Assess collar position, vertical restorative space, tissue height and visibility in the final soft-tissue contour.')
            st.write('‼️ Do **not** assume a 6-mm tissue-level SKU exists for the chosen line: verify specific length and diameter availability.')
            st.caption('Status: candidate concept only')
    with b:
        with st.container(border=True):
            st.markdown('#### B · Bone-level candidate')
            st.markdown('**Straumann BLX / bone-level family**')
            st.write('✅ Published manufacturer catalogue includes 6-mm and 8-mm length options in defined diameters.')
            st.write('⚠️ Evaluate vertical soft-tissue architecture, abutment height and restorative emergence.')
            st.write('‼️ Requires confirmation of compatible abutments, depth, anatomy and prosthetic space.')
            st.caption('Status: candidate concept only')
    with st.container(border=True):
        st.markdown('#### Dynamic evidence checks')
        if height is None:flag('Residual bone height is missing: cannot assess 6-mm versus 8-mm options.')
        elif height <6:flag('Measured residual height is below the nominal 6-mm implant length. Review safety distances and augmentation/alternative options; no implant is cleared.')
        elif height <8:st.info('Residual bone height falls between 6 and 8 mm. A short-implant strategy and a longer-implant strategy requiring additional assessment may merit comparison; implant length cannot be selected from height alone.')
        else:st.info('Residual height is at least 8 mm. Still assess anatomical safety clearance, implant geometry, depth and prosthetic positioning before selecting an implant.')
        if width is not None:st.write(f'Ridge width provided: **{width:g} mm**. Diameter suitability requires implant-specific geometry and planned buccal/palatal bone envelope.')
        if md is not None:st.write(f'Mesiodistal bone space: **{md:g} mm**. Check adjacent root distances against proposed platform/body geometry.')
        if soft is not None:st.write(f'Supracrestal tissue height: **{soft:g} mm**. Compare tissue-level collar and bone-level abutment architecture in the planned emergence profile.')
    refs(7)

elif step==7:
    st.markdown('### Competing surgical pathways')
    height=v('ridge_height');sinus=v('sinus','Not assessed');width=v('ridge_width');priority=v('priority','No preference yet')
    with st.container(border=True):
        st.markdown('**Pathway A · Short implant without additional sinus augmentation**')
        st.write('✅ May reduce surgical burden, treatment time and cost in appropriately selected posterior maxillary cases.')
        st.write('⚠️ Verify primary stability, bone volume, implant dimensions, occlusal/restorative load and future maintenance.')
        st.write('‼️ Not a substitute for appropriate anatomical clearance or a feasible prosthetic design.')
    with st.container(border=True):
        st.markdown('**Pathway B · Sinus elevation + longer implant**')
        st.write('✅ May allow a longer implant when indicated and anatomically feasible.')
        st.write('⚠️ Adds intervention and possible morbidity; assess sinus anatomy and whether a transcrestal or lateral approach is appropriate.')
        st.write('‼️ Suspected sinus pathology warrants evaluation/management before elective sinus intervention; do not infer that a short implant is automatically safe.')
    with st.container(border=True):
        st.markdown('**Pathway C · Horizontal augmentation / modified implant axis**')
        st.write('✅ Compare graft-based positioning with a modified prosthetically acceptable implant axis where feasible.')
        st.write('⚠️ Altering position may affect emergence profile, load direction or screw-channel accessibility; angulated restorative components do not correct every 3D malposition.')
        st.write('‼️ Avoid treating grafting and angulated abutments as universally interchangeable.')
    st.markdown('**Case-specific prompts**')
    if height is not None and height<8:st.info('Bone height suggests discussing short versus augmented-length treatment concepts. Literature comparisons often examine 6-mm vs 11–15-mm implants, not necessarily 6 vs 8 mm.')
    if sinus in ['Possible sinus pathology','Previously treated sinus condition']:flag('Sinus finding requires appropriate evaluation before determining augmentation feasibility.')
    if v('facial_defect') in ['Potential dehiscence / concavity','Potential fenestration']:flag('Potential facial hard-tissue deficiency relative to the ideal prosthetic axis: assess GBR or other alternatives.')
    if v('mouth_opening') is not None:st.info('Mouth opening documented: verify physical access with the selected implant system, handpiece, drills and guide before labeling fully guided surgery feasible.')
    if priority=='Avoid additional surgery':st.success('Patient preference favors fewer procedures when outcomes and safety remain clinically acceptable. Preference does not overrule surgical feasibility.')
    refs(8)

elif step==8:
    st.markdown('### Prosthetic options — Straumann-compatible concepts')
    a,b=st.columns(2)
    with a:
        with st.container(border=True):
            st.markdown('#### Straight-axis restoration')
            st.write('✅ Straight screw-access channel where implant positioning permits.')
            st.write('⚠️ Confirm sufficient restorative height and accessible hygiene contour.')
            st.write('‼️ A straight axis is not automatically preferable if it requires an unfavorable implant position or hard-tissue compromise.')
    with b:
        with st.container(border=True):
            st.markdown('#### Angled screw-channel restoration')
            st.write('✅ Straumann Variobase for Crown AS is an example of an angled screw-channel solution within documented compatibility limits.')
            st.write('⚠️ Verify implant platform, restorative space, access angle, material, software library and manufacturer IFU.')
            st.write('‼️ Not a universal substitute for bone grafting or correction of unsafe implant placement.')
    st.selectbox('Preferred retention to evaluate',['Not yet selected','Screw-retained','Cement-retained','Both alternatives'],key='retention')
    st.selectbox('Crown material for comparison',['Not yet selected','Monolithic zirconia','Lithium disilicate (conditional on indication)','Metal-ceramic','Other'],key='crown_material')
    st.selectbox('Provisional restoration',['Not yet selected','No provisional anticipated','Interim removable solution','Implant-supported provisional if clinically feasible'],key='provisional')
    st.markdown('**Clinical prompts**')
    if v('parafunction') in ['Confirmed','Possible']:flag('Parafunction reported: review occlusal loading, material selection, restoration design and protective strategies.')
    if v('soft_deficiency')=='Present' or v('ridge_contour')=='Concave ridge defect' or v('gingival')=='Vertical soft-tissue deficiency':st.info('Soft-tissue contour deficiency: compare CTG at implant placement with staged / second-stage soft-tissue augmentation if clinically appropriate.')
    st.info('For a single crown on tooth 16, routine splinting is not a default treatment option. Occlusal protection or a removable appliance may be discussed if indicated.')
    refs(9)

else:
    st.markdown('### Research demonstration summary — not a clinical prescription')
    a,b,c=st.columns(3)
    a.metric('Tooth','16'); b.metric('Bone height',f"{v('ridge_height'):g} mm" if v('ridge_height') is not None else 'Unknown');c.metric('Bone width',f"{v('ridge_width'):g} mm" if v('ridge_width') is not None else 'Unknown')
    st.markdown('**Patient priorities**');st.write(v('priority','Not entered'))
    st.markdown('**Feasible alternatives to assess**')
    st.markdown('''✅ Tissue-level versus bone-level design (subject to product and anatomic verification)  
⚠️ Short implant versus longer implant with augmentation when appropriate  
⚠️ Straight versus angulated restorative solution when prosthetically and anatomically feasible  
‼️ None of these alternatives is automatically recommended by this pilot.''')
    miss=missing()
    if miss:flag('Key data still missing: '+', '.join(miss))
    else:st.success('Key screening fields have been entered. A specialist still needs to review CBCT, medical risks, implant-specific geometry and evidence applicability.')
    st.markdown('**Next research step:** map each branch to explicit inclusion criteria, anatomical constraints, evidence certainty and patient-important outcomes, then validate expert agreement and usability.')

st.divider()
x,y,z=st.columns([1,3,1])
with x:
    if st.button('← Previous',disabled=step==0,use_container_width=True):go(step-1);st.rerun()
with z:
    if st.button('Next →' if step<9 else 'Review from start ↺',type='primary',use_container_width=True):go(step+1 if step<9 else 0);st.rerun()
st.caption('Prototype for research and discussion only. No validated individual risk estimates, automated medical clearance or treatment prescriptions. Not affiliated with ITI or Straumann.')
