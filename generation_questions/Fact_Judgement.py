""" Generate Fact_Judgement questions """

import pandas as pd
import random
import jsonlines
import warnings

from CataAgentQA.utils.jsonlines_io import IOJsonLines

warnings.filterwarnings('ignore')
TYPE = 'Fact_Judgement'

def generation_questions(info):
    questions = []
    optional = []

    for row in range(len(table_datas)):
        conditions = []

        for j in range(len(info['condition_column'])):
            conditions.append(table_datas[info['condition_column'][j]] == table_datas.iloc[row][info['condition_column'][j]])
        try:
            bool_condition = conditions[0]
        except Exception as e:
            print(e)
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

    num = min(len(optional), 10)
    if num >= 10:
        randon_index =  random.sample(range(0, num), 10)
    else:
        randon_index =  random.sample(range(0, num), num)

    num = 0
    for index in randon_index :
        value1 = []
        answer_condition = {}

        length = len(optional[0])
        if num % 2 == 0:
            for j in info['condition_column']:
                value1.append(optional[index][j])
                answer_condition[j] = optional[index][j]
                if str(optional[index][j]) == 'nan':
                    answer_condition[j] = ''
            value2 = 'true'
        else:
            error_index =  random.randint(0, length)
            i = 0
            for j in info['condition_column']:
                if i == error_index:
                    error_value = optional[random.randint(0, len(optional)-1)][j]
                    true_value = optional[index][j]
                    if error_value == true_value:
                        answer_condition[j] = true_value
                        value1.append(true_value)
                        value2 = 'true'
                    else:
                        answer_condition[j] = error_value
                        value1.append(error_value)
                        value2 = 'false'
                else:
                    value1.append(optional[index][j])
                    answer_condition[j] = optional[index][j]
                if str(optional[index][j]) == 'nan':
                    answer_condition[j] = ''
                i += 1

        try:
            question = info['question'].format(*value1)
        except IndexError:
            break
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
        num += 1
    return questions

def save(table, questions):
    with jsonlines.open(f'./Fact_Judgement_QA/{table}-{TYPE}.jsonl', mode='a') as writer:
        for q in questions:
            writer.write(q)

if __name__ == '__main__':
    for i in range(1, 69):
        table = f'table{i}'
        # print(table)

        file_path = f"../processing/output/{table}.csv"
        table_datas = pd.read_csv(file_path, nrows=5000)

        # 模板数据
        template_path = f'../generating_templates/Fact_Judgement_templates/{table}-{TYPE}.jsonl'
        template_datas = IOJsonLines.read_in(template_path)

        for tem in template_datas:
            # print(tem)
            questions = generation_questions(tem)
            # print(questions)
            save(table, questions)
