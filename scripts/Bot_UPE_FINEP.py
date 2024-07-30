#!/usr/bin/env python
# coding: utf-8

# # **Bot para coleta dos editais**

# In[2]:


get_ipython().system('pip install webdriver_manager')
get_ipython().system('pip install unidecode')
import requests
import time
from bs4 import BeautifulSoup
import time
import os
import pickle
import requests
import re
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from unidecode import unidecode


# In[3]:


class BotAPI:
    def __init__(self, base_url, username, senha):
        self.base_url = base_url
        self.username = username
        self.senha = senha
        self.session = requests.Session()

    def login(self):
        url = f"{self.base_url}/upe/usuario/login"
        payload = {
            "login": self.username,
            "senha": self.senha
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = self.session.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Login bem-sucedido!")
        else:
            print(f"Falha no login. Status code: {response.status_code}")
            print("Resposta:", response.text)
        return response.status_code == 200

    def criar_edital(self, nome, data_publicacao):
        url = f"{self.base_url}/upe/edital"
        payload = {
            "nome": nome,
            "dataPublicacao": data_publicacao,
            "idUsuario": 1,  # Usando ID de usuário 1
            "idOrgaoFomento": 2  # Finep
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = self.session.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            print("Edital criado com sucesso!")
            return response.json()  # Retorna os detalhes do edital criado
        else:
            print(f"Falha ao criar edital. Status code: {response.status_code}")
            print("Resposta:", response.text)
        return None

    def adicionar_pdf(self, id_edital, file_path):
        url = f"{self.base_url}/upe/edital/inserir/{id_edital}/pdf"
        files = {
            'edital_pdf': (os.path.basename(file_path), open(file_path, 'rb'), 'application/pdf')
        }
        response = self.session.post(url, files=files)
        if response.status_code == 200:
            print("PDF adicionado com sucesso!")
        else:
            print(f"Falha ao adicionar PDF. Status code: {response.status_code}")
            print("Resposta:", response.text)

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def file_exists_locally(filepath):
    return os.path.exists(filepath)

def extract_publication_date(soup):
    date_td = soup.find('td', string=lambda text: text and '/' in text)
    if date_td:
        return date_td.get_text(strip=True)
    return None

def extract_pdf_links(soup):
    pdf_links = []
    pdf_elements = soup.find_all('a', href=True)
    for element in pdf_elements:
        if element['href'].endswith('.pdf'):
            pdf_links.append(element['href'])
    return pdf_links

def sanitize_folder_name(name):
    name = name.replace('/', '-')
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', ' ', name)
    name = name.strip()
    return name

def scrape_finep_site(base_url, start, bot_api):
    try:
        while True:
            page_url = f"{base_url}{start}"
            print(f"Fetching page: {page_url}")
            response = requests.get(page_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            post_links = soup.find_all('a', href=True)
            for post_link in post_links:
                if '/chamadas-publicas/chamadapublica/' in post_link['href']:
                    post_url = f"http://www.finep.gov.br{post_link['href']}"
                    print(f"Processing URL: {post_url}")

                    post_response = requests.get(post_url, timeout=10)
                    post_response.raise_for_status()
                    post_soup = BeautifulSoup(post_response.content, 'html.parser')

                    publication_date = extract_publication_date(post_soup)
                    if publication_date:
                        publication_date = datetime.strptime(publication_date, "%d/%m/%Y").strftime("%d/%m/%Y %H:%M:%S")
                    else:
                        publication_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                    pdf_links = extract_pdf_links(post_soup)
                    print(f"Found {len(pdf_links)} PDF links for {post_url}")

                    for pdf_url in pdf_links:
                        if not pdf_url.startswith('http'):
                            full_pdf_url = f"http://www.finep.gov.br{pdf_url}"
                        else:
                            full_pdf_url = pdf_url

                        pdf_filename = pdf_url.split('/')[-1]
                        local_path = pdf_filename

                        if not file_exists_locally(local_path):
                            print(f"Downloading {full_pdf_url} to {local_path}")
                            download_file(full_pdf_url, local_path)
                            print(f"Downloaded {local_path}")

                            # Use the name of the PDF file for the name of the edital
                            pdf_name = os.path.splitext(pdf_filename)[0]
                            nome_edital = sanitize_folder_name(pdf_name)

                            # Criar edital e adicionar PDF
                            edital_info = bot_api.criar_edital(nome_edital, publication_date)
                            if edital_info:
                                bot_api.adicionar_pdf(edital_info['id'], local_path)
                                os.remove(local_path)  # Remove the file after posting
                            else:
                                print(f"Failed to create edital for {nome_edital}")

            start = str(int(start) + 1)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {base_url}: {e}")

def monitor_sites(folders, bot_api):
    while True:
        for idx, (base_url, scraper_function, start) in enumerate(folders, start=1):
            print(f"Starting scraping for page {idx}: {base_url}{start}")
            scraper_function(base_url, start, bot_api)
        time.sleep(60)

# Configurações do bot
base_url = "https://projetoeditaisback.onrender.com"
username = "bot"
senha = "12345678"

# Criando uma instância do bot
bot_api = BotAPI(base_url, username, senha)

# Realizar login
if bot_api.login():
    # URLs para o scraping, com o número de página dinâmico
    site_scrapers = [
        ('http://www.finep.gov.br/chamadas-publicas/chamadaspublicas?pchave=&situacao=&d1=&d2=&task=&boxchecked=0&filter_order=ordering&filter_order_Dir=asc&2462e9fe565798ce94b783db71fbb68f=1&start=', scrape_finep_site, '0')
    ]

    # Iniciar monitoramento dos sites
    monitor_sites(site_scrapers, bot_api)

