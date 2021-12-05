test.describe('what_is')
test.it('should work correctly')
tests = [
    (0, 'nothing'),
    (123, 'nothing'),
    (-1, 'nothing'),
    (42, 'everything'),
    (42 * 42, 'everything squared'),
]
for x, answer in tests:
    test.assert_equals(what_is(x), answer)
