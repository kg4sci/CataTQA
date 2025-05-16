""" Obtain the conditions in the question. """

from CataTQA.tools.condition_analyse import TableQAProcessor

def run(question, columns):
    qa_system = TableQAProcessor(question, columns)
    return qa_system.search_info()


if __name__ == '__main__':
    res = run(
        'What is the unique identifier for the material composed of Ni2.5Cu1.5Zr8 and exhibiting a Tc of 1.09?',
        ['id', 'Tc', 'formula']
    )
    print(res)
    """ {'id': '', 'Tc': '=1.09', 'formula': 'Ni2.5Cu1.5Zr8'} """
