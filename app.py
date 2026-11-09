import base64
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
/* Compact tooth selector: scoped so navigation and form buttons stay unchanged. */
.st-key-tooth_picker { max-width: 1040px; }
.st-key-tooth_picker [data-testid="stButton"] button {
  min-height: 2.15rem !important;
  height: 2.15rem !important;
  padding: .12rem .28rem !important;
  border-radius: 9px !important;
  font-size: .82rem !important;
  letter-spacing: -.015em !important;
  white-space: nowrap !important;
  line-height: 1.1 !important;
}
.st-key-tooth_picker [data-testid="stButton"] button[kind="primary"] {
  background-color: #C7CF58 !important;
  border-color: #A9B13F !important;
  color: #263246 !important;
}
.st-key-tooth_picker [data-testid="stButton"] button[kind="secondary"] {
  border-color: #BCD6D6 !important;
  background-color: #FBFDFD !important;
}
.st-key-tooth_picker [data-testid="stVerticalBlock"] { gap: .22rem !important; }
.st-key-tooth_picker .tooth-quadrant-label {
  font-size: .75rem;
  letter-spacing: .015em;
  font-weight: 700;
  color: #526879;
  margin: .35rem 0 .05rem;
}
.st-key-tooth_picker .tooth-help {
  font-size: .78rem;
  color: #607384;
  margin: .1rem 0 .3rem;
}
</style>""",unsafe_allow_html=True)

st.markdown("""<style>
[data-testid="stSidebar"] {background:#FFFFFF!important}
.patient-panel {border:1px solid #DCE8E9;border-radius:14px;padding:14px;background:#FFFFFF;margin:10px 0}
.priority-panel {border-left:5px solid #C7CF58;background:#FAFCEB;border-radius:10px;padding:12px;margin:10px 0}
.section-label {color:#435881;font-size:0.82rem;font-weight:800;text-transform:uppercase;letter-spacing:.09em}
.small-muted {font-size:.82rem;color:#536576}
.side-name {font-size:1.75rem;font-weight:800;line-height:1.15;color:#435881;letter-spacing:-.02em;margin:4px 0 6px}
.side-meta {font-size:.86rem;color:#536576;line-height:1.55}
.side-head {display:flex;align-items:center;gap:14px;margin:2px 0 4px}
.side-avatar {width:58px;height:58px;flex:none}
[data-testid="stSidebar"] .pill-top {background:#EC5A53 !important;color:#FFFFFF !important;font-weight:700}
.prio-item {padding:4px 0;color:#273246;font-size:.95rem;line-height:1.35}
.prio-top {font-weight:800}
.side-nav {margin:18px 0 6px}
.col-title {font-size:1.2rem;font-weight:800;color:#435881;letter-spacing:-.01em;margin:0 0 2px}
.col-desc {font-size:.84rem;color:#536576;line-height:1.45;margin-bottom:4px}
.sub-label {margin:16px 0 2px}
</style>""", unsafe_allow_html=True)

MODULES = [
    'Patient Data & Priorities', 'Case Type & Site', 'Prosthetic Assessment',
    'Surgical Assessment', 'Treatment Strategy & Implant Selection', 'Surgical Planning',
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
NO_PRIORITY='PAT-NEED-NONE'
PRIORITY_LABELS={NO_PRIORITY:'No specific priority',**NEEDS}
AGES = {
 'PAT-AGE-U18':'Adolescence · under 18',
 'PAT-AGE-Y18_29':'Young adult · 18–29',
 'PAT-AGE-A30_59':'Adulthood · 30–59',
 'PAT-AGE-O60P':'Older adult · 60+'
}
AGE_SCALE=[('PAT-AGE-U18','Under 18','Adolescence'),('PAT-AGE-Y18_29','18–29','Young adult'),('PAT-AGE-A30_59','30–59','Adulthood'),('PAT-AGE-O60P','60+','Older adult')]
AGE_SHORT={c:n for c,_,n in AGE_SCALE}
def age_scale_text(current=None):
    # Reminder of the classification scale; the band that matches the entered age is in bold.
    return 'Scale: '+' · '.join(('**'+rng+' '+name+'**') if code==current else rng+' '+name for code,rng,name in AGE_SCALE)
AVATAR_SVG='<svg xmlns="http://www.w3.org/2000/svg" viewBox="8 2 48 60"><path d="M32 4a14 14 0 0 0 0 28z" fill="#D8DE8C"/><path d="M32 4a14 14 0 0 1 0 28z" fill="#C7CF58"/><path d="M32 36c-13 0-22 7-22 20 0 3 2 4 5 4h17z" fill="#6FB0B0"/><path d="M32 36c13 0 22 7 22 20 0 3-2 4-5 4H32z" fill="#489595"/></svg>'
AVATAR_URI='data:image/svg+xml;base64,'+base64.b64encode(AVATAR_SVG.encode()).decode()
def age_group(years):
    # Age in years -> group code. Bands do not overlap: <18, 18-29, 30-59, >=60.
    if years is None: return None
    if years<18: return 'PAT-AGE-U18'
    if years<30: return 'PAT-AGE-Y18_29'
    if years<60: return 'PAT-AGE-A30_59'
    return 'PAT-AGE-O60P'
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
 st.session_state.record = {'needs':[],'case_type':'CASE-TYPE-SINGLE','teeth':[],'esthetic':'No'}
if 'step' not in st.session_state: st.session_state.step=0
record=st.session_state.record
record['age']=age_group(record.get('age_years'))  # derived before the sidebar renders

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

def numeric(name,label,max_value=60.0,step=.5,**kw):
    # None is intentionally retained as unknown, never converted to zero.
    # All numeric arguments must be floats: Streamlit raises StreamlitMixedNumericTypesError on int/float mixes.
    return field(name,st.number_input,label,default=None,value=None,min_value=0.0,max_value=float(max_value),step=float(step),**kw)

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
   st.markdown('- Straumann USA. iEXCEL: Four Implant Designs in a Single System (straumann.com/us, iEXCEL section).\n- Straumann. BLC, TLC, BLX and TLX: product pages and C/X design guidelines (straumann.com).\n- Straumann. Bone Level Tapered Implant, Technical Information, 702167 (straumann.com, PDF).\n- Thoma DS et al. EAO Consensus Conference 2021: Soft tissue management at implants. Clin Oral Implants Res. 2021.\n- Yu SH, Saleh MHA, Wang HL. Simultaneous or staged lateral ridge augmentation: a clinical guideline on the decision-making process. Periodontol 2000. 2023;93(1):107-128.\n- Jung RE et al. A randomized controlled clinical trial comparing small buccal dehiscence defects around dental implants treated with guided bone regeneration or left for spontaneous healing. Clin Oral Implants Res. 2017;28(3):348-354.\n- ITI Consensus 2023: buccal bone thickness above 1.5 mm at healed ridges and simultaneous regeneration of buccal dehiscences (cited in the functional specification; full citation pending).')
  elif section==5:
   link('Thoma et al., 2024 · 10-year RCT, 6-mm vs longer implants with sinus elevation','https://doi.org/10.1111/jcpe.13954')
   link('Yan et al., 2019 · Short implants vs sinus elevation','https://bmjopen.bmj.com/content/9/10/e029826')
  elif section==6:
   link('Straumann Variobase for Crown AS information','https://www.straumann.com/content/dam/media-center/straumann/en/documents/brochure/product-information/490.288-en_low.pdf')
   link('Restorative space by prosthesis type · JADA 2019','https://pubmed.ncbi.nlm.nih.gov/31352966/')
   link('Misch et al. · Crown-height space consensus (2005)','https://icoi.world/wp-content/uploads/2024/12/Consensus_Conference_Panel_Report__Crown_Height-2.pdf')
  else:
   st.caption('Future work: add site-specific maintenance evidence and patient-level risk stratification before validation.')

FAMILIES={'IMP-FAM-BLT':'BLT · Bone Level Tapered','IMP-FAM-BLC':'BLC · Bone Level C','IMP-FAM-BLX':'BLX · Bone Level X','IMP-FAM-TLC':'TLC · Tissue Level C','IMP-FAM-TLX':'TLX · Tissue Level X'}
# (macrogeometry and connection, clinical strength, especially reasonable when, main precaution)
PROFILES={
 'IMP-FAM-BLT':('Apically tapered body; CrossFit SC (2.9), NC (3.3), RC (4.1/4.8).','Controlled compression of an underprepared bed; stability in soft bone and fresh sockets; Ø2.9 for reduced indications.','Bone Level with limited anatomy; immediate socket; family alternative for narrow anterior teeth with Ø2.9.','Do not extrapolate Ø2.9 indications to molars; review anatomy, loads and SC/NC/RC components.'),
 'IMP-FAM-BLC':('Tapered, fine apex, extended cutting grooves and double-thread; TorcFit.','Efficient insertion and stability with an adjustable cortical preparation; suitable for limited anatomies.','Bone Level in healed ridges, esthetic zones, planned CTG/GBR, or narrow apical anatomy.','Do not assume every C is "low stability": drilling and stability depend on the bed.'),
 'IMP-FAM-BLX':('Fully tapered, progressive thread and bidirectional cutting elements; TorcFit.','Dynamic Bone Management and high primary stability oriented to immediate protocols.','Bone Level with immediate insertion, possible immediate provisionalization/loading and/or need for stability in trabecular bone.','In dense cortical bone, control drilling, torque and compression; stability is not an automatic indication for immediate loading.'),
 'IMP-FAM-TLC':('Apical C taper with a machined transmucosal neck; TorcFit.','Tapered C plus a prosthetic interface away from the crest; transmucosal prosthetic access.','Healed ridge, adequate tissues and bone volume, with no planned need for CTG/GBR.','Confirm shoulder position, mucosal height, emergence profile and cleansability.'),
 'IMP-FAM-TLX':('Fully tapered X with a machined transmucosal neck; TorcFit.','X properties for primary stability on a Tissue Level platform.','Adequate tissues and volume without planned regeneration, with an immediate protocol considered and an adequate transmucosal position.','Do not select Tissue Level for torque alone; avoid an unfavorable neck if augmentation or complex esthetic management is needed.')}
TIEBREAKERS=[
 ('BLC vs BLX','BLC: you seek C versatility and cortical/spatial management at Bone Level, without a special priority on immediacy.','BLX: immediate protocol and especially demanding primary stability, if the drilling and the bone allow it.'),
 ('BLC vs BLT','BLC: you need the iEXCEL/TorcFit ecosystem, the C design and the associated prosthodontic options.','BLT: the case favors CrossFit and its apical taper; Ø2.9 SC must be evaluated if applicable.'),
 ('TLC vs TLX','TLC: stable, healed site, transmucosal approach and no particular need for X.','TLX: favorable Tissue Level conditions, but primary stability is more demanding or immediacy is considered.'),
 ('Bone vs Tissue Level','Bone Level: CTG, GBR, compromised phenotype, esthetic management or complex depth/restoration.','Tissue Level: adequate bone and tissues; no planned regeneration; restorable transmucosal neck.')]
SAFETY_NOTES=[
 'CTG is not a synonym of increasing the vertical supracrestal tissue height: record both goals and their measures independently.',
 'The X design can favor primary stability, but higher torque does not prove biological superiority nor authorize immediate loading by itself.',
 'Tissue Level is not universally contraindicated in augmented sites; excluding it when CTG/GBR is planned is a deliberate, conservative rule of this CDSS.',
 'For D1 to D4 density, do not infer an indication from CBCT HU alone: consider the clinical evaluation, the drilling protocol and scanner variability.',
 'The final recommendation requires the current IFU of the SKU, prosthetic compatibility, stability, anatomical analysis and clinical judgment.',
 'SRA 7 mm and Ti-base 6 mm are local CDSS alert thresholds; compare dimensions from the SAME reference landmark and verify the exact component. Crestal crown-height >15 mm triggers biomechanical review.',
 'Dilacerated roots require a verified root-safe 3D osteotomy; an angled abutment cannot resolve a surgical collision.']
REDUCED_HEIGHT_MM=8.0  # working threshold for "reduced posterior bone height"; to be confirmed
PROX_MM=1.5      # bone/space kept mesial and distal to the implant, from the adjacent roots
BUCCAL_MM=1.5    # planned buccal bone thickness (ITI 2023: more than 1.5 mm)
PALATAL_MM=1.0   # planned palatal/lingual bone thickness
# Working clinical thresholds, not universal Straumann component specifications.
SRA_SPACE_REVIEW_MM=7.0
TIBASE_SPACE_REVIEW_MM=6.0
CROWN_HEIGHT_REVIEW_MM=15.0

_DEH,_FEN='SUR-FACIAL-DEHISCENCE','SUR-FACIAL-FENESTRATION'

def implant_level():
 # Sequence: regenerative need -> timing (simultaneous or staged) -> tissue condition after re-evaluation -> Bone/Tissue Level.
 # Returns (level, reasons, missing); level is 'BL', 'TL', 'DEFER' (staged GBR still to be done) or None (data missing).
 reasons,missing=[],[]
 ctg,gbr=r('ctg_planned'),r('gbr_approach')
 if ctg=='IMP-CTG-YES':reasons.append('Connective tissue graft at implant placement')
 elif ctg is None and tp_procedure_recommendations()['CTG']['status']=='pending':missing.append('CTG assessment')
 if gbr=='IMP-GBR-SIMULT':reasons.append('Simultaneous GBR')
 elif gbr is None and tp_procedure_recommendations()['GBR']['status']=='pending':missing.append('Bone-regeneration assessment')
 elif gbr=='IMP-GBR-STAGED':
  stt=r('staged_status')
  if stt is None:missing.append('Staged GBR status')
  elif stt=='IMP-STG-PENDING':return 'DEFER',reasons,missing
 if gbr!='IMP-GBR-STAGED':
  # Bone defects only drive the level when no staged reconstruction precedes the placement.
  tail=' with no regeneration planned' if gbr=='IMP-GBR-NONE' else ''
  fd=r('facial_defect')
  if fd in (_DEH,_FEN):reasons.append('Potential facial dehiscence or fenestration'+tail)
  elif fd is None:missing.append('Facial defect (Surgical Assessment)')
  for key,bad,lab in (('horizontal_defect',('SUR-HDEF-PRESENT','SUR-HDEF-SUSPECTED'),'Horizontal bone deficiency'),('vertical_defect',('SUR-VDEF-PRESENT','SUR-VDEF-SUSPECTED'),'Vertical bone deficiency')):
   v=r(key)
   if v in bad:reasons.append(lab+' present or suspected'+tail)
   elif v is None:missing.append(lab+' (Surgical Assessment)')
  if r('supracrestal') is not None and r('supracrestal')<2.0:
   reasons.append('STH under 2 mm: consider soft-tissue optimization and prefer Bone Level under CDSS policy')
  elif r('supracrestal') is None:missing.append('STH measurement')
  if tp_procedure_recommendations()['GBR']['status']=='suggested' and gbr!='IMP-GBR-STAGED':
   reasons.append('Bone regeneration assessment triggered by dimensional or bone-defect findings')
 if gbr=='IMP-GBR-STAGED' and r('supracrestal') is not None and r('supracrestal')<2.0:
  reasons.append('STH below 2 mm after staged GBR: soft-tissue management should be evaluated before Tissue Level selection')
 for key,bad,lab,txt in (('soft_thickness','SUR-STT-DEFICIENT','Soft-tissue thickness','Soft-tissue thickness deficient'),('keratinized','SUR-KT-DEFICIENT','Keratinized tissue','Keratinized tissue band under 2 mm')):
  v=r(key)
  if v==bad:reasons.append(txt)
  elif v is None:missing.append(lab+' (Surgical Assessment)')
 if r('sth_adequacy')=='IMP-STH-NO':reasons.append('STH judged inadequate for the intended implant platform')
 elif r('sth_adequacy') is None and r('supracrestal') is None:missing.append('STH suitability for the restorative platform')
 if r('ridge_width') is None:missing.append('Ridge width (Surgical Assessment)')
 if r('md_bone') is None:missing.append('Mesiodistal interradicular space (Surgical Assessment)')
 if reasons:return 'BL',reasons,missing
 return (None if missing else 'TL'),reasons,missing

GBR_CRITERIA=(('gbrc_pos','3D implant position is prosthetically adequate','GBRC-POS'),('gbrc_stab','CBCT anatomy appears to permit an anchorage trajectory (not achieved stability)','GBRC-STAB'),('gbrc_morph','Defect morphology favors graft stabilization and space maintenance','GBRC-MORPH'),('gbrc_clos','Soft tissues allow tension-free closure','GBRC-CLOS'))

def gbr_support():
 # Guidance for simultaneous vs staged GBR (Yu, Saleh, Wang 2023; Jung 2017). Orientative, never an automatic indication.
 rec_=tp_procedure_recommendations()['GBR']
 relevant=(rec_['status']=='suggested' and not rec_['md_only_conflict']) or r('gbr_approach') in ('IMP-GBR-SIMULT','IMP-GBR-STAGED')
 if r('gbr_approach')=='IMP-GBR-STAGED' and r('staged_status')=='IMP-STG-HEALED':return None   # already reconstructed and re-evaluated
 if not relevant:return None
 aug,deh=r('h_aug'),r('deh_height')
 rank={'small':0,'mid':1,'large':2}
 size,notes=None,[]
 def put(level,note):
  nonlocal size
  notes.append(note)
  if size is None or rank[level]>rank[size]:size=level
 if aug is not None and aug>0:
  if aug<=3:put('small','Horizontal augmentation of '+format(aug,'g')+' mm (1 to 3 mm): simultaneous GBR is generally favorable.')
  elif aug<=5:put('mid','Horizontal augmentation of '+format(aug,'g')+' mm (4 to 5 mm): simultaneous GBR only in selected cases, especially contained defects; consider a staged approach.')
  else:put('large','Horizontal augmentation of '+format(aug,'g')+' mm (6 mm or more): staged regeneration is generally preferable.')
 if deh is not None and deh>0:
  if deh<=3:put('small','Dehiscence height of '+format(deh,'g')+' mm (3 mm or less): within the small-defect criterion.')
  else:put('mid','Dehiscence height of '+format(deh,'g')+' mm exceeds the 3 mm small-defect criterion: evaluate a staged approach.')
 failed=[lab for k,lab,c in GBR_CRITERIA if r(k)=='IMP-'+c+'-NO']
 pending=[lab for k,lab,c in GBR_CRITERIA if r(k) is None]
 if size=='large' or failed:verdict='staged'
 elif size=='mid':verdict='selected'
 elif size=='small' and not pending:verdict='simult'
 else:verdict='pending'
 return dict(verdict=verdict,notes=notes,failed=failed,pending=pending,size=size)

def implant_scenarios():
 u=(r('teeth',[]) or [''])[0][-1:]
 anterior,posterior,incisor=bool(u) and u in '123',bool(u) and u in '45678',bool(u) and u in '12'
 site,bq=r('site'),r('bone_quality')
 imm_pl,imm_ld=r('immediate_placement'),r('immediate_loading')
 ctg,gbr=r('ctg_planned'),r('gbr_approach')
 defect=r('facial_defect') in (_DEH,_FEN)
 apical=r('adjacent_roots')=='SUR-ROOTS-DILACERATED'
 level,_,_=implant_level()
 S=[
 ('BL',anterior and r('esthetic')=='Yes' and ctg=='IMP-CTG-YES','Anterior esthetic site; CTG for contour or thickness','BLC','BLT / BLX','Bone Level allows planning emergence and augmentation; C has a thin apex for limited anatomy.','Do not equate CTG with a vertical STH increase; evaluate the buccal plate, platform and profile.'),
 ('BL',imm_pl=='IMP-IMMPL-YES' and imm_ld=='IMP-IMMLD-NO','Immediate post-extraction placement; conventional loading','BLT or BLC','BLX','Taper adapts to the socket bed; BLX if greater stability is required.','Assess the buccal wall, gap, 3D position, esthetic risk and dehiscences. Sufficient apical/palatal anchorage is not captured in the app: confirm clinically.'),
 ('BL',imm_pl=='IMP-IMMPL-YES' and imm_ld=='IMP-IMMLD-YES','Immediate placement with immediate provisionalization or loading','BLX','BLC / BLT if they meet the criteria','X is designed to favor primary stability and immediate protocols.','Load only after verifying torque/ISQ according to a validated protocol, absence of micromovement and occlusal control.'),
 ('BL',site=='CASE-SITE-HEALED' and bq=='SUR-BQ-D4','Healed ridge with low-density trabecular bone (D4)','BLX or BLT','BLC','Conical design and an adapted preparation provide greater stability capacity.','Do not impose generic underpreparation: follow the density protocol and control torque.'),
 ('BL',bq in ('SUR-BQ-D1','SUR-BQ-D2'),'Dense bone / thick cortex (D1 to D2)','BLC or BLT with an adequate preparation','BLX with an adapted sequence','The choice must control cortical compression, not maximize torque.','Avoid overcompression; use a specific drilling/thread protocol and control heat.'),
 ('BL',apical,'Restricted interradicular anatomy (dilacerated roots)','BLC or BLT','BLX if it allows orientation','The thin C apex and the BLT apical taper favor selective anatomical evaluation.','Confirm distances to roots, cortex and anatomical structures.'),
 ('BL',incisor and (r('pro_md') is not None and r('pro_md')<6.0),'Narrow mesiodistal space (selected incisors)','BLT Ø2.9 SC','BLC Ø3.3 if the anatomy allows','Ø2.9 has specific indications for narrow incisors; it is not a universal space solution.','Validate the mesiodistal distance, restorative diameter and forces; check the IFU exclusions.'),
 ('BL',defect and gbr=='IMP-GBR-SIMULT','Buccal defect / dehiscence with simultaneous GBR','BLC / BLT','BLX if additional stability is required','Bone Level is prioritized for regeneration management and 3D position.','Assess the severity of the defect and the need for a staged approach.'),
 ('TL',posterior and site=='CASE-SITE-HEALED' and imm_ld=='IMP-IMMLD-NO' and level=='TL','Healed posterior site; adequate STH, gingiva and bone; no GBR','TLC','TLX','Transmucosal Tissue Level when the shoulder position is prosthetically favorable.','Ensure hygiene access, emergence, restorability and phenotype.'),
 ('TL',posterior and imm_ld=='IMP-IMMLD-YES' and level=='TL','Posterior site with adequate tissues; immediate loading under evaluation','TLX','BLX if Tissue Level is not suitable','X favors stability; TLX keeps the transmucosal prosthetic connection.','Do not prioritize TLX if the tissue anatomy requires CTG/GBR.')]
 return [dict(lvl=a,name=c,first=d,alts=e,why=f,flt=g) for a,b,c,d,e,f,g in S if b]

VERT_MARGIN_MM=2.0     # provisional vertical safety margin used for the length ceiling; to be confirmed
BLT_DIAMETERS=(2.9,3.3,4.1,4.8)   # CrossFit SC, NC, RC (4.1 / 4.8) from the design matrix
_FAMRE=r'(BLT|BLC|BLX|TLC|TLX)'

def size_ceiling():
 # (max diameter, max length) in mm from the entered measures; None when not entered.
 w,md,h=r('ridge_width'),r('md_bone'),r('ridge_height')
 ds=[v for v in (None if w is None else w-(BUCCAL_MM+PALATAL_MM),None if md is None else md-2*PROX_MM) if v is not None]
 return (min(ds) if ds else None),(h-VERT_MARGIN_MM if h is not None else None)

def soft_tissue_notes():
 n=[]
 if r('soft_thickness')=='SUR-STT-DEFICIENT':n.append('Soft-tissue thickness is deficient: plan a connective tissue graft (CTG) for thickness. Record this goal separately from any vertical STH change.')
 if r('keratinized')=='SUR-KT-DEFICIENT':n.append('Keratinized band under 2 mm: plan keratinized tissue augmentation (for example a free gingival graft or an apically positioned flap), before, during or after placement.')
 return n

def implant_options(main):
 # Two parallel options: the main proposal and its first valid alternative, each with type, provisional size ceiling and considerations.
 import re
 txt=main['first']+' ; '+main['alts']
 fams=[]
 for m in re.findall(_FAMRE,txt):
  c='IMP-FAM-'+m
  if c not in fams:fams.append(c)
 fixed={'IMP-FAM-'+f:float(d) for f,d in re.findall(_FAMRE+r' Ø(\d\.\d)',txt)}
 dmax,lmax=size_ceiling()
 out=[]
 for i,c in enumerate(fams[:2]):
  macro,strength,when,caution=PROFILES[c]
  if c in fixed:
   d=fixed[c]
   dia='Ø'+format(d,'.1f')+' mm'+(' · exceeds the measured space' if dmax is not None and d>dmax else '')
  elif c=='IMP-FAM-BLT':
   ok=[x for x in BLT_DIAMETERS if dmax is None or x<=dmax]
   dia=('Ø '+' / '.join(format(x,'.1f') for x in ok)+' mm' if ok else 'No BLT diameter fits the measured space')
  else:dia=('up to Ø'+format(max(dmax,0),'.1f')+' mm (exact diameters pending the SKU table)') if dmax is not None else 'Enter ridge width and mesiodistal space to filter'
  length=('up to '+format(max(lmax,0),'.1f')+' mm (exact lengths pending the SKU table)') if lmax is not None else 'Enter ridge height to filter'
  cons=[('✅',main['why'] if i==0 else strength),('⚠️',main['flt'] if i==0 else caution)]
  if i==0 and main['flt']!=caution:cons.append(('⚠️',caution))
  out.append(dict(code=c,role='Main proposal' if i==0 else 'Alternative',dia=dia,length=length,macro=macro,cons=cons,scenario=main['name'] if i==0 else None))
 return out

def reduced_height():
 u=(r('teeth',[]) or [''])[0][-1:]
 h=r('ridge_height')
 return bool(u) and u in '45678' and (r('vertical_defect') in ('SUR-VDEF-PRESENT','SUR-VDEF-SUSPECTED') or (h is not None and h<=REDUCED_HEIGHT_MM))

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

def opts(var,rows,prefix='PRO'):
 # rows: (key,label,description) -> {response code: (label, description)}
 return {f'{prefix}-{var}-{k}':(l,d) for k,l,d in rows}
def pro_help(definition,options=None):
 parts=[definition] if definition else []
 if options and any(d for _,d in options.values()):parts.append('\n'.join(f'- **{l}**: {d}' for l,d in options.values() if d))
 return '\n\n'.join(parts) or None
def is_maxillary():
 # Upper-jaw site: any selected maxillary tooth (FDI quadrants 1-2) or a maxillary edentulous arch.
 if r('case_type')=='CASE-TYPE-EDENT':return r('arch')=='Maxilla'
 return any(str(t)[:1] in ('1','2') for t in r('teeth',[]))
def is_mandibular():
 if r('case_type')=='CASE-TYPE-EDENT':return r('arch')=='Mandible'
 return any(str(t)[:1] in ('3','4') for t in r('teeth',[]))
def pick(name,label,var_opts,definition=None):
 # Single select with NO pre-selected answer: an unanswered item stays unknown (None), never a default finding.
 labels={c:l for c,(l,_) in var_opts.items()}
 return field(name,st.selectbox,label,default=None,options=list(labels),format_func=lambda c:labels[c],index=None,placeholder='Select…',help=pro_help(definition,var_opts))
def pickmulti(name,label,var_opts,definition,none_code=None):
 labels={c:l for c,(l,_) in var_opts.items()}
 field(name,st.multiselect,label,default=[],options=list(labels),format_func=lambda c:labels[c],placeholder='Select all that apply',help=pro_help(definition,var_opts))
 sel=r(name,[]) or []
 if none_code and none_code in sel and len(sel)>1:notice('"'+labels[none_code]+'" cannot be combined with other options.')
def clear(*names,to=None):
 # Conditional items that are not active must not keep stale answers in the record.
 for n in names:
  record[n]=[] if to=='list' else to
  st.session_state.pop('ui_'+n,None)
def goto(step):
 st.session_state.step=max(0,min(8,step))
 st.rerun()


# -----------------------------------------------------------------------------
# Treatment strategy explorer: clinical-decision prototype (Module 05)
# The dimensional matrix reflects the CLINICIAN-REVISED local project catalog.
# It is not a real-time US store inventory or SKU-by-SKU regulatory check.
# -----------------------------------------------------------------------------
IMPLANT_CATALOG = {
 'IMP-FAM-BLT': {2.9:(10,12,14),3.3:(8,10,12,14),4.1:(8,10,12,14),4.8:(8,10,12,14)},
 'IMP-FAM-BLC': {3.3:(8,10,12,14),3.75:(6,8,10,12,14),4.0:(6,8,10,12,14),4.5:(6,8,10,12,14),5.0:(6,8,10,12,14),5.5:(6,8,10,12,14),6.5:(6,8,10,12,14)},
 'IMP-FAM-BLX': {3.5:(8,10,12,14),3.75:(6,8,10,12,14),4.0:(6,8,10,12,14),4.5:(6,8,10,12,14),5.0:(6,8,10,12,14),5.5:(6,8,10,12,14),6.5:(6,8,10,12,14)},
 'IMP-FAM-TLC': {3.3:(8,10,12,14),3.75:(6,8,10,12,14),4.5:(6,8,10,12,14),5.5:(6,8,10,12),6.5:(6,8,10)},
 'IMP-FAM-TLX': {3.75:(6,8,10,12,14),4.5:(6,8,10,12,14),5.5:(6,8,10,12),6.5:(6,8,10,12)},
}

st.markdown('''<style>
.tp-lead {color:#566B7D;font-size:.90rem;line-height:1.5;margin-top:-8px;margin-bottom:13px}
.tp-finding {background:linear-gradient(180deg,#F5F8FB,#FFFFFF);border:1px solid #E0E8EC;border-radius:12px;padding:13px 14px;min-height:100px}
.tp-finding .k {font-size:.74rem;font-weight:750;color:#48637D;letter-spacing:.04em;text-transform:uppercase}
.tp-finding .v {font-size:1.0rem;font-weight:800;color:#273246;margin:5px 0}
.tp-finding .s {font-size:.76rem;color:#607384;line-height:1.35}
.tp-label {font-size:.76rem;letter-spacing:.075em;text-transform:uppercase;color:#4A777B;font-weight:850;margin-top:9px;margin-bottom:4px}
.tp-chip {display:inline-block;border-radius:999px;padding:5px 11px;font-size:.76rem;font-weight:800;background:#E6F4F3;color:#1E6668;margin:2px 0 9px}
.tp-chip.alt {background:#E9F0FB;color:#355A8C}
.tp-head {border-bottom:1px solid #E3E9ED;padding-bottom:11px;margin-bottom:9px}
.tp-title {font-weight:850;font-size:1.11rem;line-height:1.25;color:#30476C}
.tp-sub {color:#647589;font-size:.82rem;margin-top:3px;line-height:1.35}
.tp-slab {background:#F6F9FA;border:1px solid #E5EBEC;border-radius:11px;padding:10px 12px;margin:7px 0}
.tp-slab h4 {font-size:.81rem;color:#3E5876;font-weight:850;margin:0 0 5px}
.tp-slab p {font-size:.85rem;color:#344253;margin:0 0 5px;line-height:1.45}
.tp-slab p:last-child {margin-bottom:0}
.tp-state {font-size:.78rem;line-height:1.4;padding:9px 11px;border-radius:9px;background:#F5F8FA;color:#344A61;margin-top:8px}
.tp-note {color:#5B6D7E;font-size:.80rem;line-height:1.5}

.tp-round { border-radius:24px; border:1px solid #DCE5E8; background:#F7FAFB; padding:15px 15px 16px; min-height:156px; height:100%; }
.tp-round.ok { border-color:#B7DFC9; background:linear-gradient(145deg,#E9F8EF,#F9FDFB); }
.tp-round.watch { border-color:#F1CB97; background:linear-gradient(145deg,#FFF2E0,#FFFCF7); }
.tp-round.pending { border-color:#E2E9F1; background:linear-gradient(145deg,#F4F7FA,#FFFFFF); }
.tp-round .tp-oval { border-radius:999px; display:inline-block; font-size:.73rem; font-weight:850; padding:4px 10px; margin-bottom:8px; }
.tp-round.ok .tp-oval { color:#18613C; background:#CDECD9; }
.tp-round.watch .tp-oval { color:#985000; background:#FFE2B4; }
.tp-round.pending .tp-oval { color:#5C6A7E; background:#E6ECF1; }
.tp-round .tp-k { font-size:.73rem; font-weight:800; color:#426075; text-transform:uppercase; letter-spacing:.05em; }
.tp-round .tp-v { font-size:1.06rem; font-weight:850; color:#24334A; margin:5px 0 4px; }
.tp-round .tp-detail { font-size:.78rem; line-height:1.4; color:#536476; }
.tp-implant-img { background:linear-gradient(140deg,#F3F8FA,#E7F0F3); border:1px solid #DBE6EA; border-radius:15px; padding:7px 9px; margin:8px 0 12px; text-align:center; }
.tp-implant-img img { height:128px; max-width:100%; width:auto; display:block; margin:auto; }
.tp-implant-caption { text-align:center; font-size:.72rem; color:#5F7282; padding-bottom:3px; }
.tp-route-note { border-radius:14px; border:1px solid #F1C68E; background:#FFF7E9; padding:11px 14px; color:#7F4B11; font-size:.88rem; margin:10px 0 14px; }
.tp-small { font-size:.80rem; line-height:1.45; color:#506277; }
</style>''',unsafe_allow_html=True)

def tp_fmt(v):
 return format(float(v),'.2f').rstrip('0').rstrip('.') if v is not None else '—'


def tp_small_visual(family):
 """Self-contained original SVG schematic, not a manufacturer's catalog image."""
 tissue=family in ('IMP-FAM-TLC','IMP-FAM-TLX')
 family_short=family.rsplit('-',1)[-1]
 xstyle=family_short in ('BLX','TLX')
 # Body with shallow or pronounced horizontal thread ridges. Neck shown only
 # for TLC/TLX. Distinctions are schematic, NOT anatomically scaled designs.
 rib_step=14 if xstyle else 18
 rib_width=44 if xstyle else 32
 ribs=''.join(f'<path d="M {145-rib_width} {y} L 145 {y+7} L {145+rib_width} {y}" stroke="#697E8D" stroke-width="3.5" stroke-linecap="round" fill="none"/>' for y in range(100,211,rib_step))
 neck=('<rect x="131" y="35" width="28" height="64" rx="5" fill="#CCD6DC" stroke="#586F7C" stroke-width="2"/><path d="M131 54H159 M131 65H159" stroke="#8799A2" stroke-width="2"/>' if tissue else '<rect x="109" y="83" width="72" height="15" rx="4" fill="#CCD6DC" stroke="#586F7C" stroke-width="2"/>')
 crest_y=102 if tissue else 97
 label='TISSUE LEVEL' if tissue else 'BONE LEVEL'
 svg=f"""<svg xmlns="http://www.w3.org/2000/svg" width="300" height="240" viewBox="0 0 300 240">
 <rect width="300" height="240" rx="17" fill="#F5F9FA"/>
 <path d="M12 {crest_y} Q68 {crest_y-8} 105 {crest_y} L105 235 H12Z" fill="#EFD7BA" stroke="#C4AB8B" stroke-width="1"/>
 <path d="M195 {crest_y} Q242 {crest_y-10} 288 {crest_y} V235 H195Z" fill="#EFD7BA" stroke="#C4AB8B" stroke-width="1"/>
 <path d="M12 {crest_y-10} Q64 {crest_y-20} 105 {crest_y-10}" fill="none" stroke="#DFAEAC" stroke-width="8" stroke-linecap="round"/>
 <path d="M195 {crest_y-10} Q250 {crest_y-21} 288 {crest_y-10}" fill="none" stroke="#DFAEAC" stroke-width="8" stroke-linecap="round"/>
 <defs><linearGradient id="metal"><stop offset="0" stop-color="#788C97"/><stop offset="0.45" stop-color="#EAF1F5"/><stop offset="0.75" stop-color="#A9BAC3"/><stop offset="1" stop-color="#5F7986"/></linearGradient></defs>
 <path d="M111 95 L179 95 L177 192 Q171 215 145 225 Q119 215 113 192Z" fill="url(#metal)" stroke="#586F7C" stroke-width="2"/>
 {ribs}{neck}
 <text x="17" y="24" font-family="Arial,sans-serif" font-size="14" font-weight="bold" fill="#395973">{family_short}</text>
 <text x="282" y="24" text-anchor="end" font-family="Arial,sans-serif" font-size="11" fill="#5D7280">{label}</text>
 <text x="150" y="235" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#667886">SCHEMATIC · NOT TO SCALE</text>
 </svg>"""
 return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode('utf-8')).decode('ascii')


def tp_clinical_summary():
 """Rounded clinical findings with green/orange/neutral status; never call an unknown safe."""
 site=tp_site_info()
 height,width,md=r('ridge_height'),r('ridge_width'),tp_root_screen()['md']
 min_d=site['low']
 bone_known=height is not None and width is not None and md is not None and min_d is not None
 bone_width_ok=(width>=min_d+2.5 and md>=min_d+3.0) if bone_known else False
 sinus_watch=site['maxilla'] and r('sinus') in ('SUR-SINUS-POSSIBLE','SUR-SINUS-TREATED')
 short_review=site['maxilla'] and site['molar'] and height is not None and height<=REDUCED_HEIGHT_MM
 bone_defect=tp_has_bone_defect()
 sth=r('supracrestal')
 soft=r('soft_thickness')
 kt=r('keratinized')
 soft_known=sth is not None and soft is not None and kt is not None
 soft_issue=(sth is not None and sth<2) or soft=='SUR-STT-DEFICIENT' or kt=='SUR-KT-DEFICIENT'
 if bone_defect or (bone_known and not bone_width_ok) or short_review:
  bone_state='watch'
 elif bone_known:
  bone_state='ok'
 else:bone_state='pending'
 if soft_issue:soft_state='watch'
 elif soft_known:soft_state='ok'
 else:soft_state='pending'
 if sinus_watch:sinus_state='watch'
 elif r('sinus')=='SUR-SINUS-NONE' and site['maxilla']:sinus_state='ok'
 else:sinus_state='pending'
 findings=[
  dict(k='Site',v=', '.join(r('teeth',[]) or [])+' (FDI)',detail=SITE.get(r('site'),'Site pending'),state='ok' if r('site') else 'pending'),
  dict(k='Bone availability',v='H '+tp_fmt(height)+' · W '+tp_fmt(width)+' mm',detail=('8 mm or less: compare sinus vs short implant. ' if short_review else '')+'Inter-root '+tp_fmt(md)+' mm',state=bone_state),
  dict(k='Soft tissue',v='STH '+tp_fmt(sth)+' mm',detail=('Thickness: deficient' if soft=='SUR-STT-DEFICIENT' else 'Thickness: adequate' if soft=='SUR-STT-ADEQUATE' else 'Thickness: unknown')+' · Keratinized: '+('deficient' if kt=='SUR-KT-DEFICIENT' else 'adequate' if kt=='SUR-KT-ADEQUATE' else 'unknown'),state=soft_state),
 ]
 if site['maxilla']:
  sinus_lbl={'SUR-SINUS-POSSIBLE':'Possible pathology','SUR-SINUS-TREATED':'Previously treated','SUR-SINUS-NONE':'No disease reported'}.get(r('sinus'),'Not assessed')
  findings.append(dict(k='Sinus assessment',v=sinus_lbl,detail='Further evaluation required before sinus augmentation' if sinus_watch else 'CBCT confirmation and clinical review required',state=sinus_state))
 else:
  findings.append(dict(k='Restorative space',v=tp_fmt(r('pro_io'))+' mm',detail='Review planned component and occlusion',state='watch' if tp_restorative_space_screen()['warnings'] else 'pending'))
 return findings


def tp_summary_html(item):
 labels={'ok':'✓ Documented','watch':'! Needs review','pending':'• Not confirmed'}
 return ('<div class="tp-round '+item['state']+'"><div class="tp-oval">'+escape(labels[item['state']])+'</div><div class="tp-k">'+escape(item['k'])+'</div><div class="tp-v">'+escape(item['v'])+'</div><div class="tp-detail">'+escape(item['detail'])+'</div></div>')


def tp_patient_alignment(plan):
 priorities=[n for n in (r('needs',[]) or []) if n in NEEDS]
 relevant=[n for n in priorities if n in ('PAT-NEED-VISITS','PAT-NEED-TIME','PAT-NEED-FEAR','PAT-NEED-PAIN')]
 if plan['key']=='B' and relevant and plan.get('short'):
  return 'Potentially aligns with: '+', '.join(NEEDS[n].lower() for n in relevant)+'. Only if clinically feasible.'
 return ''

def tp_site_info():
 t=(r('teeth',[]) or [''])[0]
 if not t:return {'anterior':False,'maxilla':False,'molar':False,'posterior':False,'kind':None,'target':None,'low':None,'high':None}
 pos=t[-1:]
 maxilla=t[0] in '12'
 lower_incisor=pos in '12' and not maxilla
 upper_lateral=pos=='2' and maxilla
 if lower_incisor or upper_lateral: return dict(anterior=True,maxilla=maxilla,molar=False,posterior=False,kind='narrow incisor',target=3.3,low=2.9,high=3.5)
 if pos=='1' and maxilla:return dict(anterior=True,maxilla=True,molar=False,posterior=False,kind='upper central incisor',target=3.75,low=3.3,high=4.0)
 if pos=='3':return dict(anterior=True,maxilla=maxilla,molar=False,posterior=False,kind='canine',target=3.75,low=3.3,high=4.0)
 if pos in '45':return dict(anterior=False,maxilla=maxilla,molar=False,posterior=True,kind='premolar',target=4.0,low=3.75,high=4.0)
 if pos in '678':return dict(anterior=False,maxilla=maxilla,molar=True,posterior=True,kind='molar',target=4.5,low=3.75,high=5.5)
 return dict(anterior=False,maxilla=maxilla,molar=False,posterior=False,kind=None,target=None,low=None,high=None)


def tp_root_screen():
 """Root morphology is a trajectory-specific safety question; an angled abutment cannot fix root collision."""
 if r('adjacent_roots')!='SUR-ROOTS-DILACERATED':
  return dict(active=False,feasible=True,md=r('md_bone'),status='not_applicable',missing=[])
 feas=r('root_3d_feasible')
 clearance=r('root_min_md')
 missing=[]
 if feas is None or feas=='SUR-ROOT3D-UNCERTAIN':missing.append('CBCT verification of a root-safe prosthetically oriented 3D trajectory')
 if clearance is None:missing.append('Minimum root-to-root clearance along the proposed trajectory')
 if feas=='SUR-ROOT3D-NO':status='unsafe_trajectory'
 elif missing:status='pending'
 else:status='measured'
 # Use the NARROWEST verified space along the entire proposed trajectory.
 md=min([float(x) for x in (r('md_bone'),clearance) if x is not None],default=None)
 return dict(active=True,feasible=feas=='SUR-ROOT3D-YES',md=md,status=status,missing=missing)


def tp_surgical_access_guidance():
 opening=r('mouth_opening')
 if opening=='CASE-MOUTH-OPTIMAL':
  return ('Guided surgery can be evaluated first if CBCT planning, guide support, instrument access and workflow suitability permit. Adequate mouth opening alone does not establish guided-surgery eligibility.', 'Guided surgery: candidate for evaluation')
 if opening=='CASE-MOUTH-LIMITED':
  return ('Prioritize assessment of a freehand or shorter-instrument approach if safely accessible. Static-guide sleeves and long drills may not fit; limited opening can also prevent freehand access. Evaluate dynamic navigation or another approach when available.', 'Limited access: freehand / short instruments to evaluate')
 return ('Record maximal mouth opening before deciding between static guidance, dynamic guidance and freehand placement.', 'Surgical access: pending assessment')


def tp_restorative_space_screen():
 """Simplified preoperative space alert based only on the reported interocclusal measure.
 The datum and abutment type are NOT assumed; screening values are not component clearances.
 """
 io=r('pro_io')
 warnings=[]
 missing=[]
 if io is None:
  missing.append('Interocclusal restorative space')
 elif io<TIBASE_SPACE_REVIEW_MM:
  warnings.append(f'LIMITED RESTORATIVE SPACE: {tp_fmt(io)} mm. Review prosthetic feasibility and verify the selected component requirements and measurement reference.')
 elif io<SRA_SPACE_REVIEW_MM:
  warnings.append(f'RESTORATIVE SPACE REVIEW: {tp_fmt(io)} mm. Confirm the space needed for the proposed abutment and restoration.')
 return dict(warnings=warnings,missing=missing,minimum=None,component=None,reference=None,io=io,chs=None)


def tp_loading_guidance():
 if r('esthetic')=='No':
  return ('Conventional/delayed loading or provisionalization is the default comparison for a non-esthetic case; an immediate protocol is secondary and requires a separate clinical indication, sufficient stability and occlusal risk control.', 'Conventional first (non-esthetic site)')
 if r('immediate_loading')=='IMP-IMMLD-YES':
  return ('Immediate provisionalization/loading is under evaluation because the clinician selected it; esthetic concern alone never establishes stability, biomechanical safety or eligibility.', 'Immediate only if validated')
 return ('Conventional loading is the neutral baseline. Consider an immediate protocol only when benefit, insertion stability, anatomy and occlusal conditions support it.', 'Conventional baseline; immediate conditional')


def tp_procedure_recommendations():
 """Screening prompts derived from recorded findings, not a treatment prescription.

 Unknowns are explicit. Favor clinician review over falsely labeling an
 unmeasured or suspected site as healthy.
 """
 info=tp_site_info()
 sth=r('supracrestal')
 thickness=r('soft_thickness')
 kt=r('keratinized')
 # STH <2.0 is a project-specific review trigger, NOT a universal CTG indication.
 ctg_why=[]
 ctg_missing=[]
 if sth is not None and sth<2.0:
  ctg_why.append(f'Supracrestal tissue height {tp_fmt(sth)} mm (<2.0 mm project review threshold): assess a vertical soft-tissue augmentation objective.')
 elif sth is None:ctg_missing.append('Supracrestal tissue height')
 if thickness=='SUR-STT-DEFICIENT':ctg_why.append('Clinician reports inadequate mucosal thickness/volume.')
 elif thickness is None:ctg_missing.append('Soft-tissue thickness/volume assessment')
 ctg_status='suggested' if ctg_why else ('pending' if ctg_missing else 'not_indicated')
 ctg=dict(status=ctg_status,why=ctg_why,missing=ctg_missing,procedure='CTG / soft-tissue augmentation review',
          note='CTG can increase tissue volume; a predictable increase in vertical STH is not guaranteed. Confirm technique and objective clinically.')

 fgg_why=[]
 fgg_missing=[]
 if kt=='SUR-KT-DEFICIENT':fgg_why.append('Keratinized mucosa is reported insufficient (<2 mm category).')
 elif kt is None:fgg_missing.append('Keratinized mucosa assessment')
 fgg_status='suggested' if fgg_why else ('pending' if fgg_missing else 'not_indicated')
 fgg=dict(status=fgg_status,why=fgg_why,missing=fgg_missing,procedure='FGG / keratinized-tissue augmentation review',
          note='FGG is one option for increasing keratinized mucosa; esthetic zone, plaque control, symptoms and alternative techniques matter.')

 # Width is measured relative to prosthetically correct position. For a single
 # tooth, mesiodistal space is assumed to be bounded by adjacent natural roots.
 min_d=info['low']
 w,md=r('ridge_width'),tp_root_screen()['md']
 gbr_why=[]
 gbr_missing=[]
 if min_d is None:gbr_missing.append('Single-tooth site and tooth type')
 else:
  width_req=min_d+1.5+1.0
  md_req=min_d+1.5+1.5
  if w is None:gbr_missing.append('Ridge width measured at the planned implant position')
  elif w+1e-8<width_req:
   gbr_why.append(f'Ridge width {tp_fmt(w)} mm < {tp_fmt(width_req)} mm needed for Ø{tp_fmt(min_d)} (vestibular 1.5 + palatal/lingual 1.0 mm).')
  if md is None:gbr_missing.append('Mesiodistal space between adjacent roots, including trajectory-specific root clearance if dilacerated')
  elif md+1e-8<md_req:
   gbr_why.append(f'Interradicular width {tp_fmt(md)} mm < {tp_fmt(md_req)} mm needed for Ø{tp_fmt(min_d)} (1.5 mm mesial + 1.5 mm distal). GBR alone does not increase root-to-root space: evaluate root positions, orthodontic/prosthetic alternatives or another eligible implant size.')
 for key,bad,label in (
  ('horizontal_defect',('SUR-HDEF-PRESENT',),'Clinician reports a horizontal bone deficiency.'),
  ('vertical_defect',('SUR-VDEF-PRESENT',),'Clinician reports a vertical bone deficiency.'),
  ('facial_defect',(_DEH,_FEN),'Clinician reports an anticipated dehiscence or fenestration.'),
 ):
  value=r(key)
  if value in bad:gbr_why.append(label)
  elif value in ('SUR-HDEF-SUSPECTED','SUR-VDEF-SUSPECTED'):
   gbr_why.append(label.replace('reports','suspects').replace('a horizontal','a possible horizontal').replace('a vertical','a possible vertical'))
  elif value is None:gbr_missing.append(key.replace('_',' ')+' assessment')
 root_check=tp_root_screen()
 # Root collision is a distinct anatomical issue, NOT an automatic indication for GBR.
 # It is handled by the root-pathway alert and blocks dimensional clearance.
 status='suggested' if gbr_why else ('pending' if gbr_missing else 'not_indicated')
 gbr=dict(status=status,why=gbr_why,missing=gbr_missing,procedure='GBR / bone-defect treatment assessment',
          note='A dimensional deficit triggers bone/space planning review, not automatic GBR. A narrow interradicular gap cannot be widened with GBR alone. Confirm CBCT 3D position, defect morphology, stability and restorative alternatives.',
          min_d=min_d,required_width=(min_d+2.5 if min_d is not None else None),required_md=(min_d+3.0 if min_d is not None else None),
          preferred_diameter=(4.0 if info['molar'] else None),
          md_only_conflict=(min_d is not None and md is not None and md+1e-8<min_d+3.0
                            and (w is None or w+1e-8>=min_d+2.5)
                            and r('horizontal_defect')=='SUR-HDEF-NONE'
                            and r('vertical_defect')=='SUR-VDEF-NONE'
                            and r('facial_defect')=='SUR-FACIAL-NONE') and not (root_check['status']=='unsafe_trajectory'))
 return {'CTG':ctg,'FGG':fgg,'GBR':gbr}

def tp_has_bone_defect():
 p=tp_procedure_recommendations()['GBR']
 # A root collision or insufficient space between roots alone is NOT a bone deficit treatable by GBR.
 if p['md_only_conflict'] or tp_root_screen()['status']=='unsafe_trajectory':return False
 return p['status']=='suggested'

def tp_has_soft_defect():
 recs=tp_procedure_recommendations()
 return recs['CTG']['status']=='suggested' or recs['FGG']['status']=='suggested' or r('sth_adequacy')=='IMP-STH-NO'

def tp_family_pair(level):
 info=tp_site_info()
 narrow=info['kind']=='narrow incisor' and ((r('pro_md') is not None and r('pro_md')<6.0))
 if narrow:return 'IMP-FAM-BLT','IMP-FAM-BLC'
 imm=r('immediate_loading')=='IMP-IMMLD-YES' and r('esthetic')=='Yes'
 if level=='TL':return ('IMP-FAM-TLX','IMP-FAM-TLC') if imm else ('IMP-FAM-TLC','IMP-FAM-TLX')
 if imm or r('bone_quality')=='SUR-BQ-D4':return 'IMP-FAM-BLX','IMP-FAM-BLT'
 if r('immediate_placement')=='IMP-IMMPL-YES':return 'IMP-FAM-BLT','IMP-FAM-BLX'
 return 'IMP-FAM-BLC','IMP-FAM-BLT'

def tp_anatomical_guidance():
 """Location-specific CBCT review inside proposals; NO additional clinician input.

 Measurements are user-entered and cannot establish 3D distance to an anatomical
 structure unless that structure is the actual measurement reference. No
 patient-specific clearance is inferred from tooth number alone.
 """
 teeth=r('teeth',[]) or []
 if r('case_type')=='CASE-TYPE-EDENT':
  arch=r('arch')
  label='Edentulous '+str(arch or 'arch')
  msg=('Mandible: identify inferior alveolar canals, mental foramina, anterior loops and lingual concavities along EACH planned implant trajectory.' if arch=='Mandible' else
       'Maxilla: evaluate sinus and nasal floors, nasopalatine canal and site-specific residual bone along EACH proposed implant trajectory.' if arch=='Maxilla' else
       'Identify the arch and the limiting anatomy for each proposed implant trajectory.')
  return dict(region=label,structure='Multiple site-specific anatomical structures',margin=None,review=msg,
              calculation='No universal length ceiling for a full arch; review each implant site individually.',limited=True)
 if not teeth:
  return dict(region='Unspecified site',structure='Not determined',margin=None,
              review='Select the tooth/region in Case Type & Site to identify the relevant structures.',
              calculation='No site-specific anatomical clearance can be estimated.',limited=True)
 t=str(teeth[0]); quadrant=t[0] if len(t)==2 else ''; pos=t[-1]
 multiple=len(teeth)>1
 prefix=('Multiple teeth selected: this review uses the first selected tooth '+t+'. Assess every additional site independently. ' if multiple else '')
 if quadrant in '34' and pos in '45678':
  premolar=pos in '45'
  return dict(region='Mandibular '+('premolar' if premolar else 'posterior'),
    structure=('Inferior alveolar canal; mental foramen and possible anterior loop' if premolar else 'Inferior alveolar canal (IAC); lingual concavity'),margin=2.0,
    review=prefix+('Identify the mental foramen and map any anterior loop in 3D; a vertical height measurement cannot establish nerve clearance.' if premolar else 'Confirm the superior IAC boundary and evaluate lingual undercut and cortical perforation risk in CBCT.'),
    calculation='A 2 mm margin is a preliminary screen ONLY if the entered height was measured from crest to the relevant nerve boundary along the proposed implant axis. The anterior loop requires separate 3D mapping.' if premolar else 'A 2 mm margin is a preliminary screen ONLY if residual height is measured from crest to the superior IAC border along the proposed implant axis.',limited=premolar or multiple)
 if quadrant in '34':
  return dict(region='Mandibular anterior',structure='Lingual cortical concavity; incisive canal / nearby mental foramen where relevant',margin=None,
   review=prefix+'Review lingual plate, mandibular incisive canal and any nearby mental neurovascular anatomy in CBCT. Do not infer a nerve-safety distance from the tooth number.',
   calculation='No universal structure-based vertical deduction is available from the entered height alone.',limited=True)
 if quadrant in '12' and pos in '45678':
  return dict(region='Maxillary posterior',structure='Maxillary sinus floor; adjacent nasal floor if applicable',margin=2.0,
   review=prefix+'Check sinus health, local anatomy and the implant trajectory. Sinus-floor elevation follows a separate treatment pathway if indicated.',
   calculation='A 2 mm no-sinus-elevation screening allowance is a conservative PROJECT assumption, not a universal safety margin. It applies only if the height was measured to the sinus floor along the proposed implant axis.',limited=multiple)
 if quadrant in '12':
  return dict(region='Maxillary anterior',structure='Nasal floor; nasopalatine canal; facial bone plate',margin=None,
   review=prefix+'Evaluate the nasal floor, nasopalatine canal, buccal plate and prosthetically driven 3D trajectory.',
   calculation='No universal height subtraction establishes safe implant length in this region; the limiting anatomy must be identified in CBCT.',limited=True)
 return dict(region='Site not classified',structure='Individual CBCT review needed',margin=None,
             review=prefix+'Assess the limiting anatomical structures in three dimensions.',
             calculation='No location-specific screening calculation available.',limited=True)


def tp_anatomical_proposal_text(plan):
 """Readable, explicitly conditional summary; never declare anatomical clearance."""
 a=tp_anatomical_guidance()
 h=r('ridge_height')
 items=['Region: '+a['region'], 'Relevant anatomy: '+a['structure'], a['review']]
 if h is None:
  items.append('Residual bone height not entered; no vertical screening calculation possible.')
 elif a['margin'] is None:
  items.append('Entered residual height: '+tp_fmt(h)+' mm. '+a['calculation'])
 else:
  cap=h-a['margin']
  items.append('Entered residual height: '+tp_fmt(h)+' mm; conditional screening allowance: '+tp_fmt(a['margin'])+' mm; numerical ceiling: '+(tp_fmt(cap)+' mm' if cap>0 else 'no positive length')+'. '+a['calculation'])
 if plan.get('post'):
  items.append('Implant dimensions must be reassessed after staged augmentation; these preoperative calculations are not post-graft clearance.')
 else:
  pick=plan.get('sizes',{}).get('pick')
  if pick:
   items.append('Candidate '+tp_fmt(pick[1])+' mm length passes the numerical filter only; verify actual 3D clearance, insertion depth, drill-tip extension and the manufacturer IFU.')
  else:
   items.append('No implant length is established from the current screened data.')
 return items


def tp_sizes(family,post_augmentation=False,short_only=False):
 'Dimensional screening only, never an implant clearance or full 3D CBCT analysis.'
 info=tp_site_info()
 w,md,h=r('ridge_width'),tp_root_screen()['md'],r('ridge_height')
 root_check=tp_root_screen()
 if root_check['status']=='unsafe_trajectory':
  return dict(diameters=[],lengths=[],pick=None,ceiling=None,facial=BUCCAL_MM,reason='Unsafe CBCT trajectory relative to dilacerated roots. No implant is cleared; an angled abutment cannot make an unsafe trajectory acceptable.')
 if root_check['status']=='pending':
  return dict(diameters=[],lengths=[],pick=None,ceiling=None,facial=BUCCAL_MM,reason='Root dilaceration: confirm minimum space along the full planned implant trajectory and verify 3D position before recommending a size.')
 # Avoid implying that an unmeasured dimension is adequate.
 dims_known=w is not None and md is not None
 # User-defined minimum is 1.5 mm buccal; ~2 mm remains a preferred esthetic target.
 # The minimal threshold is not a surgical clearance, especially in thin facial cortical bone.
 facial=1.5
 max_d=min(w-facial-PALATAL_MM,md-2*PROX_MM) if dims_known else None
 all_d=IMPLANT_CATALOG[family]
 diameters=[d for d in all_d if (info['low'] is None or info['low']<=d<=info['high']) and (max_d is None or d<=max_d)]
 # Regenerated bone must be remeasured before any candidate diameter or length is proposed.
 if post_augmentation:return dict(diameters=[],lengths=[],pick=None,ceiling=None,facial=facial,reason='Reassess the regenerated anatomy before specifying an implant dimension.')
 if not dims_known:diameters=[]
 if not diameters: return dict(diameters=[],lengths=[],pick=None,ceiling=max_d,facial=facial,reason='Bone width and interradicular distance are required.' if not dims_known else 'No listed diameter meets the current preliminary space screen.')
 if h is None:return dict(diameters=diameters,lengths=[],pick=None,ceiling=max_d,facial=facial,reason='Residual bone height is missing; no exact length is proposed.')
 # Simple conservative initial length screen, NOT a fixed safety requirement for all sites.
 length_cap=h-VERT_MARGIN_MM
 length_candidates={d:[int(x) for x in all_d[d] if x<=length_cap and (not short_only or x<=8)] for d in diameters}
 valid_diameters=[d for d in diameters if length_candidates[d]]
 if not valid_diameters:
  return dict(diameters=[],lengths=[],pick=None,ceiling=max_d,facial=facial,reason='No catalog diameter/length pair satisfies the conservative preliminary height screen; consider further assessment or reconstruction.')
 target=info['target'] or valid_diameters[0]
 diameter=min(valid_diameters,key=lambda d:(abs(d-target),d))
 ls=length_candidates[diameter]
 chosen=10 if 10 in ls else max(ls)
 return dict(diameters=valid_diameters,lengths=ls,pick=(diameter,chosen),ceiling=max_d,facial=facial,reason='Provisional dimensional match; verify complete implant/osteotomy geometry, CBCT anatomy, prosthetics, IFU and exact USA SKU.')

def tp_restoration_text():
 retention=r('preview_retention')
 access=r('preview_access')
 ret={
  'TP-RET-SCREW':'Screw-retained restoration preferred, if access and component compatibility permit.',
  'TP-RET-SCREWMENT':'Screw-cement retained (extraoral cementation) to evaluate, if components and retrievability are appropriate.',
  'TP-RET-CEMENT':'Cement-retained restoration to evaluate with particular attention to residual cement.',
 }.get(retention,'Evaluate screw-retained vs screw-cement retained vs cement-retained options.')
 acc={
  'TP-ACC-STRAIGHT':'Straight screw channel anticipated; confirm wax-up and restorability.',
  'TP-ACC-ANGLED':'Angled screw-channel concept to assess within the manufacturer-approved component limits.',
 }.get(access,'Screw-access axis not assessed; straight vs angled channel remains open.')
 return ret,acc

# Gallucci et al., Clin Implant Dent Relat Res 2026: placement x loading terminology.
# Decision logic below is a PREOPERATIVE project interpretation, not a
# validated predictor of patient-level survival or an intraoperative loading clearance.
GALLUCCI_EVIDENCE = {
 '1A': 'SCV', '1B': 'CD', '1C': 'SCV',
 '2–3A': 'SCV', '2–3B': 'CD', '2–3C': 'SCV',
 '4A': 'SCV', '4B': 'SCV', '4C': 'SCV',
}

def tp_placement_group(plan):
 """Estimate placement class from clinical site; staged changes are unclassified."""
 site=r('site')
 if plan.get('post'):
  return None,'Staged intervention: timing of implant placement cannot be assigned until the planned post-extraction/reconstruction healing interval is known.'
 if site=='CASE-SITE-EXTRACT':
  # The contemporaneous plan can be immediate only if it has not been staged.
  return '1','Type 1 candidate: extraction and implant placement in the same intervention.'
 if site=='CASE-SITE-SOFT':return '2–3','Type 2 timing: 4–8 weeks after extraction.'
 if site=='CASE-SITE-PARTIAL':return '2–3','Type 3 timing: 12–16 weeks after extraction.'
 if site=='CASE-SITE-HEALED':return '4','Type 4 timing: healed ridge, >6 months after extraction.'
 return None,'The recorded healing interval is not within the defined Type 1/2/3/4 windows; assess timing individually before assigning a Gallucci code.'

def tp_loading_candidates(placement):
 """Prioritize candidate loading times without asking for actual implant stability."""
 needs=r('needs',[]) or []
 urgency=r('esthetic')=='Yes' or any(n in needs for n in ('PAT-NEED-ESTH','PAT-NEED-TIME','PAT-NEED-VISITS'))
 para=r('pro_para')
 abnormal=para in ('PRO-PARA-SELF','PRO-PARA-SUSPECTED','PRO-PARA-BOTH')
 occlusal=r('pro_plane')
 risk=abnormal or occlusal in ('PRO-PLANE-ALTERED','PRO-PLANE-NOTASSESSABLE')
 unknown_occlusion=para is None or occlusal is None
 # Conventional is always the fallback; do not infer success of immediate loading.
 if urgency and not risk and not unknown_occlusion:return ['A','C'], 'Patient priorities justify considering immediate provisionalization, conditional on intraoperative stability, implant position and control of loading.'
 if urgency and (risk or unknown_occlusion):return ['C','A'], 'Unknown or unfavorable occlusal/parafunctional findings favor a conservative preliminary pathway; immediate provisionalization remains a conditional alternative.'
 return ['C','A'], 'Without a patient-centered reason for immediate restoration, conventional loading is the neutral initial pathway.'

def tp_protocol_for_plan(plan, loading_letter):
 group,placement_note=tp_placement_group(plan)
 if group is None:
  return dict(code=None, name='Placement/loading protocol pending',evidence=None,placement=placement_note,
              loading='Timing must be assigned after site reassessment.', provisional='Use a non-implant provisional restoration when appropriate.')
 code=group+loading_letter
 names={'A':'Immediate restoration / loading (≤1 week)',
        'B':'Early loading (>1 week to <2 months)',
        'C':'Conventional loading (≥2 months)'}
 return dict(code=code,name=names[loading_letter],evidence=GALLUCCI_EVIDENCE.get(code),placement=placement_note,
             loading=('Immediate PMMA implant-supported provisional may be considered if anatomic, stability and occlusal criteria are confirmed during surgery; distinguish non-functional restoration from functional loading.' if loading_letter=='A' else
                      'Early implant-supported restoration only after a clinical stability reassessment.' if loading_letter=='B' else
                      'Allow conventional healing before implant loading; consider Essix, adhesive provisional or another non-implant-supported interim solution if needed.'),
             provisional=('PMMA provisional concept; verify available restorative space, components, fixation and occlusal design.' if loading_letter=='A' else 'Definitive material is selected according to restorative needs and is not dictated by the Gallucci code.'))

def tp_augmentation_summary():
 rec=tp_procedure_recommendations()
 lines=[]
 if rec['GBR']['status']=='suggested':
  lines.append('GBR / bone reconstruction assessment: '+('; '.join(rec['GBR']['why'][:2]))+' Confirm whether simultaneous GBR, staged augmentation or a different implant dimension is appropriate; inter-root space cannot be increased by GBR.')
 elif rec['GBR']['status']=='pending':lines.append('GBR: cannot rule out until missing measurements and defect information are completed.')
 if rec['CTG']['status']=='suggested':
  lines.append('CTG / soft-tissue optimization to assess: '+('; '.join(rec['CTG']['why'][:2]))+' Vertical supracrestal tissue height gain is not guaranteed.')
 elif rec['CTG']['status']=='pending':lines.append('CTG: volume/thickness assessment pending.')
 if rec['FGG']['status']=='suggested':lines.append('FGG or another keratinized tissue augmentation technique to assess: '+('; '.join(rec['FGG']['why'][:2])))
 elif rec['FGG']['status']=='pending':lines.append('Keratinized tissue assessment pending.')
 if not lines:lines.append('No augmentation screening trigger detected in the recorded measurements; verify 3D anatomy and tissue suitability.')
 return lines

# Compact preoperative history; all values are patient-reported, not diagnostic.
MEDICAL_RISK_OPTIONS = {
 'NONE': 'No known relevant medical history / risk factors',
 'PERIO': 'History of periodontitis',
 'DIABETES': 'Diabetes mellitus',
 'TOBACCO': 'Tobacco / nicotine use',
 'CARDIO': 'Cardiovascular disease / hypertension',
 'IMMUNE': 'Immunosuppression / impaired healing',
 'ANTIR': 'Antiresorptive or antiangiogenic medication',
 'RADIATION': 'Head / neck radiotherapy',
 'ANTICOAG': 'Anticoagulant / antiplatelet medication',
 'HYGIENE': 'Difficulty maintaining oral hygiene',
 'OTHER': 'Other relevant medical condition or medication',
}
MAJOR_MEDICAL_FLAGS={'IMMUNE','ANTIR','RADIATION'}

def tp_medical_alerts():
 flags=set(r('medical_risk_factors',[]) or [])
 if not flags or 'NONE' in flags and len(flags)>1:return []
 alerts=[]
 if flags & MAJOR_MEDICAL_FLAGS:
  alerts.append('Medical risk factors requiring individualized implant-surgery assessment: '+', '.join(MEDICAL_RISK_OPTIONS[x] for x in sorted(flags & MAJOR_MEDICAL_FLAGS))+'. Review current therapy, dose/route/timing when relevant and interdisciplinary clearance as indicated; the CDSS cannot confirm surgical eligibility.')
 if 'ANTICOAG' in flags:
  alerts.append('Review bleeding risk and current medication with the treating physician when indicated; do not advise stopping prescribed therapy automatically.')
 if 'CARDIO' in flags:
  alerts.append('Review the relevant cardiovascular condition and medical fitness before surgery.')
 if 'OTHER' in flags:
  alerts.append('Review the additional medical history entered by the clinician before finalizing the treatment plan.')
 return alerts

def tp_maintenance_guidance():
 # A blank answer must never mean that the patient has no risk factors.
 flags=set(r('medical_risk_factors',[]) or [])
 if not flags or ('NONE' in flags and len(flags)>1):
  return 'Maintenance interval pending: patient-reported medical history / risk factors have not been completed or contain conflicting selections.'
 if 'DIABETES' in flags and r('diabetes_control') in (None, 'Control unknown'):
  return 'Maintenance interval pending: clarify patient-reported diabetes control.'
 if 'TOBACCO' in flags and r('smoking_status') in (None, 'Status unknown'):
  return 'Maintenance interval pending: clarify tobacco exposure.'
 if flags & MAJOR_MEDICAL_FLAGS:
  return 'Individualized maintenance required: medical risk warrants additional review. Do not assign a recall interval from the medical history alone.'
 higher=('PERIO' in flags or 'HYGIENE' in flags or
         ('TOBACCO' in flags and r('smoking_status')=='Current tobacco use') or
         ('DIABETES' in flags and r('diabetes_control')=='Diabetes: not well controlled'))
 if higher:
  return 'Consider supportive peri-implant maintenance every 3–4 months initially, subject to periodontal examination, plaque control and reassessment.'
 return 'Consider supportive peri-implant maintenance every 4–6 months, individualized after periodontal evaluation and re-evaluated over time.'

def tp_build_plans():
 'Two comparative pathways; unresolved/unfeasible ideas are clearly labeled.'
 level,reasons,missing=implant_level()
 info=tp_site_info()
 h=r('ridge_height')
 sinus_case=info['maxilla'] and info['molar'] and h is not None and h<=REDUCED_HEIGHT_MM
 gbr_case=tp_has_bone_defect() or r('gbr_approach')=='IMP-GBR-SIMULT' or (r('gbr_approach')=='IMP-GBR-STAGED' and r('staged_status')!='IMP-STG-HEALED')
 soft_case=tp_has_soft_defect() or r('ctg_planned')=='IMP-CTG-YES'
 staged_pending=(r('gbr_approach')=='IMP-GBR-STAGED' and r('staged_status')!='IMP-STG-HEALED')
 root_check=tp_root_screen()
 space_only=(root_check['status'] in ('unsafe_trajectory','pending') or
             (tp_procedure_recommendations()['GBR']['md_only_conflict'] and r('gbr_approach') not in ('IMP-GBR-SIMULT','IMP-GBR-STAGED')))
 mode='routine'
 if staged_pending:mode='staged_pending'
 elif space_only:mode='space'
 elif gbr_case:mode='gbr'
 elif sinus_case:mode='sinus'
 elif soft_case:mode='soft'
 first,second=tp_family_pair(level)
 plans=[dict(key='A',family=first,post=False,short=False,surgery='',title='',subtitle='',constraints='',pros='',limits=''),
        dict(key='B',family=second,post=False,short=False,surgery='',title='',subtitle='',constraints='',pros='',limits='')]
 a,b=plans
 if mode=='sinus':
  # The order is intentionally reconstructive first, less-invasive second.
  # 8 mm of residual bone prompts COMPARISON, never automatic indication for sinus lift.
  suspected=r('sinus')=='SUR-SINUS-POSSIBLE'
  sinus_first=('First assess and appropriately manage or obtain specialist clearance for the possible sinus pathology documented in Surgical Assessment. ' if suspected else 'Confirm sinus health and anatomy before planning augmentation. ')
  a.update(title='Sinus Floor Elevation',subtitle='Reconstructive option · conditional on sinus evaluation',
           family='IMP-FAM-BLC',post=True,
           surgery=sinus_first+'Then consider transcrestal or lateral sinus floor elevation, with implant placement simultaneous or staged according to residual bone, achievable primary stability and sinus assessment.',
           pros='May provide additional vertical bone support if the native bone does not allow a suitable implant.',
           limits='Sinus augmentation is not automatically required at 8 mm. It may involve extra morbidity, expense and treatment stages; a final implant length and design depend on postoperative reassessment.')
  # Under the local CDSS, Tissue Level is considered only when mucosa and bone
  # are adequate and there is no simultaneous CTG/GBR. Otherwise use Bone Level.
  short_family='IMP-FAM-TLC' if level=='TL' else 'IMP-FAM-BLC'
  b.update(title='Short Implant · No Sinus Elevation',subtitle='Reduced-intervention option · only if anatomically feasible',
           family=short_family,short=True,
           surgery='Consider direct placement of a catalog-listed short implant in native bone WITHOUT sinus elevation, provided the CBCT trajectory, restorative 3D position, stability, bone support and drilling/implant safety are appropriate. '+('The apparent sinus pathology still requires clinical assessment; absence of sinus elevation does not make sinus disease irrelevant.' if suspected else 'Confirm the sinus floor and CBCT anatomy.'),
           pros='May avoid a separate sinus augmentation procedure and align with patient priorities for fewer surgeries and less morbidity, when a safe short-implant option exists.',
           limits='A short implant remains surgery and is not always feasible. Consider crown-height space, occlusal forces, bone density, implant length/diameter and evidence; a dimensional candidate is not an automatic treatment recommendation.')
 elif mode=='space':
  a.update(title='Root-safe 3D Planning / Space Review',subtitle='Implant placement deferred until root-safe geometry is verified',surgery='Evaluate space management, neighboring root positions, orthodontic or prosthetic alternatives before any implant osteotomy. GBR alone cannot increase the distance between natural roots.',post=True,pros='Addresses the actual spatial limitation rather than adding bone unnecessarily.',limits='Dilacerated roots or inadequate root-to-root spacing require CBCT re-evaluation; no implant dimensions are cleared until the planned trajectory is safe.')
  b.update(title='Alternative Restorative Strategy',subtitle='Explore non-implant or revised restoration concepts',surgery='Reassess the planned restorative design and a revised 3D position. Only reconsider a smaller implant if its site-specific IFU indication and biomechanics allow it; no implant is dimensionally cleared at present.',post=True,pros='Avoids mistakenly describing a root-space problem as a bone-volume defect treatable by GBR.',limits='Requires clinical review and new or verified interradicular dimensions.')
 elif mode=='gbr':
  a.update(title='Simultaneous GBR',subtitle='Implant and localized augmentation in one intervention',surgery='Consider simultaneous GBR only if prosthetically correct 3D placement, primary stability, graft stabilization and tension-free soft-tissue closure are achievable.',pros='May avoid a separate reconstruction stage for a suitably contained/localized defect.',limits='Not appropriate solely because the defect appears small: morphology and stability govern feasibility.')
  b.update(title='Staged Bone Regeneration',subtitle='Reconstruct first; remeasure after healing',surgery='Perform staged ridge augmentation when the defect or inability to achieve safe 3D placement/stability calls for site development.',post=True,pros='Allows reconstruction and reassessment before implant selection.',limits='Additional intervention/healing time; final size and platform cannot be confirmed until reassessment.')
  # Local CDSS policy: simultaneous GBR -> Bone Level. Do not suggest TL until staged regeneration is healed and re-evaluated.
  if first.startswith('IMP-FAM-T'):a['family']='IMP-FAM-BLC'
  if second.startswith('IMP-FAM-T'):b['family']='IMP-FAM-BLT'
 elif mode=='soft':
  recs=tp_procedure_recommendations()
  target_text=(' Consider CTG-based augmentation for STH <2 mm or inadequate mucosal volume; assess the vertical gain objective rather than promising it.' if recs['CTG']['status']=='suggested' else '')
  kt_text=(' Consider FGG or a suitable alternative for deficient keratinized tissue.' if recs['FGG']['status']=='suggested' else '')
  a.update(title='Simultaneous Soft-tissue Augmentation',subtitle='Manage the documented deficit during implant placement',surgery='Assess soft-tissue augmentation at implant placement.'+target_text+kt_text,pros='May address the soft-tissue objective during the implant intervention.',limits='CTG does not reliably guarantee increased vertical STH. FGG and CTG have different primary objectives; technique and timing require clinical judgment.')
  b.update(title='Staged Soft-tissue Optimization',subtitle='Augment tissue and re-evaluate the implant site',surgery='Consider a staged soft-tissue procedure if adequate tissues or an appropriate restorative platform cannot be achieved at placement.',post=True,pros='Allows tissue stability and the definitive implant level to be reassessed.',limits='Extra surgical phase; Tissue Level can be reconsidered only if the final tissue and bone conditions are favorable.')
  if first.startswith('IMP-FAM-T'):a['family']='IMP-FAM-BLC'
  if second.startswith('IMP-FAM-T'):b['family']='IMP-FAM-BLT'
 elif mode=='staged_pending':
  a.update(title='Staged GBR — Required First',subtitle='Implant choice deferred until ridge reconstruction heals',surgery='Complete the planned staged GBR and reassess the reconstructed ridge, soft tissues and implant axis.',post=True,pros='Defers the implant choice until a reliable post-augmentation anatomy is available.',limits='Do not specify a definitive implant size or claim Tissue Level eligibility before reassessment.')
  b.update(title='Re-evaluate Alternative Plan',subtitle='Clinical review of reconstruction needs',surgery='Reassess defect morphology and whether a different surgical or prosthetic approach can meet the restorative objectives. No direct-placement pathway is cleared.',post=True,pros='Provides a clinician review pathway without assuming unnecessary augmentation.',limits='An alternative pathway cannot be offered as clinically feasible without new measurements and a 3D plan.')
 else:
  a.update(title='Direct Placement Strategy',subtitle='No additional regeneration if truly unnecessary',surgery='Assess direct placement within the existing ridge; confirm primary stability, 3D restoration-guided position and soft-tissue adequacy.',pros='Can avoid augmentation if sufficient bone and tissues are confirmed.',limits='Do not treat incomplete tissue, bone or sinus findings as absence of a defect.')
  b.update(title='Alternative Implant Design',subtitle='Same surgical pathway, different macrodesign',surgery='Compare the same non-regenerative surgical pathway using an alternative implant geometry and its drilling protocol.',pros='A second implant-design option without inventing a reconstructive indication.',limits='The design comparison is not evidence that a different implant is superior for this patient.')
 # Overlay a Gallucci protocol on each existing surgical alternative.
 candidate_letters, loading_reason=tp_loading_candidates(None)
 for i,p in enumerate(plans):
  p['protocol']=tp_protocol_for_plan(p,candidate_letters[i])
  p['loading_rationale']=loading_reason
  p['augmentations']=tp_augmentation_summary()
  p['maintenance']=tp_maintenance_guidance()
 for p in plans:
  access_text,_=tp_surgical_access_guidance()
  p['surgery']+=' Surgical access: '+access_text
  p['loading']=tp_loading_guidance()[0]
  recs_p=tp_procedure_recommendations()
  if (recs_p['CTG']['status']=='suggested' or r('ctg_planned')=='IMP-CTG-YES') and mode not in ('soft','staged_pending'):
   p['surgery']+=' Assess CTG/soft-tissue augmentation to address volume and/or the STH concern; vertical gain is not guaranteed.'
  if recs_p['FGG']['status']=='suggested' and mode not in ('soft','staged_pending'):
   p['surgery']+=' Assess FGG or another technique for inadequate keratinized mucosa, with timing individualized.'
  d=tp_sizes(p['family'],post_augmentation=p['post'],short_only=p['short'])
  p['sizes']=d
  p['anatomy']=tp_anatomical_proposal_text(p)
  p['size_display']=('Ø'+tp_fmt(d['pick'][0])+' × '+tp_fmt(d['pick'][1])+' mm · screening candidate') if d['pick'] else 'Dimensions pending / no valid match'
  if p['post']:p['status']='Provisional: reassess after augmentation / revised planning'
  elif not d['pick']:p['status']='Not dimensionally cleared with current data'
  else:p['status']='Dimensional candidate only — clinical validation required'
  if p['key']=='A' and mode=='gbr':
   sup=gbr_support()
   if sup and sup['verdict'] in ('staged','selected','pending'):
    p['status']=('Simultaneous GBR not supported by screening criteria' if sup['verdict']=='staged' else 'Simultaneous GBR suitability pending review')
  if mode=='sinus' and r('sinus') in ('SUR-SINUS-POSSIBLE','SUR-SINUS-TREATED'):
   p['status']='Sinus condition requires assessment before pathway selection'
  if tp_restorative_space_screen()['warnings']:
   p['status']+=' · restorative space review required'
  if root_check['active'] and r('root_access') in (None,'SUR-ROOTACCESS-UNRESOLVED'):
   p['status']+=' · restorative access pathway pending'
 return dict(mode=mode,level=level,reasons=reasons,missing=missing,plans=plans)

def tp_export_html(plans_result):
 name=escape(str(r('name') or 'Not recorded'))
 teeth=escape(', '.join(r('teeth',[]) or []))
 snippets=[]
 for p in plans_result['plans']:
  snippets.append('<section><h2>Option '+p['key']+' — '+escape(p['title'])+'</h2><p>'+escape(p['subtitle'])+'</p><p><b>Approach:</b> '+escape(p['surgery'])+'</p><p><b>Implant:</b> '+escape(FAMILIES[p['family']])+'</p><p><b>Dimensions:</b> '+escape(p['size_display'])+'</p><p><b>Anatomical considerations:</b> '+escape(' | '.join(p['anatomy']))+'</p><p><b>Loading approach:</b> '+escape(p['loading'])+'</p><p><b>Status:</b> '+escape(p['status'])+'</p><p><b>Potential benefit:</b> '+escape(p['pros'])+'</p><p><b>Limitation:</b> '+escape(p['limits'])+'</p></section>')
 recs=tp_procedure_recommendations()
 active=[k for k in ('CTG','FGG','GBR') if recs[k]['status']=='suggested']
 procedure_summary=('<section><h2>Additional procedures to evaluate</h2>'+''.join('<p><b>'+k+':</b> '+escape('; '.join(recs[k]['why']))+'</p>' for k in active)+'</section>') if active else ''
 ret,acc=tp_restoration_text()
 additional='<section><h2>Clinical review alerts</h2>'+''.join('<p>'+escape(x)+'</p>' for x in tp_restorative_space_screen()['warnings'])+'<p>'+escape(tp_loading_guidance()[0])+'</p><p>'+escape(tp_surgical_access_guidance()[0])+'</p></section>'
 return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Implant treatment comparison</title><style>body{font:15px Arial,sans-serif;max-width:970px;margin:38px auto;color:#273246}h1{color:#35537e}section{border:1px solid #dae4e7;border-radius:12px;padding:20px;margin:14px 0}h2{color:#365e74}p{line-height:1.5}.footer{font-size:12px;color:#607080}</style></head><body><h1>Treatment Strategy &amp; Implant Selection</h1><p><b>Patient:</b> '+name+' &nbsp; <b>Site (FDI):</b> '+teeth+'</p><p><b>Clinical notes:</b> '+escape(', '.join(plans_result['reasons']) or 'Pending clinical review')+'</p>'+procedure_summary+additional+''.join(snippets)+'<section><h2>Restorative discussion</h2><p>'+escape(ret)+'</p><p>'+escape(acc)+'</p></section><p class="footer">Clinical decision-support draft only. Dimensions are from the clinician-edited project matrix and are not verified US SKUs. Use current manufacturer IFU, case-specific CBCT evaluation and clinician judgment. This report may include patient data; handle securely.</p></body></html>')

with st.sidebar:
 # 1 · Patient name (large) + compact context
 if r('case_type')=='CASE-TYPE-EDENT':case_line='Edentulous · '+str(r('arch','Arch not selected'))
 else:case_line=CASE_TYPES.get(r('case_type'),'Case not set')+' · '+((', '.join(r('teeth',[]))+' (FDI)') if r('teeth',[]) else 'tooth not selected')
 st.markdown('<div class="side-head"><img class="side-avatar" src="'+AVATAR_URI+'" alt=""><div><div class="side-name">'+escape(r('name','') or 'Patient name not entered')+'</div>'
  '<div class="side-meta">'+escape(f"{int(r('age_years'))} years ({AGE_SHORT[r('age')]})" if r('age') else 'Age not recorded')+'<br>'+escape(case_line)+'</div></div></div>',unsafe_allow_html=True)
 # 2 · Patient priorities (most important first)
 needs=[n for n in r('needs',[]) if n in NEEDS]
 top=r('top_priority')
 ordered=([top] if top in needs else [])+[n for n in needs if n!=top]
 if ordered:
  items=''.join('<div class="prio-item'+(' prio-top' if i==0 and top in needs else '')+'">• '+escape(NEEDS[n])+('  <span class="pill pill-top">Top priority</span>' if i==0 and top in needs else '')+'</div>' for i,n in enumerate(ordered))
 else:items='<div class="small-muted">No priorities selected yet</div>'
 st.markdown('<div class="priority-panel"><div class="section-label">Patient priorities</div>'+items+'</div>',unsafe_allow_html=True)
 # 3 · Treatment sequence and recommendations
 st.markdown('<div class="side-nav section-label">Case Navigation</div>',unsafe_allow_html=True)
 for i in range(4):
  if st.button(MODULES[i],key=f'side_{i}',use_container_width=True,type='primary' if st.session_state.step==i else 'secondary'):goto(i)
 st.markdown('<div class="side-nav section-label">Proposals</div>',unsafe_allow_html=True)
 for i in range(4,8):
  if st.button(MODULES[i],key=f'side_{i}',use_container_width=True,type='primary' if st.session_state.step==i else 'secondary'):goto(i)
 if st.button('Case Summary',use_container_width=True,type='primary' if st.session_state.step==8 else 'secondary'):goto(8)
 if st.button('Reset demo case',use_container_width=True):
  st.session_state.record={'needs':[],'case_type':'CASE-TYPE-SINGLE','teeth':[],'esthetic':'No'}
  for k in list(st.session_state.keys()):
   if k.startswith('ui_'):del st.session_state[k]
  goto(0)

st.markdown('<div class="topline"></div>',unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="eyebrow">EVIDENCE-BASED · PATIENT-CENTERED · CLINICALLY DRIVEN</div><h1 style="margin:5px 0">Implant Planning Decision Explorer</h1></div>',unsafe_allow_html=True)
step=st.session_state.step
if step<8:
 st.progress((step+1)/8,text=('05 / 08 · Treatment proposals' if step==4 else f'{step+1:02d} / 08 · {MODULES[step]}'))
 if step != 4: st.subheader(f'{step+1:02d} · {MODULES[step]}')
else:st.subheader('Case Summary · Shared Decision-Making')

if step==0:
 st.caption('Module PAT: complete this first; values are reused in clinical proposals and the patient snapshot.')
 field('name',st.text_input,'Patient name',default='',placeholder='Enter patient name')
 field('age_years',st.number_input,'Age (years)',default=None,value=None,min_value=0,max_value=110,step=1,placeholder='Enter age in years')
 if r('age'):st.caption('Age group (automatic): '+AGES[r('age')])
 st.caption(age_scale_text(r('age')))
 listfield('needs','Patient needs and concerns · select all that apply',NEEDS,max_selections=8)
 # Human readable priority-order among selected options.
 selected=r('needs',[])
 if selected:
  prio_opts=[NO_PRIORITY]+selected
  if r('top_priority') not in prio_opts:record['top_priority']=NO_PRIORITY
  if st.session_state.get('ui_top_priority',NO_PRIORITY) not in prio_opts:st.session_state.pop('ui_top_priority',None)
  ranked=field('top_priority',st.selectbox,'Most important concern',default=NO_PRIORITY,options=prio_opts,format_func=lambda k:PRIORITY_LABELS[k])
  if r('top_priority')==NO_PRIORITY:st.caption('No single priority is highlighted; the selected concerns are shown without ranking.')
  else:st.caption('This priority influences how viable plans are compared, not clinical eligibility.')
 st.markdown('**Medical history & risk factors**')
 st.caption('Patient-reported · select all that apply. Leave blank only if the history has not yet been assessed.')
 field('medical_risk_factors',st.multiselect,'Relevant medical history / risk factors',default=[],options=list(MEDICAL_RISK_OPTIONS),format_func=lambda c:MEDICAL_RISK_OPTIONS[c],placeholder='Select conditions or No known relevant history')
 medical_flags=set(r('medical_risk_factors',[]) or [])
 if 'NONE' in medical_flags and len(medical_flags)>1:
  notice('“No known relevant medical history” cannot be selected together with a risk factor. Please correct the selection.')
 if 'DIABETES' in medical_flags:
  field('diabetes_control',st.selectbox,'Diabetes control (patient-reported)',default=None,options=['Diabetes: well controlled','Diabetes: not well controlled','Control unknown'],index=None,placeholder='Select only if known')
 else:
  clear('diabetes_control')
 if 'TOBACCO' in medical_flags:
  field('smoking_status',st.selectbox,'Tobacco use',default=None,options=['Current tobacco use','Former tobacco use','Status unknown'],index=None,placeholder='Select only if known')
 else:
  clear('smoking_status')
 if 'OTHER' in medical_flags:
  field('medical_other_details',st.text_input,'Other condition / medication (optional)',default='',placeholder='Brief description')
 else:
  clear('medical_other_details')
 for medical_alert in tp_medical_alerts():
  st.warning(medical_alert)
 if r('age')=='PAT-AGE-U18':notice('Assess completion of craniofacial growth; avoid assuming implant eligibility from chronological age alone.')
 if r('age')=='PAT-AGE-O60P':st.info('Evaluate individual dexterity, medical status and maintenance needs; age alone is not a contraindication.')

elif step==1:
 case_type=choose('case_type','Case type',CASE_TYPES)
 if case_type=='CASE-TYPE-EDENT':
  choose('arch','Edentulous arch',['Maxilla','Mandible'])
  st.caption('Full-arch treatment planning is outside the current single-tooth prototype.')
 else:
  st.markdown('**Tooth selection**')
  st.caption('Universal / FDI · Select or deselect teeth. Selected teeth appear in lime.')
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
  with st.container(key='tooth_picker'):
   for qname,teeth in QUADRANTS:
    st.markdown('<div class="tooth-quadrant-label">'+escape(qname)+'</div>',unsafe_allow_html=True)
    columns=st.columns(8,gap='small')
    for col,(fdi,universal) in zip(columns,teeth):
     with col:
      selected=fdi in record.get('teeth',[])
      st.button(f'{universal} / {fdi}',key=f'odon_{fdi}',type='primary' if selected else 'secondary',use_container_width=True,on_click=toggle_tooth,args=(fdi,))
   chosen=record.get('teeth',[])
   st.markdown('**Selected teeth:** '+(', '.join(f'{FDI_UNI[fdi]} / {fdi}' for fdi in chosen) if chosen else 'None selected'))
  if case_type=='CASE-TYPE-SHORT':st.caption('Short Span allows up to three teeth. To select another, deselect one first.')
 choose('esthetic','Does this case involve an esthetic concern?',['No','Yes'])
 pick('mouth_opening','Maximal mouth opening',opts('MOUTH',[('OPTIMAL','Optimal','Opening sufficient for surgical and restorative instrument access.'),('LIMITED','Limited','Opening that restricts access for surgical or restorative instrumentation (e.g., posterior sites, guided surgery).')],prefix='CASE'),'Assessment of whether the maximal mouth opening allows adequate access for the planned surgery and restoration.')
 field('site',st.selectbox,'Current site condition',default=None,options=list(SITE),format_func=lambda c:SITE[c],index=None,placeholder='Select…')

elif step==2:
 st.caption('Three domains of the prosthetic assessment. All are relevant to planning and none depends on another: complete them in any order. Hover over the ⓘ next to each item for its definition and options.')
 c1,c2,c3=st.columns(3)
 # ---------------- 1 · Restorative Space ----------------
 with c1:
  with st.container(border=True):
   st.markdown('<div class="col-title">Restorative Space</div><div class="col-desc">Three-dimensional space available for the planned implant-supported restoration.</div>',unsafe_allow_html=True)
   numeric('pro_md','Mesiodistal space (mm)',help='Distance available mesiodistally for the future restoration, bounded by the proximal surfaces of the adjacent teeth or restorations.')
   numeric('pro_io','Interocclusal restorative space (mm)',help='Record the available vertical restorative space measured against the opposing dentition. The reference level is essential for applying component-specific requirements.')
   space_info_=tp_restorative_space_screen()
   for msg_ in space_info_['warnings']:st.warning(msg_)
 # ---------------- 2 · Restoration–Tissue Relationship ----------------
 with c2:
  with st.container(border=True):
   st.markdown('<div class="col-title">Restoration–Tissue Relationship</div><div class="col-desc">Relationship between the existing tissue architecture and the planned restorative contours.</div>',unsafe_allow_html=True)
   st.markdown('<div class="section-label sub-label">Restorative reference</div>',unsafe_allow_html=True)
   REF=opts('REF',[('WAX','Diagnostic wax-up','Diagnostic wax-up.'),('DIGITAL','Digital restorative setup','Digital restorative planning.'),('CONTRA','Contralateral tooth','Homologous contralateral tooth.'),('ADJ','Adjacent teeth','Adjacent teeth used as anatomical reference.')])
   pick('pro_ref','Planned restoration reference',REF,'Reference used to establish the ideal position and anatomy of the future restoration.')
   if r('pro_ref') in ('PRO-REF-CONTRA','PRO-REF-ADJ'):notice('Contralateral or adjacent teeth give only an approximate reference. A diagnostic wax-up or a digital restorative setup is always recommended for a more precise evaluation.')
   st.markdown('<div class="section-label sub-label">Ridge contour &amp; volume · horizontal</div>',unsafe_allow_html=True)
   RIDGE=opts('RIDGE',[('ADEQUATE','Adequate','Existing contour is compatible with the desired restorative contour.'),('DEFICIENT','Deficient','Contour loss relative to the desired restorative volume.')])
   pick('pro_ridge','Ridge contour relative to planned restoration',RIDGE,'Relationship between the current ridge contour and the cervical volume required to reproduce the planned restoration anatomy.')
   if r('pro_ridge')=='PRO-RIDGE-DEFICIENT':numeric('pro_ridge_mm','Ridge contour discrepancy (mm)',max_value=20,help='Magnitude of the horizontal difference between the buccal ridge contour and the anatomy of the planned restoration. Does not by itself imply a bone defect diagnosis.')
   else:clear('pro_ridge_mm')
   st.markdown('<div class="section-label sub-label">Mucosal margin &amp; papillae · vertical</div>',unsafe_allow_html=True)
   MARGIN=opts('MARGIN',[('AT','At planned level','Coincides with the planned restorative level.'),('CORONAL','Coronal','More coronal than the desired level.'),('APICAL','Apical','More apical than the desired level.')])
   pick('pro_margin','Mucosal margin position',MARGIN,'Position of the current mucosal margin relative to the ideal cervical location of the future restoration.')
   if r('pro_margin')=='PRO-MARGIN-APICAL':numeric('pro_margin_mm','Mucosal margin discrepancy (mm)',max_value=20,help='Magnitude of the vertical difference between the current mucosal margin and the planned cervical margin.')
   else:clear('pro_margin_mm')
   PAP=lambda v:opts(v,[('PRESERVED','Preserved','Interproximal tissue adequately fills the intended space.'),('REDUCED','Reduced','Partial fill of the interproximal space.'),('ABSENT','Absent','No clinically identifiable papilla.'),('NA','Not applicable','Does not apply to this type of restoration.')])
   pick('pro_pap_m','Mesial papilla',PAP('PAPM'),'Degree to which mesial soft tissue fills the interproximal space relative to the planned cervical architecture.')
   pick('pro_pap_d','Distal papilla',PAP('PAPD'),'Degree to which distal soft tissue fills the interproximal space relative to the planned restorative architecture.')
 # ---------------- 3 · Occlusal Assessment ----------------
 with c3:
  with st.container(border=True):
   st.markdown('<div class="col-title">Occlusal Assessment</div><div class="col-desc">Existing occlusal relationships, functional support and anticipated loading.</div>',unsafe_allow_html=True)
   st.markdown('<div class="section-label sub-label">Occlusal relationships</div>',unsafe_allow_html=True)
   PLANE=opts('PLANE',[('PRESERVED','Preserved','Clinically stable occlusion, without relevant alterations that could compromise load distribution.'),('ALTERED','Altered','Occlusal alterations that could compromise load distribution on the future restoration.'),('NOTASSESSABLE','Not assessable','The occlusal conditions cannot be evaluated.')])
   pick('pro_plane','Occlusal plane',PLANE,'Assessment of the existing occlusal conditions and whether they could compromise load distribution on the future restoration.')
   if r('pro_plane')=='PRO-PLANE-ALTERED':
    ALT=opts('PLANEALT',[('SUPRA','Supraeruption','Extrusion of one or more teeth relative to the occlusal plane.'),('TIPPING','Tooth tipping','Dental inclination that alters the occlusal arrangement.'),('DISCREP','Occlusal plane discrepancy','Irregularity not described by the other categories.'),('OTHER','Other','Another alteration, to be specified.')])
    pickmulti('pro_plane_alt','Occlusal plane alteration',ALT,'Alteration that compromises the continuity or regularity of the occlusal plane.')
    if 'PRO-PLANEALT-OTHER' in (r('pro_plane_alt',[]) or []):field('pro_plane_alt_other',st.text_input,'Specify other alteration',default='')
    else:clear('pro_plane_alt_other',to='')
   else:clear('pro_plane_alt',to='list');clear('pro_plane_alt_other',to='')
   st.markdown('<div class="section-label sub-label">Parafunctional activity</div>',unsafe_allow_html=True)
   PARA=opts('PARA',[('NONE','None identified','No parafunctional activity identified with the available information.'),('SELF','Self-reported','Parafunctional activity reported by the patient.'),('SUSPECTED','Clinically suspected','Clinical suspicion based on the examination.'),('BOTH','Both','Both self-reported and clinically suspected.')])
   pick('pro_para','Parafunctional activity',PARA,'Reported or clinically suspected parafunctional mandibular muscle activity.')
 # ---------------- preliminary prompts (not validated rules) ----------------
 if r('esthetic')=='Yes':st.info('Esthetic concern recorded. Evaluate provisionalization and soft-tissue architecture in restorative proposals.')
 if r('pro_ridge')=='PRO-RIDGE-DEFICIENT' or r('pro_margin')=='PRO-MARGIN-APICAL':st.info('Assess soft-tissue and/or volume augmentation options; timing and indication require evaluation.')
 if tp_restorative_space_screen()['warnings']:
  st.warning('Restorative space review required before considering the treatment plan technically feasible. Confirm selected component dimensions, appropriate crestal/reference measurements, occlusion and restorative materials.')

elif step==3:
 st.caption('Three domains of the surgical assessment. All are relevant to planning and none depends on another: complete them in any order. CBCT measurements are interpreted relative to the prosthetically ideal implant position.')
 c1,c2,c3=st.columns(3)
 with c1:
  with st.container(border=True):
   st.markdown('<div class="col-title">Bone Availability &amp; Quality</div><div class="col-desc">Which bone do we have?</div>',unsafe_allow_html=True)
   numeric('ridge_height','Residual bone height (mm)')
   numeric('ridge_width','Ridge width (mm)')
   pick('bone_quality','Bone quality (density)',opts('BQ',[('D1','D1 · Dense cortical bone','Almost entirely dense cortical bone.'),('D2','D2 · Thick cortex, coarse trabeculae','Thick dense-to-porous cortical bone surrounding coarse trabecular bone.'),('D3','D3 · Thin cortex, fine trabeculae','Thin porous cortical bone surrounding fine trabecular bone.'),('D4','D4 · Fine trabeculae, minimal cortex','Fine trabecular bone with almost no cortical layer.')],prefix='SUR'),'Bone density class (Misch), estimated from CBCT and/or tactile feedback during osteotomy. Informs implant macrogeometry, drilling protocol and expectations of primary stability.')
   st.caption('Informs: dimensions, macrogeometry and expectations of primary stability.')
 with c2:
  with st.container(border=True):
   st.markdown('<div class="col-title">Anatomical &amp; Local Constraints</div><div class="col-desc">Which structures or conditions restrict the treatment?</div>',unsafe_allow_html=True)
   numeric('md_bone','Mesiodistal space between adjacent roots (mm)')
   numeric('supracrestal','Supracrestal tissue height (mm)',max_value=20)
   if is_maxillary():
    pick('sinus','Sinus assessment',opts('SINUS',[('NONE','No evident disease',''),('POSSIBLE','Possible sinus pathology',''),('TREATED','Previously treated sinus condition','')],prefix='SUR'))
   else:clear('sinus');st.caption('Sinus assessment appears for maxillary sites (select the tooth or arch in Case Type & Site).')
   pick('adjacent_pathology','Adjacent teeth',opts('ADJ',[('NONE','No pathology identified',''),('REVIEW','Pathology requires review','')],prefix='SUR'))
   pick('adjacent_roots','Adjacent root morphology',opts('ROOTS',[('NONE','No relevant alteration','Normal root morphology.'),('DILACERATED','Dilacerated roots','Roots with abnormal curvature or angulation.')],prefix='SUR'),'Morphology of the roots of the teeth adjacent to the site, assessed on CBCT. Dilacerated roots can reduce the interradicular space and alter the three-dimensional position of the implant.')
   if r('adjacent_roots')=='SUR-ROOTS-DILACERATED':
    st.warning('Reassess root-to-root clearance ALONG THE PROPOSED 3D IMPLANT TRAJECTORY. A change in axis may be possible, but only if the entire implant path remains safe. An angled abutment cannot compensate for root collision.')
    pick('root_3d_feasible','Root-safe, prosthetically guided 3D placement feasible?',opts('ROOT3D',[('YES','Yes, verified on CBCT','Correct 3D implant positioning is demonstrably feasible without root collision.'),('NO','No, unsafe root collision / inadequate trajectory','Implant placement must be re-planned; an angled prosthetic component cannot solve surgical collision.'),('UNCERTAIN','Undetermined · further CBCT planning required','Do not clear dimensions until feasibility has been established.')],prefix='SUR'),'Verify the COMPLETE trajectory, not only a cross-section at the crest.')
    numeric('root_min_md','Narrowest interradicular clearance along planned trajectory (mm)',max_value=25,help='Minimum root-to-root distance along the full proposed implant axis. The CDSS applies ≥1.5 mm to each adjacent natural root in this screening calculation.')
    pick('root_access','Prosthetic access after trajectory correction',opts('ROOTACCESS',[('STRAIGHT','Straight screw-channel access feasible','Restoration-guided straight access possible without violating root safety.'),('ANGLED','Angled screw channel / abutment to evaluate','The planned implant axis is root-safe but the prosthetic access may need manufacturer-approved angulated components.'),('UNRESOLVED','Not yet assessable','Check wax-up, component availability, angulation limits and biomechanical factors.')],prefix='SUR'),'Angled restorative parts may compensate for screw-access direction, but never for an unsafe bone/adjacent-root trajectory.')
    if r('root_3d_feasible')=='SUR-ROOT3D-NO':st.error('Unsafe 3D trajectory: no implant design or length should be cleared. Reconsider the surgical position or treatment strategy.')
   else:clear('root_3d_feasible');clear('root_min_md');clear('root_access')
   # The old multi-select of named structures was intentionally removed from the UI.
   # Stale values are not reused after this release.
   record.pop('anat_structures',None)
   st.session_state.pop('ui_anat_structures',None)
   # Retired CBCT-clearance selector; keep unknown values from affecting recommendations.
   record.pop('cbct_clearance',None)
   st.session_state.pop('ui_cbct_clearance',None)
 with c3:
  with st.container(border=True):
   st.markdown('<div class="col-title">Bone Deficiencies &amp; Surgical Considerations</div><div class="col-desc">Can the implant be placed correctly, with sufficient bone support?</div>',unsafe_allow_html=True)
   pick('horizontal_defect','Horizontal bone deficiency',opts('HDEF',[('NONE','None apparent',''),('PRESENT','Present',''),('SUSPECTED','Suspected','')],prefix='SUR'))
   if r('horizontal_defect') in ('SUR-HDEF-PRESENT','SUR-HDEF-SUSPECTED'):numeric('h_aug','Horizontal augmentation required (mm)',max_value=20,help='Horizontal bone gain needed to place the implant with adequate buccal and palatal bone. Guides simultaneous (1 to 3 mm) versus staged (6 mm or more) regeneration. The defect morphology matters as much as the number.')
   else:clear('h_aug')
   pick('vertical_defect','Vertical bone deficiency',opts('VDEF',[('NONE','None apparent',''),('PRESENT','Present',''),('SUSPECTED','Suspected','')],prefix='SUR'))
   pick('facial_defect','Facial defect relative to prosthetic axis',opts('FACIAL',[('NONE','None anticipated',''),('DEHISCENCE','Potential dehiscence',''),('FENESTRATION','Potential fenestration','')],prefix='SUR'))
   if r('facial_defect')==_DEH:numeric('deh_height','Dehiscence height (mm)',max_value=20,help='Vertical height of the exposed implant surface expected at the buccal aspect. A height of 3 mm or less is considered a small defect.')
   else:clear('deh_height')
   if r('facial_defect') in ('SUR-FACIAL-DEHISCENCE','SUR-FACIAL-FENESTRATION'):
    pick('angulation','Angulated pathway',opts('ANGUL',[('FEASIBLE','Potentially feasible',''),('NOTAPPROPRIATE','Not prosthetically appropriate','')],prefix='SUR'))
   else:clear('angulation')
   st.markdown('<div class="section-label sub-label">Soft tissue</div>',unsafe_allow_html=True)
   pick('soft_thickness','Soft-tissue thickness (volume)',opts('STT',[('ADEQUATE','Adequate',''),('DEFICIENT','Deficient','')],prefix='SUR'),'Quantity of peri-implant soft tissue (thickness/volume) at the site. A deficiency points to a connective tissue graft (CTG) to increase thickness; it is not the same as vertical supracrestal tissue height.')
   pick('keratinized','Keratinized tissue band',opts('KT',[('ADEQUATE','Adequate (2 mm or more)',''),('DEFICIENT','Deficient (less than 2 mm)','')],prefix='SUR'),'Quality of the peri-implant soft tissue: a keratinized band under 2 mm is considered deficient and calls for keratinized tissue augmentation.')
   st.caption('Informs: direct placement, alternative positions, GBR, soft-tissue augmentation and implant level.')
 st.info('No implant is cleared based on height or width alone. Anatomy, safety distances and manufacturer dimensions require independent assessment.')

elif step==4:
 # Module 05: clinical comparison first. Keep surgical screening in the logic,
 # not as noisy three-column 'not triggered' cards.
 root_review_=tp_root_screen()
 space_review_=tp_restorative_space_screen()
 if r('case_type')!='CASE-TYPE-SINGLE':
  notice('Paired plans currently cover single-tooth restorations. Other case types require separate validated logic.')
 elif not r('teeth') or r('site') is None:
  st.info('Select the tooth and current site condition in Case Type & Site to see the treatment comparison.')
 else:
  st.markdown('<div class="section-label" style="margin:5px 0 12px">Clinical summary</div>',unsafe_allow_html=True)
  fcols=st.columns(4,gap='small')
  for col_,finding_ in zip(fcols,tp_clinical_summary()):
   with col_: st.markdown(tp_summary_html(finding_),unsafe_allow_html=True)

  # Only display actionable safety information. Findings already known to be
  # adequate do not need a redundant 'not indicated' panel.
  if r('sinus')=='SUR-SINUS-POSSIBLE' and tp_site_info()['maxilla']:
   st.markdown('<div class="tp-route-note"><b>Sinus finding needs attention:</b> Surgical Assessment reports possible sinus pathology. Confirm the diagnosis and manage it or obtain appropriate clearance <b>before sinus augmentation</b>. The direct short-implant pathway also requires review of sinus health, CBCT anatomy and clinical suitability.</div>',unsafe_allow_html=True)
  elif r('sinus')=='SUR-SINUS-TREATED' and tp_site_info()['maxilla']:
   st.warning('A previously treated sinus condition is reported. Check current status and suitability before selecting either surgical pathway.')
  if root_review_['active'] and root_review_['status']!='measured':
   st.warning('Dilacerated roots: complete a root-safe 3D CBCT trajectory assessment before selecting an implant. An angled abutment cannot resolve root collision.')
  for alert_ in space_review_['warnings']:
   st.warning(alert_)
  result_=tp_build_plans()
  # Only a brief, contextual bridge between clinical findings and choices.
  st.markdown('<div class="section-label" style="margin:12px 0 10px">Treatment proposals · Gallucci placement and loading protocols</div>',unsafe_allow_html=True)
  if result_['mode']=='sinus':
   st.caption('Posterior maxillary site with '+tp_fmt(r('ridge_height'))+' mm residual height. This triggers a comparison, not an automatic indication for sinus elevation or for a short implant.')
  elif result_['mode']=='space':
   st.caption('Implant placement is not cleared while the root/mesiodistal trajectory remains unsafe or unverified.')
  cols_=st.columns(2,gap='medium')
  for col_,plan_ in zip(cols_,result_['plans']):
   with col_:
    with st.container(border=True):
     chip_class_='tp-chip' if plan_['key']=='A' else 'tp-chip alt'
     st.markdown('<div class="'+chip_class_+'">OPTION '+plan_['key']+'</div><div class="tp-head"><div class="tp-title">'+escape(plan_['title'])+'</div><div class="tp-sub">'+escape(plan_['subtitle'])+'</div></div>',unsafe_allow_html=True)
     protocol_=plan_['protocol']
     if protocol_['code']:
      st.markdown('### Protocol '+protocol_['code'])
      st.caption(protocol_['placement']+' · '+protocol_['name']+' · '+('SCV' if protocol_['evidence']=='SCV' else 'Clinically documented: limited evidence'))
     else:st.warning(protocol_['name']+': '+protocol_['placement'])
     st.markdown('<div class="tp-slab"><h4>🩺 Surgical approach</h4><p>'+escape(plan_['surgery'])+'</p></div>',unsafe_allow_html=True)
     st.markdown('**Site-derived augmentation assessment**')
     for aug_ in plan_['augmentations']:st.write('• '+aug_)
     alignment_=tp_patient_alignment(plan_)
     if alignment_:
      st.markdown('<div class="tp-state"><b>Patient-centered value:</b> '+escape(alignment_)+'</div>',unsafe_allow_html=True)
     svg_=tp_small_visual(plan_['family'])
     level_label_='Tissue Level' if plan_['family'] in ('IMP-FAM-TLC','IMP-FAM-TLX') else 'Bone Level'
     st.markdown('<div class="tp-implant-img"><img src="'+svg_+'" alt="Illustrative '+escape(level_label_)+' implant diagram"><div class="tp-implant-caption">'+escape(level_label_)+' · '+escape(FAMILIES[plan_['family']])+' · schematic, not an official product photograph</div></div>',unsafe_allow_html=True)
     sz_=plan_['sizes']
     st.markdown('<div class="tp-slab"><h4>🦷 Implant design & dimensions</h4><p><b>Family:</b> '+escape(FAMILIES[plan_['family']])+'</p><p><b>Example:</b> '+escape(plan_['size_display'])+'</p></div>',unsafe_allow_html=True)
     st.markdown('**Anatomical considerations · site-specific CBCT review**')
     for line_ in plan_['anatomy']:
      st.caption('• '+line_)
     if sz_['pick']:
      with st.expander('Catalog sizes that pass preliminary screening'):
       st.write('Diameters: '+', '.join('Ø'+tp_fmt(v)+' mm' for v in sz_['diameters']))
       st.write('Lengths for candidate diameter: '+', '.join(str(v)+' mm' for v in sz_['lengths']))
       st.caption(sz_['reason'])
     else:
      st.caption('No dimensions cleared yet: '+sz_['reason'])
     st.markdown('<div class="tp-slab"><h4>⚙️ Preliminary restorative strategy</h4><p>'+escape(tp_restoration_text()[0])+'</p><p>'+escape(tp_restoration_text()[1])+'</p></div>',unsafe_allow_html=True)
     st.markdown('<div class="tp-slab"><h4>⚙️ Prosthetic approach</h4><p>'+escape(protocol_['loading'])+'</p><p>'+escape(protocol_['provisional'])+'</p></div>',unsafe_allow_html=True)
     st.markdown('<div class="tp-slab"><h4>🗓️ Maintenance protocol</h4><p>'+escape(plan_['maintenance'])+'</p></div>',unsafe_allow_html=True)
     st.markdown('<div class="tp-state"><b>Preoperative feasibility:</b> '+escape(plan_['status'])+'</div>',unsafe_allow_html=True)
     with st.expander('Benefits, limitations & rationale'):
      st.markdown('**Benefit:** '+plan_['pros'])
      st.markdown('**Limitations:** '+plan_['limits'])
      st.markdown('**Macrodesign rationale:** '+PROFILES[plan_['family']][1])
  st.caption('Bone/Tissue Level diagrams are original conceptual illustrations, not manufacturer photos. Replace them with approved catalog product images when available. Neither plan is approved without CBCT, prosthetic analysis and current manufacturer IFU.')

  # Keep choices editable without obstructing the treatment comparison.
  with st.expander('Edit clinical decisions · CTG, FGG, GBR, loading & restoration',expanded=False):
   st.caption('These questions influence the two proposed pathways. Unanswered fields remain unknown; an unknown finding is never treated as adequate anatomy.')
   cs,ct=st.columns(2)
   yesno=lambda v:opts(v,[('YES','Yes',''),('NO','No','')],prefix='IMP')
   with cs:
    pick('ctg_planned','Clinician decision: simultaneous CTG?',yesno('CTG'),'This does not erase an automatic CTG assessment trigger. CTG can add volume but predictable vertical STH gain cannot be assumed.')
    pick('fgg_timing','Clinician decision: keratinized-tissue augmentation',opts('FGG',[('REVIEW','Undecided / review FGG or alternatives',''),('SIMULT','Consider FGG simultaneous',''),('STAGED','Consider FGG before implant placement',''),('LATER','Consider FGG after restoration / placement',''),('NO','Not planned (document rationale)','')],prefix='IMP'),'FGG is primarily used to increase keratinized mucosa; the exact approach is influenced by site and treatment stage.')
    st.caption('STH is evaluated automatically using the clinician-defined <2.0 mm review trigger; the numeric measurement comes from Surgical Assessment. Vertical graft outcome is not assumed.')
    st.caption('Immediate-placement eligibility is screened automatically from site timing and CBCT information; no surgical outcome is requested.')
    clear('immediate_placement')
   with ct:
    pick('gbr_approach','Bone-regeneration approach under consideration',opts('GBR',[('NONE','No GBR planned',''),('SIMULT','Simultaneous GBR','Implant placement and localized bone regeneration in one intervention, only when all surgical conditions support it.'),('STAGED','Staged GBR before implant','Reconstruct first, reassess after healing and then choose implant design/dimensions.')],prefix='IMP'),'Select an intended approach to compare, not a permission to bypass constraints.')
    if r('gbr_approach')=='IMP-GBR-STAGED':pick('staged_status','Status of staged GBR',opts('STG',[('PENDING','Not yet performed','Implant selection must be deferred.'),('HEALED','Healed and reevaluated','The anatomical measurements refer to the healed augmented site.')],prefix='IMP'))
    else:clear('staged_status')
    st.caption('Loading candidates are generated from preoperative findings and patient priorities. Primary stability will only be confirmed intraoperatively.')
    clear('immediate_loading')
    if r('esthetic')=='No':st.caption('No esthetic concern: the CDSS will NOT prioritize an immediate protocol as its first plan, even when selected for discussion.')
   support_=gbr_support()
   if support_:
    with st.container(border=True):
     st.caption('Defect size alone does not decide timing; morphology, positioning, stability and closure matter.')
     ac,bc=st.columns(2)
     for i_,(k_,lab_,c_) in enumerate(GBR_CRITERIA):
      with (ac if i_%2==0 else bc):pick(k_,lab_,opts(c_,[('YES','Yes',''),('NO','No','')],prefix='IMP'))
     support_=gbr_support()
     for t_ in support_['notes']:st.write('• '+t_)
     if support_['failed']:st.warning('Criteria not met: '+', '.join(support_['failed']))
     st.caption('GBR screening: '+support_['verdict']+'. This is guidance, not a surgical clearance.')
   st.markdown('**Preliminary restorative decisions**')
   rc1,rc2=st.columns(2)
   with rc1:
    field('preview_retention',st.selectbox,'Preferred retention concept',default=None,options=['TP-RET-SCREW','TP-RET-SCREWMENT','TP-RET-CEMENT'],format_func=lambda x:{'TP-RET-SCREW':'Screw-retained','TP-RET-SCREWMENT':'Screw-cement retained / screwmentable','TP-RET-CEMENT':'Cement-retained'}[x],index=None,placeholder='To be evaluated')
   with rc2:
    field('preview_access',st.selectbox,'Screw-access path',default=None,options=['TP-ACC-STRAIGHT','TP-ACC-ANGLED'],format_func=lambda x:{'TP-ACC-STRAIGHT':'Straight screw channel','TP-ACC-ANGLED':'Angled screw channel'}[x],index=None,placeholder='Not yet assessed')

  st.markdown('#### Select a pathway to investigate')
  st.caption('No pathway is automatically prescribed or approved. Choose a working strategy for review, or leave the decision open.')
  choice_=field('treatment_path',st.selectbox,'Treatment pathway to investigate',default=None,options=['A','B'],format_func=lambda v:'Option '+v+' · '+result_['plans'][0 if v=='A' else 1]['title'],index=None,placeholder='No decision yet')
  family_codes_=[p['family'] for p in result_['plans']]
  other_codes_=[c for c in FAMILIES if c not in family_codes_]
  field('implant_family',st.selectbox,'Implant design selected (clinician editable)',default=None,options=list(dict.fromkeys(family_codes_+other_codes_)),format_func=lambda c:FAMILIES[c],index=None,placeholder='Select only after review')
  if choice_ in ('A','B'):
   requested_family_=result_['plans'][0 if choice_=='A' else 1]['family']
   if st.button('Use implant family from selected pathway',key='apply_selected_path_family'):
    record['implant_family']=requested_family_
    st.session_state.pop('ui_implant_family',None)
    st.rerun()
  field('implant_reason',st.text_area,'Reason for the treatment plan and design',default='',placeholder='Clinical rationale, limitations and why this option is appropriate…')
  st.download_button('⬇ Export current treatment comparison (HTML)',data=tp_export_html(result_),file_name='implant_treatment_comparison.html',mime='text/html',help='Creates a local summary. The report may contain patient information; store securely.')
  with st.expander('Methodology, dimension-screening rules & safety limits',expanded=False):
   st.markdown('**Working catalog:** BLC, BLX, BLT, TLC and TLX; each diameter is paired only with the lengths in the clinician-edited project matrix. Stock and IFU/SKU eligibility have not been independently verified.')
   st.markdown('**Minimum dimensional screening:** 1.5 mm facial, 1.0 mm palatal/lingual, 1.5 mm mesial and distal to natural roots. Thus width ≥ implant Ø + 2.5 mm, and mesiodistal space ≥ implant Ø + 3.0 mm. Use Ø3.75 mm as the posterior screening floor (Ø4.0 mm often preferred for molars), Ø3.3 mm anteriorly, with Ø2.9 mm allowed only for selected upper laterals and lower incisors. An esthetic facial target around 2 mm remains preferable. Confirm exact CBCT geometry, shoulder/platform dimensions and IFU.')
   st.markdown('**Initial length ceiling:** residual bone height − 2.0 mm, inherited from the original app as a provisional conservative screen. It is NOT a universal fixed anatomical safety margin and cannot replace site-specific 3D planning, drill-tip clearance or the actual manufacturer-approved protocol.')
   st.markdown('**Restorative space thresholds:** 7 mm SRA and 6 mm Ti-base are working CDSS screening alerts, not universal product requirements; ~7.5 mm is reported for abutment-level fixed screw-retained prostheses in the 2019 restorative-space review. Measure crown-height space separately; >15 mm is a biomechanical review trigger based on Misch et al. Use actual component/IFU measurements.')
   st.markdown('**3D root pathway:** for dilacerated roots, minimum interradicular space is measured along the proposed path, not only at crestal level. Manufacturer-approved angled abutments can address some restorative-axis differences but NEVER surgical root collisions.')
   st.markdown('**Short vs sinus:** shown only as a comparison concept for a posterior maxillary molar with reduced native bone height. A short implant is not considered feasible if no listed length passes the conservative initial screen; sinus pathology demands separate review.')
   for n_ in SAFETY_NOTES:st.markdown('- '+n_)
  references(4)

elif step==5:
 st.markdown('### Surgical Planning · selected treatment pathway')
 patient_context()
 if r('case_type')=='CASE-TYPE-SINGLE' and r('teeth') and r('site') is not None:
  result_=tp_build_plans()
  selected_=r('treatment_path')
  if selected_ in ('A','B'):
   p_=result_['plans'][0 if selected_=='A' else 1]
   st.markdown('#### Working plan · Option '+selected_+' — '+p_['title'])
   st.info(p_['surgery'])
   st.caption('Loading concept: '+p_['loading'])
   if tp_root_screen()['active']:st.warning('Root dilaceration review: surgical axis and root clearance must be confirmed before clinical approval.')
   if tp_restorative_space_screen()['warnings']:st.warning('Restorative space alerts from Step 03 remain active; finalize component selection before definitive surgical planning.')
   st.caption('Current status: '+p_['status']+'. This is a working pathway and not a clinical clearance.')
   if p_['post']:st.warning('Re-assess after augmentation/healing before specifying final implant dimensions.')
  else:
   st.warning('No treatment pathway has been selected yet. Compare Options A and B in Step 05 before finalizing the surgical sequence.')
  with st.container(border=True):
   st.markdown('#### Record the clinician-approved surgical sequence')
   rr_=tp_procedure_recommendations()
   st.caption('Procedure assessment: '+ ' · '.join(k+': '+('evaluate' if rr_[k]['status']=='suggested' else 'data missing' if rr_[k]['status']=='pending' else 'not triggered') for k in ('CTG','FGG','GBR')))
   choose('surgical_option','Surgical approach',['Undecided','Direct placement / no augmentation','CTG simultaneous to implant placement','GBR simultaneous to implant placement','GBR staged prior to implant','Sinus floor elevation (transcrestal)','Sinus floor elevation (lateral)','Soft-tissue augmentation staged','Combination / individualized protocol'])
   field('surgical_notes',st.text_area,'Procedure rationale, sequence and anatomical safeguards',default='',placeholder='Site-specific plan, contraindications, need for stages, primary stability, closure…')
   field('surgical_reassessment',st.text_area,'Required reassessment before surgery',default='',placeholder='CBCT review, sinus assessment, tissue status, anatomical structures, IFU checks…')
  with st.expander('Surgical alternatives to compare · case-sensitive guidance',expanded=False):
   if result_['mode']=='sinus':
    st.markdown('**Short implant versus sinus elevation:** confirm a commercially valid short length, native bone support, crown/implant relationship and sinus conditions. An option with no valid screened implant length is not cleared.')
   elif result_['mode']=='space':
    st.markdown('**Interradicular space limitation:** neither simultaneous nor staged GBR alone increases the separation between adjacent natural roots. Evaluate position, orthodontic or restorative alternatives and remeasure before proposing a specific implant.')
   elif result_['mode'] in ('gbr','staged_pending'):
    st.markdown('**Simultaneous versus staged GBR:** evaluate restoration-guided 3D positioning, primary stability, defect containment, graft stabilization, closure and the need for horizontal/vertical gain.')
   elif result_['mode']=='soft':
    st.markdown('**Simultaneous versus staged tissue augmentation:** distinguish CTG for soft-tissue thickness from FGG or apically positioned flap for keratinized tissue, and assess the independent goal of STH.')
   else:
    st.markdown('**No additional procedure is automatically proposed.** Revisit clinical findings if the 3D plan cannot satisfy positioning, tissue and stability requirements.')
  references(5)
 else:st.info('Complete the single-tooth site and clinical data before finalizing a surgical plan.')

elif step==6:
 st.markdown('### Restorative Planning · selected pathway')
 patient_context()
 selected_=r('treatment_path')
 if selected_ in ('A','B') and r('case_type')=='CASE-TYPE-SINGLE':
  chosen_=tp_build_plans()['plans'][0 if selected_=='A' else 1]
  st.info('Working Option '+selected_+': '+chosen_['title']+' · '+FAMILIES[chosen_['family']]+'. Final components must be compatible with the selected platform and positioning.')
 else:st.caption('The implant and its working strategy can be carried over from Step 05 after selection.')
 preview_retention_,preview_access_=tp_restoration_text()
 st.caption('Preliminary idea from Step 05: '+preview_retention_+' '+preview_access_)
 for alert_ in tp_restorative_space_screen()['warnings']:st.warning(alert_)
 if tp_root_screen()['active']:
  st.info('Root dilaceration: a manufacturer-approved angled abutment/screw channel may be assessed only after a root-safe 3D implant axis is verified. It cannot compensate for root collision.')
 st.caption('Loading: '+tp_loading_guidance()[0])
 left,right=st.columns(2)
 with left:option('Straight screw access','Retrievability can support maintenance when implant trajectory and emergence allow.','Verify restorative space, axis, tissue profile and correct platform components.')
 with right:option('Angled screw access','A manufacturer-approved angled channel can sometimes preserve screw retention despite off-axis access.','Confirm the exact implant platform, component range and restorative space; it cannot compensate for unsafe implant positioning.')
 choose('retention','Final retention concept',['Undecided','Screw-retained','Screw-cement retained (extraoral cementation)','Cement-retained','Compare both'])
 choose('abutment_choice','Abutment or screw-channel configuration',['Undecided','Straight abutment / screw channel','Angled screw channel (if compatible)','Angled abutment (evaluate separately)','Custom abutment'])
 choose('material','Crown material',['Undecided','Monolithic zirconia','Metal-ceramic','Other'])
 choose('provisional','Provisional approach',['Undecided','No provisional','Interim prosthesis','Implant-supported provisional if feasible'])
 if r('esthetic')=='No' and r('provisional')=='Implant-supported provisional if feasible':
  st.warning('Without a specific esthetic indication, an immediate implant-supported provisional is a secondary option. Document the benefit, occlusal design and validated primary-stability criteria.')
 field('restorative_rationale',st.text_area,'Restorative rationale and limitations',default='',placeholder='Screw access, emergence, retrievability, cement risks, restorative space, cleansability…')
 if r('pro_para') in ('PRO-PARA-SELF','PRO-PARA-SUSPECTED','PRO-PARA-BOTH'):notice('Reassess occlusal loading and protective strategies.')
 references(6)

elif step==7:
 st.markdown('### Maintenance Program · proposed considerations')
 patient_context()
 st.markdown('**Maintenance recommendations must be individualized after baseline assessment.**')
 st.info('Preoperative recall suggestion: '+tp_maintenance_guidance())
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
 st.write('**Teeth (FDI):**',(', '.join(r('teeth',[])) or 'Not selected') if r('case_type')!='CASE-TYPE-EDENT' else r('arch','Unknown'))
 st.write('**Esthetic concern:**',r('esthetic','Not entered'))
 st.write('**Current site:**',SITE.get(r('site'),'Not entered'))
 st.write('**Working treatment strategy:**',r('treatment_path') or 'No plan selected')
 st.write('**Implant / surgical / restorative:**',FAMILIES.get(r('implant_family'),'Undecided'),'·',r('surgical_option','Undecided'),'·',r('retention','Undecided'))
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
