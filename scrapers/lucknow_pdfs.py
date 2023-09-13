import random
import time
import urllib.parse
from pathlib import Path

import pandas as pd
import requests

def scrape_pdfs(region: str):
    # session = configure_proxies()

    region_data = pd.read_csv(f'structured_judgements/{region}.csv')

    # Iterate over the DataFrame and download the judgement PDF from each
    # row's 'pdf_url' column
    for index, row in region_data.iterrows():
        url = row['pdf_url']

        pdf_filename = url.split('/')[-1]
        decoded_filename = urllib.parse.unquote(pdf_filename)

        save_path = f"judgement_pdfs/{region}/{decoded_filename}"

        # Check if the PDF already exists
        if Path(save_path).exists():
            print('Skipping {} as it already exists'.format(save_path))
            continue

        # Download the PDF
        try:
            response = requests.get(url)
        except requests.exceptions.InvalidSchema:
            print(f'Invalid schema for {url}')
            continue

        with open(save_path, 'wb') as f:
            f.write(response.content)

        # Wait for a random time between 0 and 0.2 seconds
        time.sleep(random.random() * 0.2)

        # Print progress
        print('Downloaded {} of {} judgements'.format(index + 1, len(region_data)))


def main():
    scrape_pdfs('lucknow')


if __name__ == '__main__':
    main()
