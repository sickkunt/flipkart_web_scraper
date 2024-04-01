from bs4 import BeautifulSoup

import requests

import pandas as pd

import numpy as np

def get_title(soup):



  try:

    # Outer Tag Object

    title = soup.find("span", attrs={"class":'B_NuCI'})

     

    # Inner NavigatableString Object

    title_value = title.text



    # Title as a string value

    title_string = title_value.strip()



  except AttributeError:

    title_string = ""



  return title_string



# Function to extract Product Price

def get_price(soup):



  try:

    price = soup.find("div", attrs={"class":'_30jeq3 _16Jk6d'}).string

     

    price_value=price.text



  except AttributeError:

    price_value = ""



  return price_value



# Function to extract Product Rating

def get_rating(soup):



  try:

    rating = soup.find("div", attrs={"class":'_2d4LTz'}).string

     

  except:

    rating = ""



  return rating







def get_discount(soup):

  try:

    discount = soup.find("div", attrs={"class":'_1V_ZGU'}).string

  except AttributeError:

    discount = ""

  return discount

if __name__ == '__main__':



  # add your user agent 

  HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})



  # The webpage URL

  URL = "https://www.flipkart.com/search?q=mobiles&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_1_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_1_0_na_na_na&as-pos=1&as-type=TRENDING&suggestionId=mobiles&requestId=04f31658-7ad8-40ea-8b73-6bfd3e4059b2"



  # HTTP Request

  webpage = requests.get(URL, headers=HEADERS)



  # Soup Object containing all data

  soup = BeautifulSoup(webpage.content, "html.parser")



  # Fetch links as List of Tag Objects

  links = soup.find_all("a", attrs={'class':'_1fQZEK'})



  # Store the links

  links_list = []



  # Loop for extracting links from Tag Objects

  for link in links:

      links_list.append(link.get('href'))



  d = {"title":[], "price":[], "rating":[],"discount":[]}

   

  # Loop for extracting product details from each link 

  for link in links_list:

    new_webpage = requests.get("https://www.flipkart.com" + link, headers=HEADERS)



    new_soup = BeautifulSoup(new_webpage.content, "html.parser")



    # Function calls to display all necessary product information

    d['title'].append(get_title(new_soup))

    d['price'].append(get_price(new_soup))

    d['rating'].append(get_rating(new_soup))

    d['discount'].append(get_discount(new_soup))



   

  flipkart_df = pd.DataFrame.from_dict(d)

  flipkart_df['title'].replace('', np.nan, inplace=True)

  flipkart_df = flipkart_df.dropna(subset=['title'])

  flipkart_df.to_csv("flipkart_data.csv", header=True, index=False)
  