def check_choice(answer, reason, model_output):
    for c in model_output:
        if c.lower() in ['a','b','c','d']:
            return 1 if c.lower() == answer.lower() else 0
    return 0
