def get_turkish_number(x): 
    birler=["","bir","iki","üç","dört","beş","altı","yedi","sekiz","dokuz"]
    onlar=["","on ","yirmi ","otuz ","kırk ","elli ","altmış ","yetmiş ","seksen ","doksan "]
    numbers=["sıfır"]
    for i in onlar:
        for j in birler:
            numbers.append((i+j))
    del numbers[1]
    return(numbers[x].rstrip())
