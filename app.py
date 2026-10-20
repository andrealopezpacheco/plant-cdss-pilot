import streamlit as st

st.set_page_config(page_title='Implant CDSS | Tooth 16', page_icon='🦷', layout='wide', initial_sidebar_state='expanded')

CSS='''<style>
:root { color-scheme: light; }
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #FFFFFF !important;
    color: #273246 !important;
}
[data-testid="stSidebar"], [data-testid="stSidebarContent"] {
    background-color: #F7FAFA !important;
    color: #273246 !important;
    border-right-color: #E1E9EA !important;
}
[data-testid="stHeader"] { background-color: #FFFFFF !important; }
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] span,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stCaptionContainer"] p,
[data-testid="stRadio"] label,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] label span,
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] label p,
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSlider"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #273246 !important;
}
[data-testid="stRadio"] [role="radiogroup"] label,
[data-testid="stRadio"] [role="radiogroup"] label p {
    color: #273246 !important;
    opacity: 1 !important;
}
[data-testid="stRadio"] [role="radio"] {
    background-color: #FFFFFF !important;
    border-color: #435881 !important;
}
[data-testid="stRadio"] [role="radio"][aria-checked="true"] { border-color: #489595 !important; }
[data-testid="stExpander"], [data-testid="stExpander"] details, [data-testid="stExpander"] summary {
    background-color: #F5F9F9 !important; color: #273246 !important;
}
[data-testid="stExpander"] details > div { background-color: #FFFFFF !important; color: #273246 !important; }
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
[data-baseweb="input"] input,
[data-baseweb="select"] input {
    background-color: #FFFFFF !important;
    color: #273246 !important;
    -webkit-text-fill-color: #273246 !important;
}
[data-baseweb="input"], [data-baseweb="select"] > div,
[data-baseweb="popover"] [role="listbox"] {
    background-color: #FFFFFF !important;
    color: #273246 !important;
    border-color: #B7C5C8 !important;
}
[data-baseweb="select"] span,
[data-baseweb="select"] div,
[data-baseweb="popover"] [role="option"] { color: #273246 !important; }
.stButton > button {
    background-color: #FFFFFF !important;
    border: 1px solid #489595 !important;
    border-radius: 10px !important;
    color: #273246 !important;
    font-weight: 600;
}
.stButton > button[kind="primary"] {
    background-color: #C7CF58 !important;
    border: 1px solid #C7CF58 !important;
    color: #263246 !important;
    font-weight: 750;
}
[data-testid="stProgressBar"] > div { background-color: #E7EEEE !important; }
[data-testid="stProgressBar"] > div > div { background-color: #489595 !important; }
h1, h2, h3, [data-testid="stHeading"] {color: #435881 !important; letter-spacing: -.02em;}
h1{font-size:2.1rem!important;} h2{font-size:1.42rem!important;}
[data-testid="stMarkdownContainer"] p {line-height:1.55;}
[data-testid="stMetric"]{background:#F6F9F9;border:1px solid #E6EDED;padding:15px;border-radius:12px;}
.topline{height:6px;border-radius:10px;background:linear-gradient(90deg,#C7CF58 0 30%,#489595 30% 72%,#435881 72%);margin:4px 0 20px;}
.hero{padding:18px 22px;border:1px solid #E4EBEB;border-radius:16px;background:#FFFFFF;margin-bottom:16px;}
.eyebrow{color:#489595;font-size:.72rem;font-weight:750;letter-spacing:.13em;}
.pill{display:inline-block;padding:4px 9px;border-radius:20px;background:#F1F6D5;color:#455217;font-size:.76rem;font-weight:600;}
.sidebar-card{background:#FFFFFF;border:1px solid #E1E9EA;border-radius:14px;padding:12px;margin-bottom:14px;}
.placeholder{border:1.5px dashed #B7C5C8;border-radius:14px;padding:20px;text-align:center;background:#FFFFFF;color:#6B7280;}
.note{background:#FBFCF4;border-left:4px solid #C7CF58;padding:12px 15px;border-radius:8px;}
.patient{border-left:4px solid #489595;background:#F7FBFB;padding:12px 15px;border-radius:8px;margin-bottom:10px;}
.smalltitle{font-size:0.8rem;color:#489595;font-weight:800;letter-spacing:0.08em;text-transform:uppercase;}
</style>'''
st.markdown(CSS, unsafe_allow_html=True)

STEPS=['Case Type','Esthetic Involvement','Patient-Related Factors','Patient Treatment Priority','Prosthetic Factors','Surgical Feasibility','Implant Selection','Surgical Planning','Restorative Planning','Decision Summary']
if 'step' not in st.session_state: st.session_state.step=0

