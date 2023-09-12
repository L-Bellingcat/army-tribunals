import pathlib

import pandas as pd
from bs4 import BeautifulSoup


def process_page(html: str):
    # Create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the second table with the class 'dataTable'
    table = soup.find_all('table', class_='dataTable')[1]

    # Load the table into a DataFrame skipping bottom row
    df = pd.read_html(str(table))[0]

    # Drop the last row
    df = df[:-1]

    return df


def main():
    dfs = []

    # Iterate through the HTML files in the directory web_pages/kolkata
    for html_file in pathlib.Path('web_pages/kolkata').iterdir():
        # Open the HTML file
        with open(html_file) as f:
            # Read the HTML file
            html = f.read()

            # Process the HTML file
            dfs.append(process_page(html))

    # Concatenate the DataFrames
    df = pd.concat(dfs, ignore_index=True)

    col_name_map = {
        'Title': 'applicant_name',
        'Description': 'description',
        'Case No': 'case_number',
        'File Name': 'pdf_url',
    }

    # Rename the columns
    df.rename(columns=col_name_map, inplace=True)

    # Append the string https://aftkolkata.nic.in/upload/court/ to the pdf_url column
    df['pdf_url'] = 'https://aftkolkata.nic.in/upload/court/' + df['pdf_url']

    # Save to CSV
    df.to_csv('structured_judgements/kolkata.csv', index=False)


if __name__ == '__main__':
    main()
