import json
from paper import *
import requests


def get_paper_data_dblp(keyword, number):
    doubleNumber = number * 10
    papersUrl = "http://dblp.org/search/publ/api?q=" + keyword + "&h=" + f"{doubleNumber}" + "&format=json"
    r = requests.get(papersUrl)
    rJson = json.loads(r.text)
    print(rJson)
    rJsonResult = ""
    if (rJson['result']['status']['@code'] != '200'):
        return False, None
    if (rJson['result']['hits']):
        rJsonResult = rJson['result']['hits']
    # print("hits: ", rJsonResult)
    resultNumber = 0
    if (rJsonResult.get('@computed')):
        resultNumber = eval(rJsonResult['@computed'])
    # print("resultNumber: ", resultNumber)
    if (resultNumber == 0):
        return False, None
    resultPapers = rJsonResult['hit']
    i = 0
    papers = []
    for paperJson in resultPapers:
        paperJson = get_paper_info(paperJson)
        print(paperJson)
        authorList = get_authors(paperJson)
        # print(authorList)
        title, venue, volumn, number, pages, year, papertype, key, doi, ee, url = get_basic_info(
            paperJson)

        paperRequest = requests.get(
            "https://api.semanticscholar.org/v1/paper/" + doi)
        paperAbJson = json.loads(paperRequest.text)
        print(paperAbJson)
        abstract = ""
        topicsJson = ""
        fieldsOfStudy = ""
        topics = []
        if (paperAbJson.get('abstract')):
            abstract = paperAbJson['abstract']
        if (paperAbJson.get('topics')):
            topicsJson = paperAbJson['topics']
        if (paperAbJson.get('fieldsOfStudy')):
            fieldsOfStudy = paperAbJson['fieldsOfStudy']
        if (paperAbJson.get('authors')):
            authorList = paperAbJson['authors']
        if (not abstract or abstract.strip() == ""):
            continue
        topics = get_topics(topicsJson)
        paper = Paper(abstract=abstract,
                      topics=topics,
                      fieldsOfStudy=fieldsOfStudy,
                      authors=authorList,
                      title=title,
                      venue=venue,
                      year=year,
                      papertype=papertype,
                      doi=doi,
                      ee=ee,
                      url=url)
        # print(paper)
        papers.append(paper)
        i = i + 1
        print("i: ", i)
        if (i == number):
            break
    return True, papers


def get_paper_data_semanticScholar(doi):
    r = requests.get("https://api.semanticscholar.org/v1/paper/" + doi)
    rJson = json.loads(r.text)
    # print(rJson)
    abstract = ""
    topics = []
    fieldsOfStudy = ""
    title = ""
    authors = []
    venue = ""
    year = ""

    if (rJson.get('abstract')):
        abstract = rJson['abstract']
    if (rJson.get('topics')):
        topics = rJson['topics']
    if (rJson.get('fieldsOfStudy')):
        fieldsOfStudy = rJson['fieldsOfStudy']
    if (rJson.get('title')):
        title = rJson['title']
    if (rJson.get('authors')):
        authors = rJson['authors']
    if (rJson.get('venue')):
        venue = rJson['venue']
    if (rJson.get('year')):
        year = rJson['year']

    if (not abstract or abstract.strip() == ""):
        return None
    paper = Paper(abstract=abstract,
                  topics=topics,
                  fieldsOfStudy=fieldsOfStudy,
                  title=title,
                  doi=doi,
                  ee="https://doi.org/" + doi,
                  authors=authors,
                  venue=venue,
                  year=year)
    return paper
