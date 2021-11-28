def solution (string):
    return string[::-1]

def tests():
    if solution ('workd') != 'dlrow':
        print ('Not correct')
    if solution('hello') != 'olleh':
        print ('Not correct')

tests()
