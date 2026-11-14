from pathlib import Path
import pandas as pd

folder = Path("data/raw/modis")
files = list(folder.rglob("*.csv"))

if not files:
    print("No CSV files found.")
    print("Check whether you extracted the ZIP file.")
else:
    for file in files:
        print(f"\nFILE: {file.name}")

        try:
            df = pd.read_csv(file)

            print("Rows:", len(df))
            print("Columns:", df.columns.tolist())
            print("\nFirst five rows:")
            print(df.head())

        except Exception as e:
            print("Error:", e)