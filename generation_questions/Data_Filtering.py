""" Generate Data_Filtering questions """

import pandas as pd
import random
import jsonlines
import warnings

from CataAgentQA.utils.jsonlines_io import IOJsonLines

warnings.filterwarnings('ignore')
TYPE = 'Data_Filtering'

def generation_questions(info, table_datas):
    questions = []
    optional = []
    conditions = []

    for j in info['condition_column']:
        try:
            conditions.append(table_datas[j].notna())
        except:
            return
    bool_condition = conditions[0]
    for d in conditions:
        bool_condition = bool_condition & d
    good_data = table_datas[bool_condition]

    for row in range(len(good_data)):
        data = {}
        for d in info['column names']:
            data[d] = good_data.iloc[row][d]
        optional.append(data)

    # print(optional)

    # Ensure that the issue is not repeated
    num = min(len(optional), 20)
    if num >= 20:
        randon_index =  random.sample(range(0, num), 20)
    else:
        randon_index =  random.sample(range(0, num), num)

    for index in randon_index :
        value1 = []
        answer_condition = {}
        for j in info['condition_column']:
            try:
                value1.append(optional[index][j])
            except:
                return
            if info['condition_column'][j] == '=':
                answer_condition[j] = info['condition_column'][j] + "='" + str(optional[index][j]) + "'"
            else:
                answer_condition[j] = info['condition_column'][j] + str(optional[index][j])

        question = info['question'].format(*value1)
        # print(question)

        rename_info = {}
        n = 0
        for j in info['condition_column']:
            rename_info[j] = chr(65+n)
            n += 1

        table_datas = table_datas.rename(columns=rename_info)
        query_parts = []
        for col, cond in answer_condition.items():
            query_parts.append(f"{rename_info[col]}{cond}")
        query_str = " and ".join(query_parts)
        # print(query_str)

        try:
            value2 = table_datas.query(query_str)[info['answer_column']].to_dict('records')
        except (SyntaxError,TypeError,KeyError,Exception):
            continue
        # print(value2)

        for l in value2:
            for v in l:
                if str(l[v]) == 'nan':
                    l[v] = ''

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
    # print(questions)
    return questions

def save(table, questions):
    with jsonlines.open(f'./Data_Filtering_QA/{table}-{TYPE}.jsonl', mode='a') as writer:
        for q in questions:
            writer.write(q)


if __name__ == '__main__':
    for i in range(1, 69):
        table = f'table{i}'
        # print(table)

        file_path = f"../processing/output/{table}.csv"
        table_datas = pd.read_csv(file_path, nrows=5000)

        template_path = f'../generating_templates/Data_Filtering_templates/{table}-{TYPE}.jsonl'
        template_datas = IOJsonLines.read_in(template_path)

        for tem in template_datas:
            questions = generation_questions(tem, table_datas)
            # print(questions)
            save(table, questions)
