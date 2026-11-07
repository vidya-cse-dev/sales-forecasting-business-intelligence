import pandas as pd

# Load daily sales
df = pd.read_csv("data/daily_sales.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)

# Exclude the final incomplete trading day
df = df.iloc[:-1].copy()

# Calendar features
df["Day"] = df["Date"].dt.day
df["Month"] = df["Date"].dt.month
df["Year"] = df["Date"].dt.year
df["DayOfWeek"] = df["Date"].dt.dayofweek
df["IsWeekend"] = (df["DayOfWeek"] >= 5).astype(int)

# Historical sales features
df["Lag_1"] = df["Daily_Sales"].shift(1)
df["Lag_7"] = df["Daily_Sales"].shift(7)
df["Lag_14"] = df["Daily_Sales"].shift(14)
df["Lag_28"] = df["Daily_Sales"].shift(28)

# Rolling averages (shift first to avoid data leakage)
df["Rolling_7"] = (
    df["Daily_Sales"].shift(1).rolling(7).mean()
)

df["Rolling_14"] = (
    df["Daily_Sales"].shift(1).rolling(14).mean()
)

df["Rolling_28"] = (
    df["Daily_Sales"].shift(1).rolling(28).mean()
)

# Remove rows without sufficient historical data
df = df.dropna().reset_index(drop=True)

# Save forecasting dataset
df.to_csv("data/forecasting_data.csv", index=False)

print("Forecasting dataset prepared!")
print("Dataset shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst five records:")
print(df.head())

print("\nDate range:")
print(df["Date"].min(), "to", df["Date"].max())

print("\nSaved as data/forecasting_data.csv")