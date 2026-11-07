
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os

from sklearn.ensemble import RandomForestRegressor

# ==========================================
# 1. LOAD HISTORICAL DATA
# ==========================================

df = pd.read_csv(
    "data/forecasting_data.csv",
    parse_dates=["Date"]
)

daily = pd.read_csv(
    "data/daily_sales.csv",
    parse_dates=["Date"]
)

# Model features
features = [
    "Day", "Month", "Year", "DayOfWeek",
    "IsWeekend", "Lag_1", "Lag_7",
    "Lag_14", "Lag_28",
    "Rolling_7", "Rolling_14", "Rolling_28"
]

# ==========================================
# 2. TRAIN RANDOM FOREST MODEL
# ==========================================

X = df[features]
y = df["Daily_Sales"]

model = RandomForestRegressor(
    n_estimators=300,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

os.makedirs("models", exist_ok=True)
os.makedirs("charts", exist_ok=True)

joblib.dump(
    model,
    "models/random_forest_sales.pkl"
)

print("Model retrained using all historical data!")

# ==========================================
# 3. PREPARE HISTORICAL SALES
# ==========================================

# Exclude incomplete final trading day
incomplete_date = daily["Date"].max()

history = daily.loc[
    daily["Date"] < incomplete_date,
    "Daily_Sales"
].astype(float).tolist()

# Use the actual dataset's final date as the
# forecast anchor, so predictions start on Dec 10.
last_date = incomplete_date

# ==========================================
# 4. GENERATE NEXT 30 DAYS FORECAST
# ==========================================

forecast_results = []

for i in range(30):

    forecast_date = last_date + pd.Timedelta(days=i + 1)

    values = np.array(history)

    row = pd.DataFrame([{
        "Day": forecast_date.day,
        "Month": forecast_date.month,
        "Year": forecast_date.year,
        "DayOfWeek": forecast_date.dayofweek,
        "IsWeekend": int(forecast_date.dayofweek >= 5),
        "Lag_1": values[-1],
        "Lag_7": values[-7],
        "Lag_14": values[-14],
        "Lag_28": values[-28],
        "Rolling_7": values[-7:].mean(),
        "Rolling_14": values[-14:].mean(),
        "Rolling_28": values[-28:].mean()
    }])

    # Predict sales
    prediction = model.predict(row[features])[0]

    # Historical business closure rule:
    # Saturday has almost always had zero sales.
    if forecast_date.dayofweek == 5:
        prediction = 0

    # Revenue cannot be negative
    prediction = max(0, prediction)

    # Store prediction
    forecast_results.append({
        "Date": forecast_date,
        "Predicted_Sales": round(prediction, 2)
    })

    # Update history for recursive forecasting
    history.append(prediction)

# ==========================================
# 5. CREATE AND VALIDATE FORECAST DATAFRAME
# ==========================================

forecast_df = pd.DataFrame(forecast_results)

forecast_df = forecast_df.sort_values(
    "Date"
).reset_index(drop=True)

# Validate forecast
assert len(forecast_df) == 30, \
    "Expected exactly 30 forecast records!"

assert forecast_df["Date"].nunique() == 30, \
    "Duplicate forecast dates detected!"

# Save forecast
forecast_df.to_csv(
    "data/30_day_forecast.csv",
    index=False
)

print("\nNumber of forecast records:", len(forecast_df))

print("\n30-Day Sales Forecast:")
print(forecast_df.to_string(index=False))

print("\nTotal predicted revenue:",
      round(forecast_df["Predicted_Sales"].sum(), 2))

print("\nAverage predicted daily revenue:",
      round(forecast_df["Predicted_Sales"].mean(), 2))

print("\nForecast period:",
      forecast_df["Date"].min(),
      "to",
      forecast_df["Date"].max())

# ==========================================
# 6. PLOT FORECAST
# ==========================================

plt.figure(figsize=(14, 6))

plt.plot(
    forecast_df["Date"],
    forecast_df["Predicted_Sales"],
    marker="o",
    linewidth=2,
    label="Predicted Sales"
)

plt.title("Next 30 Days Sales Forecast")
plt.xlabel("Date")
plt.ylabel("Predicted Revenue (£)")

plt.xticks(rotation=45)
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "charts/30_day_forecast.png",
    dpi=300
)

plt.close()

print("\nForecast chart saved successfully!")
print("Forecast CSV saved successfully!")
