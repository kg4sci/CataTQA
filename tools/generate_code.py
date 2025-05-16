""" Generate code using LLM """

import re

from CataTQA.utils.config import *
from CataTQA.utils.prompt import get_generate_code_prompt

def get_prompt(question):
    prompt = get_generate_code_prompt(question)
    return prompt

def generate_code(question):
    response = LLMClient.query(get_prompt(question))
    code = re.match(r"```python(.*?)```", response, re.DOTALL).group(1)
    pattern = r'table(\d+)\.csv'
    replacement = r'../processing/output/table\1.csv'
    code = re.sub(pattern, replacement, code)
    return code