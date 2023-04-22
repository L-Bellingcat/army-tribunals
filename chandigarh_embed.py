import os

import openai
import pandas as pd
import tiktoken
from dotenv import load_dotenv
from pdfminer.high_level import extract_text
from tqdm import tqdm

enc = tiktoken.get_encoding("cl100k_base")
assert enc.decode(enc.encode("hello world")) == "hello world"

# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4")

load_dotenv()
openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")

MAX_TOKENS = 8191
ENCODING = tiktoken.get_encoding("cl100k_base")


def trim_text(text: str, max_tokens: int = MAX_TOKENS):
    tokens = ENCODING.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return ENCODING.decode(tokens)


def embed_text(text: str):
    text = trim_text(text)

    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']


def process_row(row: pd.Series) -> pd.Series:
    pdf_text = extract_text(f"judgement_pdfs/chandigarh/{row['case_number']}.pdf")

    # Add the text to the row
    row['pdf_text'] = pdf_text

    # Compute the embedding using OpenAI text-embedding-ada-002 model
    row['embedding'] = embed_text(pdf_text)

    return row


def main():
    output_df = pd.read_csv('embeddings/chandigarh.csv')

    # Load the CSV file
    source_df = pd.read_csv('structured_judgements/chandigarh.csv')

    # Add columns for pdf_text and embedding
    source_df['pdf_text'] = None
    source_df['embedding'] = None

    row_num = 0

    # Iterate over the rows of the DataFrame
    for index, row in tqdm(source_df.iterrows(), total=len(source_df)):
        # Skip rows that have already been processed
        if not pd.isna(output_df.loc[index]['pdf_text']):
            print(f"Skipping row {row_num} as it has already been embedded")
            row_num += 1
            continue

        try:
            # Process the row
            source_df.loc[index] = process_row(row)
        except Exception as e:
            print(f"Error processing row {row_num}: {e}")
        row_num += 1

    # Save the DataFrame to a CSV file
    source_df.to_csv('embeddings/chandigarh.csv', index=False)


if __name__ == '__main__':
    main()
