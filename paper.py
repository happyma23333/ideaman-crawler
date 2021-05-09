import json
import types


class Paper:
    #basic infomation
    def __init__(self,
                 abstract="",
                 topics="",
                 fieldsOfStudy="",
                 authors="",
                 title="",
                 venue="",
                 year=0,
                 papertype="",
                 doi="",
                 ee="",
                 url=""):
        self.id = None
        self.abstract = abstract
        self.topics = topics
        self.fieldsOfStudy = fieldsOfStudy
        self.authors = authors
        self.title = title
        self.venue = venue
        self.year = year
        self.papertype = papertype
        self.doi = doi
        self.ee = ee
        self.url = url

    def __str__(self) -> str:
        return 'authors: ' + (', '.join(str(i) for i in self.authors) if self.authors else '') + \
               '\ntopics: ' + (', '.join(str(i) for i in self.topics) if self.topics else '') + \
               '\nabstract: ' + (self.abstract if self.abstract else '') +\
               '\nid: ' + (f"{self.id}" if self.id else '') + \
               '\ntitle: ' + (self.title if self.title else '') +\
               '\nfields of study: ' +  (', '.join(str(i) for i in self.fieldsOfStudy) if self.fieldsOfStudy else '') +\
               '\nvenue: ' + (self.venue if self.venue else '') +\
               '\nyear: ' + (f"{self.year}" if self.year else '') +\
               '\npapertype: ' + (self.papertype if self.papertype else '') +\
               '\ndoi: ' + (self.doi if self.doi else '') +\
               '\nee: ' + (self.ee if self.ee else '') +\
               '\nurl: ' + (self.url if self.url else '') + "\n\n"

    def __eq__(self, o: object) -> bool:
        return type(o) == type(self) and self.doi == o.doi

    def set_id(self, id):
        self.id = id


def dblp_get_paper_data(jsonstr):
    parse_result = json.loads(jsonstr)
    if (parse_result.get('result')):
        parse_result = parse_result['result']
    # print(parse_result['hits'])
    if (parse_result.get('hits')):
        parse_result_hits = parse_result['hits']
        if (eval(parse_result_hits['@total']) > 0):
            parse_result_hit = parse_result_hits['hit']
            return parse_result_hit
    return None


def get_paper_info(paperJson):
    if (paperJson.get('info')):
        return paperJson['info']
    return None


def get_authors(paperJson):
    authorList = []
    if (paperJson.get('authors')):
        authorsJson = paperJson['authors']
        if (authorsJson.get('author')):
            authors = authorsJson['author']
            for author in authors:
                if (type(author) == type(authorsJson) and author.get('text')):
                    authorList.append(author['text'])
    return authorList


def get_topics(topicsJson):
    topics = []
    for topic in topicsJson:
        topics.append(topic)
    return topics


def get_basic_info(paper):
    title = ''
    venue = ''
    volumn = ''
    number = ''
    pages = ''
    year = ''
    papertype = ''
    key = ''
    doi = ''
    ee = ''
    url = ''
    if (paper.get('title')):
        title = paper['title']
    if (paper.get('venue')):
        venue = paper['venue']
    if (paper.get('volumn')):
        volumn = paper['volumn']
    if (paper.get('number')):
        number = paper['number']
    if (paper.get('pages')):
        pages = paper['pages']
    if (paper.get('year')):
        year = paper['year']
    if (paper.get('papertype')):
        papertype = paper['papertype']
    if (paper.get('key')):
        key = paper['key']
    if (paper.get('doi')):
        doi = paper['doi']
    if (paper.get('ee')):
        ee = paper['ee']
    if (paper.get('url')):
        url = paper['url']
    return title, venue, volumn, number, pages, year, papertype, key, doi, ee, url
