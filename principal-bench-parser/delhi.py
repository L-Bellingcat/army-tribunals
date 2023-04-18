import os
import re
import logging
import time
from tqdm import tqdm
import time
import boto3
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import io
import csv
from urllib.parse import urljoin
from pathlib import Path
from page_parser import parse_row

URL="https://www.aftdelhi.nic.in/index.php/site-links/judgement-by-case?start={}"


# Checkpoint file
checkpoint_file = "checkpoint.txt"

def save_checkpoint(page):
    with open(checkpoint_file, "w") as f:
        f.write(str(page))

def load_checkpoint():
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            return int(f.read().strip())
    return 0


def get_total_pages(URL,start_page):
    

    response = requests.get(URL.format(start_page),timeout=30)
    soup = BeautifulSoup(response.text, 'html.parser')

    
    div_block = soup.find('div', {'class': 'block'})

    
    p_text = div_block.find('p').text
    total_pages = int(p_text.split('of ')[1].split('\n')[0])

    
    results_per_page = int(div_block.find('select', {'id': 'limit'}).find('option', {'selected': True}).text)

    return total_pages,results_per_page

def get_results_from_page(page, URL):
    print("Returning page.",URL.format(page))

    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(URL.format(page))
            soup = BeautifulSoup(response.text, 'html.parser')

           
            rows = soup.find_all("div", class_="tr")
            if not rows:
                print("Nothing to see here. ",page," ...it is empty")
                return None
            return rows
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}, retrying ({retries + 1}/{max_retries})")
            retries += 1
            time.sleep(2 * retries)
    raise Exception("Max retries exceeded")


def save_progress(file_path, data, mode='a'):
    with open(file_path, mode, newline='', encoding='utf-8') as csvfile:
        fieldnames = ["case_number","registration_date","respondent","judgement_date","petitioner","mode","petitioner_advocate","respondent_advocate","subject","pdf_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if mode == 'w':
            writer.writeheader()
        for row in data:
            writer.writerow(row)


def main(URL, output_dir):

    print("This is only for delhi...")

    os.makedirs(output_dir, exist_ok=True)
    start_page = load_checkpoint()

    total_pages, results_per_page = get_total_pages(URL, start_page)

    print("Total pages: ",total_pages)
    print("Results per page: ",results_per_page)


    all_parsed_data=[]
    temp_file_path = os.path.join(output_dir, 'only_delhi_temp.csv')
    save_progress(temp_file_path,all_parsed_data,mode='w')


    for page in tqdm(range(start_page * results_per_page, total_pages * results_per_page, results_per_page), desc="Pages Now"):

        print("This is the page ", page//results_per_page+1)
        rows=get_results_from_page(page, URL)
        if rows is None:
            continue

        

        for i,row in enumerate(rows):
            
            parsed_data = parse_row(row)
            all_parsed_data.append(parsed_data)
            
            if len(all_parsed_data) >= 50:
                print(len(all_parsed_data))
                save_progress(temp_file_path, all_parsed_data, mode='a')
                print(f"Temporary progress saved after processing {len(all_parsed_data)} rows.")
                all_parsed_data=[]
                
        
        save_checkpoint(page)
        time.sleep(0.8)
        
    remaining_rows = len(all_parsed_data) % 50
    if remaining_rows > 0:
        print(f"Saving the remaining {remaining_rows} rows.")
        save_progress(temp_file_path, all_parsed_data[-remaining_rows:], mode='a')
        all_parsed_data=[]
            
    print("All files saved")
            
    
if __name__ == "__main__":
    
    output_dir = "Armed_Forces_Tribunal_Judgements"
    main(URL, output_dir)
    
 
            











