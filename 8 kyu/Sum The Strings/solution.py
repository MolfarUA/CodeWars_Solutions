def sum_str(a, b):
    if a == "" and b != "":
        return f'{b}'
    if a != "" and b == "":
        return f'{a}'
    if a == "" and b == "":
        return f'0'
    return f'{int(a) + int(b)}'
