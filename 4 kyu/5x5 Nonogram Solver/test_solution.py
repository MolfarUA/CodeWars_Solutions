import random


test.describe('Basic tests')


def sample_tests():
    test.it('Sample cases')

    clues = (((1, 1), (4,), (1, 1, 1), (3,), (1,)),
              ((1,), (2,), (3,), (2, 1), (4,)))
    
    ans = ((0, 0, 1, 0, 0),
           (1, 1, 0, 0, 0),
           (0, 1, 1, 1, 0),
           (1, 1, 0, 1, 0),
           (0, 1, 1, 1, 1))
    
    test.assert_equals(Nonogram(clues).solve(), ans)
    
    
    clues = (((1,), (3,), (1,), (3, 1), (3, 1)),
              ((3,), (2,), (2, 2), (1,), (1, 2)))
    
    ans = ((0, 0, 1, 1, 1),
           (0, 0, 0, 1, 1),
           (1, 1, 0, 1, 1),
           (0, 1, 0, 0, 0),
           (0, 1, 0, 1, 1))
    
    test.assert_equals(Nonogram(clues).solve(), ans)


def rand_tests():
    test.it('Random tests')

    test1 = [(((2,), (3,), (4,), (1, 1), (1, 1)),
              ((2,), (3, 1), (3,), (1, 1), (2,))),
             ((1, 1, 0, 0, 0),
              (1, 1, 1, 0, 1),
              (0, 1, 1, 1, 0),
              (0, 0, 1, 0, 1),
              (0, 0, 1, 1, 0))]
    test2 = [(((1, 1), (1, 1), (4,), (3,), (1, 1)),
              ((3,), (1, 1), (2,), (3,), (2, 1))),
             ((1, 1, 1, 0, 0),
              (0, 0, 1, 0, 1),
              (0, 0, 1, 1, 0),
              (0, 0, 1, 1, 1),
              (1, 1, 0, 1, 0))]
    test3 = [(((3,), (4,), (1, 3), (1,), (1,)),
              ((1, 1, 1), (2,), (3,), (2,), (3,))),
             ((1, 0, 1, 0, 1),
              (1, 1, 0, 0, 0),
              (1, 1, 1, 0, 0),
              (0, 1, 1, 0, 0),
              (0, 1, 1, 1, 0))]
    test4 = [(((4,), (4,), (1,), (1,), (3,)),
              ((2,), (2,), (2, 2), (3, 1), (1,))),
             ((1, 1, 0, 0, 0),
              (1, 1, 0, 0, 0),
              (1, 1, 0, 1, 1),
              (1, 1, 1, 0, 1),
              (0, 0, 0, 0, 1))]
    test5 = [(((1, 3), (2,), (2,), (1, 1), (3,)),
              ((1, 2), (1,), (1, 1), (3,), (4,))),
             ((1, 0, 0, 1, 1),
              (0, 0, 0, 0, 1),
              (1, 0, 0, 0, 1),
              (1, 1, 1, 0, 0),
              (1, 1, 1, 1, 0))]
    test6 = [(((3,), (2,), (1, 1), (2,), (4,)),
              ((2,), (3, 1), (1, 2), (3,), (1,))),
             ((1, 1, 0, 0, 0),
              (1, 1, 1, 0, 1),
              (1, 0, 0, 1, 1),
              (0, 0, 1, 1, 1),
              (0, 0, 0, 0, 1))]
    test7 = [(((2, 2), (2,), (3,), (1,), (3,)),
              ((1, 1, 1), (3, 1), (4,), (1,), (1,))),
             ((1, 0, 1, 0, 1),
              (1, 1, 1, 0, 1),
              (0, 1, 1, 1, 1),
              (1, 0, 0, 0, 0),
              (1, 0, 0, 0, 0))]
    test8 = [(((1, 1), (1, 1), (3,), (3,), (3,)),
              ((1,), (2,), (4,), (3,), (3,))),
             ((1, 0, 0, 0, 0),
              (0, 0, 0, 1, 1),
              (0, 1, 1, 1, 1),
              (0, 0, 1, 1, 1),
              (1, 1, 1, 0, 0))]
    test9 = [(((3,), (2,), (3,), (2,), (1, 2)),
              ((1,), (3,), (3,), (3, 1), (1, 1))),
             ((0, 0, 0, 1, 0),
              (0, 0, 1, 1, 1),
              (1, 1, 1, 0, 0),
              (1, 1, 1, 0, 1),
              (1, 0, 0, 0, 1))]
    test10 = [(((3,), (2, 2), (1,), (2,), (3,)),
               ((4,), (1, 2), (1, 1), (2,), (2,))),
              ((0, 1, 1, 1, 1),
               (0, 1, 0, 1, 1),
               (1, 0, 0, 0, 1),
               (1, 1, 0, 0, 0),
               (1, 1, 0, 0, 0))]
    test11 = [(((4,), (4,), (1,), (2,), (2,)),
               ((3,), (2, 2), (2,), (2,), (2,))),
              ((0, 0, 1, 1, 1),
               (1, 1, 0, 1, 1),
               (1, 1, 0, 0, 0),
               (1, 1, 0, 0, 0),
               (1, 1, 0, 0, 0))]
    test12 = [(((1,), (2,), (3,), (1, 3), (3,)),
               ((1, 1), (3,), (3,), (3,), (2,))),
              ((0, 1, 0, 1, 0),
               (1, 1, 1, 0, 0),
               (0, 0, 1, 1, 1),
               (0, 0, 1, 1, 1),
               (0, 0, 0, 1, 1))]
    test13 = [(((3,), (4,), (3,), (2,), (1,)),
               ((3,), (3,), (3,), (2,), (2,))),
              ((0, 0, 1, 1, 1),
               (0, 1, 1, 1, 0),
               (1, 1, 1, 0, 0),
               (1, 1, 0, 0, 0),
               (1, 1, 0, 0, 0))]
    test14 = [(((1,), (2,), (2, 2), (1, 1, 1), (3,)),
               ((3,), (1, 1), (2,), (3,), (3,))),
              ((0, 0, 1, 1, 1),
               (0, 0, 1, 0, 1),
               (0, 0, 0, 1, 1),
               (1, 1, 1, 0, 0),
               (0, 1, 1, 1, 0))]
    test15 = [(((1,), (1,), (3, 1), (2, 2), (1, 2)),
               ((4,), (3,), (1,), (2,), (3,))),
              ((1, 1, 1, 1, 0),
               (0, 0, 1, 1, 1),
               (0, 0, 1, 0, 0),
               (0, 0, 0, 1, 1),
               (0, 0, 1, 1, 1))]
    test16 = [(((3, 1), (2,), (2,), (1, 1), (3,)),
               ((4,), (3,), (1, 1), (1,), (1, 2))),
              ((1, 1, 1, 1, 0),
               (1, 1, 1, 0, 0),
               (1, 0, 0, 0, 1),
               (0, 0, 0, 0, 1),
               (1, 0, 0, 1, 1))]
    
    TESTS = [test1, test2, test3, test4,
             test5, test6, test7, test8,
             test9, test10, test11, test12,
             test13, test14, test15, test16]
    random.shuffle(TESTS)

    for t in TESTS:
        test.assert_equals(Nonogram(t[0]).solve(), t[1])

sample_tests()
rand_tests()
