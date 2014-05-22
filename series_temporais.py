# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:14:43 2013

@author: jmrosal
"""

import suds
import xml.dom.minidom as minidom
import pandas as pd
import main_series
from datetime import datetime

url = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl'
client = suds.client.Client(url)
TODAY = (datetime.today()).strftime('%d/%m/%Y')


def get_xml(ini=TODAY, end=TODAY, *series):
    '''(string, string, tuple)-> xml_doc
    list populated by strings with the numbers of the series from BCB
    time series webservice. ini is the begining and end is the end of
    the observation. Returns an xml_doc with the information'''

    assert type(ini) == str
    assert type(end) == str
    assert datetime.strptime(ini, '%d/%m/%Y') <= \
        datetime.strptime(end, '%d/%m/%Y')

    codigo = []
    for s in series:
        if (type(s) == long):
            codigo.append(long(s))
        elif (type(s) == str):
            codigo.append(main_series.main_series[s])

    response = client.service.getValoresSeriesXML(codigo, ini, end)
    return minidom.parseString(response.encode('utf-8'))


def handle_element_series(element_series):
    '''(dom element)-> dict
    takes a single dom element SERIES and return a dictionary with keys,value:
    ('id', string), ('date', list) and ('value',list)
    '''
    series = {}
    series['id'] = element_series.attributes['ID'].value
    series['obs'] = {}
    series['obs']['date'] = []
    series['obs']['value'] = []
    seq = (node for node in element_series.childNodes if node.nodeType == 1)
    for node in seq:
        data = node.childNodes.item(1).firstChild.wholeText
        valor = node.childNodes.item(3).firstChild.wholeText
        series['obs']['date'].append(data)
        series['obs']['value'].append(valor)
    return series


def get_series(xml_doc):
    '''(xml.dom) -> dict
    take an xml response from a request to BCB's time series webservices, and
    returns a dict of date and values of the requested series.
    '''
    mult_series = []
    for serie in xml_doc.getElementsByTagName('SERIE'):
        single_series = handle_element_series(serie)
        mult_series.append(single_series)
    return mult_series


def series_dict(ini, end, *series):
    tree = get_xml(ini, end, *series)
    return get_series(tree)


def data_frame(start=TODAY, end=TODAY, *series):
    '''(dict)-> DataFrame
    takes a dictionary with series' information and return it on pandas
    DataFrame format'''
    dict_series = series_dict(start, end, *series)
    data = {}
    for s in dict_series:
        data[s['id']] = map(float, s['obs']['value'])
    return pd.DataFrame(data, index=pd.to_datetime(s['obs']['date'],
                                                   dayfirst='TRUE'))


if __name__ == '__main__':
#    resp = data_frame('01/01/1996', long(1253), long(1253))
    #    print resp
    resp = data_frame('01/01/1996', '01/10/2014', long(1253))
    print resp
