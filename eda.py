import pandas as pd
import matplotlib.pyplot as plt
import os

# Create charts folder
os.makedirs("charts", exist_ok=True)

# Load datasets
df = pd.read_csv(
    "data/cleaned_retail.csv",
    dtype={"Invoice": "string"},
    low_memory=False
)
daily = pd.read_csv("data/daily_sales.csv")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
daily["Date"] = pd.to_datetime(daily["Date"])

# 1. Daily sales trend
plt.figure(figsize=(14, 5))
plt.plot(daily["Date"], daily["Daily_Sales"])
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Revenue (£)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("charts/daily_sales_trend.png")
plt.close()

# 2. Monthly revenue
df["Month"] = df["InvoiceDate"].dt.to_period("M")

monthly = df.groupby("Month")["Revenue"].sum()

plt.figure(figsize=(14, 5))
monthly.plot(kind="bar")
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("charts/monthly_revenue.png")
plt.close()

# 3. Top 10 products by revenue
products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))
products.sort_values().plot(kind="barh")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (£)")
plt.tight_layout()
plt.savefig("charts/top_products.png")
plt.close()

# 4. Top 10 countries by revenue
countries = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))
countries.sort_values().plot(kind="barh")
plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue (£)")
plt.tight_layout()
plt.savefig("charts/top_countries.png")
plt.close()

print("\nEDA completed successfully!")

print("\nTop 5 months:")
print(monthly.sort_values(ascending=False).head())

print("\nTop 5 products:")
print(products.head())

print("\nTop 5 countries:")
print(countries.head())

print("\nCharts saved inside charts folder.")