""" Retrieve field information from a table. """

import json

from CataTQA.utils.config import TABLE_PAR_PATH

class Tool:
    # 获取单个表格列名
    @classmethod
    def get_table_columns(cls, table_name: str) -> str:
        with open(TABLE_PAR_PATH, encoding='utf-8') as f:
            s = f.read()
        parameters = json.loads(s)['tabular_parameters']
        for par in parameters:
            if par['tabular name'] == table_name:
                return par['field description']