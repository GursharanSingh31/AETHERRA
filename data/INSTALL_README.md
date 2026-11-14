# AETHERRA / Field Shift — Full UI Replacement

This bundle contains a replacement **`app/streamlit_app.py`**, complete **`app/styles.css`**, `.streamlit/config.toml` for the dark visual theme, and the five decorative image assets.

## Install in your EXISTING AETHERRA project

1. **Back up** your current `app/streamlit_app.py` and `app/styles.css` files.
2. Extract the ZIP. Copy **`app/streamlit_app.py`** and **`app/styles.css`** into `AETHERRA/app/`, replacing the old copies.
3. Copy all five files from `app/assets/` to your `AETHERRA/app/assets/` folder.
4. Copy the folder `.streamlit/` into the **root** of your AETHERRA project. This sets the dark theme and accent color.
5. **Keep your existing `AETHERRA/app/recommendations.py` unchanged.** Do not replace or delete your `data/` or `models/` folders. This package does not contain those original files.
6. In the VS Code terminal **at the root of AETHERRA**, run:

   ```powershell
   python -m pip install --upgrade streamlit pandas plotly
   python -m streamlit run app/streamlit_app.py
   ```

7. Force-refresh the browser with **Ctrl+Shift+R**. If the previous appearance persists, stop all old Streamlit servers with Ctrl+C and confirm you're viewing the URL printed by the latest terminal run.

## Required data

- `data/processed/merged_dataset.csv` with `date`, `district`, `ndvi`, `temperature`, `rainfall`, `humidity`, `solar_radiation`.

## Optional existing files

- `data/processed/model_predictions.csv` with `date`, `district`, `actual_ndvi`, `predicted_ndvi`, `baseline_ndvi` (for the AI Lab).
- `app/recommendations.py` exporting `get_recommendations(filtered, crop)` (for climate insights).

## Design and scientific notes

- Satellite and farm images are **generated illustration assets**, not raw NASA satellite imagery.
- The crop choice changes illustrative context; it does **not** crop-mask the NASA NDVI points.
- The weather dashboard displays observations in weather windows aligned with good-quality MODIS periods, not complete annual climatologies.
- Historical held-out model estimates are **not** live crop yield or growing-season forecasts.

## Troubleshooting

- **No visual change:** Ensure both replacement files are in `AETHERRA/app/`, and the running command points to that folder. Hard-refresh the browser.
- **No hero background:** Ensure `app/assets/hero_farm.jpg` exists exactly at that path.
- **No ML graph:** Confirm `data/processed/model_predictions.csv` exists and contains test predictions for the selected district and years.
- **No recommendation cards:** Keep your existing `app/recommendations.py` in the app directory.
- **Module error:** Install missing packages into the same Python virtual environment used by Streamlit.
