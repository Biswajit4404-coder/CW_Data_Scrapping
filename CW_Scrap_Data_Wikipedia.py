import requests
from bs4 import BeautifulSoup
import csv

# Wikipedia URL
wiki_url = "https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Fetch the webpage
response = requests.get(wiki_url, headers=headers)

# Check if the request was successful
if response.status_code != 200:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    exit()

# Fetch HTML content
response = requests.get(wiki_url)
if response.status_code != 200:
    print("Failed to fetch Wikipedia page. Status code:", response.status_code)
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all tables
tables = soup.find_all('table')
print(f"Found {len(tables)} tables on the page.")

# Look for the table
table = soup.find('table', class_='wikitable sortable mw-datatable sticky-header-multi sort-under plainrowheaders jquery-tablesorter')

if not table:
    print("Failed to find the table")
    exit()

# Extract rows
rows = table.find_all('tr')

# Prepare data
state_data = []
for row in rows[1:]:  # Skip the header row
    cells = row.find_all(['th', 'td'])  # Include headers for state names
    if len(cells) > 2:  # Ensure the row has enough data
        state_name = cells[0].text.strip()
        population = cells[2].text.strip()
        state_data.append({"State": state_name, "Population": population})

# Save to CSV
csv_file = "US_States_Population.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["State", "Population"])
    writer.writeheader()
    writer.writerows(state_data)

print(f"US state data saved to '{csv_file}'")
