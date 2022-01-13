def stock_list(listOfArt, listOfCat):
    if (len(listOfArt) == 0) or (len(listOfCat) == 0):
        return ""
    result = ""
    for cat in listOfCat:
        total = 0
        for book in listOfArt:
            if (book[0] == cat[0]):
                total += int(book.split(" ")[1])
        if (len(result) != 0):
            result += " - "
        result += "(" + str(cat) + " : " + str(total) + ")"
    return result
________________________________________
from collections import Counter

def stock_list(listOfArt, listOfCat):
    if not listOfArt:
        return ''
    codePos = listOfArt[0].index(' ') + 1
    cnt = Counter()
    for s in listOfArt:
        cnt[s[0]] += int(s[codePos:])
    return ' - '.join('({} : {})'.format(cat, cnt[cat]) for cat in listOfCat)
________________________________________
def stock_list(stocklist, categories):
    if not stocklist or not categories:
        return ""
    return " - ".join(
        "({} : {})".format(
            category,
            sum(int(item.split()[1]) for item in stocklist if item[0] == category))
        for category in categories)
________________________________________
def stock_list(listOfArt, listOfCat):
    if listOfArt and listOfCat:
        return " - ".join(['(%s : %d)' % (c, sum([int(i.split(" ")[1]) for i in listOfArt if c==i[0]])) for c in listOfCat])
    else:
        return ""
________________________________________
def stock_list(l, m):
    if len(l) == 0 or len(m) == 0:
        return ''
        
    result = {}
    
    for category in m:
        result[category] = 0
        
    for pair in l:
        if pair[0] in result:
            result[pair[0]] += int(pair.split()[1])
    
    return ' - '.join([f'({key} : {value})' for (key, value) in result.items()])
________________________________________
from collections import defaultdict
from typing import List


def stock_list(list_of_art: List[str], list_of_cat: List[str]) -> str:
    if not list_of_art or not list_of_cat:
        return ""

    cats = defaultdict(int)
    for a in list_of_art:
        cats[a[0]] += int(a.split()[1])

    return ' - '.join(f"({c} : {cats[c]})" for c in list_of_cat)
________________________________________
def stock_list(listOfArt, listOfCat):   
    
    # Nothing check
    if not listOfArt or not listOfCat:
        return ''
    
    stock, result = [], {}
    
    # format the art array into [string, int] pairs - (stock array)
    for i in listOfArt:
        entry = i.split(" ")
        stock.append( [entry[0], int(entry[1])] )    
        
    # Search first letters in stock array for matches.
    # If we find one, find a key in result. 
    # If not there make one, then add the value from the stock if its there
    for search in listOfCat:
        if search[0] not in result:
            result[search[0]] = 0
        for art in stock:
            if search[0] == art[0][0]:
                result[search[0]] += art[1]
    return " - ".join(["({0} : {1})".format(k, v) for (k, v) in result.items() ])
________________________________________
def stock_list(listOfArt, listOfCat):
    """Return a the number of books by category in a formatted way

    Args:
        listOfArt (tuple or list): list of book codes
        listOfCat (tuple or list): list of categories

    Returns:
        str: number of books by category in the format '<category> : <number of books> - ...'
    """
    if len(listOfArt) == 0 or listOfCat == 0:
        return ''
        
    books = {} 
    for code in listOfArt:
        book = code.split() 
        if book[0][0] in books: 
            books[book[0][0]] += int(book[1])
        else:
            books[book[0][0]] = int(book[1])
    result = []
    for cat in listOfCat:
        num = books[cat] if cat in books else 0
        result.append('({} : {})'.format(cat, num))
    return ' - '.join(result)
________________________________________
def stock_list(a, c):
    return ' - '.join(["({} : {})".format(cat,sum([int(s.split()[1]) for s in a if s.split()[0][0]==cat])) for cat in c]) if a else ''
    
