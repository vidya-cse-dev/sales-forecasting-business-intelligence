import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Load data
df = pd.read_csv(
    "data/forecasting_data.csv",
    parse_dates=["Date"]
)

features = [
    "Day", "Month", "Year", "DayOfWeek",
    "IsWeekend", "Lag_1", "Lag_7",
    "Lag_14", "Lag_28",
    "Rolling_7", "Rolling_14", "Rolling_28"
]

# Same chronological split as training
split_index = int(len(df) * 0.8)

test = df.iloc[split_index:].copy()

X_test = test[features]
actual = test["Daily_Sales"]

# Load trained model
model = joblib.load("models/random_forest_sales.pkl")

# Predict
predicted = model.predict(X_test)

# Compare results
results = pd.DataFrame({
    "Date": test["Date"],
    "Actual_Sales": actual,
    "Predicted_Sales": predicted
})

print("\nActual vs Predicted Sales:")
print(results.head(15))

# Plot comparison
plt.figure(figsize=(14, 6))

plt.plot(
    results["Date"],
    results["Actual_Sales"],
    label="Actual Sales"
)

plt.plot(
    results["Date"],
    results["Predicted_Sales"],
    label="Predicted Sales"
)

plt.title("Actual vs Predicted Daily Sales")
plt.xlabel("Date")
plt.ylabel("Revenue (£)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("charts/actual_vs_predicted.png")
plt.close()

results.to_csv(
    "data/prediction_results.csv",
    index=False
)

print("\nEvaluation chart saved!")
print("Prediction results saved!")