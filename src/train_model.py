
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Read the merged dataset
path = Path("data/processed/merged_dataset.csv")
df = pd.read_csv(path, parse_dates=["date"])

df = df.sort_values(["district", "date"]).copy()

print("Original rows:", len(df))

# 2. Create previous-observation features
# Never use weather measured during the target
# period to predict that same period.

features_to_lag = [
    "ndvi",
    "temperature",
    "max_temperature",
    "rainfall",
    "humidity",
    "solar_radiation"
]

for col in features_to_lag:
    df["previous_" + col] = (
        df.groupby("district")[col].shift(1)
    )

df["previous_date"] = (
    df.groupby("district")["date"].shift(1)
)

df["gap_days"] = (
    df["date"] - df["previous_date"]
).dt.days

# Keep observations close to the next MODIS cycle
df = df[df["gap_days"].between(15, 32)].copy()

# Seasonal information known in advance
day_of_year = df["date"].dt.day_of_year
df["season_sin"] = np.sin(2 * np.pi * day_of_year / 365.25)
df["season_cos"] = np.cos(2 * np.pi * day_of_year / 365.25)

feature_cols = [
    "previous_ndvi",
    "previous_temperature",
    "previous_max_temperature",
    "previous_rainfall",
    "previous_humidity",
    "previous_solar_radiation",
    "season_sin",
    "season_cos"
]

df = df.dropna(subset=feature_cols + ["ndvi"])

# Add district information
district_columns = sorted(df["district"].unique())

for district in district_columns:
    col = "district_" + district
    df[col] = (df["district"] == district).astype(int)
    feature_cols.append(col)

print("Usable rows:", len(df))

if len(df) < 30:
    raise ValueError(
        "Too few training rows. "
        "Review the quality filters and date gaps."
    )

# 3. Chronological train/test split
# Prefer testing on the most recent three years
train = df[df["date"] < "2023-01-01"].copy()
test = df[df["date"] >= "2023-01-01"].copy()

if len(train) < 20 or len(test) < 10:
    # Fallback: last 20% of dates for testing
    dates = sorted(df["date"].unique())
    cutoff = dates[max(1, int(len(dates) * 0.8))]

    train = df[df["date"] < cutoff].copy()
    test = df[df["date"] >= cutoff].copy()

if len(train) < 20 or len(test) < 10:
    raise ValueError("Insufficient data for evaluation.")

X_train = train[feature_cols]
y_train = train["ndvi"]

X_test = test[feature_cols]
y_test = test["ndvi"]

print("Training rows:", len(train))
print("Testing rows:", len(test))

# 4. Train Random Forest
model = RandomForestRegressor(
    n_estimators=150,
    max_depth=8,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# 5. Evaluate against unseen dates
predictions = model.predict(X_test)
predictions = np.clip(predictions, -1, 1)

model_mae = mean_absolute_error(
    y_test, predictions
)

# Simple persistence baseline:
# predict that NDVI stays unchanged
baseline_mae = mean_absolute_error(
    y_test, test["previous_ndvi"]
)

print("\nMODEL RESULTS")
print("Random Forest MAE:", round(model_mae, 4))
print("Baseline MAE:", round(baseline_mae, 4))
print("R2 score:", round(r2_score(y_test, predictions), 4))

if model_mae < baseline_mae:
    print("Model beats the persistence baseline.")
else:
    print("Model does not beat the baseline yet.")

# 6. Save model and its feature order
Path("models").mkdir(exist_ok=True)

joblib.dump(
    {"model": model, "features": feature_cols},
    "models/ndvi_model.joblib"
)

# 7. Save predictions for dashboard
results = test[[
    "date", "district", "ndvi", "previous_ndvi"
]].copy()

results["predicted_ndvi"] = predictions

results = results.rename(columns={
    "ndvi": "actual_ndvi",
    "previous_ndvi": "baseline_ndvi"
})

results.to_csv(
    "data/processed/model_predictions.csv",
    index=False
)

print("\nModel saved: models/ndvi_model.joblib")
print("Predictions saved: data/processed/model_predictions.csv")
