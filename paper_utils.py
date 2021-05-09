from config import *
from paper import *
from papers_getter import *
from references_getter import *
import time
from log_process import logger
import traceback
import sys
import pymysql

conn = pymysql.connect(host=mysql_host,
                       port=mysql_port,
                       user=mysql_user,
                       password=mysql_password,
                       db=mysql_db,
                       charset='utf8')


def search_paper(paper: Paper):
    paperTitle = paper.title
    if (not paperTitle):
        return None
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = "select * from paper where title=\"%s\"" % (paper.title)
    cur.execute(sql)
    res = cur.fetchone()
    #print(res)
    if (not res):
        return None
    paperResult = Paper(authors=res[2],
                        title=res[3],
                        venue=res[4],
                        year=res[5],
                        papertype=res[6],
                        doi=res[7],
                        ee=res[8],
                        url=res[9],
                        topics=res[10],
                        fieldsOfStudy=res[11],
                        abstract=res[12])
    paperResult.set_id(res[0])
    return paperResult


def search_keyword_paper(paper: Paper):
    paperTitle = paper.title
    if (not paperTitle):
        return None
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = "select * from paper where doi=\"%s\"" % (paper.doi)
    cur.execute(sql)
    res = cur.fetchone()
    paperResultId = res[0]
    #print(res)
    if (not paperResultId):
        return None
    return paperResultId


def insert_paper(paper: Paper):
    foundPaper = search_paper(paper)
    conn.ping(reconnect=True)
    if (foundPaper):
        return foundPaper
    else:
        cur = conn.cursor()
        for topic_block in paper.topics:
            topic_block['topic'] = topic_block['topic'].replace("'", "")
        for author_block in paper.authors:
            author_block['name'] = author_block['name'].replace("`", "")

        sql = "insert into paper(abstract, topics, fieldsOfStudy, authors_name, title, venue, year, papertype, doi, ee, url) values (\"%s\", \"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (
            paper.abstract, paper.topics, paper.fieldsOfStudy, paper.authors,
            paper.title, paper.venue, paper.year, paper.papertype, paper.doi,
            paper.ee, paper.url)
        cur.execute(sql)
        pid = cur.lastrowid
        paper.set_id(pid)
        conn.commit()
        cur.close()
        return paper


def insert_keyword_paper_recommendation(paper, keyword):
    conn.ping(reconnect=True)
    if (not paper.id):
        return None
    if (search_keyword_paper(paper)):
        return None
    cur = conn.cursor()
    sql = "insert into keyword_paper_recommendation(id, doi, belongsTo) values(\"%s\",\"%s\",\"%s\")" % (
        paper.id, paper.doi, keyword)
    cur.execute(sql)
    conn.commit()
    cur.close()
    return paper


def insert_paper_relationship(paper: Paper, references_id_list: list,
                              citations_id_list: list):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    references_id_list_str = ', '.join(
        str(i) for i in references_id_list) if references_id_list else ''
    citations_id_list_str = ', '.join(
        str(i) for i in citations_id_list) if citations_id_list else ''
    sql = "insert into paper_relationship(paperid, paper_references, citations) values(\"%s\", \"%s\", \"%s\")" % (
        paper.id, references_id_list_str, citations_id_list_str)
    print(sql)
    cur.execute(sql)
    conn.commit()
    cur.close()


def generate_paper_graph(paper, depth):
    conn.ping(reconnect=True)
    if (depth == 0):
        return
    references = get_references_from_semanticscholar(paper.doi)
    print("references: ")
    for reference in references:
        print(reference)
    references_id_list = []
    if (references and len(references) > 0):
        for reference in references:
            try:
                inserted_reference = insert_paper(reference)
                references_id_list.append(inserted_reference.id)
                generate_paper_graph(inserted_reference, depth - 1)
            except Exception as e:
                traceback.print_exc()
                logger.error(e)
    citations = get_citations_from_semanticscholar(paper.doi)
    print("citations: ")
    for citation in citations:
        print(citation)
    citations_id_list = []
    if (citations and len(citations) > 0):
        for citation in citations:
            try:
                inserted_citation = insert_paper(citation)
                citations_id_list.append(inserted_citation.id)
                generate_paper_graph(inserted_citation, depth - 1)
            except Exception as e:
                traceback.print_exc()
                logger.error(e)
    insert_paper_relationship(paper, references_id_list, citations_id_list)


def generate_paper_graph_sleep(paper, depth):
    conn.ping(reconnect=True)
    if (depth == 0):
        return
    references = get_references_from_semanticscholar(paper.doi)
    print("references: ")
    for reference in references:
        print(reference)
    references_id_list = []
    if (references and len(references) > 0):
        for reference in references:
            try:
                inserted_reference = insert_paper(reference)
                references_id_list.append(inserted_reference.id)
                if (inserted_reference.id % 1000 == 0):
                    time.sleep(1800)
                generate_paper_graph(inserted_reference, depth - 1)
            except Exception as e:
                traceback.print_exc()
                logger.error(e)
    citations = get_citations_from_semanticscholar(paper.doi)
    print("citations: ")
    for citation in citations:
        print(citation)
    citations_id_list = []
    if (citations and len(citations) > 0):
        for citation in citations:
            try:
                inserted_citation = insert_paper(citation)
                citations_id_list.append(inserted_citation.id)
                if (inserted_citation.id % 1000 == 0):
                    time.sleep(1800)
                generate_paper_graph(inserted_citation, depth - 1)
            except Exception as e:
                traceback.print_exc()
                logger.error(e)
    insert_paper_relationship(paper, references_id_list, citations_id_list)


#isFound, papers = get_paper_data_dblp("nlp", 20)
#for paper in papers:
#    #print("111111111")
#    inserted_paper = insert_paper(paper)
#    print(inserted_paper)
#    insert_keyword_paper_recommendation(inserted_paper, "nlp")
#    generate_paper_graph(inserted_paper, 2)
