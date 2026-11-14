AETHERRA / FIELD SHIFT — UI UPGRADE

1. Keep your EXISTING AETHERRA project folder, including data/, models/ and app/recommendations.py.
2. Make a backup copy of your current app/streamlit_app.py.
3. From this ZIP, copy app/streamlit_app.py and app/styles.css into your project's app/ folder.
4. Copy the 5 JPG files from app/assets/ into your project's app/assets/ folder.
5. From the AETHERRA project ROOT in VS Code terminal run:
   python -m pip install streamlit plotly pandas scikit-learn
   python -m streamlit run app/streamlit_app.py

The upgrade expects:
 data/processed/merged_dataset.csv
 data/processed/model_predictions.csv
 app/recommendations.py  (your existing file)

It does NOT replace your original NASA data, model, or recommendation rules.
The art images are illustrative, not real NASA measurements.
