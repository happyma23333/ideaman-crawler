from paper_utils import *
import sys, getopt


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


def main(argv):
    keyword = ''
    number = ''
    level = ''
    timeout = False
    try:
        opts, args = getopt.getopt(
            argv, "k:n:l:", ["keyword=", "number=", "level=", "withtimeout"])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-k", "--keyword"):
            keyword = arg
        elif opt in ("-n", "--number"):
            number = arg
        elif opt in ("-l", "--level"):
            level = arg
        elif opt in ("--withtimeout"):
            timeout = True
    print("keyword: ", keyword)
    print("number: ", number)
    print("level: ", level)
    print("timeout: ", timeout)
    if (timeout):
        set_up_ideaman_database_timeout(keyword, number, level)
    else:
        set_up_ideaman_database(keyword, number, level)


if __name__ == "__main__":
    main(sys.argv[1:])
