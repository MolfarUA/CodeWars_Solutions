@test.describe('Fixed tests')
def fixed_tests():
    class U:
        def __init__(self, x=0):
            self.x = x.x if isinstance(self, x.__class__) else x
        def f(self, y):
            return self.x + y
    
    @change_detection
    class Struct:
        x = 42
        no = None
        def __init__(self, y=0):
            self.y = y
            self.u = U(4)
            self.uuu = None
        def f(self):
            if self.tt.get_change:
                self.tt += 1
            else:
                self.tt = 0
    
    a = Struct(11)
    
    @test.it('Object attributes')
    def it_1():
        test.assert_equals(a.y, 11, 'Instance attribute has a correct value')
        test.assert_equals(a.y.get_change, 'INIT', 'Initial state is correct')
        test.assert_equals(2 * a.y + 20, 42, 'Integer attributes should work as integers')
        a.y = 11
        msg = "The state doesn't change if the same value is assigned"
        test.assert_equals(a.y.get_change, 'INIT', msg)
        a.y = 12
        test.assert_equals(a.y.get_change, 'MOD', 'Attribute was modified')
        a.y = 12
        msg = 'Modified attribute was assigned the same value again'
        test.assert_equals(a.y.get_change, 'MOD', msg)
        del a.y
        test.assert_equals(a.y.get_change, 'DEL', 'Attribute was deleted')
    
    @test.it('Class attributes')
    def it_2():
        test.assert_equals(Struct.x, 42, 'Class attribute has a correct values')
        test.assert_equals(a.x, 42, 'Class attribute has a correct values')
        test.assert_equals(a.x.get_change, 'INIT', 'Initial state is correct')
        a.y = 12
        test.assert_equals(a.x - a.y, 30, 'Integer attributes should work as integers')
        a.x = '42'
        msg = 'Class attribute was changed on an instance'
        test.assert_equals(a.x, '42', msg)
        test.assert_equals(a.x.get_change, 'MOD', msg)
        test.assert_equals(a.x+'1', '421', 'String attributes should work as strings')
        del a.x
        msg = 'Class attribute was deleted on an instance'
        test.expect((a.x == 42 and a.x.get_change == 'INIT') or
                     (not a.x and a.x.get_change == 'DEL'), msg)
    
    @test.it('Undefined attributes')
    def it_3():
        test.assert_equals(a.z.get_change, '', 'Non-existent attribute has no state')
        test.assert_equals(a._mumu_.get_change, '', 'Non-existent attribute has no state')
        msg = 'No state should be assigned after trying to access it once'
        test.assert_equals(a._mumu_.get_change, '', msg)
    
    @test.it('When attribute is from Final class (None, bool)')
    def it_4():
        msg = "Value of None should equal to None. You can use predefined NONE."
        test.assert_equals(a.uuu, None, msg)
        msg = "None attributes should also support 'get_change'. Have you tried NONE?"
        test.assert_equals(a.uuu.get_change, 'INIT', msg)
        a.uuu = None
        msg = 'None was assigned to a None attribute'
        test.assert_equals(a.uuu, None, msg)
        test.assert_equals(a.uuu.get_change, 'INIT', msg)
        a.uuu = False
        msg = 'False was assigned to a None attribute'
        test.assert_equals(a.uuu, False, msg)
        test.assert_equals(a.uuu.get_change, 'MOD', msg)
        a.uuu = None
        msg = 'None was assigned to a None attribute back'
        test.assert_equals(a.uuu, None)
        test.assert_equals(a.uuu.get_change, 'MOD')
        test.assert_equals(Struct.no, None, 'None class attribute is None')
        test.assert_equals(a.no, None, 'None class attribute is also None on an instance')
        test.assert_equals(a.no.get_change, 'INIT', 'Initial state is correct')
        a.no = None
        msg = 'None was assigned to a None class attribute on the instance'
        test.assert_equals(a.no.get_change, 'INIT', msg)
        a.no = 0
        msg = '0 was assigned to a None class attribute on the instance'
        test.assert_equals(a.no, 0, msg)
        test.assert_equals(a.no.get_change, 'MOD', msg)
    
    @test.it('An instance of one class is an attribute of another class')
    def it_5():
        msg = "The instance's attribute has a correct value"
        test.assert_equals(a.u.x, 4, msg)
        msg = "The instance's state is correct"
        test.assert_equals(a.u.get_change, 'INIT', msg)
        msg = "The instance's method returns a correct value"
        test.assert_equals(a.u.f(10), 14, msg)
        msg = "The instance's state didn't change after its attributes were modified"
        test.assert_equals(a.u.get_change, 'INIT', msg)
        a.u.x += 8
        test.assert_equals(a.u.x, 12, "The instance's attribute was modified")
    
    @test.it('Methods should work')
    def it_6():
        test.assert_equals(a.tt.get_change, '', 'Non-existent attribute has no state')
        a.f()
        msg = 'An attribute was created by a method call'
        test.assert_equals(a.tt.get_change, 'INIT', msg)
        a.f()
        msg = 'An attribute was modified by a method call'
        test.assert_equals(a.tt, 1, msg)
        test.assert_equals(a.tt.get_change, 'MOD', msg)

    @test.it('Integer and boolean tests')
    def it_7():
        @change_detection
        class H(object):
            def __init__(self):
                self.a = 0
                self.b = 1
                self.c = False
                self.d = True
        a = H()
        
        test.assert_equals(a.a, 0, 'Initial value is correct')
        test.assert_equals(a.a.get_change, 'INIT', 'Initial state is correct')
        test.assert_equals(a.b, 1, 'Initial value is correct')
        test.assert_equals(a.b.get_change, 'INIT', 'Initial state is correct')
        test.assert_equals(a.c, False, 'Initial value is correct')
        test.assert_equals(a.c.get_change, 'INIT', 'Initial state is correct')
        test.assert_equals(a.d, True, 'Initial value is correct')
        test.assert_equals(a.d.get_change, 'INIT', 'Initial state is correct')
        
        a.a = False
        msg = 'False was assigned to 0 attribute'
        test.assert_equals(a.a, False, msg)
        test.assert_equals(a.a.get_change, 'MOD', msg)
        a.b = True
        msg = 'True was assigned to 1 attribute'
        test.assert_equals(a.b, True, msg)
        test.assert_equals(a.b.get_change, 'MOD', msg)
        a.c = 0
        msg = '0 was assigned to False attribute'
        test.assert_equals(a.c, 0, msg)
        test.assert_equals(a.c.get_change, 'MOD', msg)
        a.d = 1
        msg = '1 was assigned to True attribute'
        test.assert_equals(a.d, 1, msg)
        test.assert_equals(a.d.get_change, 'MOD', msg)

