import streamlit as st

st.title("🥤 Customize Your Smoothie! 🥤")

st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")

st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")

fruit_df = cnx.query("""
    SELECT FRUIT_NAME
    FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS
""")

fruit_list = fruit_df["FRUIT_NAME"].tolist()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

if ingredients_list:

    ingredients_string = " ".join(ingredients_list)

    if st.button("Submit Order"):

        insert_sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (INGREDIENTS, NAME_ON_ORDER)
        VALUES
        ('{ingredients_string}', '{name_on_order}')
        """

        cnx.query(insert_sql)

        st.success("Your Smoothie is ordered!", icon="✅")

        st.success('Your Smoothie is ordered!', icon="✅")
        
