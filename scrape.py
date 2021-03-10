# URL to scrape: https://apps.irs.gov/app/picklist/list/priorFormPublication.html

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

#%%
import requests 
from bs4 import BeautifulSoup

# %%
# Declare the url you want to scrape
URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"

# Request the raw HTML data from URL and store it in a variable 
page = requests.get(URL)

# Use BeautifulSoup to parse the page content and store it in a variable
soup = BeautifulSoup(page.content, 'html.parser')

# Find all useful table rows by searching for their even/odd class
results = soup.findAll(True, {'class':['even','odd']})

print(results)