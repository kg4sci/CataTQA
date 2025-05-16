""" executable code """

def exec_code(question, code):
    local_var = {}
    exec(code, local_var)
    rand_func = local_var["get_answer"]
    question['code_answer'] = rand_func()
    return question