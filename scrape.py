#%%
import requests 
from bs4 import BeautifulSoup
import json
import os

#%%
desired_form = input("Which form are you looking for? \n")

# change spaces to + for url
sanitzed_desired_form = desired_form.replace(" ", "+")

print("Looking for " + desired_form + " \n")

# %%
# Declare the url you want to scrape
URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value=" + sanitzed_desired_form + "&isDescending=false"

# Request the raw HTML data from URL and store it in a variable 
page = requests.get(URL)

# Use BeautifulSoup to parse the page content and store it in a variable
soup = BeautifulSoup(page.content, 'html.parser')

# Find all useful table rows by searching for their even/odd class
results = soup.findAll(True, {'class':['even','odd']})

print("HTML data retrieved \n")

# %%
# Declare an empty array of the future cleaned results
clean_results = []

# Declare empty strings for form number and title so they can be used later
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
        clean_results.append({"form_number":row_form_number, "form_link":row_form_link, "form_title":row_form_title, "form_year": int(row_form_year)})

        # Assign the title and form number to be used later
        searched_form_number = row_form_number
        searched_form_title = row_form_title

print("Results cleaned \n")

# %%
# If the URL has isDescending set to false than the first item will be the max year
#   and the last item will be the min year

max_form_year = clean_results[0]["form_year"]
min_form_year = clean_results[len(clean_results)-1]["form_year"]

# Innitialize an empty array to hold the final output
desired_format = []
# Append desired data in disired order
desired_format.append({"form_number": searched_form_number,"form_title": searched_form_title, "min_year": min_form_year, "max_year": max_form_year})

print("Forms found: \n", json.dumps(desired_format), '\n')

#%%
# Get input for desired form year or years
desired_years = input("If you want to download, please enter a 4 digit year xxxx or range of years xxxx-xxxx \n")
# Save the desired year or range of years to reference later
desired_year = 0
max_year = 0
min_year = 0 
# Save the form url for downloading 
form_url = " "

# If the input was only 4 digits then 1 year is desired
if len(desired_years) == 4:
    # Set the input as the desired year
    desired_year = desired_years
    print("Downloading " + desired_year + " " + searched_form_number + "\n")
       
    # Itterate through the clean results 
    for form in clean_results:

        # Check to see if the form year is the same as desired year
        if form['form_year'] == int(desired_year):

            # Set the form url from the cleaned data
            form_url = form['form_link']

            # Check if subdirectory with file name exists
            if not os.path.exists(desired_form):
                print("Creating subdirectory... \n")

                # Make a new directory with read write access
                os.mkdir(desired_form, mode = 0o666)

                # Get the data from the url
                requested_download = requests.get(form_url, stream = True)

                # Change into the directory we want to save the data in
                os.chdir(f'{desired_form}')

                # Steam the data to be saved
                with open(f"{desired_form} - {desired_year}.pdf", 'wb') as f:
                    for chunk in requested_download.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                    f.close()    

                print("Enjoy your download! \n")
                # Go up a level, useful if cell is ran multiple times
                os.chdir('..')

            # Else if the directory does exist
            elif os.path.exists(desired_form):

                # Change to the desired directory
                os.chdir(f'{desired_form}')

                # Get the data from the url
                requested_download = requests.get(form_url, stream = True)

                # Stream the data to be saved
                with open(f"{desired_form} - {desired_year}.pdf", 'wb') as f:
                    for chunk in requested_download.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                    
                    f.close()

                print("Enjoy your download! \n")

                # Go up a level, useful if cell is ran multiple times
                os.chdir('..')

# If the input was length 9, then a range of years is desired
elif len(desired_years) == 9:

    # Slice the input string for the max and min year
    max_year = desired_years[5:]
    min_year = desired_years[:4]
    print("Downloading " + searched_form_number + " forms from " + min_year + " to " + max_year)

    # Create an empty array to store the download urls
    url_list = []

    # Itterate over the cleaned results
    for form in clean_results:

        # If the form year fall within the range of desired years
        if int(min_year) <= form['form_year'] <= int(max_year):

            # Append the url and form year to the url list
            url_list.append({"form_link":form['form_link'], "form_year": form['form_year']})

    # Itterate over the urls
    for url in url_list:
        # If the directory does not exist
        if not os.path.exists(desired_form):
            print("Creating subdirectory... \n")
            
            # Create the subdirectory 
            os.mkdir(desired_form, mode = 0o666)
            
            # Get the data from the url
            requested_download = requests.get(url['form_link'], stream = True)

            # Navigate to the desired directory
            os.chdir(f'{desired_form}')

            # Stream and save the data
            with open(f"{desired_form} - {url['form_year']}.pdf", 'wb') as f:
                for chunk in requested_download.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                f.close()    

            print(f"Downloading {url['form_year']} \n")

            # Go up a level
            os.chdir('..')

            print("Enjoy your downloads!")

        # If the directory does exist
        elif os.path.exists(desired_form):

            # Navigate to the directory
            os.chdir(f'{desired_form}')

            # Download the data 
            requested_download = requests.get(url['form_link'], stream = True)
            
            # Steam and save the data
            with open(f"{desired_form} - {url['form_year']}.pdf", 'wb') as f:
                for chunk in requested_download.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                    
                f.close()

            print(f"Downloading {url['form_year']} \n")

            # Go up a level
            os.chdir('..')

            print("Enjoy your downloads!")
# %%
