""" Supplement QA parameters """

import re

from CataAgentQA.utils.jsonlines_io import IOJsonLines

TYPES = ['Cell_Query', 'Fact_Judgmen', 'Data_Filtering', 'Numerical_Calculation']
USE_TOOLS = ['search_value', 'making_judge', 'making_judge', 'calculate_data']

def add_info(TYPE, USE_TOOL):
    for i in range(1, 69):
        TABLE = f'table{i}'
        template_path = f'templates/{TABLE}-templates.jsonl'
        template_datas = IOJsonLines.read_in(template_path)

        data_search = []
        for template in template_datas:
            if template['question_type'] == f'{TYPE}':
                template['question'] = re.sub(r'\{(\w+.*?)\}', r'\1', template['question'])
                count = template['question'].count('{}')

                template['condition_column'] = template['column names'][0:count]
                template['answer_column'] = template['column names'][count:]
                template['use_tool'] = f'{USE_TOOL}'
                data_search.append(template)

        SAVE_PATH = f'{TYPE}_templates/'
        IOJsonLines.write_out(f'{SAVE_PATH}{TABLE}-{TYPE}.jsonl',data_search)

if __name__ == '__main__':
    for index in range(len(TYPES)):
        add_info(TYPES[index], USE_TOOLS[index])