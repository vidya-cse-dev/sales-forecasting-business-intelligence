import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import joblib
import os

# Load forecasting dataset
df = pd.read_csv(
    "data/forecasting_data.csv",
    parse_dates=["Date"]
)

df = df.sort_values("Date").reset_index(drop=True)

# Define features
features = [
    "Day",
    "Month",
    "Year",
    "DayOfWeek",
    "IsWeekend",
    "Lag_1",
    "Lag_7",
    "Lag_14",
    "Lag_28",
    "Rolling_7",
    "Rolling_14",
    "Rolling_28"
]

X = df[features]
y = df["Daily_Sales"]

# Chronological 80:20 split
split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# Evaluation function
def evaluate_model(name, actual, predicted):

    mae = mean_absolute_error(actual, predicted)

    rmse = np.sqrt(
        mean_squared_error(actual, predicted)
    )

    r2 = r2_score(actual, predicted)

    print(f"\n{name}")
    print("MAE:", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R2 Score:", round(r2, 4))


# 1. Linear Regression
lr = LinearRegression()

lr.fit(X_train, y_train)

lr_predictions = lr.predict(X_test)

evaluate_model(
    "Linear Regression",
    y_test,
    lr_predictions
)


# 2. Random Forest
rf = RandomForestRegressor(
    n_estimators=300,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

rf_predictions = rf.predict(X_test)

evaluate_model(
    "Random Forest",
    y_test,
    rf_predictions
)


# 3. Seasonal Naive baseline
naive_predictions = X_test["Lag_7"].to_numpy()

evaluate_model(
    "Seasonal Naive (7-day)",
    y_test,
    naive_predictions
)


# Save Random Forest model
os.makedirs("models", exist_ok=True)

joblib.dump(rf, "models/random_forest_sales.pkl")

print("\nRandom Forest model saved successfully!")

# Feature importance
importance = pd.Series(
    rf.feature_importances_,
    index=features
).sort_values(ascending=False)

print("\nTop 5 important features:")
print(importance.head())