def go(x): st.session_state.step=max(0,min(9,x))
def unfilled(k): return st.session_state.get(k) in [None,'Not assessed','Unknown','Not recorded','']
def v(k,default=None):return st.session_state.get(k,default)
def flag(text): st.warning(text, icon='⚠️')
def ref(title,url): st.markdown(f'📖 [{title}]({url})')

def refs(section):
    with st.expander('Evidence & manufacturer references · illustrative, not individualized recommendations', expanded=False):
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
    names={'ridge_height':'Residual bone height','ridge_width':'Ridge width','md_bone':'Mesiodistal bone space','interocclusal':'Interocclusal space','supracrestal':'Supracrestal tissue height','mouth_opening':'Mouth opening','sinus':'Sinus assessment','priority':'Primary patient treatment priority'}
    return [val for key,val in names.items() if unfilled(key)]

# HEADER
st.markdown('<div class="topline"></div>', unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="eyebrow">CLINICAL DECISION SUPPORT · RESEARCH PROTOTYPE</div><h1 style="margin:5px 0">Single Implant Planning Explorer</h1><span class="pill">Tooth 16 · Maxillary right first molar</span> &nbsp; <span class="pill">Patient-centered logic</span> &nbsp; <span class="pill">Illustrative evidence rules · V4</span></div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown('### Case navigation')
    st.caption('Select any module to review or update the case.')

    with st.container():
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('**Case image**')
        uploaded = st.file_uploader('Upload case image / CBCT / intraoral photo', type=['png','jpg','jpeg'], key='case_image', label_visibility='collapsed')
        if uploaded is not None:
            st.image(uploaded, use_container_width=True)
        else:
            st.markdown('<div class="placeholder">Insert case image here<br><span style="font-size:0.85rem;">CBCT slice, intraoral photo or radiograph</span></div>', unsafe_allow_html=True)
        st.caption('Recommended over a branded logo. Avoid implying institutional endorsement.')
        st.markdown('</div>', unsafe_allow_html=True)

    selected=st.radio('Module', options=list(range(10)), format_func=lambda i:f'{i+1:02d} · {STEPS[i]}', index=st.session_state.step, label_visibility='collapsed')
    if selected!=st.session_state.step:
        go(selected)
        st.rerun()
    st.divider()
    st.markdown('**Patient-centered focus**')
    st.caption('The tool should compare feasible options according to patient priorities, treatment burden and maintenance implications.')
    st.divider()
    st.caption('Educational prototype only · No patient-identifying information · Independent academic concept, not endorsed by ITI or Straumann.')
    if st.button('Reset case', use_container_width=True):
        for k in list(st.session_state.keys()):
            if k!='step':
                del st.session_state[k]
        go(0)
        st.rerun()

step=st.session_state.step
st.progress((step+1)/10, text=f'Step {step+1} of 10 — {STEPS[step]}')
st.subheader(f'{step+1:02d}. {STEPS[step]}')

if step==0:
    st.markdown('Choose the extent of tooth replacement. **This pilot evaluates one single implant restoration at tooth 16.**')
    options=['Single Tooth','Short Span (≤ 3 teeth)','Extended Span (> 3 teeth)','Partially edentulous — removable','Edentulous — Maxilla','Edentulous — Mandible']
    st.radio('Case type', options, key='case_type', index=0)
    with st.expander('Case type definitions', expanded=True):
        st.markdown('''- **Single Tooth:** one missing tooth planned to be replaced by an implant-supported crown.\n- **Short Span:** up to three missing teeth; number of implants and pontic design depend on the case.\n- **Extended Span:** more than three missing teeth; implant distribution and prosthesis design require individualized planning.\n- **Partially edentulous — removable:** implant-assisted or implant-retained removable options in a partially dentate arch.\n- **Edentulous — Maxilla:** fully edentulous upper arch requiring assessment for fixed or removable rehabilitation.\n- **Edentulous — Mandible:** fully edentulous lower arch requiring assessment for fixed or removable rehabilitation.''')
    st.text_input('Tooth designation (FDI)', value='16', disabled=True)
    st.selectbox('Site status', ['Healed edentulous ridge','Failing tooth / extraction planned','Fresh extraction socket'], key='site_status')

elif step==1:
    st.radio('Does this case involve an esthetic concern?', ['No relevant esthetic concern','Yes — patient-visible esthetic concern','Uncertain / needs evaluation'], key='esthetic')
    st.multiselect('Possible reasons for esthetic priority', ['Smile line','Gingival margin discrepancy','Soft-tissue contour deficiency','Immediate implant consideration','Need for provisional / interim restoration','Patient-reported esthetic concern'], key='esthetic_reasons')
    st.info('Esthetic concern can modify the need for provisionalization, soft-tissue management, implant timing and restorative design. It does not automatically indicate immediate implant placement.')

elif step==2:
    st.markdown('For today, these ten categories are recorded at a screening level. Detailed subquestions and evidence rules can be added later.')
    categories=['Medical Fitness','Medications','Radiation Treatment','Growth Status','Oral Hygiene','Compliance','Periodontal Status','Access','Pathology Near Implant Site','Previous Surgeries at Planned Implant Site']
    for i,name in enumerate(categories):
        a,b=st.columns([3,2]); a.write(name)
        with b: st.selectbox(f'{name} level', ['Not assessed','Low concern','Requires review','Potential high concern'], key=f'risk_{i}', label_visibility='collapsed')

elif step==3:
    st.radio('Primary patient preference', ['No preference yet','Avoid additional surgery','Shorter treatment time','Long-term predictability','Minimize cost'], key='priority')
    st.multiselect('Other considerations / patient expectations', ['Fewer appointments','Reduced postoperative discomfort','Esthetics','Retrievability','Easy hygiene and maintenance','Avoid donor-site surgery'], key='secondary_priorities')
    st.text_area('Additional patient expectations or concerns', key='patient_expectations', placeholder='e.g., wants to avoid sinus surgery, worried about treatment time, values easy maintenance...')
    st.slider('Importance of avoiding additional surgery', 0, 10, 5, key='surgery_importance')
    st.markdown('<div class="patient"><div class="smalltitle">Patient-centered interpretation</div>The final plan should not only be anatomically possible; it should also be compared according to treatment burden, number of interventions, expected maintenance and patient priorities.</div>', unsafe_allow_html=True)

elif step==4:
    st.markdown('Enter measurements from the prosthetically driven diagnostic plan. **All numerical fields may be left blank.**')
    a,b=st.columns(2)
    with a:
        st.number_input('Interocclusal / restorative space (mm)', min_value=0.0, max_value=30.0, value=None, step=.5, key='interocclusal')
        st.number_input('Mesiodistal prosthetic space (mm)', min_value=0.0, max_value=30.0, value=None, step=.5, key='md_prosthetic')
        st.selectbox('Gingival margin relative to planned restoration', ['Not assessed','Acceptable','Vertical soft-tissue deficiency','Excess / discrepancy'], key='gingival')
        st.selectbox('Contour relative to diagnostic wax-up', ['Not assessed','Adequate','Concave ridge defect','Convex / overcontoured anatomy'], key='ridge_contour')
    with b:
        st.selectbox('Occlusal scheme', ['Not assessed','Canine guidance','Group function','Other / complex'], key='occlusion')
        st.selectbox('Parafunction', ['Unknown','None reported','Possible','Confirmed'], key='parafunction')
        st.selectbox('Antagonist', ['Not assessed','Natural tooth','Fixed restoration','Implant-supported restoration','Removable prosthesis'], key='antagonist')
        st.selectbox('Operator restorative experience', ['Not assessed','Limited','Intermediate','Advanced'], key='operator_exp')
    if v('md_prosthetic') is not None and v('md_prosthetic') < 7:
        flag('Restricted mesiodistal prosthetic space: assess neighboring tooth contours, orthodontic space management and crown feasibility. The 7-mm flag is an illustrative review trigger, not a validated threshold.')
    if v('interocclusal') is not None and v('interocclusal') < 6:
        flag('Limited interocclusal clearance: assess restorative material thickness, prosthetic component dimensions and possible space creation. Review trigger only.')

elif step==5:
    st.markdown('Measurements should be related to the **planned prosthetically driven implant position**, not merely the narrowest arbitrary CBCT slice.')
    a,b=st.columns(2)
    with a:
        st.number_input('Residual bone height below sinus (mm)', min_value=0.0, max_value=30.0, value=None, step=.5, key='ridge_height')
        st.number_input('Ridge width at proposed implant site (mm)', min_value=0.0, max_value=30.0, value=None, step=.5, key='ridge_width')
        st.number_input('Mesiodistal bone space between adjacent roots (mm)', min_value=0.0, max_value=30.0, value=None, step=.5, key='md_bone')
        st.number_input('Vertical supracrestal soft-tissue height (mm)', min_value=0.0, max_value=12.0, value=None, step=.5, key='supracrestal')
        st.number_input('Measured maximal mouth opening (mm)', min_value=0.0, max_value=75.0, value=None, step=1.0, key='mouth_opening')
    with b:
        st.selectbox('Sinus assessment', ['Not assessed','No evident disease on initial review','Possible sinus pathology','Previously treated sinus condition'], key='sinus')
        st.selectbox('Adjacent tooth pathology', ['Not assessed','None identified','Present / requires evaluation'], key='adjacent_pathology')
        st.selectbox('Horizontal bony defect', ['Unknown','None apparent','Present / suspected'], key='horizontal_defect')
        st.selectbox('Vertical bony deficiency', ['Unknown','None apparent','Present / suspected'], key='vertical_defect')
        st.selectbox('Residual facial defect after ideal straight-axis placement', ['Not assessed','None anticipated','Potential dehiscence / concavity','Potential fenestration'], key='facial_defect')
        st.selectbox('Could implant angulation reduce graft requirements?', ['Unknown','Potentially — to be evaluated','Not appropriate based on prosthetic plan'], key='angulation_option')
        st.selectbox('Soft-tissue volume deficiency', ['Unknown','No obvious volume deficiency','Present'], key='soft_deficiency')

elif step==6:
    st.markdown('### Straumann-based comparison — illustrative candidate systems')
    height=v('ridge_height'); width=v('ridge_width'); md=v('md_bone'); soft=v('supracrestal')
    a,b=st.columns(2)
    with a:
        with st.container(border=True):
            st.markdown('#### A · Tissue-level candidate')
            st.write('✅ Straumann Standard Plus / tissue-level family')
            st.write('⚠️ Assess collar position, vertical restorative space, tissue height and visibility in the final soft-tissue contour.')
            st.write('‼️ Verify specific length and diameter availability for the selected line.')
    with b:
        with st.container(border=True):
            st.markdown('#### B · Bone-level candidate')
            st.write('✅ Straumann BLX / bone-level family')
            st.write('⚠️ Evaluate vertical soft-tissue architecture, abutment height and restorative emergence.')
            st.write('‼️ Requires confirmation of compatible abutments, depth, anatomy and prosthetic space.')
    with st.container(border=True):
        st.markdown('#### Dynamic evidence checks')
        if height is None:
            flag('Residual bone height is missing: cannot assess 6-mm versus 8-mm options.')
        elif height < 6:
            flag('Measured residual height is below the nominal 6-mm implant length. Review safety distances and augmentation/alternative options; no implant is cleared.')
        elif height < 8:
            st.info('Residual bone height falls between 6 and 8 mm. A short-implant strategy and a longer-implant strategy requiring additional assessment may merit comparison.')
        else:
            st.info('Residual height is at least 8 mm. Still assess anatomical safety clearance, implant geometry, depth and prosthetic positioning before selecting an implant.')
        if width is not None:
            st.write(f'Ridge width provided: **{width:g} mm**')
        if md is not None:
            st.write(f'Mesiodistal bone space: **{md:g} mm**')
        if soft is not None:
            st.write(f'Supracrestal tissue height: **{soft:g} mm**')
    refs(7)

elif step==7:
    st.markdown('### Competing surgical pathways')
    height=v('ridge_height'); sinus=v('sinus','Not assessed'); priority=v('priority','No preference yet')
    with st.container(border=True):
        st.markdown('**Pathway A · Short implant without additional sinus augmentation**')
        st.write('✅ May reduce surgical burden, treatment time and cost in appropriately selected posterior maxillary cases.')
        st.write('⚠️ Verify primary stability, bone volume, implant dimensions, occlusal/restorative load and maintenance.')
    with st.container(border=True):
        st.markdown('**Pathway B · Sinus elevation + longer implant**')
        st.write('✅ May allow a longer implant when indicated and anatomically feasible.')
        st.write('⚠️ Adds intervention and possible morbidity; assess whether a transcrestal or lateral approach is appropriate.')
    with st.container(border=True):
        st.markdown('**Pathway C · Horizontal augmentation / modified implant axis**')
        st.write('✅ Compare graft-based positioning with a modified prosthetically acceptable implant axis where feasible.')
        st.write('⚠️ Altering position may affect emergence profile, load direction or screw-channel accessibility.')
    if height is not None and height < 8:
        st.info('Bone height suggests discussing short versus augmented-length treatment concepts.')
    if sinus in ['Possible sinus pathology','Previously treated sinus condition']:
        flag('Sinus finding requires appropriate evaluation before determining augmentation feasibility.')
    if priority == 'Avoid additional surgery':
        st.success('Patient preference favors fewer procedures when outcomes and safety remain clinically acceptable.')
    st.markdown('<div class="patient"><div class="smalltitle">Decision emphasis</div>At this stage, compare each pathway not only by anatomical feasibility, but also by treatment burden, time, postoperative morbidity and the patient’s priorities.</div>', unsafe_allow_html=True)
    refs(8)

elif step==8:
    st.markdown('### Prosthetic options — Straumann-compatible concepts')
    a,b=st.columns(2)
    with a:
        with st.container(border=True):
            st.markdown('#### Straight-axis restoration')
            st.write('✅ Straight screw-access channel where implant positioning permits.')
            st.write('⚠️ Confirm sufficient restorative height and accessible hygiene contour.')
    with b:
        with st.container(border=True):
            st.markdown('#### Angled screw-channel restoration')
            st.write('✅ Variobase for Crown AS is an example of an angled screw-channel solution within documented compatibility limits.')
            st.write('⚠️ Verify implant platform, restorative space, access angle, material and software library.')
    st.selectbox('Preferred retention to evaluate', ['Not yet selected','Screw-retained','Cement-retained','Both alternatives'], key='retention')
    st.selectbox('Crown material for comparison', ['Not yet selected','Monolithic zirconia','Lithium disilicate (conditional on indication)','Metal-ceramic','Other'], key='crown_material')
    st.selectbox('Provisional restoration', ['Not yet selected','No provisional anticipated','Interim removable solution','Implant-supported provisional if clinically feasible'], key='provisional')
    if v('parafunction') in ['Confirmed','Possible']:
        flag('Parafunction reported: review occlusal loading, material selection, restoration design and protective strategies.')
    st.markdown('<div class="patient"><div class="smalltitle">Decision emphasis</div>The restorative solution should respond to patient expectations regarding retrievability, maintenance, comfort and esthetics—not only to the implant system.</div>', unsafe_allow_html=True)
    refs(9)

else:
    st.markdown('### Research demonstration summary — not a clinical prescription')
    a,b,c=st.columns(3)
    a.metric('Tooth', '16')
    b.metric('Bone height', f"{v('ridge_height'):g} mm" if v('ridge_height') is not None else 'Unknown')
    c.metric('Bone width', f"{v('ridge_width'):g} mm" if v('ridge_width') is not None else 'Unknown')

    d,e=st.columns(2)
    with d:
        st.markdown('**Primary patient priority**')
        st.write(v('priority', 'Not entered'))
        st.markdown('**Secondary priorities**')
        st.write(', '.join(v('secondary_priorities', [])) if v('secondary_priorities') else 'Not entered')
    with e:
        st.markdown('**Additional patient expectations**')
        st.write(v('patient_expectations', 'Not entered') if not unfilled('patient_expectations') else 'Not entered')
        st.markdown('**Esthetic concern**')
        st.write(v('esthetic', 'Not entered'))

    st.markdown('**Key measurements**')
    f,g,h=st.columns(3)
    f.metric('Mesiodistal bone space', f"{v('md_bone'):g} mm" if v('md_bone') is not None else 'Unknown')
    g.metric('Interocclusal space', f"{v('interocclusal'):g} mm" if v('interocclusal') is not None else 'Unknown')
    h.metric('Supracrestal tissue height', f"{v('supracrestal'):g} mm" if v('supracrestal') is not None else 'Unknown')

    st.markdown('**Feasible alternatives to assess**')
    st.markdown('''✅ Tissue-level versus bone-level design (subject to product and anatomic verification)  
⚠️ Short implant versus longer implant with augmentation when appropriate  
⚠️ Straight versus angled restorative solution when prosthetically and anatomically feasible  
‼️ None of these alternatives is automatically recommended by this pilot.''')

    st.markdown('<div class="patient"><div class="smalltitle">Patient-centered decision focus</div>The preferred option should emerge from the interaction between anatomy, restorative feasibility, treatment burden and the patient’s stated priorities.</div>', unsafe_allow_html=True)

    miss=missing()
    if miss:
        flag('Key data still missing: ' + ', '.join(miss))
    else:
        st.success('Key screening fields have been entered. A specialist still needs to review CBCT, medical risks, implant-specific geometry and evidence applicability.')

st.divider()
x,y,z=st.columns([1,3,1])
with x:
    if st.button('← Previous', disabled=step==0, use_container_width=True):
        go(step-1)
        st.rerun()
with z:
    if st.button('Next →' if step<9 else 'Review from start ↺', type='primary', use_container_width=True):
        go(step+1 if step<9 else 0)
        st.rerun()

st.caption('Prototype for research and discussion only. No validated individual risk estimates, automated medical clearance or treatment prescriptions. Not affiliated with ITI or Straumann.')
