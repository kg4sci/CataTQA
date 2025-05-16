""" Filter data by criteria """

import pandas as pd

from CataTQA.utils.config import TABLE_PATH

def read_table(table_name, column_names, condition):
    datas = pd.read_csv(TABLE_PATH + table_name + '.csv')
    for c in condition:
        if condition[c]:
            try:
                datas = datas[datas[c] == float(condition[c])]
            except ValueError:
                datas = datas[datas[c] == condition[c]]
    return datas[column_names]