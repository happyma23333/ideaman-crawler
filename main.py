from paper_utils import *


def set_up_ideaman_database(keyword, number, level):
    isFound, papers = get_paper_data_dblp(keyword, number)
    if (isFound and papers):
        for paper in papers:
            inserted_paper = insert_paper(paper)
            insert_keyword_paper_recommendation(inserted_paper, keyword)
            generate_paper_graph(inserted_paper, level)


def set_up_ideaman_database_timeout(keyword, number, level):
    isFound, papers = get_paper_data_dblp(keyword, number)
    if (isFound and papers):
        for paper in papers:
            inserted_paper = insert_paper(paper)
            insert_keyword_paper_recommendation(inserted_paper, keyword)
            generate_paper_graph_sleep(inserted_paper, level)


def main():
    set_up_ideaman_database("recommendation", 3, 4)


if __name__ == "__main__":
    main()
