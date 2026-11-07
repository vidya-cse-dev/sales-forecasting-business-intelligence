import pandas as pd

# Load combined dataset
df = pd.read_csv("data/combined_retail.csv")

print("Original dataset:", df.shape)

# 1. Remove duplicate records
df = df.drop_duplicates()
print("After removing duplicates:", df.shape)

# 2. Remove cancelled invoices
df["Invoice"] = df["Invoice"].astype(str)

df = df[~df["Invoice"].str.startswith("C")]
print("After removing cancellations:", df.shape)

# 3. Remove negative or zero quantities
df = df[df["Quantity"] > 0]
print("After removing invalid quantities:", df.shape)

# 4. Remove zero or negative prices
df = df[df["Price"] > 0]
print("After removing invalid prices:", df.shape)

# 5. Convert invoice date
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# 6. Calculate revenue
df["Revenue"] = df["Quantity"] * df["Price"]

# 7. Extract date
df["Date"] = df["InvoiceDate"].dt.date

# 8. Save cleaned dataset
df.to_csv("data/cleaned_retail.csv", index=False)

print("\nCleaning completed successfully!")
print("Final dataset shape:", df.shape)
print("Total revenue:", round(df["Revenue"].sum(), 2))
print("Missing customer IDs:", df["Customer ID"].isnull().sum())
print("Missing descriptions:", df["Description"].isnull().sum())