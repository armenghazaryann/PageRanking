import requests
from bs4 import BeautifulSoup
import json


# Define a recursive function to scrape websites
def scrape_website(url, visited, depth=0, max_websites=100):
    # Create a dictionary to store child links
    child_links = {}

    # Check if the max websites limit is reached
    if len(visited) >= max_websites:
        return child_links

    # Check if the URL is already visited
    if url in visited:
        return child_links

    # Mark the URL as visited
    visited.add(url)

    # Send an HTTP GET request to the URL
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        # If there is any request error, return an empty dictionary
        return child_links

    # Parse the response content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all anchor tags with 'href' attribute
    links = soup.find_all('a', href=True)

    # Iterate through the found links
    for link in links:
        href = link['href']

        # Filter out relative and invalid URLs
        if not href.startswith(('http://', 'https://')):
            continue

        # Recursively scrape the child link
        if len(visited) < max_websites:
            child_links[href] = scrape_website(href, visited, depth + 1, max_websites)

    return child_links


# Main function
def main(start_url):
    # Create a set to track visited URLs
    visited = set()

    # Start the recursive scraping from the start URL
    web_structure = scrape_website(start_url, visited)

    # Convert the web structure to JSON
    web_structure_json = json.dumps(web_structure, indent=4)

    # Save the JSON to a file
    with open('web_structure.json', 'w') as json_file:
        json_file.write(web_structure_json)

    # Print completion message
    print('Web structure saved to web_structure.json')


# Provide the starting URL
start_url = 'https://aua.am/'  # Replace with your desired start URL

# Call the main function with the starting URL
main(start_url)
