""" Retrieve the description information of the specified table. """

import json

from CataTQA.utils.config import TABLE_PAR_PATH

class Tool:
    @classmethod
    def get_table_desc(cls) -> str:
        with open(TABLE_PAR_PATH, encoding='utf-8') as f:
            s = f.read()
        parameters = json.loads(s)['tabular_parameters']
        table_description = ''
        for index, par in zip(range(len(parameters)), parameters):
            table_description += '   - [table{1}]:[{2}]\n'.format(
                index+1,
                    index+1,
                    par['tabular description']
            )
        return table_description