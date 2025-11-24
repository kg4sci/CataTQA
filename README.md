# CataTQA
**CataTQA: A Benchmark for Tool-Augmented LLM Question Answering over Heterogeneous Catalysis Tables.**

## Abstact 
Despite their success in general question answering, large language models (LLMs) struggle with hallucinations and inaccurate reasoning in scientific domains. A major challenge stems from experimental data, which are often stored in external sources like supplementary materials and domain-specific databases. These tables are large, heterogeneous, and semantically complex, making them difficult for LLMs to interpret. While external tools show promise, current benchmarks fail to assess LLMs' ability to navigate this data—particularly in locating relevant tables, retrieving key columns, interpreting experimental conditions, and invoking tools.To address this gap, we introduce CataTQA, a new benchmark for catalytic materials. CataTQA features an automated dataset framework and four auxiliary tools. We evaluate tool-enhanced LLMs across five dimensions: table location, column retrieval, condition analysis, tool calling, and question answering, identifying their strengths and weaknesses.Our work sets a new benchmark for evaluating LLMs in scientific fields and paves the way for future advancements.

![](https://github.com/kg4sci/CataTQA/blob/main/images/main.png)

## Setup
To run our project, you need to first clone the project and use the following command to install dependencies.
```python
  pip install -r requirements.txt
```
## Download dataset
You can download our metadata and QA dataset through the following methods.   
  metadata: <https://huggingface.co/datasets/felix-hugweb/CataTQA_Metadata>
  dataset: <https://huggingface.co/datasets/felix-hugweb/CataTQA>

## Data source
We have retrieved data from multiple open-source databases. The following lists the top 9 categories of data with large volumes. For the complete data sources, please refer to the tabular metadata in our GitHub repository.

- Catalyst Acquisition by Data Science(CADS): An innovative web-based integrated catalyst informatics platform, Catalyst Acquisition by Data Science (CADS), is developed for use towards the discovery and design of catalysts.
- Catalytic Material Database(CMD): CMD contains material composition, properties, reactions, products and other information.
- Catalyst Hub: A featured database for surface reactions contains more than 100,000 chemisorption and reaction energies obtained from electronic structure calculations, and is continuously being updated with new datasets.
- Crystallography Open Database(COD): An open-access collection of crystal structures of organic, inorganic, metal-organic compounds and minerals.
- Materials Project: The Materials Project provides computed information on known and predicted materials as well as powerful analysis tools to inspire and design novel materials.
- 2DMatPedia dataset: DMatPedia dataset is a collection of 2D materials, contains 6351 materials.
- Alexandria_DB PBE 3D: A dataset of 2.5m+ stable and metastable materials calculated with the PBE functional.
- OQMD-3D dataset: The OQMD is a database of DFT calculated thermodynamic and structural properties of 1,226,781 materials, created in Chris Wolverton's group at Northwestern University.
  
## Config
To run our project, we need to configure our own API_KEY.
Open **utils/config.py** through a text editor.Modify the following code.
```python
API_KEY = 'YOUR_API_KEY'
MODEL = 'YOUR_MODEL_NAME'
```
## An example of a running result
**Just provide a question and run the tool/run. py program to automatically retrieve answers from all tables.**
```
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
```Annotate the table data, summarize the main problems that this table can solve and its contributions based on the content of the table data.
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
- Prompts for Table Order
```Please analyze the relevance of the table according to the problem.
    question:{question}
    Available tables and table descriptions:
    {table_desc}
    Please sort the tables by relevance from high to low, give the first five possible tables, and directly return the table name list.
    For example: ["table1", "table2"]
```
- Prompts for Column Selection
```Only provide the column names required to answer the question:
    question: {question}
    {table} information: [column]-[column name explanation]
    {table_field}
    directly return to the column name list, for example: ['col1','col2']
```

- Prompts for Condition Extraction
```Please extract the query criteria from the question and return the results according to the table structure:
    question: {question}
    table information:
    column name: [{tar}]
    Output requirements:
    1. Return to dictionary format, with the key being the column name and the value being the query condition
    2. The values corresponding to all column names must be output. The output not found in the problem is ''.
    3. Extract and preserve comparison symbols (>,<,=, etc.)
    4. example:{{"column1":">50", "column2":"Liming"}}
    Please return the JSON dictionary directly without including any other content
```

- Prompts for Tool Invocation
```Please use the tools needed to answer the questions according to the question analysis. 
    You need to specify the calculated column name when you need to perform calculation, but you do not need to specify it when you are performing table lookup.
    Question: {question}
    Description of available tools:
    {tool_desc}
    Please return the tool and column name to be used directly. For example: {{"tool":"","colnum name":""}}
```

- Tool Invocation
```Generate python code based on the question and given conditions, index CSV file data, and answer the question.
    Generate a function named "get_answer"(No parameters required). The function must use the "return" keyword to return the variable "answer", which is the answer to the question.
    question: {question['question']}
    refer_dataset: {question['refer_dataset']}
    column names: {question['column names']}
    condition: {question['condition']}
    Code must be used in markdown format("python").
    Do not return redundant content.The returned results must be saved in the "answer" variable.
```
## Verify the origin of the answer
To verify whether LLMs can answer relevant questions based on their own memorization, we conducted supplementary experiments. We directly input the questions into the large model and asked it to provide answers, then evaluated the accuracy of its responses. 

- Prompt
```Please provide the answer directly to the question without giving any explanation.
    question:{question}
    The output format is: {"answer": ""}
```
- Result

| Question Type       | Level   | ACC   | AVG ACC |
|---------------------|---------|-------|---------|
| Cell Query          | simple  | 0.004 | 0.002   |
|                     | complex | 0     |         |
| Fact Judgment       | simple  | 0.253 | 0.236   |
|                     | complex | 0.217 |         |
| Data Filtering      | simple  | 0     | 0       |
|                     | complex | 0     |         |
| Numerical Calculation | simple  | 0.034 | 0.056   |
|                     | complex | 0.094 |         |

## Alluvial plot of the Table Positioning Ability of Large Language Models

<img width="900" height="800" alt="image" src="https://github.com/user-attachments/assets/0984d991-e469-4bb2-9e84-9213a619ecc3" />


## Evaluation
We experimented with four proprietary LLMs on CataTQA, GPT-4o (gpt-4o-2024-11-20), DeepSeek V3 (deepseek-v3-250324), Claude-3 (claude-3-haiku-20240307) and Gemini-2.5 (gemini-2.5-flash-preview-04-17). For all experiments, we used the same hyperparameters and perform 0-shot prompting via the APIs.
![](https://github.com/kg4sci/CataTQA/blob/main/images/evaluation.png)
![](https://github.com/kg4sci/CataTQA/blob/main/images/benchmark.png)
