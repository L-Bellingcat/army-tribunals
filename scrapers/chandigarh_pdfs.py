import random
import time
from pathlib import Path

import pandas as pd
import requests

def main():
    # session = configure_proxies()

    # Load structured_judgements/Chandigarh.csv into DataFrame
    chandigarh = pd.read_csv('../structured_judgements/chandigarh.csv')

    # Iterate over the DataFrame and download the judgement PDF from each
    # row's 'pdf_url' column
    for index, row in chandigarh.iterrows():
        url = row['pdf_url']
        filename = f"judgement_pdfs/chandigarh/{row['case_number']}.pdf"

        # Check if the PDF already exists
        if Path(filename).exists():
            print('Skipping {} as it already exists'.format(filename))
            continue

        # Download the PDF
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

        # Wait for a random time between 0 and 0.2 seconds
        time.sleep(random.random() * 0.2)

        # Print progress
        print('Downloaded {} of {} judgements'.format(index + 1, len(chandigarh)))


if __name__ == '__main__':
    main()
