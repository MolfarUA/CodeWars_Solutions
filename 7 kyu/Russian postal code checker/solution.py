import re

def zipvalidate(postcode):
    return bool(re.fullmatch('[12346]\d{5}', postcode))
