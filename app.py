import json
from html import escape
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Implant CDSS · Patient-centered planning", page_icon="🦷", layout="wide", initial_sidebar_state="expanded")
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
.tech{border-left:4px solid #435881;background:#F8FBFB;padding:12px 15px;border-radius:8px;margin-bottom:10px;}
.patient{border-left:4px solid #489595;background:#F7FBFB;padding:12px 15px;border-radius:8px;margin-bottom:10px;}
.smalltitle{font-size:0.8rem;color:#489595;font-weight:800;letter-spacing:0.08em;text-transform:uppercase;}
</style>'''
st.markdown(CSS, unsafe_allow_html=True)
st.markdown("""<style>
[data-testid="stSidebar"] {background:#FFFFFF!important}
.patient-panel {border:1px solid #DCE8E9;border-radius:14px;padding:14px;background:#FFFFFF;margin:10px 0}
.priority-panel {border-left:5px solid #C7CF58;background:#FAFCEB;border-radius:10px;padding:12px;margin:10px 0}
.section-label {color:#435881;font-size:0.82rem;font-weight:800;text-transform:uppercase;letter-spacing:.09em}
.small-muted {font-size:.82rem;color:#536576}
.side-name {font-size:1.75rem;font-weight:800;line-height:1.15;color:#435881;letter-spacing:-.02em;margin:4px 0 6px}
.side-meta {font-size:.86rem;color:#536576;line-height:1.55}
.prio-item {padding:4px 0;color:#273246;font-size:.95rem;line-height:1.35}
.prio-top {font-weight:800}
.side-nav {margin:18px 0 6px}
</style>""", unsafe_allow_html=True)

MODULES = [
    'Patient Data & Priorities', 'Case Type & Site', 'Prosthetic Assessment',
    'Surgical Feasibility', 'Implant Selection', 'Surgical Planning',
    'Restorative Planning', 'Maintenance Program'
]
NEEDS = {
 'PAT-NEED-VISITS':'Fewer appointments',
 'PAT-NEED-TIME':'Shorter treatment time',
 'PAT-NEED-LONG':'Long-term predictability',
 'PAT-NEED-FEAR':'Afraid of surgery',
 'PAT-NEED-PAIN':'Minimize postoperative discomfort',
 'PAT-NEED-COST':'Minimize cost',
 'PAT-NEED-ESTH':'Esthetic outcomes',
 'PAT-NEED-HYG':'Easy maintenance and hygiene'
}
AGES = {
 'PAT-AGE-U18':'Adolescence · under 18',
 'PAT-AGE-Y18_29':'Young adult · 18–29',
 'PAT-AGE-A30_59':'Adulthood · 30–59',
 'PAT-AGE-O60P':'Older adult · 60+'
}
CASE_TYPES = {
 'CASE-TYPE-SINGLE':'Single Tooth',
 'CASE-TYPE-SHORT':'Short Span (≤ 3 teeth)',
 'CASE-TYPE-EXT':'Extended Span (> 3 teeth)',
 'CASE-TYPE-EDENT':'Edentulous'
}
SITE = {
 'CASE-SITE-EXTRACT':'Tooth present and requiring extraction',
 'CASE-SITE-SOFT':'Edentulous ridge · soft tissue healing (4–8 weeks post-extraction)',
 'CASE-SITE-PARTIAL':'Edentulous ridge · partial bone healing (12–16 weeks post-extraction)',
 'CASE-SITE-HEALED':'Completely healed edentulous ridge (>6 months post-extraction)'
}
# Universal / FDI equivalences for permanent teeth (numeric pairs).
# All teeth are shown by quadrant, from posterior to anterior when viewed in each quadrant.
QUADRANTS = [
 ('Maxillary right',[(str(10+i),9-i) for i in range(8,0,-1)]),   # 18=#1 ... 11=#8
 ('Maxillary left', [(str(20+i),8+i) for i in range(1,9)]),     # 21=#9 ... 28=#16
 ('Mandibular left',[(str(30+i),25-i) for i in range(8,0,-1)]),  # 38=#17 ... 31=#24
 ('Mandibular right',[(str(40+i),24+i) for i in range(1,9)]),  # 41=#25 ... 48=#32
]
FDI_UNI = {fdi:universal for _,teeth in QUADRANTS for fdi,universal in teeth}

if 'record' not in st.session_state:
 st.session_state.record = {'age':'PAT-AGE-A30_59','needs':[],'case_type':'CASE-TYPE-SINGLE','teeth':['16'],'site':'CASE-SITE-HEALED','esthetic':'No'}
if 'step' not in st.session_state: st.session_state.step=0
record=st.session_state.record

def field(name, widget, label, *, default=None, **kwargs):
    k='ui_'+name
    if k not in st.session_state:
        st.session_state[k]=record.get(name, default)
    # Make the record reflect what the widget displays, even if the user never touches it.
    record.setdefault(name, st.session_state[k])
    # Values live in record throughout navigation, even after widget cleanup.
    def sync(): record[name]=st.session_state[k]
    return widget(label, key=k, on_change=sync, **kwargs)

def choose(name,label,choices,default=None,**kw):
    if default is None: default=list(choices)[0]
    return field(name,st.selectbox,label,default=record.get(name,default),options=list(choices),format_func=(lambda x:choices[x]) if isinstance(choices,dict) else str,**kw)

def numeric(name,label,max_value=60.0,step=.5):
    # None is intentionally retained as unknown, never converted to zero.
    # All numeric arguments must be floats: Streamlit raises StreamlitMixedNumericTypesError on int/float mixes.
    return field(name,st.number_input,label,default=None,value=None,min_value=0.0,max_value=float(max_value),step=float(step))

def listfield(name,label,options,default=None,max_selections=None):
    kwargs={'options':list(options)}
    if isinstance(options,dict): kwargs['format_func']=lambda code:options[code]
    if max_selections is not None: kwargs['max_selections']=max_selections
    return field(name,st.multiselect,label,default=default if default is not None else [],**kwargs)

def r(key,default=None):return record.get(key,default)
def notice(s): st.warning(s,icon='⚠️')
def link(label,url):st.markdown('📖 ['+label+']('+url+')')

def references(section):
 with st.expander('Evidence and manufacturer references · illustrative',expanded=False):
  if section==4:
   link('Straumann BLX official catalogue','https://www.straumann.com/content/dam/media-center/straumann/en/documents/brochure/technical-information/450.006-en_low.pdf')
   link('Straumann Standard Plus overview','https://www.straumann.com/en/dental-professionals/dental-implants/tissue-level-implant-line/standard-plus-implant.html')
  elif section==5:
   link('Thoma et al., 2024 · 10-year RCT, 6-mm vs longer implants with sinus elevation','https://doi.org/10.1111/jcpe.13954')
   link('Yan et al., 2019 · Short implants vs sinus elevation','https://bmjopen.bmj.com/content/9/10/e029826')
  elif section==6:
   link('Straumann Variobase for Crown AS information','https://www.straumann.com/content/dam/media-center/straumann/en/documents/brochure/product-information/490.288-en_low.pdf')
  else:
   st.caption('Future work: add site-specific maintenance evidence and patient-level risk stratification before validation.')

def option(title,benefit,caution,safety=None):
 with st.container(border=True):
  st.markdown('#### '+title)
  st.write('✅ '+benefit)
  st.write('⚠️ '+caution)
  if safety: st.write('‼️ '+safety)

def patient_context():
 labels=[NEEDS[n] for n in r('needs',[]) if n in NEEDS]
 if labels: st.info('Patient priorities in this case: '+', '.join(labels)+'. Preferences guide comparison among clinically feasible options; they do not override anatomical and safety constraints.')
 else: st.info('Patient preferences are not yet recorded. Complete Step 1 to inform the comparisons.')

def goto(step):
 st.session_state.step=max(0,min(8,step))
 st.rerun()

with st.sidebar:
 # 1 · Patient name (large) + compact context
 if r('case_type')=='CASE-TYPE-EDENT':case_line='Edentulous · '+str(r('arch','Arch not selected'))
 else:case_line=CASE_TYPES.get(r('case_type'),'Case not set')+' · '+', '.join(r('teeth',[]))+' (FDI)'
 st.markdown('<div class="side-name">'+escape(r('name','') or 'Patient name not entered')+'</div>'
  '<div class="side-meta">'+escape(AGES.get(r('age'),'Age not recorded'))+'<br>'+escape(case_line)+'</div>',unsafe_allow_html=True)
 # 2 · Patient priorities (most important first)
 needs=[n for n in r('needs',[]) if n in NEEDS]
 top=r('top_priority')
 ordered=([top] if top in needs else [])+[n for n in needs if n!=top]
 if ordered:
  items=''.join('<div class="prio-item'+(' prio-top' if i==0 and top in needs else '')+'">• '+escape(NEEDS[n])+('  <span class="pill">Top priority</span>' if i==0 and top in needs else '')+'</div>' for i,n in enumerate(ordered))
 else:items='<div class="small-muted">No priorities selected yet</div>'
 st.markdown('<div class="priority-panel"><div class="section-label">Patient priorities</div>'+items+'</div>',unsafe_allow_html=True)
 # 3 · Treatment sequence and recommendations
 st.markdown('<div class="side-nav section-label">Case Navigation</div>',unsafe_allow_html=True)
 for i in range(4):
  if st.button(f'{i+1:02d}  {MODULES[i]}',key=f'side_{i}',use_container_width=True,type='primary' if st.session_state.step==i else 'secondary'):goto(i)
 st.markdown('<div class="side-nav section-label">Proposals</div>',unsafe_allow_html=True)
 for i in range(4,8):
  if st.button(f'{i+1:02d}  {MODULES[i]}',key=f'side_{i}',use_container_width=True,type='primary' if st.session_state.step==i else 'secondary'):goto(i)
 if st.button('Case Summary',use_container_width=True,type='primary' if st.session_state.step==8 else 'secondary'):goto(8)
 if st.button('Reset demo case',use_container_width=True):
  st.session_state.record={'age':'PAT-AGE-A30_59','needs':[],'case_type':'CASE-TYPE-SINGLE','teeth':['16'],'site':'CASE-SITE-HEALED','esthetic':'No'}
  for k in list(st.session_state.keys()):
   if k.startswith('ui_'):del st.session_state[k]
  goto(0)

st.markdown('<div class="topline"></div>',unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="eyebrow">EVIDENCE-BASED · PATIENT-CENTERED · CLINICALLY DRIVEN</div><h1 style="margin:5px 0">Implant Planning Decision Explorer</h1><span class="pill">Independent research prototype</span> &nbsp; <span class="pill">Native odontogram · V7.1</span></div>',unsafe_allow_html=True)
step=st.session_state.step
if step<8:
 st.progress((step+1)/8,text=f'{step+1:02d} / 08 · {MODULES[step]}')
 st.subheader(f'{step+1:02d} · {MODULES[step]}')
else:st.subheader('Case Summary · Shared Decision-Making')

if step==0:
 st.caption('Module PAT: complete this first; values are reused in clinical proposals and the patient snapshot.')
 field('name',st.text_input,'Patient name / study pseudonym',default='',placeholder='Demo Patient 01')
 choose('age','Age group',AGES)
 listfield('needs','Patient needs and concerns · select all that apply',NEEDS,max_selections=8)
 # Human readable priority-order among selected options.
 selected=r('needs',[])
 if selected:
  if r('top_priority') not in selected or st.session_state.get('ui_top_priority',r('top_priority')) not in selected:
   record['top_priority']=selected[0]
   st.session_state.pop('ui_top_priority',None)
  ranked=field('top_priority',st.selectbox,'Most important concern',default=selected[0] if r('top_priority') not in selected else r('top_priority'),options=selected,format_func=lambda k:NEEDS[k])
  st.caption('This priority influences how viable plans are compared, not clinical eligibility.')
 if r('age')=='PAT-AGE-U18':notice('Assess completion of craniofacial growth; avoid assuming implant eligibility from chronological age alone.')
 if r('age')=='PAT-AGE-O60P':st.info('Evaluate individual dexterity, medical status and maintenance needs; age alone is not a contraindication.')

elif step==1:
 st.caption('Module CASE: current site condition, not a request to choose ITI implant placement timing.')
 case_type=choose('case_type','Case type',CASE_TYPES)
 if case_type=='CASE-TYPE-EDENT':
  choose('arch','Edentulous arch',['Maxilla','Mandible'])
  st.caption('Full-arch treatment planning is outside the current single-tooth prototype.')
 else:
  st.markdown('**Interactive odontogram · Select missing teeth**')
  st.caption('Click a tooth to select or deselect it. Each tile shows Universal / FDI numbering (for example, 3 / 16). Selected tiles are highlighted in lime green.')
  if case_type=='CASE-TYPE-SINGLE' and len(r('teeth',[]))>1:
   record['teeth']=r('teeth',[])[:1]
  def toggle_tooth(fdi):
   current=list(record.get('teeth',[]))
   if fdi in current:
    current.remove(fdi)
   elif case_type=='CASE-TYPE-SINGLE':
    current=[fdi]
   elif case_type=='CASE-TYPE-SHORT' and len(current)>=3:
    # Short span has a maximum of three teeth; no silent overflow.
    return
   else:
    current.append(fdi)
   record['teeth']=current
  for qname,teeth in QUADRANTS:
   st.caption(qname)
   columns=st.columns(8)
   for col,(fdi,universal) in zip(columns,teeth):
    with col:
     selected=fdi in record.get('teeth',[])
     st.button(f'{universal} / {fdi}',key=f'odon_{fdi}',type='primary' if selected else 'secondary',use_container_width=True,on_click=toggle_tooth,args=(fdi,))
  chosen=record.get('teeth',[])
  st.write('**Selected teeth:** '+(', '.join(f'{FDI_UNI[fdi]} / {fdi}' for fdi in chosen) if chosen else 'None selected'))
  if case_type=='CASE-TYPE-SHORT':st.caption('Short Span allows up to three teeth. To select another, deselect one first.')
 choose('esthetic','Does this case involve an esthetic concern?',['No','Yes'])
 choose('site','Current site condition',SITE)
 if r('site')!='CASE-SITE-EXTRACT':
  numeric('weeks','Weeks since extraction (optional)',max_value=520,step=1.0)
  w=r('weeks')
  if w is not None and ((r('site')=='CASE-SITE-SOFT' and not 4<=w<=8) or (r('site')=='CASE-SITE-PARTIAL' and not 12<=w<=16) or (r('site')=='CASE-SITE-HEALED' and w<26)):
   notice('Reported time and selected healing category may not align. Confirm clinical healing; timing alone cannot establish suitability.')
 if r('site')=='CASE-SITE-EXTRACT':st.info('Tooth is still present. Evaluate extraction considerations and potential timing options later; Type 1 is not assumed.')

elif step==2:
 st.caption('Prosthetically driven dimensions and restorative considerations.')
 left,right=st.columns(2)
 with left:
  numeric('interocclusal','Interocclusal space (mm)')
  numeric('md_prosthetic','Mesiodistal prosthetic space (mm)')
  choose('gingival','Gingival margin',['Not assessed','Acceptable','Vertical soft-tissue deficiency'])
  choose('ridge_contour','Ridge contour',['Not assessed','Adequate','Concave defect','Other deficiency'])
 with right:
  choose('occlusion','Occlusal scheme',['Not assessed','Canine guidance','Group function','Other'])
  choose('parafunction','Parafunction',['Unknown','None reported','Possible','Confirmed'])
  choose('antagonist','Antagonist',['Not assessed','Natural tooth','Fixed restoration','Implant restoration','Removable prosthesis'])
  choose('operator_exp','Operator experience',['Not assessed','Limited','Intermediate','Advanced'])
 if r('esthetic')=='Yes':st.info('Esthetic concern recorded. Evaluate provisionalization and soft-tissue architecture in restorative proposals.')
 if r('ridge_contour')=='Concave defect' or r('gingival')=='Vertical soft-tissue deficiency':st.info('Assess soft-tissue volume augmentation options; timing and indication require evaluation.')

elif step==3:
 st.caption('CBCT measurements are interpreted relative to the prosthetically ideal implant position.')
 left,right=st.columns(2)
 with left:
  numeric('ridge_height','Residual bone height (mm)')
  numeric('ridge_width','Ridge width (mm)')
  numeric('md_bone','Mesiodistal space between adjacent roots (mm)')
  numeric('supracrestal','Supracrestal tissue height (mm)',max_value=20)
  numeric('mouth_opening','Maximal mouth opening (mm)',max_value=80,step=1.)
 with right:
  choose('sinus','Sinus assessment',['Not assessed','No evident disease','Possible sinus pathology','Previously treated sinus condition'])
  choose('adjacent_pathology','Adjacent teeth',['Not assessed','No pathology identified','Pathology requires review'])
  choose('horizontal_defect','Horizontal bone deficiency',['Unknown','None apparent','Present / suspected'])
  choose('vertical_defect','Vertical bone deficiency',['Unknown','None apparent','Present / suspected'])
  choose('facial_defect','Facial defect relative to prosthetic axis',['Not assessed','None anticipated','Potential dehiscence','Potential fenestration'])
  choose('angulation','Angulated pathway',['Unknown','Potentially feasible','Not prosthetically appropriate'])
 st.info('No implant is cleared based on height or width alone. Anatomy, safety distances and manufacturer dimensions require independent assessment.')

elif step==4:
 st.markdown('### Implant configuration · candidate concepts')
 patient_context()
 if r('case_type')!='CASE-TYPE-SINGLE':notice('This demonstration evaluates a single restoration only; selected case type requires a future pathway.')
 left,right=st.columns(2)
 with left:option('Option A · Tissue-level candidate','Restorative interface can be supracrestal with an appropriate collar and soft-tissue architecture.','Check restorative space, collar position, esthetic concerns and current product dimensions.','Do not assume a specific 6-mm tissue-level product is available.')
 with right:option('Option B · Bone-level candidate','Flexible transmucosal design and restorative abutment choices where compatible.','Check abutment height, depth and emergence profile.','Implant length, diameter and components must be checked in a current Straumann catalogue.')
 st.caption('Illustrative candidate families: Straumann Standard Plus (tissue-level) and Straumann BLX (bone-level).')
 if r('ridge_height') is None:notice('Bone height not entered; length cannot be evaluated.')
 elif r('ridge_height')<8:st.info('Limited vertical height: evaluate short implant versus other treatment pathways; no automatic recommendation.')
 choose('implant_option','Candidate implant pathway to investigate',['Undecided','Tissue-level candidate','Bone-level candidate','Compare both'])
 references(4)

elif step==5:
 st.markdown('### Surgical pathways · patient-centered comparison')
 patient_context()
 option('Option A · Short implant concept','May limit surgical intervention in carefully selected posterior sites.','Evaluate primary stability, implant dimensions, restorative load and long-term evidence.','No automatic clearance from nominal bone height.')
 option('Option B · Sinus augmentation + longer implant','May permit additional implant length where anatomically justified.','Compare treatment burden, healing timeline, sinus anatomy and morbidity.','Sinus disease and anatomical limitations require separate assessment.')
 option('Option C · Horizontal regeneration / adjusted axis','Allows comparison of prosthetically feasible site-development strategies.','Check graft need, emergence and restorative component compatibility.','An angled component cannot compensate for unsafe 3D implant positioning.')
 if r('sinus') in ('Possible sinus pathology','Previously treated sinus condition'):notice('Sinus finding needs appropriate evaluation before considering sinus intervention.')
 choose('surgical_option','Surgical pathway to investigate',['Undecided','Short implant concept','Sinus augmentation concept','Horizontal augmentation / altered axis','Compare multiple options'])
 references(5)

elif step==6:
 st.markdown('### Restorative alternatives')
 patient_context()
 left,right=st.columns(2)
 with left:option('Straight screw access','Retrievability can support maintenance where geometry allows.','Verify restorative dimensions, tissue profile and access direction.')
 with right:option('Angled screw access','May support a screw-retained solution when an angulated channel is compatible.','Verify platform, manufacturer-approved correction range and restorative thickness.','Does not correct an unsafe implant trajectory.')
 choose('retention','Retention',['Undecided','Screw-retained','Cement-retained','Compare both'])
 choose('material','Crown material',['Undecided','Monolithic zirconia','Metal-ceramic','Other'])
 choose('provisional','Provisional approach',['Undecided','No provisional','Interim prosthesis','Implant-supported provisional if feasible'])
 if r('parafunction') in ('Possible','Confirmed'):notice('Reassess occlusal loading and protective strategies.')
 references(6)

elif step==7:
 st.markdown('### Maintenance Program · proposed considerations')
 patient_context()
 st.markdown('**Maintenance recommendations must be individualized after baseline assessment.**')
 st.write('✅ Record baseline soft-tissue and radiographic parameters after prosthesis delivery.')
 st.write('✅ Assess plaque control, probing parameters, restorability, access for hygiene, and patient ability to attend recall visits.')
 st.write('⚠️ Periodontal history, smoking, prosthetic cleansability and peri-implant findings may modify follow-up intervals.')
 st.write('‼️ Do not assign a fixed interval from age or preferences alone; clinical risk evaluation is required.')
 choose('maintenance_plan','Recall plan for clinician review',['Not assigned','Individualized after risk assessment','Consider shorter interval pending assessment','Standard follow-up pending assessment'])
 references(7)

else:
 st.markdown('### Case summary and selected pathways')
 a,b,c=st.columns(3)
 a.metric('Patient',r('name') or 'Not entered')
 b.metric('Bone height',f"{r('ridge_height')} mm" if r('ridge_height') is not None else 'Unknown')
 c.metric('Bone width',f"{r('ridge_width')} mm" if r('ridge_width') is not None else 'Unknown')
 st.write('**Age group:**',AGES.get(r('age'),'Not entered'))
 st.write('**Needs:**',', '.join(NEEDS.get(x,x) for x in r('needs',[])) or 'Not entered')
 st.write('**Case:**',CASE_TYPES.get(r('case_type')))
 st.write('**Teeth (FDI):**',', '.join(r('teeth',[])) if r('case_type')!='CASE-TYPE-EDENT' else r('arch','Unknown'))
 st.write('**Esthetic concern:**',r('esthetic','Not entered'))
 st.write('**Current site:**',SITE.get(r('site'),'Not entered'))
 st.write('**Implant / surgical / restorative:**',r('implant_option','Undecided'),'·',r('surgical_option','Undecided'),'·',r('retention','Undecided'))
 st.write('**Maintenance:**',r('maintenance_plan','Not assigned'))
 st.caption('The summary represents the current working plan, not a treatment prescription or an approved clinical recommendation.')
 # Structured codes allow downstream research and software iterations.
 st.download_button('Export coded case as JSON',data=json.dumps(record,indent=2,ensure_ascii=False),file_name='implant_cdss_demo_case.json',mime='application/json')
 st.warning('Demo only. Export may include patient name; use pseudonyms and avoid patient-identifiable data on publicly deployed applications.')

st.divider()
left,mid,right=st.columns([1,3,1])
with left:
 if st.button('← Previous',disabled=step==0,use_container_width=True):goto(step-1)
with right:
 if st.button('Next →' if step<8 else 'Restart navigation ↺',type='primary',use_container_width=True):goto(step+1 if step<8 else 0)
st.caption('Research prototype; decision rules require evidence mapping, clinician review and validation. Not affiliated with ITI or Straumann.')
