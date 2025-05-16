""" Obtain the column names for answering questions """

from CataTQA.tools.field_seclection import TableQAProcessor

def run(question: str, table: str):
    qa_system = TableQAProcessor(question, table)
    return qa_system.select_columns()

if __name__ == '__main__':
    res = run(
        'What is the unique identifier for the material composed of Ni2.5Cu1.5Zr8 and exhibiting a Tc of 1.09?',
        'table65'
    )
    print(res)
    """ ['id', 'Tc', 'formula'] """