def get_count(input_str):
    return (sum(input_str.count(items) for items in ("a","e","i","o","u")))
