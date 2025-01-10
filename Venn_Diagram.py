import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

# Database paths
ubereats_db_path = "C:/Users/hp/Imad/Food_Delivery/ubereats.db"
deliveroo_db_path = "C:/Users/hp/Imad/Food_Delivery/deliveroo.db"
takeaway_db_path = "C:/Users/hp/Imad/Food_Delivery/takeaway.db"



# Function to run a query
def get_restaurant_names(database_path, query):
    conn = sqlite3.connect(database_path)
    result = pd.read_sql_query(query, conn)
    conn.close()
    return set(result['name'])

#Queries
ubereats_restaurant_names_query = "SELECT title AS name FROM restaurants;"
deliveroo_restaurant_names_query = "SELECT name FROM restaurants;"
takeaway_restaurant_names_query = "SELECT name FROM restaurants;"

# Fetch results from each database
ubereats_restaurants = get_restaurant_names(ubereats_db_path, ubereats_restaurant_names_query)
deliveroo_restaurants = get_restaurant_names(deliveroo_db_path, deliveroo_restaurant_names_query)
takeaway_restaurants = get_restaurant_names(takeaway_db_path, takeaway_restaurant_names_query)

# Create the Venn diagram
plt.figure(figsize=(10, 8))
venn = venn3(
    [ubereats_restaurants, deliveroo_restaurants, takeaway_restaurants],
    ('Uber Eats', 'Deliveroo', 'Takeaway')
)
plt.title("Restaurant Distribution Across Platforms")
plt.show()
{
    "Uber Eats Only": len(ubereats_restaurants - deliveroo_restaurants - takeaway_restaurants),
    "Deliveroo Only": len(deliveroo_restaurants - ubereats_restaurants - takeaway_restaurants),
    "Takeaway Only": len(takeaway_restaurants - ubereats_restaurants - deliveroo_restaurants),
    "Uber Eats & Deliveroo": len(ubereats_restaurants & deliveroo_restaurants - takeaway_restaurants),
    "Uber Eats & Takeaway": len(ubereats_restaurants & takeaway_restaurants - deliveroo_restaurants),
    "Deliveroo & Takeaway": len(deliveroo_restaurants & takeaway_restaurants - ubereats_restaurants),
    "All Three": len(ubereats_restaurants & deliveroo_restaurants & takeaway_restaurants)
}
