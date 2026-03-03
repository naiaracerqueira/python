import gspread
from google.oauth2 import service_account
import os
import pandas as pd


def login_sheet():
    PATH = os.path.dirname(os.path.realpath(__file__))
    cred_loc = PATH+"/credentials.json"
    credentials = service_account.Credentials.from_service_account_file(cred_loc)
    scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/spreadsheets",
                                                  "https://www.googleapis.com/auth/drive"])
    gc = gspread.authorize(scoped_credentials)
    return gc


def leitor_sheet(documento, aba):
    gc = login_sheet()
    planilha = gc.open(documento)
    aba = planilha.worksheet(aba)
    dados = aba.get_all_records()
    df = pd.DataFrame(dados)
    return df


def escritor_sheet(documento, aba, valor):
    gc = login_sheet()
    planilha = gc.open(documento)
    planilha = planilha.worksheet(aba)
    planilha.append_row(valor, value_input_option='USER_ENTERED')


def limpa_sheet(documento, aba):
    gc = login_sheet()
    planilha = gc.open(documento)
    planilha = planilha.worksheet(aba)
    planilha.clear()


def deleta_linhas(documento, aba, start_index, end_index):
    gc = login_sheet()
    planilha = gc.open(documento)
    planilha = planilha.worksheet(aba)
    planilha.delete_rows(start_index, end_index)
