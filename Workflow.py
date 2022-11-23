"""
workflow
  check input
  check environment
  check duplication
  id mapping
  drawing function annotation
  merging
"""
import uuid
from ConfigContainer import ConfigContainer
from Logger import Logger
import Utils
import os
import pandas as pd
import numpy as np
from IDMapper import IDMapper
from TempRecord import TempRecord


class MainWorkflow:
    def __init__(self, configPath):
        self.configContainer = ConfigContainer(configPath)

    # ******************* feature field *****************
    configContainer = None
    params = None
    logger = None
    TEMP_PREFIX = 'temp_'
    workingPlace = None
    tempFile = None
    idMapper = IDMapper()
    tempRecord = None

    # ******************* method field *****************
    def run(self):
        self.checkInput()
        self.setEnv()
        self.IDMapping()
        self.drawAnnotation()

    def checkInput(self):
        self.params = self.configContainer.globalConfig
        if not (self.params['workingPath'] and self.params['projectName'] and self.params['identityTable']):
            Utils.consoleLog('One or more required arguments has not been set properly, exit!')
            exit()
        elif not os.path.exists(self.params['workingPath']):
            Utils.consoleLog(self.params['workingPath'], 'is not exist, exit!')
            exit()
        elif not os.path.exists(self.params['identityTable']):
            Utils.consoleLog(self.params['identityTable'], 'is not exist, exit!')
            exit()
        if self.params['resume']:
            self.params.resume = False
        if not self.params['uniprotSetting']:
            self.params['uniprotSetting']['run'] = True
            self.params['uniprotSetting']['runMode'] = 'online'
        else:
            if self.params['uniprotSetting']['run'] and self.params['uniprotSetting']['runMode'] == 'local':
                if os.path.exists(self.params['uniprotSetting']['database']):
                    pass  # check files one by one
                else:
                    Utils.consoleLog('Local database is invalid, exit!')
                    exit()
        if not self.params['entrezSetting']:
            self.params['entrezSetting']['run'] = True
            self.params['entrezSetting']['runMode'] = 'online'
        else:
            if self.params['entrezSetting']['run'] and self.params['entrezSetting']['runMode'] == 'local':
                if os.path.exists(self.params['entrezSetting']['database']):
                    pass  # check files one by one
                else:
                    Utils.consoleLog('Local database is invalid, exit!')
                    exit()
        self.workingPlace = os.path.join(self.params['workingPath'], self.params['projectName'])

    def setEnv(self):
        if not os.path.exists(self.workingPlace):
            os.makedirs(self.workingPlace)
        self.logger = Logger(self.workingPlace)
        if self.params['resume']:
            for f in os.listdir(self.workingPlace):
                if self.TEMP_PREFIX in f:
                    self.tempFile = os.path.join(self.workingPlace, f)
                    self.logger.logging(self.logger.MES_TYPE.INFO, 'using files in', self.tempFile,
                                        'to resume the job.')
                    break
        else:
            name = self.TEMP_PREFIX + str(uuid.uuid4())
            self.tempFile = os.path.join(self.workingPlace, name)
            os.makedirs(self.tempFile)
            self.tempRecord = TempRecord(self.tempFile)

    def IDMapping(self):
        identityTable = pd.read_table(self.params['identityTable'])
        identityTable = identityTable.drop_duplicates()
        identityTable = identityTable.pivot(columns='TYPE', values='ID')
        idTable = identityTable.copy()
        # idTable = idTable.reindex(columns=IDMapper.SUPPORT_ID)
        # for i in IDMapper.SUPPORT_ID:
        #     if i not in list(identityTable):
        #         # idTable[i] = float('nan')
        #         app = pd.Series(np.repeat(float('nan'), idTable.shape[0]))
        #         idTable = pd.concat([idTable, app.to_frame()], axis=1, ignore_index=True)
        schedule = [('ENTREZ_PROTEIN_AC', 'ENTREZ_GENE_ID'),
                    ('ENTREZ_PROTEIN_AC', 'UNIPROT_ENTRY'),
                    ('UNIPROT_ENTRY', 'ENTREZ_PROTEIN_AC'),
                    ('UNIPROT_ENTRY', 'ENTREZ_GENE_ID')]
        for e in schedule:
            i, j = e[0], e[1]
            queryList = idTable[i][pd.notna(idTable[i])]
            queryList = queryList.drop_duplicates()
            mapTab = None
            if i == 'ENTREZ_PROTEIN_AC' and j == 'ENTREZ_GENE_ID':
                mapTab = self.idMapper.entrezProteinAc2entrezGeneID(queryList)
                mapTab = mapTab.rename(columns={'TO': 'ENTREZ_GENE_ID'})
                idTable = Utils.updateTable(idTable, mapTab, i, 'FROM', updateKey=None)
            elif i == 'ENTREZ_PROTEIN_AC' and j == 'UNIPROT_ENTRY':
                mapTab = self.idMapper.entrezProteinAc2uniprotRntry(queryList)
                idTable = Utils.updateTable(idTable, mapTab, i, 'FROM', updateKey={j: 'TO'})
            elif i == 'UNIPROT_ENTRY' and j == 'ENTREZ_PROTEIN_AC':
                mapTab = self.idMapper.uniprotRntry2entrezProteinAc(queryList)
                idTable = Utils.updateTable(idTable, mapTab, i, 'FROM', updateKey={j: 'TO'})
            elif i == 'UNIPROT_ENTRY' and j == 'ENTREZ_GENE_ID':
                mapTab = self.idMapper.uniprotRntry2entrezGeneID(queryList)
                idTable = Utils.updateTable(idTable, mapTab, i, 'FROM', updateKey={j: 'TO'})
        self.tempRecord.writeIdTable(idTable)
        return idTable

    def drawAnnotation(self, *idTable):
        idTable = pd.read_table(r'C:\Users\fbh\Desktop\AngelaLab\homology2function\workingPath\test1\temp_1b3999c4-f179-4c7c-87c2-70143585ce4a\ID_MAPPING')
        schedule = ['UNIPROT_ENTRY', 'ENTREZ_PROTEIN_AC', 'ENTREZ_GENE_ID']
        for s in schedule:
            queryList = idTable[s][pd.notna(idTable[s])]
            queryList = queryList.drop_duplicates()
            if s == 'UNIPROT_ENTRY':
                mapTab = self.idMapper.drawUniprotAnnotation(queryList)
                idTable = Utils.updateTable(idTable, mapTab, s, 'FROM', updateKey=None)
            elif s == 'ENTREZ_PROTEIN_AC':
                mapTab = self.idMapper.drawProteinAnnotation(queryList)
                idTable = Utils.updateTable(idTable, mapTab, s, 'FROM', updateKey=None)
            elif s == 'ENTREZ_GENE_ID':
                mapTab = self.idMapper.drawGeneAnnotation(queryList)
                idTable = Utils.updateTable(idTable, mapTab, s, 'FROM', updateKey=None)

    def merging(self):
        pass


c = r'C:\Users\fbh\Desktop\AngelaLab\homology2function\data\config.yml'
mw = MainWorkflow(c)
mw.run()
