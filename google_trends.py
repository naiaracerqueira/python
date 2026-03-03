import pandas as pd
import os
import time

# Pytrends
from pytrends.request import TrendReq

# Sheets
import gspread
from google.oauth2 import service_account


def login():
    PATH = os.path.dirname(os.path.realpath(__file__))
    cred_loc = PATH+"/credentials.json"
    credentials = service_account.Credentials.from_service_account_file(cred_loc)
    scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/analytics.readonly",
                                                  "https://spreadsheets.google.com/feeds", 
                                                  "https://www.googleapis.com/auth/drive"])
    gc = gspread.authorize(scoped_credentials)
    return gc


def tendencias():
    #cria o objeto
    pytrend = TrendReq(hl='pt-BR')
    #seta as palavras chave e 12 meses de dados:
    pytrend.build_payload(kw_list=["cozinhas", "geladeira"], timeframe='today 1-m', geo = 'BR')
    interesse = pytrend.interest_over_time()
    int_sheet = interesse.reset_index()
    #transformando tudo em string
    int_sheet['date'] = int_sheet['date'].dt.strftime('%Y/%m/%d')
    int_sheet['cozinhas'] = int_sheet['cozinhas'].astype(str)
    int_sheet['geladeira'] = int_sheet['geladeira'].astype(str)
    #pegando último valor e guardando em lista
    lista = list(int_sheet.iloc[-1,:3])
    return lista


def escritor(valor):
    gc = login()
    planilha = gc.open('Arquivo')
    planilha = planilha.worksheet('Aba')
    planilha.append_row(valor, value_input_option='USER_ENTERED')


if __name__ == "__main__":
    lista = tendencias()
    escritor(lista)

