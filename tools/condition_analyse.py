""" Analyze the conditions in the problem. """

import re

from CataTQA.utils.config import LLMClient
from CataTQA.utils.prompt import get_condition_prompt

class TableQAProcessor:
    def __init__(self, question, tar_names):
        self.question = question
        self.tar_names = tar_names


    def get_prompt(self):
        return get_condition_prompt.format(
            question=self.question,
            tar = ", ".join(self.tar_names)
        )

    def search_info(self) ->dict:
        prompt = self.get_prompt()
        response = LLMClient.query(prompt)
        condition =  eval(re.findall(r"\{['|\"].*?['|\"]\}", response)[0])
        return condition