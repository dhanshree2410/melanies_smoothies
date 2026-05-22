import streamlit as st

# Snowflake connection
cnx = st.connection("snowflake")

# App title
st.title("🥤 Customize Your Smoothie! 🥤")

st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")

st.write("The name on your Smoothie will be:", name_on_order)

# Read fruits from Snowflake
fruit_df = cnx.query("""
    SELECT FRUIT_NAME
    FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS
""")

fruit_list = fruit_df["FRUIT_NAME"].tolist()

# Fruit selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Submit order
if ingredients_list:

    ingredients_string = " ".join(ingredients_list)

    if st.button("Submit Order"):

        insert_sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (INGREDIENTS, NAME_ON_ORDER)
        VALUES
        ('{ingredients_string}', '{name_on_order}')
        """

        conn = cnx.raw_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(insert_sql)
            conn.commit()
            st.success("Your Smoothie is ordered!", icon="✅")

        finally:
            cursor.close()
            conn.close()

      
