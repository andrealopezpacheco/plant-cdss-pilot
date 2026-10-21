# Implant Planning Decision Explorer · Interactive Odontogram

This release replaces the plain FDI multiselect and text-only tooth chart in **Module 02 — Case Type & Site** with an interactive odontogram.

## What is included

- `app.py` — the updated Streamlit application, with all 8 original modules and sidebar intact.
- `iti_odontogram/index.html` — the custom interactive HTML/JavaScript component (sends its state back to Python via Streamlit Components v1).
- `iti_odontogram/images/*.png` — 32 individual tooth illustrations extracted from the reference image provided in the conversation.

## Add it to your existing application

1. **Back up your existing `app.py`** and existing project files.
2. Upload the new `app.py` to the same location as your current one. If you customized your copy of `app.py` after it was shared here, merge the changes rather than overwrite them.
3. Upload the entire `iti_odontogram` folder **next to** `app.py` (preserve the exact folder name and the `images` subfolder).
4. Keep your existing `requirements.txt`; it must include `streamlit`. No new pip packages are required for the odontogram.
5. If hosted on Streamlit Community Cloud and sourced from GitHub, commit the files in the GitHub repository that hosts the app. The Streamlit app will pick up the new commit/redeploy. If working locally, launch `streamlit run app.py`.
6. Open **02 — Case Type & Site** and click the teeth. The selected FDI codes should update the case snapshot and the exported JSON.

## Selection behavior

- **Single Tooth:** one tooth at a time.
- **Short Span:** up to three teeth.
- **Extended Span:** multiple teeth; an advisory is shown until at least four are selected.
- **Edentulous:** shows Maxilla or Mandible instead of individual teeth.
- Dental chart: clinically oriented from patient's right to patient's left; **FDI** is displayed first and **Universal** (`#`) second.
- **FDI values are stored internally** as `record['teeth']` and exported in the JSON.

## Notes

- This is an *independent research prototype*, not an officially branded or endorsed ITI product. Its palette is merely inspired by ITI. No third-party logo was embedded.
- The provided component is purposefully self-contained (no CDN, no JavaScript build pipeline) and supports keyboard focus and horizontal scrolling on narrow screens.
- Do not upload identifiable patient images or data to a public demonstration instance.
