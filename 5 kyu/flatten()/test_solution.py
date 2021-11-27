@test.describe('Full Test Suite')
def run_full_test():
    @test.it('Basic tests')
    def basic_tests():
        test.assert_equals(flatten(),[])
        test.assert_equals(flatten(1,2,3),[1,2,3])
        test.assert_equals(flatten(1,2),[1,2])
        test.assert_equals(flatten(5,'string'),[5,'string'])
        test.assert_equals(flatten(-4.5,-3,1,4),[-4.5,-3,1,4])
    
    @test.it('2D arrays')
    def two_d_tests():
        test.assert_equals(flatten([3,4,5],[1,2,3]),[3,4,5,1,2,3])
        test.assert_equals(flatten([1],[],2,[4,5,6]),[1,2,4,5,6])
        test.assert_equals(flatten([4,"string",9,3,1],[],[],[],[],["string"]),[4,"string",9,3,1,"string"])
        
    @test.it('Deeper nested arrays')
    def deeper_tests():
        test.assert_equals(flatten(1,2,['9',[],[]],None),[1,2,'9',None])
        test.assert_equals(flatten([1,2],[3,4,5],[6,[7],[[8]]]),[1,2,3,4,5,6,7,8])
        test.assert_equals(flatten(['hello',2,['text',[4,5]]],[[]],'[list]'),['hello',2,'text',4,5,'[list]'])
    
    @test.it('More fixed tests')
    def bigger_tests():
        test.assert_equals(
            flatten([[[[['b`|}.d+.LQ<F']]]]], [[[[[[[6726]], ['b`|}.d+.LQ<F']], [7939]]]]], [[[[7939]]]], [[[[2037, [7939]]]]], [[[[[[['zuj# ?']], [7939]]], [-502]]]], [[[-502], [1798]]], [[1798]], [[[[[[-4997]]]], [1798]]], [[[[[[9449]]], [1798]], [2231]]], [[2231]], [[[[[';Se[0*vxFcnRsND']]], [2231]]]),
            ['b`|}.d+.LQ<F', 6726, 'b`|}.d+.LQ<F', 7939, 7939, 2037, 7939, 'zuj# ?', 7939, -502, -502, 1798, 1798, -4997, 1798, 9449, 1798, 2231, 2231, ';Se[0*vxFcnRsND', 2231])
        test.assert_equals(
            flatten(' RhD):vR+Ue}', '2K+),un', 6281, None, [[[[['d%;nPxZw<3N*m!n!$:m{9l#sF\'a"SDan_"K']]]]]),
            [' RhD):vR+Ue}', '2K+),un', 6281, None, 'd%;nPxZw<3N*m!n!$:m{9l#sF\'a"SDan_"K'])
        test.assert_equals(
            flatten([[6178], [-4570]], [-4570], [[[-6803]], [-4570]], [[[[5498]], [-4570]]], [[[[None], [-4570]]]], [[[['v/M[Bv#/.vx9k0x<3?.FdqF"4Jf\'`O6U,tqfGV\'', [-4570]]]]], [[[[[['~nKjizLQ()?5w;&}P|~`<1HB*rP\\k)=3t.wzb'], [-4570]]], [2343]]]], [[[2343]]], [[[597, [2343]]]], [[[[[[['aw#|Tc)iCS5S']]], [2343]], [None]]]], [[[None], [-4441]]], [[-4441]], [[[[None]], [-4441]]], [[[[[[['2*V!]U<_0]a(`=v`}]@)GHg|B.b-Lu^-R']]]], [-4441]]]], [[[[[[-9991]], [-4441]], [1761]]]], [[[1761]]], [[[[[['|qs{LnFQ>hb@:kfFU0cHh05&s$$bnBTFrGA*JIO0Zfq>']]], [1761]]]], [[[['(@(?q@|2#f2FD}[g`\\Km/v+_+L=R]J+6+A', [1761], [1472]]]]], [[[[1472]]]], [[[[[['`q+?{UMnIMa"^pb?2/j)$LvYZU`J`bo\\e8qp2u1tM&x\'%Q0C']], [1472]]]]]),
            [6178, -4570, -4570, -6803, -4570, 5498, -4570, None, -4570, 'v/M[Bv#/.vx9k0x<3?.FdqF"4Jf\'`O6U,tqfGV\'', -4570, '~nKjizLQ()?5w;&}P|~`<1HB*rP\\k)=3t.wzb', -4570, 2343, 2343, 597, 2343, 'aw#|Tc)iCS5S', 2343, None, None, -4441, -4441, None, -4441, '2*V!]U<_0]a(`=v`}]@)GHg|B.b-Lu^-R', -4441, -9991, -4441, 1761, 1761, '|qs{LnFQ>hb@:kfFU0cHh05&s$$bnBTFrGA*JIO0Zfq>', 1761, '(@(?q@|2#f2FD}[g`\\Km/v+_+L=R]J+6+A', 1761, 1472, 1472, '`q+?{UMnIMa"^pb?2/j)$LvYZU`J`bo\\e8qp2u1tM&x\'%Q0C', 1472])
        test.assert_equals(
            flatten([[[[[[[-7423]]]]]], [None]], [None], [[[[[[[[[['<PRDX[%~y,:H%.)6^I=twt']]]]]]]]], [None]], [[[[[[[[[[[[[[[[[[[[[None]]]]]]]]]]]]]]]]]]], [None]]], [[[[[[[[[[[[[[[[[[[[[[[[None]]]]]]]]]]]]]]]]]]]]], [None]]]], [[[[[[['KND;F(Ql']]], [None]]]]], [[[[[[None], [None]]]]]], [[[[[[[[[[[[[[[[[[[[[6499]]]]]]]]]]]]]]], [None]]]], [-8173]]]], [[[-8173]]], [[[[[[['q}z\\n%A=u8L:IJBbP']]]], [-8173]]]], [[[[[[[[[[[[[[[[[[[[[None]]]]]]]]]]]]]]]]], [-8173]]]]], [[[[[[[[[[[[[[[[[[[-5346]]]]]]]]]]]]]], [-8173]]]]]], [[[[[[[[[[[[[[-1369]]]]]]]], [-8173]]]]]]], None, [[[[[[[[[[[[['0 4Mw#"C']]]]]]]]]]]]], [[[[[[[[[[[[[[['BZ?G/5YVFY%i']], ['0 4Mw#"C']]]]]]]]]]]]]]),
            [-7423, None, None, '<PRDX[%~y,:H%.)6^I=twt', None, None, None, None, None, 'KND;F(Ql', None, None, None, 6499, None, -8173, -8173, 'q}z\\n%A=u8L:IJBbP', -8173, None, -8173, -5346, -8173, -1369, -8173, None, '0 4Mw#"C', 'BZ?G/5YVFY%i', '0 4Mw#"C'])
        test.assert_equals(
            flatten([[[[[[[[[[[[[[[[[[[[[[[['6)n"R?1Pw}q3+K$<D@Tin><wMGX406#){OQ`qrwfE(=']]]]]]]]]]]]]]]]]]]]], ['9,P|?ML]KJw(n7_uxB`']]]], [[['9,P|?ML]KJw(n7_uxB`']]], [[[[[[[[[[[[[[[['W!hJoL%']]]]]]]]]]]]], ['9,P|?ML]KJw(n7_uxB`']]]], [[[[[[[[[[[[[[[["K'~awsc{tAezEeAZ`PJ["]]]]]]]]]]]], ['9,P|?ML]KJw(n7_uxB`']]]]], [[[[[[[[[[[[[[[[[[[[[[[[[-244]]]]]]]]]]]]]]]]]]]], ['9,P|?ML]KJw(n7_uxB`']]]]]], [[[[[[[[[[[[[[['$\\h"IS$"\'$MMuuu?I@_hYV$laR*SbZ']]]]]]]]], ['9,P|?ML]KJw(n7_uxB`']]]]]]], [[[[[[[[[[[[[[[[['<8\\LNV{"']]]]]]]]]], ['9,P|?ML]KJw(n7_uxB`']]]]]]]], [[[[[[[[[[[[[[[[[[[[[[[[['h-PJ#fTCb7;l[zz3&nm\\nEf6?[.hPtZiD"1{clH:F:}^>*z|']]]]]]]]]]]]]]]]], ['9,P|?ML]KJw(n7_uxB`']]]]]]]]], [[[[[[[[[[[[[[[[[[[[[[[9751]]]]]]]]]]]]]], ['9,P|?ML]KJw(n7_uxB`']]]]]]]]]], [[[[[[[[[[[[-3839]], ['9,P|?ML]KJw(n7_uxB`']]]]]]]]]]]),
            ['6)n"R?1Pw}q3+K$<D@Tin><wMGX406#){OQ`qrwfE(=', '9,P|?ML]KJw(n7_uxB`', '9,P|?ML]KJw(n7_uxB`', 'W!hJoL%', '9,P|?ML]KJw(n7_uxB`', "K'~awsc{tAezEeAZ`PJ[", '9,P|?ML]KJw(n7_uxB`', -244, '9,P|?ML]KJw(n7_uxB`', '$\\h"IS$"\'$MMuuu?I@_hYV$laR*SbZ', '9,P|?ML]KJw(n7_uxB`', '<8\\LNV{"', '9,P|?ML]KJw(n7_uxB`', 'h-PJ#fTCb7;l[zz3&nm\\nEf6?[.hPtZiD"1{clH:F:}^>*z|', '9,P|?ML]KJw(n7_uxB`', 9751, '9,P|?ML]KJw(n7_uxB`', -3839, '9,P|?ML]KJw(n7_uxB`'])
    
    @test.it('Random tests')
    def random_tests():
        from random import randrange,choice
        RR = lambda x=2,*z: randrange(x,*z)
        
        # REFERENCE SOLUTION
        def ref_func(*r):
            flat_inner = []
            for val in r:
                if isinstance(val, list):
                    flat_inner.extend(ref_func(*val))
                else:
                    flat_inner.append(val)
            return flat_inner
        
        # RANDOM TEST GENERATOR FUNCTIONS
        def rand_string():
            char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890!@#$%^&*()<>,.?;:[]'
            return ''.join(char_list[RR(len(char_list))] for _ in range(2,20))
        
        def rand_int():
            return RR(1000000)
        
        def rand_other():
            return choice([None,[],True,False])
        
        def gen_test(q,n):
            r = []
            ct = 0
            for _ in range(q):
                if RR(3) or n > 15:
                    next_elem = (rand_string,rand_int,rand_other)[RR(3)]()
                    ct += 1
                else:
                    next_elem,qq = gen_test(RR(max(2,q-ct)),n+1)
                    ct += qq
                r.append(next_elem)
                if ct > q: break
            return (r,ct)
        
        for i in range(100):
            v,_ = gen_test(RR(5,36),0)
            test.assert_equals(flatten(*v),ref_func(*v))
