# CataTQA
**CataTQA: A Benchmark for Tool-Augmented LLM Question Answering over Heterogeneous Catalysis Tables**

## Abstact 
Despite their success in general question answering, large language models (LLMs) struggle with hallucinations and inaccurate reasoning in scientific domains. A major challenge stems from experimental data, which are often stored in external sources like supplementary materials and domain-specific databases. These tables are large, heterogeneous, and semantically complex, making them difficult for LLMs to interpret. While external tools show promise, current benchmarks fail to assess LLMs' ability to navigate this data—particularly in locating relevant tables, retrieving key columns, interpreting experimental conditions, and invoking tools.To address this gap, we introduce CataTQA, a new benchmark for catalytic materials. CataTQA features an automated dataset framework and four auxiliary tools. We evaluate tool-enhanced LLMs across five dimensions: table location, column retrieval, condition analysis, tool calling, and question answering, identifying their strengths and weaknesses.Our work sets a new benchmark for evaluating LLMs in scientific fields and paves the way for future advancements.

![](https://github.com/kg4sci/CataTQA/blob/main/images/main.png)

## setup
To run our project, you need to first clone the project and use the following command to install dependencies.
```python
  pip install -r requirements.txt
```
## download dataset
You can download our metadata and QA dataset through the following methods.   
  metadata: <https://huggingface.co/datasets/CuiQiang/CataTQA_Metadata>    
  dataset: <https://huggingface.co/datasets/CuiQiang/CataTQA>
  
## config
To run our project, we need to configure our own API_KEY.
Open **utils/config.py** through a text editor.Modify the following code.
```python
API_KEY = 'YOUR_API_KEY'
MODEL = 'YOUR_MODEL_NAME'
```
### an example
**Just provide a question and run the tool/run. py program to automatically retrieve answers from all tables.**
```python
python tool/run.py
```
question: What is the hydrogen production rate (RH2) for a photocatalyst prepared using the Polymerized complex Sol-gel method method?
answer:
```python
table_rank：['table1', 'table3', 'table4', 'table2', 'table5']
select_table：['RH2(µmol h-1 g-1)', 'Preparation method']
get_condition:{'RH2(µmol h-1 g-1)': '', 'Preparation method': 'Polymerized complex Sol-gel method'}
get_tool: {'tool': 'search_value', 'column name': 'RH2'}
get_answer: 64
```
## Prompt

- Prompts for Table Annotation
```Annotate the table data, summarize the main problems that this table can solve and its contributions based on the content of the table data.
    Table data:{dataset}
    Output requirements:
    1. Summarize the role of data and avoid discussing a single column or row of data
    2. Output is limited to 50 words or less
```

- Prompts for Template Questions Generation
```Annotate the table data, summarize the main problems that this table can solve and its contributions based on the content of the table data.\\
    Please generate questions according to the following rules:
    1. Requirements to be met:
    - template questions type: {question_description} 
    - number of columns required to obtain answers: at least two columns
    - level: The level of the template questions is differentiated according to the number of columns used.
    Including two levels of simple and complex.
    2. Example:
    Input:
    - table description:{example_tabular_description}
    - [column names] - [description]:{example_field_description}
    Output:{example}
    3. output format:
    - Mark the level of each question.At least ten questions per level.
    - Mark the column names that need to be used to answer this question template.
    - Use"{}" for template variables.The template variable must be one of the columns of the table.
    - Use of multiple sentence structures.Questions need to be phrased in a way that is easy to understand.
    Use the information in the table below to generate template questions according to the above rules:
    Input:
    - table description:{tabular_description}
    - [column names] - [description]:{field_description}
```







  
## evaluation
![](https://github.com/kg4sci/CataTQA/blob/main/images/evaluation.png)
![](https://github.com/kg4sci/CataTQA/blob/main/images/benchmark.png)
