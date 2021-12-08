@test.describe('Fixed Tests')
def fixed_tests():
    @test.it('Tests')
    def it_1():
        test.assert_equals(encode('hello'), 'h2ll4')
        test.assert_equals(encode('How are you today?'), 'H4w 1r2 y45 t4d1y?')
        test.assert_equals(encode('This is an encoding test.'), 'Th3s 3s 1n 2nc4d3ng t2st.')
        test.assert_equals(decode('h2ll4'), 'hello')

@test.describe('Random Tests')
def random_tests():
    from string import ascii_lowercase
    from random import choices, randint

    def randstr(options="", n=10): 
        return ''.join(choices(options, k=n))

    def solution_encode(st): 
        res = ''
        for c in st: 
            if c=='a': res += '1'
            elif c == 'e': res += '2'
            elif c == 'i': res += '3'
            elif c == 'o': res += '4'
            elif c == 'u': res += '5'
            else: res += c
        return res
        
    def solution_decode(st): 
        res = ''
        for c in st: 
            if c=='1': res += 'a'
            elif c == '2': res += 'e'
            elif c == '3': res += 'i'
            elif c == '4': res += 'o'
            elif c == '5': res += 'u'
            else: res += c
        return res

    @test.it('Encode')
    def it_1():
        for _ in range(100):
            s = randstr(options=ascii_lowercase, n=randint(10, 30))
            test.assert_equals(encode(s), solution_encode(s))

    @test.it('Decode')
    def it_2():
        valid = list(set(ascii_lowercase+'12345') - set('aeiou'))
        for _ in range(100):
            s = randstr(options=valid, n=randint(10, 30))
            test.assert_equals(decode(s), solution_decode(s))
