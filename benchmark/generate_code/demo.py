""" Generate code using LLM to obtain answers """

from CataTQA.utils.jsonlines_io import IOJsonLines
from CataTQA.tools.generate_code import generate_code
from CataTQA.tools.exec_code import exec_code

# Cell_Query / Fact_Judgement / Data_Filtering / Numerical_Calculation'
Type = 'Cell_Query'

questions = IOJsonLines.read_in(f'dataset/{Type}_QA.jsonl')
result = []
for question in questions:
    code = generate_code(question)
    # print(code)
    res = exec_code(question, code)
    result.append(res)
IOJsonLines.write_out(f'result/{Type}_QA.jsonl', result)