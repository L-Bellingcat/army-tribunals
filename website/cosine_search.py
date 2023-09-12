import time

import numpy as np
import pandas as pd
from pandas import DataFrame

from embed import embed_text


def create_index():
    data = pd.read_csv('chandigarh.csv')

    # Remove all rows that have NaN values
    data = data.dropna()

    # Convert the 'embedding' column from string to numpy array
    data['embedding'] = data['embedding'].apply(
        lambda x: np.fromstring(x[1:-1], sep=',')
    )

    print(data['embedding'].head())

    # Compute the cosine similarity between the embeddings
    similarities = data['embedding'].apply(
        lambda x: data['embedding'].apply(lambda y: np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y)))
    )

    # Save the similarities to a CSV file
    similarities.to_csv('similarities/chandigarh.csv', index=False)


class FindSimilar:
    def __init__(self, df: DataFrame):
        self.df = df

    def find_closest(self, text: str, K: int = 10):
        """Embed the text and find the closest judgement in the index using cosine similarity."""
        embedding = embed_text(text)

        # Compute the cosine similarity between the embedding and all the embeddings in the index
        self.df['similarity'] = self.df['embedding'].apply(
            lambda x: np.dot(x, embedding) / (np.linalg.norm(x) * np.linalg.norm(embedding)))

        # Sort the df by similarity in descending order
        similarities = self.df.sort_values(by='similarity', ascending=False)

        # Return the top K similar judgements
        return similarities.head(K)


def load_chandigarh_df(path: str) -> DataFrame:
    data = pd.read_csv(path)

    print(data.head())

    # Remove all rows that have NaN values
    data = data.dropna()

    # Convert the 'embedding' column from string to numpy array
    data['embedding'] = data['embedding'].apply(
        lambda x: np.fromstring(x[1:-1], sep=',')
    )

    return data


def main():
    # Create an instance of FindSimilar

    start = time.time()
    find_similar = FindSimilar(load_chandigarh_df('../embeddings/chandigarh.csv'))
    end = time.time()
    print("Time taken to load data: ", end - start)

    # Find the closest judgement to the given text
    print(find_similar.find_closest(
        "Bhani Devi Vs. Union of India & Ors"
    ))


if __name__ == '__main__':
    # time main() execution time
    import timeit

    print(timeit.timeit(main, number=1))
