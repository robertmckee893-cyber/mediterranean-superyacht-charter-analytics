import sqlite3
import pandas as pd

# Connect to our maritime database
connection = sqlite3.connect("superyacht_analytics.db")

# Compare high-season charter prices
query = """
SELECT
    label AS destination,
    ROUND(median, 2) AS median_charter_rate,
    n AS observations
FROM med_charter_prices
WHERE season = 'high'
AND cls = 'all'
ORDER BY median DESC
"""

df = pd.read_sql_query(query, connection)

print("\nMEDITERRANEAN HIGH-SEASON CHARTER PRICES:")
print(df.to_string(index=False))

# Compare high and low season charter rates

season_query = """
SELECT
    label AS destination,
    ROUND(MAX(CASE WHEN season = 'high' THEN median END), 2)
        AS high_season_rate,
    ROUND(MAX(CASE WHEN season = 'low' THEN median END), 2)
        AS low_season_rate
FROM med_charter_prices
WHERE cls = 'all'
GROUP BY label
ORDER BY label
"""

season_df = pd.read_sql_query(season_query, connection)

season_df["seasonal_premium_pct"] = (
    (season_df["high_season_rate"] -
     season_df["low_season_rate"])
    / season_df["low_season_rate"] * 100
).round(2)

print("\nMEDITERRANEAN SEASONAL PRICE COMPARISON:")
print(season_df.to_string(index=False))
connection.close()
# Export SQL analysis results for KNIME

df.to_csv("med_high_season_prices.csv", index=False)

season_df.to_csv(
    "med_seasonal_comparison.csv",
    index=False
)

print("\nSQL analysis exported successfully!")