import random
import time
from pathlib import Path

import pandas as pd
import requests


def main():
    # Load structured_judgements/Chandigarh.csv into DataFrame
    kolkata = pd.read_csv('structured_judgements/kolkata.csv')

    # Iterate over the DataFrame and download the judgement PDF from each
    # row's 'pdf_url' column
    for index, row in kolkata.iterrows():
        url = row['pdf_url']

        # Extract filename from URL
        filename = url.split('/')[-1]

        save_path = f"judgement_pdfs/kolkata/{filename}"

        # Check if the PDF already exists
        if Path(save_path).exists():
            print('Skipping {} as it already exists'.format(save_path))
            continue

        # Download the PDF
        response = requests.get(url, verify=False)
        with open(save_path, 'wb') as f:
            f.write(response.content)

        # Wait for a random time between 0 and 0.1 seconds
        time.sleep(random.random() * 0.1)

        # Print progress
        print('Downloaded {} of {} judgements'.format(index + 1, len(kolkata)))


if __name__ == '__main__':
    main()
