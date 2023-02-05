import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom''s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)
#create repeatable code block (called a function)
def get_fruitivice_data (this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +  this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
    
#New section to display fruitvice  api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruitivice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    #streamlit.write('The user entered ', fruit_choice)
 
except URLError as e:
    streamlit.error()
 
# streamlit.text(fruityvice_response.json()) #This  .json actually showed json version of the response as opposed to   showing <response 200>

# write your own comment passed the response to pandas library
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - this shows the response in a  table 
streamlit.dataframe(fruityvice_normalized)

#import snowflake.connector
streamlit.header("The fruit load list contains:|")
#snowflake-related functions:
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    retunr my_cur.fetchall()
    
# add a button to load fruit    
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
    
#stop processing anything beyond here
streamlit.stop()
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

#this is not supposed to work properly
my_cur.execute ("insert into fruit_load_list values ('values from steamlit')")
