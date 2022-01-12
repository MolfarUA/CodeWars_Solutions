ttribute was changed from its initial value at least once
'DEL'   -  if the attribute gets deleted on the object
We can assume that each attribute has its copy constructor implemented.

Example
As an example, after the following class definition, the python terminal output should show as follows.

@change_detection
class Struct:
    x = 42
    def __init__(self, y=0):
        self.y = y

a = Struct(11)

Struct.x == 42
# Struct.x.get_change - will not be tested

a.x, a.y == 42, 11
a.x.get_change == a.y.get_change == 'INIT'

a.z.get_change == ''

a.y = 11
a.y.get_change == 'INIT'

a.y = 12
a.y.get_change == 'MOD'

a.x = '42'
a.x.get_change == 'MOD'

del a.y
a.y.get_change == 'DEL'
Note that the behaviour in case of any other operation on an undefined attribute is up to you: AttributeError might be raised or just a None, NONE or NO_SUCH might be returned.

For your convenience, two objects: NO_SUCH and NONE are predefined, which has copy constructor. Also, the envelope class Bool of the nonsubclassable bool is predefined in case you might need it...

56e02d5f2ebcd50083001300
