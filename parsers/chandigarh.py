"""Parses the table of judgements from the Chandigarh bench of the Armed Forces Tribunal website.

From each row in the table it extracts the following information:
* Case number
* Court
* Year
* Month
* URL to the judgement
* Names of the judges
"""
import re

from bs4 import BeautifulSoup


def extract_case_number(row_html: str):
    regex = r'Case No\.:\s*<span style="color:blue">(.+?)<\/span>'
    match = re.search(regex, row_html)
    if not match:
        raise ValueError('Could not parse case number from row: {}'.format(row_html))
    return match.group(1)


def extract_court(row_html: str):
    regex = r'Bench\s*:\s*<span style="color:blue">\s*(.*?)\s*</span>'
    match = re.search(regex, row_html)
    if not match:
        raise ValueError('Could not parse court from row: {}'.format(row_html))
    return match.group(1)


def extract_year(row_html: str):
    regex = r'Year\s*:\s*<span style="color:blue">\s*(.*?)\s*</span>'
    match = re.search(regex, row_html)
    if not match:
        raise ValueError('Could not parse year from row: {}'.format(row_html))
    return match.group(1)


def extract_month(row_html: str):
    regex = r'Month\s*:\s*<span style="color:blue">\s*(.*?)\s*</span>'
    match = re.search(regex, row_html)
    if not match:
        raise ValueError('Could not parse month from row: {}'.format(row_html))
    return match.group(1)


def extract_pdf_url(row_html: str):
    regex = r'<a href="([^"]+)" target="_blank">ViewPDF<\/a>'
    match = re.search(regex, row_html)
    if not match:
        raise ValueError('Could not parse pdf url from row: {}'.format(row_html))
    return match.group(1)


def cleanup_judge_name(name: str):
    name = name.lower()

    # Strings to remove from the name
    strip_list = [
        'hon’ble',
        'hon`ble',
        "hon'ble",
        '(member)',
        'member',
        '(administrative member)',
        '(administrative )',
        'administrative',
        'administrative member',
        '(j)',
        '(judicial )',
        'judicial',
        'mr.',
        'mr',
        'justice',
        '(retd.)',
        '(a)',
        '(retd)'
    ]

    for s in strip_list:
        name = name.replace(s, '')

    # Strip whitespace
    name = name.strip()

    # Strip trailing comma
    if name.endswith(','):
        name = name[:-1]

    return name


def extract_judges(row_html: str):
    regex = r'Judgement given by:\s*<span style="color:blue">([\w\s.,\'’()]+)</span>\s*&amp;\s*<span style="color:blue">([\w\s.,\'’()]+)</span>'

    match = re.search(regex, row_html)
    if not match:
        raise ValueError('Could not parse judges from row: {}'.format(row_html))
    return cleanup_judge_name(match.group(1)), cleanup_judge_name(match.group(2))


def parse_row(row_html: str):
    """Parses a row from the table of judgements.

    Args:
        row_html: The HTML of the row to parse.

    Returns:
        A dictionary containing the parsed information.
    """
    civilian, military = extract_judges(row_html)
    return {
        'case_number': extract_case_number(row_html),
        'court': extract_court(row_html),
        'year': extract_year(row_html),
        'month': extract_month(row_html),
        'pdf_url': extract_pdf_url(row_html),
        'civilian_judge': civilian.lower(),
        'military_judge': military.lower(),
    }


def main():
    # Load Chandigarh.html into a string
    with open('/home/laurence/dev/indian_army_tribunals/web_pages/Chandigarh.html', 'r') as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    # Find all div tags with class 'tr'
    rows = soup.find_all('div', class_='tr')

    # Parse each whilst printing the row number
    parsed_rows = []
    for i, row in enumerate(rows):
        print('Parsing row {}'.format(i))
        parsed_rows.append(parse_row(str(row)))

    # Print the parsed rows
    print(parsed_rows)

    # Load into a dataframe
    import pandas as pd
    df = pd.DataFrame(parsed_rows)
    print(df)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Save to CSV
    df.to_csv('structured_judgements/Chandigarh.csv', index=False)


if __name__ == '__main__':
    main()
