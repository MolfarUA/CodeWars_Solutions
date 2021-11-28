import re

def increment_string(strng):
    if re.search(r"(\d+)$", strng) is not None:
        strng = re.sub(r"(\d+)$", lambda x: str(int(x.group(1)) + 1).zfill(len(x.group(1))), strng)
    else:
        strng += "1"

    return strng
