import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

# Path to the .snappy.parquet file
file_path = 'websites.snappy.parquet'

# Read the Parquet file into a DataFrame
df = pd.read_parquet(file_path, engine='pyarrow')

domains = np.array(df['domain'].tolist())
# Now you can work with the DataFrame
#print(df.head())
#print(domains)

# Define a function to extract address information from a given URL
def extract_address(url):
    try:
        url="http://www."+url
        # Send a GET request to the URL
        response = requests.get(url)
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element containing address information (you need to inspect the webpage to find this)
        div_elements = soup.find_all('div')  # Example: div with class 'address'

        # Initialize variables to store address components
        addresses = []

        # Define regular expressions to extract address components
        country_regex = re.compile(r'Country: (.+)')
        region_regex = re.compile(r'Region: (.+)')
        city_regex = re.compile(r'City: (.+)')
        postcode_regex = re.compile(r'Postcode: (\d+)')
        road_regex = re.compile(r'Road: (.+)')
        road_number_regex = re.compile(r'Road Number: (\d+)')

        # Extract address components from each div element
        for div_element in div_elements:
            address_text = div_element.get_text()
            if "Country:" in address_text:
                country = country_regex.search(address_text).group(1) if country_regex.search(address_text) else None
                region = region_regex.search(address_text).group(1) if region_regex.search(address_text) else None
                city = city_regex.search(address_text).group(1) if city_regex.search(address_text) else None
                postcode = postcode_regex.search(address_text).group(1) if postcode_regex.search(address_text) else None
                road = road_regex.search(address_text).group(1) if road_regex.search(address_text) else None
                road_number = road_number_regex.search(address_text).group(1) if road_number_regex.search(
                    address_text) else None

                # Append address components to addresses list
                addresses.append((country, region, city, postcode, road, road_number))

        # Return the list of extracted addresses
        return addresses

    except Exception as e:
        print(f"Error extracting address from {url}: {str(e)}")
        return None, None, None, None, None, None


# List of company websites
websites = [
    "https://www.example.com",
    "https://www.example2.com",
    # Add more websites as needed
]

# Iterate over each website and extract address information
for website in domains:
    addresses = extract_address(website)
    if addresses:
        print(f"Addresses for {website}:")
        for address in addresses:
            print(f"Country: {address[0]}")
            print(f"Region: {address[1]}")
            print(f"City: {address[2]}")
            print(f"Postcode: {address[3]}")
            print(f"Road: {address[4]}")
            print(f"Road Number: {address[5]}")
            print()
    else:
        print(f"No address found for {website}")
