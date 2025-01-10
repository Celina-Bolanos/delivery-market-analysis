import sqlite3
import pandas as pd
import streamlit as st

# Function to run a query
def run_query(database, query):
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"Error executing query on {database}: {e}")
        return []

# Function to format ratings
def format_ratings(df):
    df['Rating'] = df['Rating'].apply(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
    return df

# Function to get top 10 restaurants based on a keyword
def get_top_restaurants(keyword):
    deliveroo_query = f"""
    SELECT name, rating
    FROM restaurants
    WHERE category LIKE '%{keyword}%'
    ORDER BY rating DESC
    LIMIT 10;
    """
    takeaway_query = f"""
    SELECT r.name, r.ratings
    FROM restaurants r
    JOIN categories_restaurants c
    ON LOWER(TRIM(r.name)) LIKE LOWER(TRIM('%' || c.restaurant_id || '%'))
    WHERE LOWER(c.category_id) LIKE '%{keyword}%'
    ORDER BY r.ratings DESC
    LIMIT 10;   
    """
    ubereats_query = f"""
    SELECT r.title AS name, r.rating__rating_value AS ratings
    FROM restaurants r
    JOIN restaurant_to_categories c ON r.id = c.restaurant_id
    WHERE LOWER(c.category) LIKE '%{keyword}%'
    ORDER BY r.rating__rating_value DESC
    LIMIT 10;
    """

    # Database paths
    ubereats_db = "C:/Users/hp/Imad/Food_Delivery/ubereats.db"
    deliveroo_db = "C:/Users/hp/Imad/Food_Delivery/deliveroo.db"
    takeaway_db = "C:/Users/hp/Imad/Food_Delivery/takeaway.db"

    # Fetch results from each database
    deliveroo_results = run_query(deliveroo_db, deliveroo_query)
    takeaway_results = run_query(takeaway_db, takeaway_query)
    ubereats_results = run_query(ubereats_db, ubereats_query)

    # Combine results into a single dataframe
    all_results = pd.concat(
        [
            pd.DataFrame(deliveroo_results, columns=['Restaurant', 'Rating']),
            pd.DataFrame(takeaway_results, columns=['Restaurant', 'Rating']),
            pd.DataFrame(ubereats_results, columns=['Restaurant', 'Rating']),
        ],
        ignore_index=True
    )

    # Create final top 10 list
    final_top_10 = all_results.sort_values(by='Rating', ascending=False).drop_duplicates(subset='Restaurant').head(10)

    # Format ratings to one decimal place
    final_top_10 = format_ratings(final_top_10)

    # Reset index to start from 1
    final_top_10.reset_index(drop=True, inplace=True)
    final_top_10.index += 1  # Start index at 1

    return final_top_10

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #DFF1EF; /* Set background color */
    }

    /* Style for the title */
    h1 {
        font-size: 5rem; /* Very large font size for the main title */
        color: #55828b; /* Custom color for the title */
    }

    /* Style for text input label */
    label {
        font-size: 20rem; /* Larger font for labels */
        color: #55828b;
    }

    /* Style for all other text */
    body {
        font-size: 10rem; /* Larger font size for the body text */
        color: #55828b;
    }

    /* Table font size */
    .stTable {
        font-size: 1.8rem; /* Larger table text */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit
st.title("Restaurant Search")
st.subheader("Search for the top 10 restaurants.")
st.subheader("Enter a keyword below to get started (e.g., pizza, sushi, burger):")

# User input
keyword = st.text_input("", value="pizza").strip().lower()

st.subheader(f"Top 10 restaurants for '{keyword}':")

if keyword:
    top_10_restaurants = get_top_restaurants(keyword)

    if top_10_restaurants.empty:
        st.warning(f"No results found for '{keyword}'.")
    else:
        st.write(f"Top 10 restaurants for '{keyword}':")
        st.table(top_10_restaurants)
