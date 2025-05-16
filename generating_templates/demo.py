""" Generation template """

import json
import os

from CataTQA.utils.prompt import get_templates_prompt
from CataTQA.utils.config import *

def get_prompt(question_description,
               example_tabular_description,
               example_field_description,
               example,
               tabular_description,
               field_description):
    prompt = get_templates_prompt.format(question_description,
               example_tabular_description,
               example_field_description,
               example,
               tabular_description,
               field_description)
    return prompt

def get_templates(prompt):
    response = LLMClient.query(prompt)
    return response

if __name__ == '__main__':
    par_path = '../metadata/parameters.json'
    output_filename = 'output.json'
    dir_path = os.getcwd()
    with open(par_path) as f:
        parameters = json.loads(f.read())
    tables_par = parameters['tabular_parameters']
    templates_par = parameters['templates_parameters']

    # Tables and question types
    for table in tables_par:
        for example in templates_par:
            tabular_description = table['tabular description']
            field_description = table['field description']
            table_name = table['tabular name']
            example_type = example['question type']
            example_description = example['question description']
            example_tabular_description = example['tabular description']
            example_field_description = example['field description']
            example_result = example['example']

            prompt = get_prompt(
                example_description,
                example_tabular_description,
                example_field_description,
                example_result,
                tabular_description,
                field_description
            )

            response = get_templates(prompt)
            with open(f'output/{table_name}-{example_type}.txt', 'w', encoding='utf-8') as f:
                f.write(response)


