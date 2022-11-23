import os
from threading import Lock
import Utils
import pandas as pd


class TempRecord:
    def __init__(self, path):
        self.root = path

    # ******************* feature field *****************
    root = None
    ID_MAPPING_SUB_PATH = 'ID_MAPPING'
    ID_TABLE_FILE_NAME = 'ID_TABLE'

    # ******************* method field *****************
    def writeIdTable(self, tab):
        fName = os.path.join(self.root, self.ID_MAPPING_SUB_PATH)
        tab.to_csv(path_or_buf=fName, sep='\t')





