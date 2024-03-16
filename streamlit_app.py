# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie! """
)


# option = st.selectbox(
#     'What is your favorite fruit?',
#     ('Banana', 'Strawberries', 'Peaches'))

# st.write('You selected:', option)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on you Smoothie will be ', name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop

ingredients_list=st.multiselect('Choose upto 5 ingredients:',my_dataframe, max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit + ' '
        st.subheader(each_fruit + ' Nutrition Information')
        fruityvice_reponse= requests.get("https://fruityvice.com/api/fruit/" + each_fruit)
        fv_df=st.dataframe(data=fruityvice_reponse.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    
    # st.write(my_insert_stmt)
    if ingredients_string:
        time_to_insert=st.button('Submit Order')
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")


