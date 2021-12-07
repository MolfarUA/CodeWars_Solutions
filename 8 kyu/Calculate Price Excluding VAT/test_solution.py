# for backward compatibility
try:
    excluding_vat_price = excludingVatPrice
except NameError:
    pass

test.describe('Fixed Tests')
test.assert_equals(excluding_vat_price(230.00), 200.00)
test.assert_equals(excluding_vat_price(123), 106.96)
test.assert_equals(excluding_vat_price(777), 675.65)
test.assert_equals(excluding_vat_price(460.00), 400.00)
test.assert_equals(excluding_vat_price(None), -1)

test.describe('Random Tests')
from random import randint

for _ in range(100):
    test_price = randint(50, 5000) / 100
    expected_price = round(test_price/1.15, 2)
    test.it('Testing: %.2f, expecting: %.2f' % (test_price, expected_price))
    test.assert_equals(excluding_vat_price(test_price), expected_price)
