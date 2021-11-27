def valid_parentheses(string):
    unmatched_opens = 0

    for character in string:
        if character == "(":
            unmatched_opens += 1
        elif character == ")":
            if unmatched_opens > 0:
                unmatched_opens -= 1
            else:
                return False

    return unmatched_opens == 0
