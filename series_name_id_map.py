# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:14:43 2013

@author: jmrosal



"""
import suds
import json

url = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl'
client = suds.client.Client(url)
LAST = 12366


def get_series(serie_ini, serie_end):
    '''(long)-> dict
    Inputs the code number of the series and returns the meta
    data in a dictionary format'''
    serie = serie_ini
    meta = {}

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

    for s in range(serie_ini, serie_end+1):
        try:
            resp = client.service.getUltimoValorVO(serie)
            date_ini = form_date(resp, "Inicio")
            date_end = form_date(resp, "Fim")
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


def save_meta(serie_ini, serie_end):
    '''save metadata from series ranging from serie_ini to serie_end
    onto the hard disk'''
    resp = get_series(serie_ini, serie_end)
    f = open("meta.json", "w")
    json.dump(resp, f)
    f.close()


def fetch_meta(serie):
    '''fetch metadada from meta file'''
    f = open("meta.json", "r")
    parser = json.load(f)
    f.close()
    try:
        par = parser[str(serie)]
        return par
    except (KeyError):
        print "serie inexistente"


