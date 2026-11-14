from pathlib import Path
import pandas as pd

files = list(Path("data/raw/modis").rglob("*.csv"))

if not files:
    raise FileNotFoundError("No MODIS CSV files found.")

for file in files:
    df = pd.read_csv(file)

    print("\nFile:", file.name)
    print("\nColumns:")
    for col in df.columns:
        print(col)

    print("\nSample data:")
    print(df.head(3).to_string(index=False))