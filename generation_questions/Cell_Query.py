""" Generate Cell_Query questions """

import pandas as pd
import random
import jsonlines
import warnings

from CataAgentQA.utils.jsonlines_io import IOJsonLines

warnings.filterwarnings('ignore')
TYPE = 'Cell_Query'


def generation_questions(info, table_datas):
    questions = []
    optional = []

    for row in range(len(table_datas)):
        conditions = []
        for j in range(len(info['condition_column'])):
            conditions.append(table_datas[info['condition_column'][j]] == table_datas.iloc[row][info['condition_column'][j]])
        try:
            bool_condition = conditions[0]
        except Exception as e:
            continue
        for d in conditions:
            bool_condition = bool_condition & d
        repeat_num = table_datas[bool_condition]

        if len(repeat_num) == 1:
            data = {}
            for d in info['column names']:
                data[d] = str(table_datas.iloc[row][d])
            optional.append(data)

    # print(optional)

    # Ensure that the issue is not repeated
    num = min(len(optional), 10)
    if num >= 10:
        randon_index =  random.sample(range(0, num), 10)
    else:
        randon_index =  random.sample(range(0, num), num)

    for index in randon_index :
        value1 = []
        answer_condition = {}
        for j in info['condition_column']:
            value1.append(optional[index][j])
            answer_condition[j] = optional[index][j]
            if str(optional[index][j]) == 'nan':
                answer_condition[j] = ''

        question = info['question'].format(*value1)

        # Get answer
        value2 = {}
        for j in info['answer_column']:
            value2[j] = optional[index][j]
            if str(optional[index][j]) == 'nan':
                value2[j] = ''

        questions.append(
            {
                "question": question,
                "refer_dataset": info['refer dataset'],
                "column names": info['column names'],
                "condition_column": info['condition_column'],
                "answer_column": info['answer_column'],
                "condition": answer_condition,
                "tool": info['use_tool'],
                "answer": value2,
                "level": info['level'],
                "question description": info['question description'],
                "refer_template": info['question'],
            }
        )
    return questions

def save(table, questions):
    with jsonlines.open(f'./Cell_Query_QA/{table}-{TYPE}.jsonl', mode='a') as writer:
        for q in questions:
            writer.write(q)

if __name__ == '__main__':
    for i in range(1, 69):
        table = f'table{i}'
        file_path = f"../processing/output/{table}.csv"
        table_datas = pd.read_csv(file_path, nrows=2000)

        template_path = f'../generating_templates/Cell_Query_templates/{table}-{TYPE}.jsonl'
        template_datas = IOJsonLines.read_in(template_path)

        for tem in template_datas:
            questions = generation_questions(tem, table_datas)
            # print(questions)
            save(table, questions)
