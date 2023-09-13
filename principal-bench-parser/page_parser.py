import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import List, Tuple
import datetime

import re
from bs4 import BeautifulSoup


def extract_case_number_registration_date(row_html: str) -> Tuple[str, str]:
    try:
        soup = BeautifulSoup(row_html, 'html.parser')
        case_number_with_reg_date = soup.h3.text.strip()
        case_number, reg_date_str = re.match(r'(.+?)\s+\(Regn Date:\s*(.+?)\s*\)', case_number_with_reg_date).groups()
        reg_date = datetime.datetime.strptime(reg_date_str, '%d-%m-%Y').date()
        return case_number, reg_date.strftime('%Y-%m-%d')
    except AttributeError:
        raise ValueError(f'Could not parse case number and registration date from row: {row_html}')

def extract_respondent(row_html: str) -> str:
    try:
        soup = BeautifulSoup(row_html, 'html.parser')
        respondent = soup.find('span', {'style': 'color:blue'}).find_next('span', {'style': 'color:blue'}).text
        return respondent
    except AttributeError:
        raise ValueError('Could not parse respondent from row: {}'.format(row_html))

def extract_mode(row_html: str) -> str:
    """
    Extracts the mode from the given HTML row.
    """
    try:
        soup = BeautifulSoup(row_html, 'html.parser')
        mode = soup.find('span', string='Status :').find_next_sibling('span').text.strip()
        return mode
    except AttributeError:
        raise ValueError('Could not parse mode from row: {}'.format(row_html))
        
def extract_extract_judgement_date(p):
    
    try:
        judgement_date = p.find("span", style="color:blue", text=re.compile(r"\d{2}-\d{2}-\d{4}"))
        if judgement_date:
            judgement_date = judgement_date.get_text(strip=True).replace(';', '')
            return judgement_date
    except AttributeError:
        raise ValueError('Could not parse judgement from row')
        
def extract_petitioner(p):
    
    vs_span = p.find("span", style="color:red;font-weight:bold")
    if vs_span:
        petitioner = vs_span.find_previous("span", style="color:blue")

        try:
            petitioner = petitioner.get_text(strip=True)
            return petitioner
        except AttributeError:
            raise ValueError('Could not parse petitioner from row')
            
        
def extract_span_element(p):
    
    span_elements = p.find_all("span", style="color:blue")
    mode = span_elements[3].get_text(strip=True)
    petitioner_advocate = span_elements[5].get_text(strip=True)
    respondent_advocate = span_elements[6].get_text(strip=True)
    subject_full = span_elements[7].get_text(strip=True)
    subject=subject_full.split('.')[-1]
    
    return mode,petitioner_advocate,respondent_advocate,subject

def extract_url(p):
    pdf_link = p.find("a", href=re.compile(r"/assets/judgement/"))
    if pdf_link:
        pdf_url = f"https://www.aftdelhi.nic.in{pdf_link['href']}"
    else:
        pdf_url=""
        
    return pdf_url

def parse_row(result):
    case_number,registration_date=extract_case_number_registration_date(str(result))
    respondent=extract_respondent(str(result))
            
    td = result.find("div", class_="td")
    if td:
        dept_text=td.get_text()
        p=td.find("p")
                
        if p:
            judgement_date=extract_extract_judgement_date(p)
            petitioner=extract_petitioner(p)
            mode,petitioner_advocate,respondent_advocate,subject=extract_span_element(p)

            pdf_url=extract_url(p)
                 
    # Append the extracted information to the data list
    return {
        'case_number': case_number,
        'registration_date': registration_date,
        'respondent': respondent,
        'judgement_date': judgement_date,
        'petitioner': petitioner,
        'mode': mode,
        'petitioner_advocate': petitioner_advocate,
        'respondent_advocate': respondent_advocate,
        'subject': subject,
        'pdf_url': pdf_url                               
    }



    