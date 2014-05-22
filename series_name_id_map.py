
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:14:43 2013

@author: jmrosal
#Falta fazer:
1. Fazer write para salvar no disco rígido.

"""
import suds
import json
from datetime import datetime

url = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl'
client = suds.client.Client(url)
TODAY = (datetime.today()).strftime('%d/%m/%Y')
LAST = 12366


def get_series(serie_ini, serie_end):
    '''(long)-> dict
    Inputs the code of the series and series in list format'''
    serie = serie_ini
    meta = {}

    for s in range(serie_ini, serie_end+1):
        try:
            resp = client.service.getUltimoValorVO(serie)
            date_ini = form_data(resp, "Inicio")
            data_end = form_data(resp, "Fim")
            meta[serie] = {}
            meta[serie]['Disponibilidade'] = "T"
            meta[serie]['nome'] = resp['nomeCompleto'].encode('utf-8')
            meta[serie]['freq'] = resp['periodicidadeSigla'].encode('utf-8')
            meta[serie]['unidade'] = resp['unidadePadrao'].encode('utf-8')
            meta[serie]['dataInicio'] = date_ini
            meta[serie]['dataFim'] = date_end
        except (BaseException):
            meta[serie] = {}
            meta[serie]['Disponibilidade'] = "F"
        serie += 1
    return meta


def form_date(dic, post):
    if post == "Inicio":
        dia = str(dic["dia"+post])
        mes = str(dic["mes"+post])
        ano = str(dic["ano"+post])
    else:
        dia = str(dic["ultimoValor"]["dia"])
        mes = str(dic["ultimoValor"]["mes"])
        ano = str(dic["ultimoValor"]["ano"])
    return dia+'/'+mes+'/'+ano
    

def save_meta(serie_ini, serie_end):
    '''save metadata from seires ranging from serie_ini to serie_end
    onto the hard disk'''
    resp = get_series(serie_ini, serie_end)
    f = open("meta.json", "w")
    json.dump(resp, f)
    f.close()


def return_meta(serie):
    '''return metadada from meta file'''
    f = open("meta.json", "r")
    parser = json.load(f)
    f.close()
    return parser[str(serie)]
    

save_meta(long(1), long(2))
print json.dumps(return_meta(long(1)), indent=1)


