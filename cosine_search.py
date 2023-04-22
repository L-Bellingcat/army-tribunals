import numpy as np
import pandas as pd


def main():
    data = pd.read_csv('embeddings/chandigarh.csv')

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


if __name__ == '__main__':
    main()
