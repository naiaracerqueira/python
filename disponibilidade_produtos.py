from google.oauth2 import service_account
import gspread
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import time
# gera classe que sqlalchemy usa, que gerencia as coisas:
from sqlalchemy.ext.declarative import declarative_base
# sqlalchemy: orm x core 
# sessionmaker: mexe com a sessão:
from sqlalchemy.orm import sessionmaker
# básicos para montar tabela:
from sqlalchemy import *
# interface de mysql para python:
import pymysql


#### url para conectar ao banco da komuh: ####
K_HOST = "34.193.166.110"
K_USUARIO = "datastudio"
K_PASSWORD = "h4a5ti%GR#EvDbn$3"
K_BASE = "itatiaia_komuh"

banco_komuh = f"mysql+pymysql://{K_USUARIO}:{K_PASSWORD}@{K_HOST}/{K_BASE}"
engine_komuh = create_engine(banco_komuh)
Session_komuh = sessionmaker(bind=engine_komuh)
session_komuh = Session_komuh()

Base = declarative_base()
metadata = MetaData()


def login():
    PATH = os.path.dirname(os.path.realpath(__file__))
    cred_loc = PATH+"/credenciaisGcloudPerformanceKomuh.json"
    credentials = service_account.Credentials.from_service_account_file(cred_loc)
    scoped_credentials = credentials.with_scopes(["https://spreadsheets.google.com/feeds", 
                                                  "https://www.googleapis.com/auth/drive"])
    gc = gspread.authorize(scoped_credentials)
    return gc


def leitor():
    #objeto autenticado:
    gc = login()
    planilha = gc.open("Itatiaia - Dataset - Disponibilidade de Produtos")
    aba = planilha.worksheet("urls")
    dados = aba.get_all_records()
    df = pd.DataFrame(dados)
    lista = list(df.iloc[:,0])
    return lista
 

# def escritor(valor):
#     gc = login()
#     planilha = gc.open('Itatiaia - Dataset - Disponibilidade de Produtos')
#     planilha = planilha.worksheet('Dados')
#     planilha.append_row(valor, value_input_option='USER_ENTERED')


def pega_disponibilidade(url):
    try:
        r = requests.get(url)
        status_code = r.status_code
        html_page = r.content
        soup = bs(html_page, "lxml")
        
        if soup.find(text="Item indisponível no momento"):
            disponibilidade = "Item Indisponível"
            
        elif status_code == 404:
            disponibilidade = "Página não Encontrada"
        else:
            disponibilidade = "OK"
    except:
        disponibilidade = "Problema na coleta"
        pass 
    return disponibilidade


def pega_produto(url):
    try:
        r = requests.get(url)
        html_page = r.content
        soup = bs(html_page, "lxml")
        produto = soup.find('h1', attrs={'class':'product-name'})
        produto = produto.text
    except:
        produto = "Produto não identificado"
    return produto


def pega_preco(url):
    try:
        r = requests.get(url)
        html_page = r.content
        soup = bs(html_page, "lxml")  
        if soup.find('span', attrs={'class':'price final-price-grouped'}):
            preco0 = soup.find('span', attrs={'class':'price final-price-grouped'}).text
            preco1 = re.sub('^(..)', '', preco0)
            preco2 = re.sub('\.', '', preco1)
            preco = re.sub(',', '.', preco2)
        elif len(soup.find_all('span', attrs={'class':'price'})) > 1:
            preco0 = soup.find_all('span', attrs={'class':'price'})[1].text
            preco1 = re.sub('\n|\s','', preco0)
            preco2 = re.sub('^(..)', '', preco1)
            preco3 = re.sub('\.', '', preco2)
            preco = re.sub(',', '.', preco3)
        else:
            preco0 = soup.find('span', attrs={'class':'price'}).text
            preco1 = re.sub('^(..)', '', preco0)
            preco2 = re.sub('\.', '', preco1)
            preco = re.sub(',', '.', preco2)
    except:
        preco = ''
    return preco


### Unir as tabelas ###
class DisponibilidadeProdutos(Base):
    __tablename__ = "disponibilidade_produto"
    table_id = Column('table_id', Integer, primary_key=True, autoincrement=True)
    data = Column('data_insert', DateTime)
    produto = Column('produto', String(200))
    disponibilidade = Column('disponibilidade', String(25))
    preco = Column('preco', String(15), nullable=True)
    url = Column('url', String(200))

    # self pega tudo que é da classe:
    def __repr__(self):
        return self.table_id

    def cria_tabela(self):
        Base.metadata.create_all(engine_komuh, checkfirst=True)

    # def le_tabela(self):
    #     dados_da_tabela = session_komuh.query(TransacoesUnidas).all()
    #     return dados_da_tabela

    def escreve_tabela(self):
        lista = leitor()

        for url in lista:
            disponibilidade = pega_disponibilidade(url)
            preco = pega_preco(url)
            produto = pega_produto(url)

            entrada = DisponibilidadeProdutos(data = datetime.now(),
                                              produto = produto,
                                              disponibilidade = disponibilidade,
                                              preco = preco,
                                              url=url
            )
            session_komuh.add(entrada)
            session_komuh.commit()


# def escreve_dados(df):
#     now = str(datetime.now())
#     #roda em cada linha do dataframe da aba
#     for linha in range(len(df)):
#         url = df.iloc[linha,0]
#         disp = pega_disponibilidade(url)
#         preco = pega_preco(url)
#         produto = pega_produto(url)
#         lista = [now, url, produto, disp, preco]
#         print(lista)
#         time.sleep(2)
#         escritor(lista)


if __name__ == "__main__":   
    disp = DisponibilidadeProdutos()
    disp.cria_tabela()
    disp.escreve_tabela()

