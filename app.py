import streamlit as st

st.set_page_config(page_title='Implant Planning | CDSS Pilot', page_icon='🦷', layout='wide')
st.title('Single-Implant Treatment Planning')
st.caption('Research prototype | Illustrative case only — not validated for clinical decision-making')

if 'step' not in st.session_state:
    st.session_state.step = 1

steps = ['Patient & site', 'Bone assessment', 'Alternatives', 'Prosthetic planning', 'Shared decision']
st.progress(st.session_state.step / len(steps), text=f'Step {st.session_state.step} of {len(steps)} · {steps[st.session_state.step-1]}')

with st.sidebar:
    st.header('Example case')
    st.write('Single-tooth posterior maxilla, fictional adult patient.')
    st.warning('No actual patient identifiers or images. Rules are illustrative, not clinical thresholds.')
    st.markdown('**Navigation**')
    for i, step in enumerate(steps, 1):
        if st.button(f'{i}. {step}', key=f'nav_{i}', use_container_width=True):
            st.session_state.step = i
            st.rerun()

if st.session_state.step == 1:
    st.subheader('1 · Patient and site assessment')
    st.selectbox('Site', ['Posterior maxilla — single molar', 'Other (outside pilot scope)'], key='site')
    st.selectbox('Periodontal history', ['Not yet documented', 'No reported history', 'History of periodontitis'], key='perio')
    st.selectbox('Patient treatment priority', ['Avoid additional surgery', 'Shorter treatment time', 'Long-term predictability', 'Minimize cost', 'No preference yet'], key='priority')
    st.selectbox('Operator experience with sinus augmentation', ['Limited', 'Intermediate', 'Experienced'], key='experience')
    st.info('Pilot scope: one single posterior maxillary restoration. A clinical system would additionally require medical risk assessment, CBCT review and examination.')
elif st.session_state.step == 2:
    st.subheader('2 · Bone and anatomy assessment')
    st.number_input('Available ridge width (mm)', 2.0, 15.0, 7.0, 0.5, key='width')
    st.number_input('Residual vertical bone height below sinus (mm)', 1.0, 20.0, 7.0, 0.5, key='height')
    st.selectbox('CBCT and sinus anatomy reviewed by clinician?', ['No', 'Yes'], key='cbct')
    st.selectbox('Restoratively guided 3D implant position feasible?', ['Unknown', 'Yes', 'No'], key='position')
    st.caption('Numbers do not trigger a clinical recommendation. Applicability depends on implant diameter, safety margins, anatomy, and the complete prosthetic plan.')
elif st.session_state.step == 3:
    st.subheader('3 · Generate alternatives')
    st.write('This pilot keeps both strategies under consideration until case-specific feasibility is reviewed.')
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('### Option A · 6-mm implant')
        st.write('Potentially avoids sinus augmentation if anatomically and prosthetically feasible.')
        st.write('Review residual height, implant positioning, biomechanics and evidence for a matching clinical population.')
    with c2:
        st.markdown('### Option B · Longer implant + sinus augmentation')
        st.write('May permit a longer implant if augmentation is anatomically appropriate.')
        st.write('Adds procedure-related morbidity, cost and possibly treatment time; review surgical feasibility and patient preference.')
    if st.session_state.get('cbct', 'No') != 'Yes':
        st.warning('Missing evidence: CBCT/sinus anatomy has not been reviewed. Feasibility cannot be established.')
    if st.session_state.get('position', 'Unknown') != 'Yes':
        st.warning('Restoratively guided implant position is unconfirmed or infeasible. Reassess the surgical plan before comparing outcomes.')
elif st.session_state.step == 4:
    st.subheader('4 · Restorative considerations')
    st.number_input('Available restorative vertical space (mm)', 2.0, 25.0, 10.0, 0.5, key='rest_space')
    st.number_input('Estimated clinical crown height (mm)', 2.0, 25.0, 10.0, 0.5, key='crown')
    st.selectbox('Planned restoration', ['Screw-retained single crown', 'Cement-retained single crown', 'Undecided'], key='retention')
    st.selectbox('Soft tissue height assessed?', ['No', 'Yes'], key='soft_tissue')
    crown = st.session_state.get('crown', 10.0)
    st.metric('Illustrative crown/implant length ratio · 6-mm option', f'{crown/6:.2f}')
    st.caption('Simple arithmetic only, not a validated crown-to-implant biomechanical or risk prediction metric. Actual definitions and clinical measurements may differ.')
else:
    st.subheader('5 · Patient-centered comparison')
    st.write('**Possible trade-offs to discuss**')
    rows = [
        {'Consideration':'Additional sinus procedure','6-mm option':'May avoid','Longer + sinus option':'Required by scenario'},
        {'Consideration':'Surgical burden','6-mm option':'Potentially less','Longer + sinus option':'Potentially greater'},
        {'Consideration':'Time and cost','6-mm option':'May be lower','Longer + sinus option':'May be higher'},
        {'Consideration':'Implant survival / complications','6-mm option':'Evidence review needed','Longer + sinus option':'Evidence review needed'},
        {'Consideration':'Restorative / biomechanical evaluation','6-mm option':'Required','Longer + sinus option':'Required'},
        {'Consideration':'Patient preference','6-mm option':'Discuss','Longer + sinus option':'Discuss'},
    ]
    st.dataframe(rows, hide_index=True, use_container_width=True)
    st.warning('No validated risk estimates are provided. Neither alternative is selected automatically.')
    missing = []
    if st.session_state.get('cbct') != 'Yes': missing.append('CBCT/sinus review')
    if st.session_state.get('position') != 'Yes': missing.append('restoratively guided 3D position')
    if st.session_state.get('soft_tissue') != 'Yes': missing.append('soft tissue assessment')
    if st.session_state.get('perio') == 'Not yet documented': missing.append('periodontal history')
    st.markdown('**Data gaps:** ' + (', '.join(missing) if missing else 'Key illustrative inputs completed; comprehensive clinical review still necessary.'))
    st.info('Research question: Can an explainable decision-support interface improve the completeness and transparency of treatment-option discussions?')

cprev, cnext = st.columns(2)
with cprev:
    if st.button('← Previous', disabled=st.session_state.step == 1, use_container_width=True):
        st.session_state.step -= 1
        st.rerun()
with cnext:
    if st.button('Next →', disabled=st.session_state.step == len(steps), use_container_width=True):
        st.session_state.step += 1
        st.rerun()
