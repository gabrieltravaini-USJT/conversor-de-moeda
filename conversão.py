import os
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
from pandas.io.json import json_normalize
import json
from decimal import Decimal
import datetime as dt
import numpy as np
from datetime import timedelta


os.system('cls')

def consultaCotacao (dataIniCotacao,dataFimCotacao):
    url_api = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial='" + dataIniCotacao + "',dataFinalCotacao='" + dataFimCotacao + "')?$format=json"

    resp = requests.get(url_api)

    df_dolar = pd.json_normalize(json.loads(resp.text)['value'])

    df_dolar.rename(columns = {'cotacaoCompra': 'BuyPrice', 'cotacaoVenda': 'SellPrice', 'dataHoraCotacao': 'ExchangeDate'}, inplace = True)

    return df_dolar


today = dt.datetime.now().isoformat()
today = pd.to_datetime(today)
tomorrow = today + timedelta(days=1)
tomorrow  = tomorrow.strftime("%m-%d-%Y")
today = today.strftime("%m-%d-%Y")

func = input('Tecle 1 para valor de dolar histórico, e 2 para conversão: ')

if func == '1':
    dataIniCotacao = input('desde quando você quer consultar? (use formato "MM-DD-AAAA") ')
    print('---------------------------------------------------------------------------')
    dataFimCotacao = tomorrow

    df_dolar = consultaCotacao(dataIniCotacao,dataFimCotacao)

    print('tabela com as taxas de conversão do periodo solicitado:')
    print('-------------------------------------------------------------------------------------------------------------')
    print(df_dolar)

elif func =='2':
    dataIniCotacao = today
    dataFimCotacao = tomorrow

    df_dolar = consultaCotacao(dataIniCotacao,dataFimCotacao)
    
    cotacao_dolar = df_dolar.SellPrice.to_list()[0]
    qtd_dolares  = input('quantos dolares você quer comprar? ')
    valor_reais = cotacao_dolar * float(qtd_dolares)
    print ('a cotação do dolar hoje está em: R$'+str(cotacao_dolar))
    print('Para comprar USD'+ str(qtd_dolares)+', você precisa pagar R$'+ str(valor_reais))
