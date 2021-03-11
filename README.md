# IRS-Form-Scraper

Program to search and download tax forms by name and year.

## Python Version

    3.9.0

## How To Run

## Thoughts

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
