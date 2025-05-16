""" Select calling tool """


from CataTQA.tools.tool_invocation import TableQAProcessor

def run(question):
    qa_system = TableQAProcessor(question)
    return qa_system.get_tool()

if __name__ == '__main__':
    res = run('Determine the maximum irradiation time (h) for Bi type BiOCl, Main product CO, and loading > 0.142857143 g/l.')
    print(res)
    """{'tool': 'calculate_data', 'column name': 'irradiation time'}"""