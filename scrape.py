#%%
import requests 
from bs4 import BeautifulSoup
import json

#%%
desired_form = input("Which form are you looking for?")
# desired_form = "Form W-2"
sanitzed_desired_form = desired_form.replace(" ", "+")
# change spaces to + for url
print("Looking for " + desired_form)

# %%
# Declare the url you want to scrape
URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value=" + sanitzed_desired_form + "&isDescending=false"

# Request the raw HTML data from URL and store it in a variable 
page = requests.get(URL)

# Use BeautifulSoup to parse the page content and store it in a variable
soup = BeautifulSoup(page.content, 'html.parser')

# Find all useful table rows by searching for their even/odd class
results = soup.findAll(True, {'class':['even','odd']})

print("HTML data retrieved")

# %%
# Declare an empty array of the future cleaned results
clean_results = []
searched_form_number = ""
searched_form_title = ""

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

    # If the form number matches the searched form
    if row_form_number == desired_form:
        # Append each row as a dictionary to the cleaned results array
        clean_results.append({"form_number":row_form_number, "form_link":row_form_link, "form_title":row_form_title, "form_year":row_form_year})

        # Assign the title and form number to be used later
        searched_form_number = row_form_number
        searched_form_title = row_form_title

print("Results cleaned")

# %%
# If the URL has isDescending set to false than the first item will be the max year
#   and the last item will be the min year

max_form_year = clean_results[0]["form_year"]
min_form_year = clean_results[len(clean_results)-1]["form_year"]

# Innitialize an empty array to hold the final output
desired_format = []
# Append desired data in disired order
desired_format.append({"form_number": searched_form_number,"form_title": searched_form_title, "min_year": int(min_form_year), "max_year": int(max_form_year)})

print(json.dumps(desired_format))

#%%
# input("If you want to download, please enter a year xxxx or range of years xxxx-xxxx")

# establish if it is one year or multiple
# search the cleaned results for that year or years and the download links
# check if subdirectory with form number exists
# if it doesn't, create the subdirectory and download the file there with form number and year as file name
# else, download the file there 

