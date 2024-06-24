# -*- coding: utf-8 -*-
"""Bot_UPE

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KS8euNg_sLHLNpEcIKhvVYDsvNiyk_hf

# **Bot para coleta dos editais**
"""

!pip install Selenium
!pip install webdriver_manager
import requests
from bs4 import BeautifulSoup
import time
import os
import pickle
import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.colab import drive
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:     #Isso é coisa da biblioteca para fazer download... Tou aprendendo ainda, mas tem doc!
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def file_exists_locally(filepath):
    return os.path.exists(filepath)

def scrape_site_1(url, download_folder):
    try:
        response = requests.get(url, timeout=60)   #Tenta conectar no servidor, se passar x tempo segundos e não conectar ele encerra e vai para a próxima!
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        links = soup.find_all('a', class_='wpfd_downloadlink', href=True) #Tenta encontrar todos os links de download com a classe 'wpfd_downloadlink'

        for link in links:
            href = link['href']

            if href.endswith('.pdf'):
                filename = href.split('/')[-1]
                local_path = os.path.join(download_folder, filename)

                if not file_exists_locally(local_path):     # verifica se tem ou não tem o arquivo no drive já
                    download_file(href, local_path)
                    print(f"Downloaded {local_path}")

                else:
                    print(f"File {filename} already exists locally")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")

def scrape_site_2(url, download_folder):
    try:
        response = requests.get(url, timeout=10)  #Tenta conectar no servidor, se passar x tempo segundos e não conectar ele encerra e vai para a próxima!
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        links = soup.find_all('span', class_='avia_iconbox_title')  #Tenta encontrar todos os links que contêm a classe 'avia_iconbox_title'

        for link in links:
            parent = link.find_parent('a', href=True)

            if parent:
                href = parent['href']

                if href.endswith('.pdf'):
                    filename = href.split('/')[-1]
                    local_path = os.path.join(download_folder, filename)

                    if not file_exists_locally(local_path):     # verifica se tem ou não tem o arquivo no drive já
                        download_file(href, local_path)
                        print(f"Downloaded {local_path}")

                    else:
                        print(f"File {filename} already exists locally")

    except requests.exceptions.RequestException as e:

        print(f"Error fetching {url}: {e}")

def scrape_site_3(url, download_folder):
    try:
        response = requests.get(url, timeout=60) #Tenta conectar no servidor, se passar x tempo segundos e não conectar ele encerra e vai para a próxima!
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        links = soup.find_all('a', href=True)  #Tenta encontrar todos os links que contêm um href e têm um span com o texto "Chamada"

        for link in links:
            if link.find('span') and 'Chamada' in link.text:
                href = link['href']

                if href.endswith('.pdf'):
                    filename = href.split('/')[-1]
                    local_path = os.path.join(download_folder, filename)

                    if not file_exists_locally(local_path):     # verifica se tem ou não tem o arquivo no drive já
                        download_file(href, local_path)
                        print(f"Downloaded {local_path}")

                    else:
                        print(f"File {filename} already exists locally")

    except requests.exceptions.RequestException as e:

        print(f"Error fetching {url}: {e}")

def monitor_sites(folders):    #Isso aqui é para ficar verificando quando a gente deixar rodando, pode arrancar fora se a gente não for deixar essa aplicação rodando full num server!
    while True:
        for url, folder_name, scraper_function in folders:
            download_folder = os.path.join(base_download_folder, folder_name)
            os.makedirs(download_folder, exist_ok=True)
            scraper_function(url, download_folder)
        time.sleep(300) # <--- Esperar x tempo antes de verificar novamente

#variáveis contendo os sites = Input!!!
site_scrapers = [
    ('https://www.secti.pe.gov.br/editais/', 'secti', scrape_site_1),
    ('https://www.facepe.br/editais/todos/?c=todos', 'facepe', scrape_site_2),
    ('http://memoria2.cnpq.br/web/guest/chamadas-publicas', 'cnpq', scrape_site_3)
]

base_download_folder = '/content/drive/MyDrive/Engenharia de Software'  #Pasta onde os arquivos serão salvos -- Inicialmente, depois a gente joga para um banco!!!
os.makedirs(base_download_folder, exist_ok=True)

monitor_sites(site_scrapers) #Mostra o que ta rolando nas conexões!