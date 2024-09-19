53f40dff5f9d31b813000774

def recover_secret(triplets):
    risultato = []
    
    for tripletta in triplets:
        i = 0
        while(i < 3):
            lettera = tripletta[i]
            j = 0
            while(j < len(triplets)):
                if(lettera in triplets[j]):
                    for c in triplets[j]:
                        if(c == lettera):
                            break
                        elif(c not in risultato):
                            lettera = c
                            j = -1
                            break
                j += 1
            if(lettera not in risultato):
                risultato.append(lettera)
                i -= 1
            i += 1
        
    return "".join(risultato)

#######################################
def recover_secret(triplets):
    dict = {}
    for triplet in triplets:
        for j, letter in enumerate(triplet):
            if letter not in dict.keys():
                dict[letter] = []
            dict[letter] += triplet[j+1:]
    output = list(dict.keys())
    sorted_chars = []
    for i in range(0, 5):
        for letter in list(dict.keys()):
            indx = output.index(letter)
            LHS = output[:indx]
            for p, itm in enumerate(LHS):
                if itm in dict[letter]:
                    output.insert(p, letter)
                    del output[indx+1]
                    break
    return ''.join(output)

#######################################
from collections import defaultdict

def recover_secret(triplets):
    # Create a graph where each letter is a node
    graph = defaultdict(set)
    # Keep track of all unique letters
    letters = set()
    
    # Build the graph
    for triplet in triplets:
        for i in range(2):
            graph[triplet[i]].add(triplet[i+1])
        letters.update(triplet)
    
    # Function to perform DFS
    def dfs(node, visited, result):
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                dfs(neighbor, visited, result)
            result.append(node)
    
    # Perform topological sort
    visited = set()
    result = []
    for letter in letters:
        dfs(letter, visited, result)
    
    # Return the reversed result (as we appended in reverse order)
    return ''.join(result[::-1])

##################################
def recover_secret(triplets):
    pass # triplets is a list of triplets from the secrent string. Return the string.def recover_secret(triplets):
    characters = list(set([char for triplet in triplets for char in triplet]))

    secret = []

    while characters:
        for char in characters:
            if all((len(triplet) < 2 or char != triplet[1]) and (len(triplet) < 3 or char != triplet[2]) for triplet in
                   triplets):

                secret.append(char)
                characters.remove(char)

                triplets = [[c for c in triplet if c != char] for triplet in triplets]

                triplets = [triplet for triplet in triplets if triplet]

                break

    return ''.join(secret)
