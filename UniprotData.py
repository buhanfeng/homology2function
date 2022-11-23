import json
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import xmltodict
import Logger
import time
from libs import UniprotIDMappingAPI as uma



class UniprotData:
    def __init__(self):
        # TODO
        # initialize ID_FIELD by query https://rest.uniprot.org/configure/idmapping/fields
        pass

    # ******************* feature field *****************
    maxWaiting = 60 * 30
    ID_FIELD = None

    # ******************* method field *****************
    def GetIndividualEntry(self):
        test = 'https://rest.uniprot.org/uniprotkb/P12345.xml'
        request = urllib.request.Request(test)
        with urllib.request.urlopen(request) as response:
            res = response.read()
            soup = BeautifulSoup(res)
            cc = soup.find_all(type="function")
            print()
        return soup

    # Find allowable field in
    # https://www.uniprot.org/id-mapping or https://rest.uniprot.org/configure/idmapping/fields
    # deprecated
    def idMapping(self, ids, fr, to):
        url = 'https://rest.uniprot.org/idmapping/run'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'ids': ids,
            'from': fr,
            'to': to}
        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')
        re = urllib.request.Request(url=url, data=data, headers=headers)
        response = urllib.request.urlopen(re)
        content = response.read()
        content = str(content, 'utf-8')
        content = json.loads(content)
        jobID = content['jobId']
        print('Executing uniprot id mapping. Job ID:' + jobID)
        statusUrl = r'https://rest.uniprot.org/idmapping/status/$jobID'.replace('$jobID', jobID)
        resultsUrl = r'https://rest.uniprot.org/idmapping/results/$jobID'.replace('$jobID', jobID)
        # streamUrl = 'https://rest.uniprot.org/idmapping/stream/$jobID'.replace('$jobID', jobID)
        waitingTime = 0
        while True:
            time.sleep(2)
            waitingTime += 5
            req = urllib.request.Request(url=statusUrl)
            response = urllib.request.urlopen(req)
            content = response.read()
            content = str(content, 'utf-8')
            content = json.loads(content)
            if content['jobStatus'] == 'FINISHED':
                print('Mapping finished.')
                break
            else:
                if waitingTime > self.maxWaiting:
                    print('exceeding max waiting time, uniprot mapping halt!')
                    break
                else:
                    print('Mapping ...')
        req = urllib.request.Request(url=resultsUrl)
        response = urllib.request.urlopen(req)
        content = response.read()
        content = str(content, 'utf-8')
        content = json.loads(content)
        return content

    def idMapping2(self, ids, from_db, to_db):
        job_id = uma.submit_id_mapping(
            from_db=from_db, to_db=to_db, ids=ids
        )
        if uma.check_id_mapping_results_ready(job_id):
            link = uma.get_id_mapping_results_link(job_id)
            results = uma.get_id_mapping_results_search(link)
            # Equivalently using the stream endpoint which is more demanding
            # on the API and so is less stable:
            # results = get_id_mapping_results_stream(link)
            return results


if __name__ == '__main__':
    # uniprotData = UniprotData()
    # uniprotData.IDMapping()
    pass
