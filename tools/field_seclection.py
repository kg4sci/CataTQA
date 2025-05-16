""" Column name found """

import re
from typing import List

from CataTQA.utils.prompt import get_field_prompt
from CataTQA.tools.field_desc import Tool
from CataTQA.utils.config import LLMClient

class TableQAProcessor:
    def __init__(self, question: str, table: str):
        self.question = question
        self.table = table

    def get_prompt(self):
        return get_field_prompt.format(
            question=self.question,
            table=self.table,
            table_field = Tool.get_table_columns(self.table)
        )

    def select_columns(self) -> List[str]:
        prompt = self.get_prompt()
        response = LLMClient.query(prompt)
        target_columns = eval(re.findall(r"\[['|\"].*?['|\"]\]", response)[0])
        return target_columns