# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# App title
st.title("🥤 Customize Your Smoothie! 🥤")

st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

# Name input
name_on_order = st.text_input('Name on Smoothie:')

st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# Read fruit table
my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(col('FRUIT_NAME'))

# Fruit selection
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# If fruits selected
if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # Create insert statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    # Show SQL query
    st.write(my_insert_stmt)

    # Stop app for debugging
    #st.stop()

    # Submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!', icon="✅")
        
