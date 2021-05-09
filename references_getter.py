from requests.api import get
from papers_getter import *
import json
import crossref_commons.retrieval
import requests


def get_references_from_semanticscholar(doi):
    r = requests.get("https://api.semanticscholar.org/v1/paper/" + doi)
    rjson = json.loads(r.text)
    references = []
    rreferences = []
    if (rjson.get('references')):
        references = rjson['references']
        for reference in references:
            if (not (reference.get('doi'))):
                continue
            paper = get_paper_data_semanticScholar(reference['doi'])
            if (paper):
                rreferences.append(paper)
    return rreferences


def get_citations_from_semanticscholar(doi):
    r = requests.get("https://api.semanticscholar.org/v1/paper/" + doi)
    rjson = json.loads(r.text)
    citations = []
    rcitations = []
    if (rjson.get('citations')):
        citations = rjson['citations']
        for citation in citations:
            if (not (citation.get('doi'))):
                continue
            paper = get_paper_data_semanticScholar(citation['doi'])
            if (paper):
                rcitations.append(paper)
    return rcitations


def get_references_from_opencitation(doi):
    r = requests.get("https://opencitations.net/index/api/v1/metadata/" + doi)
    rJson = json.loads(r.text)
    result = rJson[0]
    references = []
    rreferences = []
    if (result.get('reference')):
        references = result['reference']
        for reference in references:
            paper = get_paper_data_semanticScholar(reference['DOI'])
            rreferences.append(paper)
    return rreferences


def get_citations_from_opencitation(doi):
    r = requests.get("https://opencitations.net/index/api/v1/metadata/" + doi)
    rJson = json.loads(r.text)
    result = rJson[0]
    citations = []
    rcitations = []
    if (result.get('citation')):
        citations = result['citation']
        for citation in citations:
            paper = get_paper_data_semanticScholar(citation['DOI'])
            rcitations.append(paper)
    return rcitations


def get_references_from_crossref(doi):
    crossrefJsonData = crossref_commons.retrieval.get_publication_as_json(doi)
    references = crossrefJsonData['reference']
    references = []
    rreferences = []
    for reference in references:
        if (reference.get('DOI') and reference.get('abstract')
                and reference['abstract'].strip() != ""):
            paper = get_paper_data_semanticScholar(reference['DOI'])
            rreferences.append(paper)
    return rreferences


#isFound, papers = get_paper_data_dblp("recommendation", 5)
#for paper in papers:
#    print(paper)
#    if (type(paper.doi) is str):
#        references = get_references_from_semanticscholar(paper.doi)
#        citations = get_citations_from_semanticscholar(paper.doi)
#        print("references:")
#        for reference in references:
#            print(reference)
#        print("citations: ")
#        for citation in citations:
#            print(citation)
