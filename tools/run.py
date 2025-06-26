import get_table
import get_field
import get_condition
import get_tool
import get_answer


questions = [
    "What is the hydrogen production rate (RH2) for a photocatalyst prepared using the Polymerized complex Sol-gel method method?",
    "What is the average hydrogen production rate for samples prepared using the Wet chemical reaction method?",
    "Which references report hydrogen production rates over 20 µmol h-1 g-1 using preparation method Template?",
    "Does calcination at 20 K for 3 hours optimize activity?"
]

for question in questions:
    table_rank = get_table.run(question)
    print(f"table_rank：{table_rank}")
    for table in table_rank[0:5]:
        column = get_field.run(question, table)
        condition = get_condition.run(question, column)
        tool = get_tool.run(question)
        answer = get_answer.run(table, column, condition, tool)
        print(f"select_table：{table}")
        print(f"get_field: {column}")
        print(f"get_condition: {condition}")
        print(f"get_tool: {tool}")
        print(f"get_answer: {answer}")

