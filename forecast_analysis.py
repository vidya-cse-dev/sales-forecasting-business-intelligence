import pandas as pd

# Load historical and forecast data
daily = pd.read_csv(
    "data/daily_sales.csv",
    parse_dates=["Date"]
)

forecast = pd.read_csv(
    "data/30_day_forecast.csv",
    parse_dates=["Date"]
)

# Exclude incomplete final historical day
daily = daily[daily["Date"] < daily["Date"].max()].copy()

# Add weekday names
daily["Weekday"] = daily["Date"].dt.day_name()
forecast["Weekday"] = forecast["Date"].dt.day_name()

# Historical weekday analysis
print("\nHISTORICAL SALES BY WEEKDAY")

weekday_analysis = daily.groupby("Weekday").agg(
    Average_Sales=("Daily_Sales", "mean"),
    Zero_Sales_Days=("Daily_Sales", lambda x: (x == 0).sum()),
    Total_Days=("Daily_Sales", "count")
)

print(weekday_analysis)

# Forecast weekday analysis
print("\nFORECAST BY WEEKDAY")

print(
    forecast.groupby("Weekday")["Predicted_Sales"]
    .agg(["mean", "min", "max"])
)

# Identify unusually low predictions
print("\nUNUSUALLY LOW FORECASTS")

print(
    forecast[
        forecast["Predicted_Sales"] < 1000
    ]
)