import pandas as pd

# Load the charter pricing dataset
df = pd.read_csv("price-index-2026-10.csv")

# Inspect the dataset
print("DATASET SHAPE:")
print(df.shape)

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nFIRST 5 ROWS:")
print(df.head().to_string(index=False))

print("\nMISSING VALUES:")
print(df.isnull().sum())
# Identify available charter destinations
print("\nAVAILABLE DESTINATIONS:")

print(sorted(df["label"].dropna().unique()))
# Filter Mediterranean charter destinations

med_countries = [
    "France",
    "Italy",
    "Spain",
    "Greece",
    "Croatia",
    "Monaco",
    "Montenegro",
    "Cyprus",
    "Turkey"
]

med_df = df[df["label"].isin(med_countries)].copy()

print("\nMEDITERRANEAN DATASET:")
print(med_df.shape)

print("\nMEDITERRANEAN CHARTER PRICES:")
print(
    med_df[
        ["label", "cls", "season", "n", "median"]
    ].to_string(index=False)
)
import sqlite3

# Connect to our existing maritime database
connection = sqlite3.connect("superyacht_analytics.db")

# Store Mediterranean charter data in a new SQL table
med_df.to_sql(
    "med_charter_prices",
    connection,
    if_exists="replace",
    index=False
)

print("\nMediterranean charter data imported into SQLite!")

# Check how many records were imported
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM med_charter_prices")

print("Records imported:", cursor.fetchone()[0])

connection.close()