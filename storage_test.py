import os

from google.cloud import storage


def main():
    storage_client = storage.Client('army-tribunals')

    bucket = storage_client.bucket('army-tribunals')
    blobs = bucket.list_blobs()

    for blob in blobs:
        local_file_name = 'downloads/' + blob.name
        os.makedirs(os.path.dirname(local_file_name), exist_ok=True)
        blob.download_to_filename(local_file_name)


if __name__ == '__main__':
    main()
