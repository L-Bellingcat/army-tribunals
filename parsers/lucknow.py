"""Parses the table of judgements from the Chandigarh bench of the Armed Forces Tribunal website.

From each row in the table it extracts the following information:
* S number
* Applicant name
* Subject
"""
from typing import List

from bs4 import BeautifulSoup

month_to_number = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'sept': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12,
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12,
}

month_year_bodges = {
    'oct , nov 2020': (10, 2020),
    '125': (None, None),
    '156': (None, None),
    '9': (None, None),
    'judgment 2015': (None, None),
    'oct & sept 2015': (9, 2015),
    'judgment 2014': (1, 2014),
    'august 2015 to jan 2015': (1, 2015),
    'judgment 2013': (None, None),
    'judgment 2012': (None, None),
    'jul 17': (7, 2017),
}


def parse_row_fragment_table_1(columns):
    """Takes in three columns from a row in table 1 and returns a dictionary of the parsed values."""
    s_number = columns[0].text.strip()
    applicant_name = columns[1].text.strip()
    pdf_url = columns[1].find('a')['href']
    subject = columns[2].text.strip()

    return {
        's_number': s_number,
        'applicant_name': applicant_name,
        'pdf_url': pdf_url,
        'subject': subject,
    }


def date_from_row(row):
    """Checks if all cols are empty apart from one. If so, returns the date from that column."""
    cols = row.find_all('td')

    # If there are not 12 columns this row contains the month and year
    if len(cols) == 1:
        row_text = row.text.strip().lower()
    else:
        # If only one of the columns contains text, it is the date
        if sum([bool(col.text.strip()) for col in cols]) == 1:
            for col in cols:
                if col.text.strip():
                    row_text = col.text.strip().lower()
        else:
            return None, None

    # Replace \xa02020 with space
    row_text = row_text.replace(u'\xa0', ' ')

    # Replace - with space
    row_text = row_text.replace('-', ' ')

    # Convert double spaces to single spaces
    row_text = ' '.join(row_text.split())

    print(f"row_text: {row_text}")

    # check if in bodges
    if row_text in month_year_bodges:
        return month_year_bodges[row_text]

    print(f"row_text: {row_text}")
    month_str, year_str = row_text.split(' ')
    month_str = month_str.strip()
    month_str = month_str.replace(',', '')

    month = month_to_number[month_str]

    year = int(year_str.strip())

    if year < 2010:
        raise ValueError(f"Year {year} is too old")

    return month, year


def parse_12_width_table(table, month_initial, year_initial) -> List[dict]:
    month = month_initial
    year = year_initial

    judgements = []

    # Iterate through rows enumerating them
    for i, row in enumerate(table.find_all('tr')):
        print(f"processing row {i}, month {month}, year {year}")

        # Extract the columns
        cols = row.find_all('td')

        candidate_month, candidate_year = date_from_row(row)
        if candidate_month and candidate_year:
            month = candidate_month
            year = candidate_year
            continue

        # If none of the columns contain an anchor tag, skip this row
        if not any([col.find('a') for col in cols]):
            continue

        for fragment_i in range(0, len(cols), 3):
            fragment = cols[fragment_i:fragment_i + 3]
            try:
                fragment_data = parse_row_fragment_table_1(fragment)
            except Exception as e:
                print(f"Error parsing row {i} fragment {fragment_i}: {e}")
                continue
            fragment_data['month'] = month
            fragment_data['year'] = year

            judgements.append(fragment_data)

    return judgements


def main():
    # Load Chandigarh.html into a string
    with open('web_pages/Lucknow.html', 'r') as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    # Extract the 6 tables
    tables = soup.find_all('table')

    # Parse first table
    judgements = parse_12_width_table(tables[0], 3, 2023)

    # Skip empty second and third tables
    # Parse fourth table
    judgements += parse_12_width_table(tables[3], 9, 2019)

    # Parse fifth table
    judgements += parse_12_width_table(tables[4], 5, 2018)

    # Skip empty sixth table

    # Parse seventh table
    judgements += parse_12_width_table(tables[6], 12, 2016)

    # Load into a dataframe
    import pandas as pd
    df = pd.DataFrame(judgements)
    print(df)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Save to CSV
    df.to_csv('structured_judgements/lucknow.csv', index=False)


if __name__ == '__main__':
    main()
