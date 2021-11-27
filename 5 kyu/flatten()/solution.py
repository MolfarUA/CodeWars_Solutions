def flatten(*args):
    final_list= []

    for i in args:
        if isinstance(i, list):
            final_list += flatten(*i)
        else:
            final_list.append(i)

    return final_list
