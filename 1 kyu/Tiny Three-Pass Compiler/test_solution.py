prog = '[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)';
t1 = {'op':'/','a':{'op':'-','a':{'op':'+','a':{'op':'*','a':{'op':'*','a':{'op':'imm','n':2},'b':{'op':'imm','n':3}},'b':{'op':'arg','n':0}},'b':{'op':'*','a':{'op':'imm','n':5},'b':{'op':'arg','n':1}}},'b':{'op':'*','a':{'op':'imm','n':3},'b':{'op':'arg','n':2}}},'b':{'op':'+','a':{'op':'+','a':{'op':'imm','n':1},'b':{'op':'imm','n':3}},'b':{'op':'*','a':{'op':'imm','n':2},'b':{'op':'imm','n':2}}}};
t2 = {'op':'/','a':{'op':'-','a':{'op':'+','a':{'op':'*','a':{'op':'imm','n':6},'b':{'op':'arg','n':0}},'b':{'op':'*','a':{'op':'imm','n':5},'b':{'op':'arg','n':1}}},'b':{'op':'*','a':{'op':'imm','n':3},'b':{'op':'arg','n':2}}},'b':{'op':'imm','n':8}};

c = Compiler()

p1 = c.pass1(prog)
test.assert_equals(p1, t1, 'Pass1')

p2 = c.pass2(p1)
test.assert_equals(p2, t2, 'Pass2')

p3 = c.pass3(p2)
test.assert_equals(simulate(p3, [4,0,0]), 3, 'prog(4,0,0) == 3')
test.assert_equals(simulate(p3, [4,8,0]), 8, 'prog(4,8,0) == 8')
test.assert_equals(simulate(p3, [4,8,16]), 2, 'prog(4,8,6) == 2')

order_of_ops_prog = '[ x y z ] x - y - z + 10 / 5 / 2 - 7 / 1 / 7'
order_of_ops = c.pass3(c.pass2(c.pass1(order_of_ops_prog)))
test.assert_equals(simulate(order_of_ops, [5,4,1]), 0, order_of_ops_prog + ' @ [5,4,1]')
