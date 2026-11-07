import pandas as pd

# Load cleaned dataset
df = pd.read_csv(
    "data/cleaned_retail.csv",
    parse_dates=["InvoiceDate"]
)

print("Loaded cleaned dataset:", df.shape)

# Set invoice date as index
df.set_index("InvoiceDate", inplace=True)

# Aggregate transaction data by day
daily_sales = df.resample("D").agg(
    Daily_Sales=("Revenue", "sum"),
    Orders=("Invoice", "nunique"),
    Units_Sold=("Quantity", "sum")
)

# Fill dates without recorded transactions with zero
daily_sales = daily_sales.fillna(0)

# Reset index
daily_sales.reset_index(inplace=True)

# Rename date column
daily_sales.rename(
    columns={"InvoiceDate": "Date"},
    inplace=True
)

# Save daily sales dataset
daily_sales.to_csv(
    "data/daily_sales.csv",
    index=False
)

# Display results
print("\nDaily sales dataset created!")
print("Dataset shape:", daily_sales.shape)

print("\nFirst 10 records:")
print(daily_sales.head(10))

print("\nLast 10 records:")
print(daily_sales.tail(10))

print("\nTotal daily revenue:",
      round(daily_sales["Daily_Sales"].sum(), 2))

print("\nTotal orders:",
      daily_sales["Orders"].sum())

print("\nTotal units sold:",
      daily_sales["Units_Sold"].sum())

print("\nDays with zero recorded sales:",
      (daily_sales["Daily_Sales"] == 0).sum())