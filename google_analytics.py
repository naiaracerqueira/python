import login
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import login
import gspread
import lidaSheets
import time

idItatiaia = "XXXXXXXXXXXXXXX"

#Cria a query a ser usada
def report():
    analytics = login.analytics()
    return analytics.reports().batchGet(
        body={
        'reportRequests': [
        {
            'viewId': idItatiaia,
            'dateRanges': [{'startDate': '60daysAgo', 'endDate': 'Yesterday'}],
            'metrics': [{'expression': 'ga:transactionRevenue'}],
            'dimensions': [{"name":"ga:date"},{'name': 'ga:transactionId'},{'name': 'ga:sourceMedium'}],
            'pageSize' : 100000
        }]
        }
    ).execute()

#executa e coleta a resposta
def resposta(query):
    listaResposta = []
    for relatorio in query.get("reports"):
        cabecalhoColuna = relatorio.get('columnHeader')
        cabecalhoDimensoes = cabecalhoColuna.get("dimensions")
        cabecalhoMetricas = cabecalhoColuna.get("metricHeader").get("metricHeaderEntries")
        for linhasRelatorio in relatorio.get('data').get('rows'):
            linhaDimensoes = linhasRelatorio.get('dimensions')
            linhaMetricas = linhasRelatorio.get('metrics')
            resposta = [str(linhaDimensoes[0]),str(linhaDimensoes[1]), str(linhaDimensoes[2])]
            listaResposta.append(resposta)
        return listaResposta


def reportOrigemMidia():
    analytics = login.analytics()
    return analytics.reports().batchGet(
        body={
        'reportRequests': [
        {
            'viewId': idItatiaia,
            'dateRanges': [{'startDate': '60daysAgo', 'endDate': 'today'}],
            'metrics': [{'expression': 'ga:transactionRevenue'}],
            'dimensions': [{"name":"ga:date"},{'name': 'ga:transactionId'},{'name': 'ga:sourceMedium'}],
            'filters':[{'name':'ga:transactionId'},{'operator':'=@'},{'expression':'000000511'}]
        }]
        }
    ).execute()



def respostaOrigemMidia(query):
    listaResposta = []
    for relatorio in query.get("reports"):
        cabecalhoColuna = relatorio.get('columnHeader')
        cabecalhoDimensoes = cabecalhoColuna.get("dimensions")
        cabecalhoMetricas = cabecalhoColuna.get("metricHeader").get("metricHeaderEntries")
        for linhasRelatorio in relatorio.get('data').get('rows'):
            linhaDimensoes = linhasRelatorio.get('dimensions')
            linhaMetricas = linhasRelatorio.get('metrics')
            resposta = [str(linhaDimensoes[0]),str(linhaDimensoes[1]), str(linhaDimensoes[2])]
            listaResposta.append(resposta)
        return listaResposta


if __name__ == '__main__':
    query = report()
    listaAnalytics = analytics.resposta(query)
    # dfAnalytics = pd.DataFrame(listaAnalytics)
    # saida = reportOrigemMidia()
    print(query)
