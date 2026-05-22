import streamlit as st
import pandas as pd
import requests

# Snowflake connection
cnx = st.connection("snowflake")

# App title
st.title("🥤 Customize Your Smoothie! 🥤")

st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")

st.write("The name on your Smoothie will be:", name_on_order)

# Read fruit table with FRUIT_NAME and SEARCH_ON
pd_df = cnx.query("""
    SELECT FRUIT_NAME, SEARCH_ON
    FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS
""")

# Fruit selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"],
    max_selections=5
)

if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:

        ingredients_string += fruit_chosen + " "

        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        st.write("The search value for", fruit_chosen, "is", search_on, ".")

        st.subheader(fruit_chosen + " Nutrition Information")

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )

        st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

    if st.button("Submit Order"):

        insert_sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (INGREDIENTS, NAME_ON_ORDER)
        VALUES
        ('{ingredients_string}', '{name_on_order}')
        """

        conn = cnx.raw_connection
        cursor = conn.cursor()

        try:
            cursor.execute(insert_sql)
            conn.commit()
            st.success("Your Smoothie is ordered!", icon="✅")

        finally:
            cursor.close()
