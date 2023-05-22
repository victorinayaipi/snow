import streamlit as st
import pandas as pd
import requests
import snowflake.connector

# Title and header
st.title('My parents\' new healthy diner')
st.header('Breakfast Menu')
st.text('Omega 3 & Blueberry Oatmeal')
st.text('Kale, Spinach & Rocket Smoothie')
st.text('Hard-Boiled Free-Range Egg')

# Read fruit list from URL
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Select fruits
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list['Fruit']))

# Filter and display selected fruits
fruits_to_show = my_fruit_list[my_fruit_list['Fruit'].isin(fruits_selected)]
st.dataframe(fruits_to_show.set_index('Fruit'))

# Fruityvice Fruit Advice
fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice.lower())
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalized)

# Snowflake integration
st.header("Snowflake Integration")

# Connect to Snowflake using credentials from Streamlit secrets
snowflake_credentials = st.secrets["snowflake"]
my_cnx = snowflake.connector.connect(**snowflake_credentials)
my_cur = my_cnx.cursor()

# Fetch and display data from Snowflake
my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("Fruit Load List")
st.dataframe(pd.DataFrame(my_data_rows, columns=my_cur.description))

# Insert data into Snowflake
add_my_fruit = st.text_input("Add a fruit to the load list:")
if st.button("Add Fruit"):
    my_cur.execute(f"INSERT INTO fruit_load_list VALUES ('{add_my_fruit}')")
    st.write('Thanks for adding', add_my_fruit)

# Close Snowflake connection
my_cur.close()
my_cnx.close()
