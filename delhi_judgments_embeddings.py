
import pandas as pd
import tiktoken
from pdfminer.high_level import extract_text
from tqdm import tqdm
from google.cloud import storage
import os
import re
import warnings
warnings.filterwarnings("ignore")
import time


from website.embed import embed_text

enc = tiktoken.get_encoding("cl100k_base")
assert enc.decode(enc.encode("hello world")) == "hello world"


def main():

    storage_client = storage.Client.from_service_account_json('army-tribunals-c8dd2aeb6f6e.json')
    bucket_name = "army-tribunals"
    csv_file='Delhi.csv'

    try:
        output_df=pd.read_csv(csv_file)
        completed_conversions=set(output_df["case_id"].tolist())
    except FileNotFoundError:
        output_df = pd.DataFrame(columns=["case_id", "pdf_text", "embeddings"])
        completed_conversions = set()

    blobs = list(storage_client.list_blobs(bucket_name, prefix='Text Cases/Delhi/'))
    print("Length of blobs is ",len(blobs))

    #directory="Text Cases/Delhi"
    #completed_conversions=[]

    for num,blob in tqdm(enumerate(blobs)):

        case_id = os.path.splitext(os.path.splitext(os.path.basename(blob.name))[0])[0]
        if case_id in completed_conversions:
            print(f"Skipping row {case_id} as it has already been embedded")
            continue


        data_dict=process_row(blob)

        if data_dict:
            output_df = output_df.append(data_dict, ignore_index=True)
            if (num+1)%500==0:
                with open(csv_file, 'a') as f:
                    output_df.to_csv(f, header=f.tell() == 0, index=False)
                output_df = pd.DataFrame(columns=["case_id", "pdf_text", "embeddings"])
                current_csv=pd.read_csv(csv_file)
                print(f"Total number of rows in CSV: {len(current_csv)}")

    with open(csv_file, 'a') as f:
        output_df.to_csv(f, header=f.tell() == 0, index=False)

    
    #output_df.to_csv('Delhi.csv',index=False)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob('embeddings/Delhi.csv')
    blob.upload_from_filename(csv_file)

def process_row(blob,max_retries=3):

    if blob.name.endswith('pdf.txt'):

        case_id=os.path.splitext(os.path.splitext(os.path.basename(blob.name))[0])[0]
        pdf_text=blob.download_as_text()

        retries=0
        delay=1

        while retries<max_retries:

            try:
                embedding=embed_text(pdf_text)
                data_dict={
                "case_id":case_id,
                "pdf_text":pdf_text,
                "embeddings":embed_text(pdf_text)
                }
                return data_dict

            except Exception as e:

                print(f"Error processing case {case_id}: {e}")
                time.sleep(delay)
                retries+=1
                delay*=2

        print(f"Failed to process case {case_id} after {max_retries} retries.")
        return None
    

if __name__ == '__main__':
    main()



