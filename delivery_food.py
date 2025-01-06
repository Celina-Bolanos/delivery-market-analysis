import sqlite3

# Connect and attach databases
con = sqlite3.connect(':memory:')  # In-memory connection
con.execute("ATTACH DATABASE 'deliveroo.db' AS deliveroo")
con.execute("ATTACH DATABASE 'ubereats.db' AS ubereats")
con.execute("ATTACH DATABASE 'takeaway.db' AS takeaway")

# Query across databases
query = """
SELECT name, latitude, longitude, city, region, 'Deliveroo' AS source
FROM deliveroo.restaurants
UNION ALL
SELECT name, latitude, longitude, city, region, 'UberEats' AS source
FROM ubereats.restaurants
UNION ALL
SELECT name, latitude, longitude, city, region, 'Takeaway' AS source
FROM takeaway.restaurants;
"""
cursor = con.execute(query)
results = cursor.fetchall()
