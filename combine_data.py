import pandas as pd

file_path = "data/online_retail_II.xlsx"

# Read both sheets
sheets = pd.read_excel(file_path, sheet_name=None)

# Combine all sheets
df = pd.concat(sheets.values(), ignore_index=True)

print("Dataset combined successfully!")

print("\nDataset shape:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nDate range:")
print(df["InvoiceDate"].min(), "to", df["InvoiceDate"].max())

print("\nTotal duplicate rows:")
print(df.duplicated().sum())

print("\nCancelled invoices:")
print(df["Invoice"].astype(str).str.startswith("C").sum())

print("\nNegative quantities:")
print((df["Quantity"] < 0).sum())

print("\nZero or negative prices:")
print((df["Price"] <= 0).sum())

# Save combined dataset
df.to_csv("data/combined_retail.csv", index=False)

print("\nCombined dataset saved successfully!")