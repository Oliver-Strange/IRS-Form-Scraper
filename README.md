# IRS-Form-Scraper

Program to search and download tax forms by name and year.

## Python Version

    3.9.0

## How To Run

- pip install requirements.txt

Run scrape.py file

- python scrape.py
- or run by cell in jupyter notebook

Program will ask for form type, ex Form W-2

You can then specify a year or range of years to download

## Thoughts

This was a really fun project! Thank you for having your coding challenge be something that could be required on the job and not just a regurgitation of knowledge.

## Next Steps

- convert algorithm into definitions that can be referenced via api
- create a front end to interact with the forms and data
- have list of existing forms to choose from or search through
- make sure only correct type of info gets passed through input
- download personal list of forms to reference incase the IRS HTML changes

## Notes

- data is in div with class "picklistTable" in table with class "picklist-dataTable"
- table rows have class even/odd but probably just for color
- each row has table data:
  - class "LeftCellSpacer" - a link to download pdf with text as the product number
  - class "MiddleCellSpacer" - the title
  - class "EndCellSpacer" - the year
- max amount of results is 200 per page

 URL to scrape: https://apps.irs.gov/app/picklist/list/priorFormPublication.html

 When W-2 is searched for, URL looks like:

 https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value=Form+W-2&isDescending=false

 Data to pull:

    Product Number, 
    Title, 
    Year Min & Year Max available download range

 Json Shape:

    [
        {
        "form_number": "Form W-2",
        "form_title": "Wage and Tax Statement (Info Copy Only)",
        "min_year": 1954,
        "max_year": 2021,
        },
        ...
    ]
