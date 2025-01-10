import sqlite3
import pandas as pd

# Queries
ubereats_hummus_query = """
SELECT r.title AS Restaurant, r.rating__rating_value AS Rating, r.rating__review_count AS RatingCount, m.name AS Dish
FROM restaurants r
JOIN menu_items m ON r.id = m.restaurant_id
WHERE LOWER(m.name) = 'hummus' AND r.rating__review_count >= 100
ORDER BY r.rating__rating_value DESC
LIMIT 4;
"""

deliveroo_hummus_query = """
SELECT r.name AS Restaurant, r.rating AS Rating, r.rating_number AS RatingCount, m.name AS Dish
FROM restaurants r
JOIN menu_items m ON r.id = m.restaurant_id
WHERE LOWER(m.name) = 'hummus' AND r.rating_number >= 100
ORDER BY r.rating DESC
LIMIT 4;
"""

takeaway_hummus_query = """
SELECT r.name AS Restaurant, r.ratings AS Rating, r.ratingsNumber AS RatingCount, m.name AS Dish
FROM restaurants r
JOIN menuItems m ON r.primarySlug = m.primarySlug
WHERE LOWER(m.name) = 'hummus' AND r.ratingsNumber >= 100
ORDER BY r.ratings DESC
LIMIT 4;
"""

# Database paths
ubereats_db = "C:/Users/hp/Imad/Food_Delivery/ubereats.db"
deliveroo_db = "C:/Users/hp/Imad/Food_Delivery/deliveroo.db"
takeaway_db = "C:/Users/hp/Imad/Food_Delivery/takeaway.db"

# Function to execute queries
def get_restaurant_data(database_path, query):
    conn = sqlite3.connect(database_path)
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

# Function to clean and convert RatingCount to integers
def clean_rating_count(rating_count):
    if isinstance(rating_count, str) and '+' in rating_count:
        return int(rating_count.replace('+', ''))  # Convert "500+" to 500
    return int(rating_count)

# Apply function on databases
ubereats_hummus_restaurants = get_restaurant_data(ubereats_db, ubereats_hummus_query)
deliveroo_hummus_restaurants = get_restaurant_data(deliveroo_db, deliveroo_hummus_query)
takeaway_hummus_restaurants = get_restaurant_data(takeaway_db, takeaway_hummus_query)

# Combine results and remove duplicates
all_hummus_restaurants_combined = pd.concat(
    [ubereats_hummus_restaurants, deliveroo_hummus_restaurants, takeaway_hummus_restaurants]
)
all_hummus_restaurants_combined.drop_duplicates(subset=["Restaurant"], keep="first", inplace=True)

# Clean RatingCount column
all_hummus_restaurants_combined["RatingCount"] = all_hummus_restaurants_combined["RatingCount"].apply(clean_rating_count)

# Filter for restaurants with RatingCount >= 100
filtered_hummus_restaurants = all_hummus_restaurants_combined[
    all_hummus_restaurants_combined["RatingCount"] >= 100
]

# Sort by rating to rank the restaurants
ranked_hummus_restaurants = filtered_hummus_restaurants.sort_values(by="Rating", ascending=False)

# Display the ranked restaurants using print
print("\nRanked Hummus-Serving Restaurants Across Platforms:")
print(ranked_hummus_restaurants)