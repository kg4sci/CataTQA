""" Generate Numerical_Calculation questions """

import pandas as pd
import random
import jsonlines
import warnings

from CataAgentQA.utils.jsonlines_io import IOJsonLines

warnings.filterwarnings('ignore')
TYPE = 'Numerical_Calculation'

def generation_questions(info, table_datas):
    questions = []
    optional = []

    optional_datas = table_datas[info['column names']]
    df_deduped = optional_datas[info['condition_column'].keys()].drop_duplicates()
    # print(df_deduped)

    for row in range(len(df_deduped)):
        data = {}
        for d in info['condition_column']:
            data[d] = df_deduped.iloc[row][d]
        optional.append(data)
    # print(optional)

    num = min(len(optional), 20)
    if num >= 20:
        randon_index =  random.sample(range(0, num), 20)
    else:
        randon_index =  random.sample(range(0, num), num)

    num = 0
    for index in randon_index :
        value1 = []
        answer_condition = {}
        for j in info['condition_column']:
            value1.append(optional[index][j])
            if info['condition_column'][j] == '=':
                answer_condition[j] = info['condition_column'][j] +"='" +str(optional[index][j])+"'"
            else:
                answer_condition[j] = info['condition_column'][j] + str(optional[index][j])

        question = info['question'].format(*value1)
        # print(question)

        rename_info = {}
        n = 0
        for j in info['condition_column']:
            rename_info[j] = f"col_{chr(65+n)}"
            n += 1
        optional_datas = optional_datas.rename(columns=rename_info)
        # print(optional_datas)
        query_parts = []
        for col, cond in answer_condition.items():
            query_parts.append(f"{rename_info[col]}{cond}")
        query_str = " and ".join(query_parts)
        # print(query_str)
        try:
            value2 = optional_datas.query(query_str)[info['answer_column'].keys()].to_dict('records')
        except Exception:
            continue
        # print(value2)
        datas = []
        for i in info['answer_column']:
            k = i
        for d in value2:
            if str(d[k]) == 'nan':
                continue
            if d.values:
                datas.append(d)
        # print(f'value:{datas}')

        if datas:
            try:
                answer = cal_data(info['answer_column'], datas)
            except Exception:
                continue
        else:
            answer = ''
        questions.append(
            {
                "question": question,
                "refer_dataset": info['refer dataset'],
                "column names": info['column names'],
                "condition_column": info['condition_column'],
                "answer_column": info['answer_column'],
                "condition": answer_condition,
                "tool": info['use_tool'],
                "answer": answer,
                "level": info['level'],
                "question description": info['question description'],
                "refer_template": info['question'],
            }
        )
        num += 1
    return questions

def cal_data(info, datas):
    for j in info:
        name = j
        tool = info[j]

    if tool == 'avg':
        sum = 0
        for data in datas:
            sum += data[name]
        avg_res = sum / len(datas)
        return avg_res
    elif tool == 'max':
        max_value = datas[0][name]
        for data in datas:
            max_value = max(max_value, data[name])
        return max_value
    elif tool == 'min':
        min_value = datas[0][name]
        for data in datas:
            min_value = max(min_value, data[name])
        return min_value
    elif tool == 'sum':
        sum = 0
        for data in datas:
            sum += data[name]
        return sum
    elif tool == 'count':
        count = len(datas)
        return count
    else:
        return datas

def save(table, questions):
    with jsonlines.open(f'./Numerical_Calculation_QA/{table}-{TYPE}.jsonl', mode='a') as writer:
        for q in questions:
            writer.write(q)

if __name__ == '__main__':
    for i in range(1, 69):
        table = f'table{i}'

        file_path = f"../processing/output/{table}.csv"
        table_datas = pd.read_csv(file_path, nrows=5000)

        template_path = f'../generating_templates/Numerical_Calculation_templates/{table}-{TYPE}.jsonl'
        template_datas = IOJsonLines.read_in(template_path)
        # print(template_datas)

        for tem in template_datas:
            # print(tem)
            questions = generation_questions(tem, table_datas)
            # print(questions)
            save(table, questions)
