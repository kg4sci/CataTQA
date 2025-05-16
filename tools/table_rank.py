""" Table rank """

from typing import List
import re

from CataTQA.tools.table_desc import Tool
from CataTQA.utils.prompt import get_table_prompt
from CataTQA.utils.config import LLMClient


class TableQAProcessor:
    def __init__(self, question):
        self.question = question

    def get_prompt(self):
        return get_table_prompt.format(
            question=self.question,
            table_desc=Tool.get_table_desc()
        )

    def rank_tables(self) -> List[str]:
        response = LLMClient.query(prompt=self.get_prompt())
        ranked_tables = eval(re.findall(r"\[['|\"].*?['|\"]\]", response)[0])
        return ranked_tables