a = {'Mike':'aye','Joe':'aye','Johnson':'aye','Peter':'aye'}
b = {'Mike':'aye','Joe':'nay','Johnson':'aye','Peter':'aye'}
test.assert_equals(cannons_ready(a),'Fire!')
test.assert_equals(cannons_ready(b),'Shiver me timbers!')

test.describe("Random Tests")
test.assert_equals(cannons_ready(a),'Fire!')

from random import randint
for x in range(15):
    load = randint(0,1)
    r = {'Mike':('aye' if load==1 else 'nay'),'Joe':'aye','Johnson':'aye','Peter':'aye'}
    if sum( x == 'aye' for x in r.values() )==len(r):ans = 'Fire!'
    else: ans = 'Shiver me timbers!'
    test.assert_equals(cannons_ready(r),ans)
    
for x in range(12):
    load = randint(0,1)
    r = {'Johnson':('aye' if load==1 else 'nay'),'Peter':'aye'}
    if sum( x == 'aye' for x in r.values() )==len(r):ans = 'Fire!'
    else: ans = 'Shiver me timbers!'
    test.assert_equals(cannons_ready(r),ans)
    
for x in range(17):
    load = randint(0,1)
    r = {'Mike':'aye','Joe':('aye' if load==1 else 'nay'),'Johnson':'aye'}
    if sum( x == 'aye' for x in r.values() )==len(r):ans = 'Fire!'
    else: ans = 'Shiver me timbers!'
    test.assert_equals(cannons_ready(r),ans)
    
test.assert_equals(cannons_ready(a),'Fire!')
test.assert_equals(cannons_ready({'Joe':'nay','Johnson':'nay','Peter':'aye'}),'Shiver me timbers!')
print('Yar! Victory be yours! Check out the next kata in description')
