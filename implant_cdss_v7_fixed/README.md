# Implant CDSS · Working demo V7

Native Streamlit odontogram; no external frontend folder, no custom component registration.

## Deploy
1. Replace the root `app.py` on GitHub with this file.
2. Make sure `requirements.txt` is at repo root. The `.streamlit/config.toml` theme is optional.
3. Streamlit Community Cloud should point to branch `main` and entrypoint `app.py`.
4. Use **fictional or fully de-identified** patient information; public demo is not a secure clinical record.

## Notes
- The interactive 32-tooth chart uses Universal / FDI numbering.
- Case data persists across Streamlit widget navigation in `st.session_state.record`, not across Cloud sessions.
- Proposals are illustrative; no patient-specific validated risk estimates.
- This fixes the missing `iti_odontogram` directory by removing the dependency.
