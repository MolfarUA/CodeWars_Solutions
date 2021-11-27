@test.describe('Example Tests')
def example_tests():
    @test.it('Example Test Case')
    def example_test_case():
        test.assert_equals(sp_eng("english"), True)
        test.assert_equals(sp_eng("egnlish"), False)
        test.assert_equals(sp_eng("1234egn lis;h"), False);
        test.assert_equals(sp_eng("1234english ;k"), True);
        test.assert_equals(sp_eng("English"), True);
        test.assert_equals(sp_eng("eNgliSh"), True);
        test.assert_equals(sp_eng("1234#$%%eNglish ;k9"), True);
        test.assert_equals(sp_eng("EGNlihs"), False);
        test.assert_equals(sp_eng("1234englihs**"), False);

    @test.it('Edge Test Case')
    def edge_test_case():
        test.assert_equals(sp_eng(""), False)


from random import choices, random, randint
import string

@test.describe('Random Tests')
def random_tests():

    def generate_random_case(bottom_size=0, top_size=100): 
        res = ''.join(choices(string.printable, k=randint(bottom_size, top_size)))
        if random() < 0.5: 
            res += 'english'
        res += ''.join(choices(string.printable, k=randint(bottom_size, top_size)))
        
        # swap case randomly
        res = ''.join(ch.upper() if random() < 0.5 else ch.lower() for ch in res)
        return res

    def _sp_eng_solution(sentence): 
        return 'english' in sentence.lower()

    def _do_one_test():
        sentence = generate_random_case()
        expected_solution = _sp_eng_solution(sentence)
        user_solution = sp_eng(sentence)
        test.assert_equals(user_solution, expected_solution)

    @test.it('Random Test Cases')
    def random_test_cases():
        for _ in range(100):
            _do_one_test()
