
get_templates_prompt = """You need to generate template questions for a tabular data.Input as table description, column name and column name description.

Please generate questions according to the following rules:
1. Requirements to be met：
 - template questions type: {question_description}
 - number of columns required to obtain answers: at least two columns
 - level: The level of the template questions is differentiated according to the number of columns used. Including two levels of simple and complex.

2. Example：
    Input:
     - table description:{example_tabular_description}
     - [column names] - [description]:{example_field_description}
    Output:```{example}```

3. output format：
    - Mark the level of each question.At least ten questions per level.
    - Mark the column names that need to be used to answer this question template.
    - Use “{{}}” for template variables.The template variable must be one of the columns of the table.
    - Use of multiple sentence structures.Questions need to be phrased in a way that is easy to understand.

Use the information in the table below to generate template questions according to the above rules:
Input:
 - table description:{tabular_description}
 - [column names] - [description]:{field_description}
"""


get_table_prompt = """Please analyze the relevance of the table according to the problem.
question：{question}

Available tables and table descriptions:
{table_desc}

Please sort the tables by relevance from high to low, give the first five possible tables, and directly return the table name list.for example:["table1", "table2"]
"""


get_field_prompt = """Only provide the column names required to answer the question:
question：{question}

{table} information：[column]-[column name explanation]
{table_field}

Please directly return to the column name list, for example：['col1','col2']
"""


get_condition_prompt = """Please extract the query criteria from the question and return the results according to the table structure:
question：{question}

table information：
column name：[{tar}]

Output requirements:
1. Return to dictionary format, with the key being the column name and the value being the query condition
2. The values corresponding to all column names must be output. The output not found in the problem is ''.
3. Extract and preserve comparison symbols (>,<,=, etc.)
4. example：{{"column1": ">50", "column2": "Liming"}}

Please return the JSON dictionary directly without including any other content"""


get_tool_prompt = """Please use the tools needed to answer the questions according to the question analysis. 
Question: {question}

Description of available tools:
{tool_desc}

Please return the tool name.If using calculate_data, you also need to specify the column name for the calculation.For example: {{"tool":"","column name":""}}
"""





