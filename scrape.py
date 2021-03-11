# URL to scrape: https://apps.irs.gov/app/picklist/list/priorFormPublication.html

# When W-2 is searched for, URL looks like: 
# https://apps.irs.gov/app/picklist/list/priorFormPublication.html
# ?resultsPerPage=200
# &sortColumn=sortOrder
# &indexOfFirstRow=0
# &criteria=formNumber
# &value=Form+W-2
# &isDescending=false 

# Data to pull: Product Number, Title, Year Min & Year Max available download range

# Json Shape: [
#    {
#       "form_number": "Form W-2",
#       "form_title": "Wage and Tax Statement (Info Copy Only)",
#       "min_year": 1954,
#       "max_year": 2021,
#    },
#    ...
# ]

# Notes:
# - data is in div with class "picklistTable" in table with class "picklist-dataTable"
# - table rows have class even/odd but probably just for color
# - each row has table data:
#    - class "LeftCellSpacer" - a link to download pdf with text as the product number
#    - class "MiddleCellSpacer" - the title 
#    - class "EndCellSpacer" - the year
# - max amount of results is 200 per page


#%%
import requests 
from bs4 import BeautifulSoup
import json

# %%
# Declare the url you want to scrape
URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"

# Request the raw HTML data from URL and store it in a variable 
page = requests.get(URL)

# Use BeautifulSoup to parse the page content and store it in a variable
soup = BeautifulSoup(page.content, 'html.parser')

# Find all useful table rows by searching for their even/odd class
results = soup.findAll(True, {'class':['even','odd']})

print("HTML grabbed")
# %%
# Declare an empty array of the 
clean_results = []

# Itterate over the soup results 
for row in results:
    # Find and assign desired data in the HTML
    html_form_number = row.find('td', class_='LeftCellSpacer')
    html_form_link = row.find('a', href=True)
    html_form_title = row.find('td', class_='MiddleCellSpacer')
    html_form_year = row.find('td', class_='EndCellSpacer')

    # Format the HTML data into useable text
    row_form_number = html_form_number.text.strip()
    row_form_link = html_form_link['href']
    row_form_title = html_form_title.text.strip()
    row_form_year = html_form_year.text.strip()
    
    # Append each row as a dictionary to the cleaned results array
    clean_results.append({"form_number":row_form_number, "form_link":row_form_link, "form_title":row_form_title, "form_year":row_form_year})

print(json.dumps(clean_results))

# %%
# Itterate over the array looking for like form numbers
# Find the minimum and maximum year for each form