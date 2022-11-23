"""
This Class control IDMapping business, which is one of the core component of the tools.
  to be specific, it cover below operation:
1) control batch size
2) control searching method according to configuration file
3) parsing return from data access API

"""

from EntrezData import EntrezData
from UniprotData import UniprotData
import pandas as pd

class IDMapper:
    # ***************** singleton ****************
    _instance = None

    def __new__(cls, *args, **kw):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IDMapper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.entrezData = EntrezData()
        self.uniprotData = UniprotData()

    # ******************* feature field *****************
    entrezData = None
    uniprotData = None
    SUPPORT_ID = ['ENTREZ_GENE_ID', 'ENTREZ_PROTEIN_AC', 'UNIPROT_ENTRY']

    # ******************* method field *****************
    # base on uniprot idmapping  service
    def uniprotRntry2entrezProteinAc(self, tab):
        ids = tab.array
        ret = self.uniprotData.idMapping2(ids, 'UniProtKB_AC-ID', 'RefSeq_Protein')
        li = [{'FROM': e['from'], 'TO': e['to']} for e in ret['results']]
        out = pd.DataFrame(li)
        return out

    # base on uniprot idmapping service
    def uniprotRntry2entrezGeneID(self, tab):
        ids = tab.array
        ret = self.uniprotData.idMapping2(ids, 'UniProtKB_AC-ID', 'GeneID')
        li = [{'FROM': e['from'], 'TO': e['to']} for e in ret['results']]
        out = pd.DataFrame(li)
        return out

    # base on uniprot idmapping service
    def entrezProteinAc2uniprotRntry(self, tab):
        ids = tab.array
        ret = self.uniprotData.idMapping2(ids, 'RefSeq_Protein', 'UniProtKB')
        li = [{'FROM': e['from'], 'TO': e['to']['primaryAccession']} for e in ret['results']]
        out = pd.DataFrame(li)
        return out

    # base on entrez e-utilities
    def entrezProteinAc2entrezGeneID(self, tab):
        ids = tab.array
        di = self.entrezData.eLink('protein', 'gene', ids)
        li = []
        for e in di['eLinkResult']['LinkSet']:
            if 'LinkSetDb' in e and 'Link' in e['LinkSetDb'] and 'Id' in e['LinkSetDb']['Link']:
                li.append({'FROM': e['IdList']['Id'], 'TO': e['LinkSetDb']['Link']['Id']})
        out = pd.DataFrame(li)
        return out

    # base on gene2accession.gz file under https://ftp.ncbi.nlm.nih.gov/gene/DATA/
    def entrezProteinAc2entrezGeneID2(self, tab):
        pass

    # Entry	Gene Names	Organism (ID)	Function [CC]	Pathway	EC number	Gene Ontology (GO)	Gene Ontology IDs	PubMed ID
    # UP_Entry	UP_Gene_Names	UP_Organism_ID	UP_Function_CC	UP_Pathway	UP_EC_number
    # UP_Gene_Ontology_GO	UP_Gene_Ontology_IDs	UP_PubMed_ID
    def drawUniprotAnnotation(self, tab):
        ids = tab.array
        ret = self.uniprotData.idMapping2(ids, 'UniProtKB_AC-ID', 'UniProtKB')
        li = []
        for e in ret['results']:
            n = {}
            n['FROM'] = e['from']
            to = e['to']
            # UP_Gene_Names
            if 'genes' in to:
                geneName = []
                for g in to['genes']:
                    if 'geneName' in g:
                        geneName.append(g['geneName']['value'])
                n['UP_Gene_Names'] = ' # '.join(geneName)
            # UP_Organism_ID UP_Organism_LINEAGE
            if 'organism' in to:
                n['UP_Organism_ID'] = to['organism']['taxonId']
                n['UP_Organism_LINEAGE'] = '; '.join(to['organism']['lineage'])
            # UP_Function_CC
            if 'comments' in to:
                comment = []
                for com in to['comments']:
                    if com['commentType'] == 'FUNCTION':
                        for comt in com['texts']:
                            comment.append(comt['value'])
                n['UP_Function_CC'] = '; '.join(comment)
            # UP_Pathway UP_EC_number
            # UP_Gene_Ontology_GO	UP_Gene_Ontology_IDs
            if 'uniPortKBCrossReference' in to:
                for ref in to['uniPortKBCrossReference']:
                    database = ref['database']
                    if database == '':
                        pass
            li.append(n)
        out = pd.DataFrame(li)
        out = pd.DataFrame(li)
        return out