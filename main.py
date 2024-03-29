import requests
from bs4 import BeautifulSoup
import re


# Define a function to extract address information from a given URL
def extract_address(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element containing address information (you need to inspect the webpage to find this)
        address_element = soup.find('div', class_='address')  # Example: div with class 'address'

        # Extract text containing address information
        address_text = address_element.get_text() if address_element else None

        # Define regular expressions to extract address components
        country_regex = re.compile(r'Country: (.+)')
        region_regex = re.compile(r'Region: (.+)')
        city_regex = re.compile(r'City: (.+)')
        postcode_regex = re.compile(r'Postcode: (\d+)')
        road_regex = re.compile(r'Road: (.+)')
        road_number_regex = re.compile(r'Road Number: (\d+)')

        # Extract address components using regular expressions
        country = country_regex.search(address_text).group(1) if country_regex.search(address_text) else None
        region = region_regex.search(address_text).group(1) if region_regex.search(address_text) else None
        city = city_regex.search(address_text).group(1) if city_regex.search(address_text) else None
        postcode = postcode_regex.search(address_text).group(1) if postcode_regex.search(address_text) else None
        road = road_regex.search(address_text).group(1) if road_regex.search(address_text) else None
        road_number = road_number_regex.search(address_text).group(1) if road_number_regex.search(
            address_text) else None

        # Return the extracted address components
        return country, region, city, postcode, road, road_number

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
for website in websites:
    country, region, city, postcode, road, road_number = extract_address(website)
    if country:
        print(f"Address for {website}:")
        print(f"Country: {country}")
        print(f"Region: {region}")
        print(f"City: {city}")
        print(f"Postcode: {postcode}")
        print(f"Road: {road}")
        print(f"Road Number: {road_number}")
        print()
    else:
        print(f"No address found for {website}")
