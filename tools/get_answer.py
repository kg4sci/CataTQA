""" Get answers to questions """

from CataTQA.tools.filter_table import read_table
from CataTQA.utils.jsonlines_io import IOJsonLines
import jsonlines

class GetAnswer:
    def __init__(self, datas, condition, tool):
        self.datas = datas
        self.condition = condition
        self.tool = tool

    def average_list(self) -> float:
        column_name = self.tool['column name']
        data = self.datas[column_name]
        return data.fillna(0).mean()

    def sum_list(self) -> float:
        column_name = self.tool['column name']
        data = self.datas[column_name]
        return data.fillna(0).mean()

    def max_list(self) -> float:
        column_name = self.tool['column name']
        data = self.datas[column_name]
        return data.fillna(0).max()

    def min_list(self) -> float:
        column_name = self.tool['column name']
        data = self.datas[column_name]
        return data.fillna(0).min()

    def media_list(self) -> float:
        column_name = self.tool['column name']
        data = self.datas[column_name]
        return data.fillna(0).median()

    def search_value(self):
        result = self.datas[self.condition]
        print(f'res:{result}')
        res = []
        for v in self.condition:
            res.append(result[v].to_string(index=False))
        # print(res)
        return res

    def making_judge(self):
        if len(self.datas) == 1:
            return True

    def data_filtering(x: list):
        return object

    def calculate_data(x: list):
        return object



def get_a():
    questions = {"question": "Retrieve the total magnetization value for the material identified by material ID 2dm-9.", "refer_dataset": "table67", "column names": ["material_id", "total_magnetization"], "condition_column": ["material_id"], "answer_column": ["total_magnetization"], "condition": {"material_id": "2dm-9"}, "tool": "search_value", "answer": {"total_magnetization": "0.0"}, "level": "simple", "question description": "In a tabular data structure, locate the cells that meet the requirements.", "refer_template": "Retrieve the total magnetization value for the material identified by material ID {}.", "llm_field": ["material_id", "total_magnetization"]}
    column_names, condition, tool = questions['column names'], questions['condition'], questions['tool']
    answer_col = questions['answer_column']
    datas = read_table(questions['refer_dataset'], column_names, condition)

    Answer = GetAnswer(datas, answer_col, tool)
    print(Answer)



def run(q, table_name):
    column_names, condition, tool = q['llm_field'], q['llm_condition'], q['llm_tool']
    answer_col = q['answer_column']
    datas = read_table(table_name, column_names, condition)

    Answer = GetAnswer(datas, answer_col, tool)

    if tool['tool'] == 'search_value':
        search_res = Answer.search_value()
        return search_res
    elif tool['tool'] == 'making_judge':
        judge_res = Answer.making_judge()
        return judge_res


def alone_run():
    import time
    QA_data = []
    with jsonlines.open('../../dataset/test_dataset/data_search_QA.jsonl') as reader:
        for data in reader:
            QA_data.append(data)
    for q in QA_data:
        # print(q)
        q['llm_answer'] = run(q)
        print(q['llm_answer'][0])
        print(q['answer'][q['answer_column'][0]])
        print('=======')
        time.sleep(3)
        # yield q


if __name__ == '__main__':
    alone_run()