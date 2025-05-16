""" Define tools and generate prompt """

from langchain_core.tools import tool
from langchain_core.tools import render_text_description

class Tool:
    @tool
    def search_value(x: list):
        """Find the value of a specific cell based on the problem."""
        return object

    @tool
    def making_judge(x: list):
        """Determine whether it is correct according to the problem."""
        return object

    @tool
    def data_filtering(x:list):
        """Filter data based on the conditions in the question."""
        return object

    @tool
    def calculate_data(x: list):
        """The results are calculated according to the conditions in the problem."""
        return object

    @classmethod
    def get_tool(cls):
        tools = [
            cls.search_value,
            cls.making_judge,
            cls.data_filtering,
            cls.calculate_data
        ]
        rendered_tools = render_text_description(tools)
        return rendered_tools