@test.describe("Random tests")
def random_tests():
    from random import randint as R, choice as C, choices as Cs
    from string import ascii_lowercase as AL

    initializers = [
        lambda: None,
        lambda: bool(R(0, 1)),
        lambda: R(0, 1),
        lambda: R(-10, 10),
        lambda: "".join(Cs(AL, k=R(1, 4)))
    ]

    def randstr():
        return "".join(Cs(AL, k=R(5, 10)))

    @test.it('Object attributes')
    def it_1():
        for _ in range(100):
            attr_name = randstr()
            value = C(initializers)()
            
            init = (lambda s: lambda self, v: setattr(self, s, v))(attr_name)
            cls = change_detection(type(randstr().capitalize(), (), {"__init__": init}))
            a = cls(value)
            
            attr = getattr(a, attr_name)
            state = 'INIT'
            if attr != value or attr.get_change != state:
                test.assert_equals(attr, value, 'Instance attribute has a correct value')
                test.assert_equals(attr.get_change, state, 'Initial state is correct')
                break
            
            f = 0
            for _ in range(R(0, 3)):
                new_value = C(initializers)()
                if state == 'INIT' and value != new_value or type(value) != type(new_value):
                    state = 'MOD'
                
                setattr(a, attr_name, new_value)
                attr = getattr(a, attr_name)
                if attr != new_value or attr.get_change != state:
                    test.assert_equals(attr, new_value)
                    test.assert_equals(attr.get_change, state)
                    f = 1
                    break
            if f:
                break
            if R(0, 1):
                delattr(a, attr_name)
                attr = getattr(a, attr_name)
                if attr.get_change != 'DEL':
                    test.assert_equals(attr.get_change, 'DEL', 'Attribute was deleted')
                    break
        else:
            test.pass_()

    @test.it('Class attributes')
    def it_2():
        for _ in range(100):
            attr_name = randstr()
            value = C(initializers)()
            
            cls = change_detection(type(randstr().capitalize(), (), {attr_name: value}))
            a = cls()
            
            attr = getattr(cls, attr_name)
            if attr != value:
                test.assert_equals(attr, value, 'Class attribute has a correct value')
                break

            attr = getattr(a, attr_name)
            state = 'INIT'
            msg = 'Class attribute on an instance has a correct value'
            if attr != value or attr.get_change != state:
                test.assert_equals(attr, value, msg)
                test.assert_equals(attr.get_change, state, 'Initial state is correct')
                break
            
            f = 0
            for _ in range(R(0, 3)):
                new_value = C(initializers)()
                if state == 'INIT' and value != new_value or type(value) != type(new_value):
                    state = 'MOD'
                
                setattr(a, attr_name, new_value)
                attr = getattr(a, attr_name)
                if attr != new_value or attr.get_change != state:
                    test.assert_equals(attr, new_value)
                    test.assert_equals(attr.get_change, state)
                    f = 1
                    break
            if f:
                break
            if R(0, 1):
                delattr(a, attr_name)
                attr = getattr(a, attr_name)
                msg = 'Class attribute was deleted on an instance'
                cond = (attr == value and attr.get_change == state) or \
                        (not attr and attr.get_change == 'DEL')
                if not cond:
                    test.expect(cond, msg)
                    break
        else:
            test.pass_()

    @test.it('Undefined attributes')
    def it_3():
        for _ in range(10):
            attr_names = [randstr() for _ in range(3)]
            values = [C(initializers)() for _ in range(3)]
            
            def factory(a, b, c):
                def init(self, x, y, z):
                    setattr(self, a, x)
                    setattr(self, b, y)
                    setattr(self, c, z)
                return init
            init = factory(*attr_names)
            cls = change_detection(type(randstr().capitalize(), (), {"__init__": init}))
            a = cls(*values)
            
            for _ in range(R(5, 10)):
                if R(0, 1):
                    attr_name = C(attr_names)
                    msg = 'Existing attribute has a state'
                    test.assert_equals(getattr(a, attr_name).get_change, 'INIT', msg)
                else:
                    attr_name = randstr()
                    while attr_name in attr_names:
                        attr_name = randstr()
                    msg = 'Non-existent attribute has no state'
                    test.assert_equals(getattr(a, attr_name).get_change, '', msg)
