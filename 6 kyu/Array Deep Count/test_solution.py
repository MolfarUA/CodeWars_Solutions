test.describe('Basic Tests')
test.assert_equals(deep_count([]), 0, "Expected 0")
test.assert_equals(deep_count([1, 2, 3]), 3, "Expected 3")
test.assert_equals(deep_count(["x", "y", ["z"]]), 4, "Expected 4")
test.assert_equals(deep_count([1, 2, [3, 4, [5]]]), 7, "Expected 7")
test.assert_equals(deep_count([[[[[[[[[]]]]]]]]]), 8, "Expected 8")

test.describe('Advanced Tests')
test.assert_equals(deep_count(['a']), 1, "Expected 1")
test.assert_equals(deep_count([['a']]), 2, "Expected 2")
test.assert_equals(deep_count([['a'], []]), 3, "Expected 3")
test.assert_equals(deep_count(['[a]']), 1, "Expected 1")
test.assert_equals(deep_count([[[[[[[[['Everybody!']]]]]]]]]), 9, "Expected 9")
test.assert_equals(deep_count(['cat', [['dog']], ['[bird]']]), 6, "Expected 6")
