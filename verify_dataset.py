import pandas as pd
import os

file_path = "data/online_retail_II.xlsx"

# Check whether the file exists
if not os.path.exists(file_path):
    print("Dataset file not found!")
else:
    print("Dataset found successfully!")

    # Read Excel sheets
    excel = pd.ExcelFile(file_path)

    print("\nAvailable sheets:", excel.sheet_names)

    for sheet in excel.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)

        print("\nSheet:", sheet)
        print("Shape:", df.shape)
        print("Columns:", df.columns.tolist())

        print("\nFirst 5 records:")
        print(df.head())

        print("\nMissing values:")
        print(df.isnull().sum())