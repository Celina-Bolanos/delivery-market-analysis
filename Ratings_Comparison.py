import sqlite3
import pandas as pd
import matplotlib.pyplot as plt  # Correct import

# Queries
ubereats_query = "SELECT LOWER(TRIM(title)) AS name, rating__rating_value AS rating FROM restaurants;"
deliveroo_query = "SELECT LOWER(TRIM(name)) AS name, rating AS rating FROM restaurants;"
takeaway_query = "SELECT LOWER(TRIM(name)) AS name, ratings AS rating FROM restaurants;"

def get_restaurant_ratings(database_path, query):
    conn = sqlite3.connect(database_path)
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

# Paths
ubereats_db_path = "C:/Users/hp/Imad/Food_Delivery/ubereats.db"
deliveroo_db_path = "C:/Users/hp/Imad/Food_Delivery/deliveroo.db"
takeaway_db_path = "C:/Users/hp/Imad/Food_Delivery/takeaway.db"

# Fetch restaurant names and ratings
ubereats_data = get_restaurant_ratings(ubereats_db_path, ubereats_query)
deliveroo_data = get_restaurant_ratings(deliveroo_db_path, deliveroo_query)
takeaway_data = get_restaurant_ratings(takeaway_db_path, takeaway_query)

# Merge data
merged_data = pd.merge(ubereats_data, deliveroo_data, on="name", how="inner", suffixes=('_ubereats', '_deliveroo'))
merged_data = pd.merge(merged_data, takeaway_data, on="name", how="inner")
merged_data.rename(columns={"rating": "rating_takeaway"}, inplace=True)

# Filter out restaurants with 0 or empty ratings
filtered_data = merged_data[
    (merged_data['rating_ubereats'] > 0) &
    (merged_data['rating_deliveroo'] > 0) &
    (merged_data['rating_takeaway'] > 0)
]

# Calculate differences in ratings
filtered_data['diff_ubereats_deliveroo'] = abs(filtered_data['rating_ubereats'] - filtered_data['rating_deliveroo'])
filtered_data['diff_ubereats_takeaway'] = abs(filtered_data['rating_ubereats'] - filtered_data['rating_takeaway'])
filtered_data['diff_deliveroo_takeaway'] = abs(filtered_data['rating_deliveroo'] - filtered_data['rating_takeaway'])

# Calculate average differences
filtered_rating_differences_summary = filtered_data[
    ['diff_ubereats_deliveroo', 'diff_ubereats_takeaway', 'diff_deliveroo_takeaway']
].mean()

# Prepare data for the bar chart
average_differences = filtered_rating_differences_summary.reset_index()
average_differences.columns = ['Comparison', 'Average Difference']

# Simple bar chart for average differences
plt.figure(figsize=(8, 5))
plt.barh(average_differences['Comparison'], average_differences['Average Difference'])
plt.title('Average Rating Differences Across Platforms')
plt.xlabel('Average Rating Difference')
plt.ylabel('Platform Comparison')
plt.tight_layout()
plt.show()


