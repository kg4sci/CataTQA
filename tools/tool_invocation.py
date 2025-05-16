import re

from CataTQA.utils.config import LLMClient
from CataTQA.utils.prompt import get_tool_prompt
from CataTQA.tools.calculate_tool import Tool

class TableQAProcessor:
    def __init__(self, question):
        self.question = question

    def get_prompt(self):
        return get_tool_prompt.format(
            question=self.question,
            tool_desc=Tool.get_tool()
        )
        # python_desc=Tool.get_tool()[1]

    def get_tool(self):
        response = LLMClient.query(prompt=self.get_prompt())
        tool_par = eval(re.findall(r"\{['|\"].*?['|\"]}", response)[0])
        return tool_par