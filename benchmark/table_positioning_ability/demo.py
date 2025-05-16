""" Obtain table ranking """

from CataTQA.tools.table_rank import TableQAProcessor


def run(question):
    qa_system = TableQAProcessor(question)
    return qa_system.rank_tables()


if __name__ == '__main__':
    res = run('Which secondary cation occupies the A2 site in the perovskite material HTiTaO5?')
    print(res)
    """ ['table31', 'table37', 'table14', 'table22', 'table49'] """