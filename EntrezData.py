import json
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import xmltodict
import Logger
import time
import requests


class EntrezData:
    def __init__(self):
        pass

    # ******************* feature field *****************
    maxWaiting = 60 * 30
    maxFetch = 500
    maxSearch = 10
    urlBase = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'

    # ******************* method field *****************
    # def eSearch(self):
    #     req = urllib.request.Request(url=url, data=data, headers=headers)
    #     response = urllib.request.urlopen(req)

    def eFetch(self):
        pass

    def getProtein(self):
        query = 'chimpanzee[orgn]+AND+biomol+mrna[prop]'
        # assemble the esearch URL
        sup = "esearch.fcgi?db=protein&term=$query&usehistory=y".replace('$query', query)
        url = '/'.join([self.urlBase, sup])
        # post the esearch URL
        req = urllib.request.Request(url=url)
        response = urllib.request.urlopen(req)
        content = response.read()
        content = str(content, 'utf-8')
        return content

    def eLink(self, dbfrom, db, ids):
        API_URL = '/'.join([self.urlBase, 'elink.fcgi'])
        request = requests.post(
            f"{API_URL}",
            data={"dbfrom": dbfrom, "db": db, 'idtype': 'acc', "id": ids}
        )
        di = xmltodict.parse(request.text)
        return di


if __name__ == '__main__':
    entrezData = EntrezData()
    entrezData.getGenbank()
