56e02d5f2ebcd50083001300


def change_detection(cls):
    class attr_cls():
        def __init__(self,value,get_change='INIT'):
            self.value=value
            self.get_change=get_change
        
        def __getattr__(self,name):
            return getattr(self.value,name)
        
        def __repr__(self):
            return str(self.value)
        
        def __bool__(self):
            return bool(self.value)
        
        def __call__(self):
            return self.value()
        
        def __eq__(self,other):
            return self.value==other
        
        def __add__(self,other):
            return self.value+other
        
        def __sub__(self,other):
            return self.value-other
        
        def __mul__(self,other):
            return self.value*other

        def __truediv__(self,other):
            return self.value/other

        def __radd__(self,other):
            return other+self.value
        
        def __rsub__(self,other):
            return other-self.value
        
        def __rmul__(self,other):
            return other*self.value
        
        def __rtruediv__(self,other):
            return other/self.value
    
    def __getattribute__(self,name):
        try:
            attr=super(cls, self).__getattribute__(name)
            if type(attr)!=attr_cls:
                new_attr=attr_cls(attr)
                super(cls, self).__setattr__(name,new_attr)
                return new_attr
            return attr
        except:
            return attr_cls(None,'')

    def __setattr__(self, name, value):
        target=getattr(self,name,None)
        if type(target)!=attr_cls or not target.get_change:
            super(cls, self).__setattr__(name, attr_cls(value))
        elif target.value!=value or type(target.value)!=type(value):
            target.value=value
            target.get_change='MOD'
    
    def __delattr__(self, name):
        target=getattr(self,name)
        target.value=None
        target.get_change='DEL'
            
    setattr(cls,'__setattr__', __setattr__)
    setattr(cls,'__getattribute__', __getattribute__)
    setattr(cls,'__delattr__', __delattr__)

    return cls
####################
from types import FunctionType

def changed(value, change=''):
    if value is None:
        value = NONE
    cls = value.__class__
    if cls is bool:
        cls = Bool
    try:
        class Envelope(cls): pass
    except TypeError: # methods still not covered, but out of scope for this kata
        return value
    Envelope.__name__ = cls.__name__ + "'"
    envelope = Envelope(value)
    envelope.get_change = change
    return envelope

UNDEFINED = changed(NO_SUCH)
DELETED = changed(NO_SUCH, 'DEL')

def change_detection(cls):
    class Decorated(cls):
        def __getattribute__(self, attr):
            try:
                value = cls.__getattribute__(self, attr)
                if not hasattr(value, 'get_change'): # class attribute
                    value = changed(value, 'INIT')
            except AttributeError:
                value = UNDEFINED
            return value
        def __setattr__(self, attr, value):
            oldvalue = getattr(self, attr)
            change = oldvalue.get_change
            if not change:
                 change = 'INIT'
            elif oldvalue != value or type(value) == bool and oldvalue != Bool(value):
                change = 'MOD'
            cls.__setattr__(self, attr, changed(value, change))
        def __delattr__(self, attr):
            cls.__setattr__(self, attr, DELETED)
    
    Decorated.__name__ = cls.__name__ + "'"
    return Decorated
############################
def change_detection(cls):
    o_init = cls.__init__
    o_getattribute = cls.__getattribute__
    o_setattr = cls.__setattr__
    o_delattr = cls.__delattr__
       
    def new_init(self, *args, **kwords):
        o_init(self, *args, **kwords)
        self.mydeleted = set()
        self.mymoddedd = set()
    cls.__init__ = new_init
    
    def new_delattr(self, name):       
        success = False
        
        try:
            o_delattr(self, name)
            success = True
        except AttributeError:
            pass
            
        try:
            delattr(type(self),name)
            success = True
        except AttributeError:
            pass
        
        if success:
            o_getattribute(self,'mydeleted').add(name) 
            o_getattribute(self,'mymoddedd').add(name)        
    cls.__delattr__ =  new_delattr
    
    def new_setattr(self, name, value):
        try:
            old = o_getattribute(self, name)
            oldexists = True
        except AttributeError:
            oldexists = False
        o_setattr(self, name, value)
        if oldexists and ( old != value or type(old) != type(value) ):
            o_getattribute(self,'mymoddedd').add(name)
    cls.__setattr__ =  new_setattr

    def new_getattribute(self, name):
        val = o_getattribute(self, name)
        if callable(val):
            return val

        if type(val) == bool:
            val = Bool(val)
        elif val ==None:
            val = NONE       
        
        msg = 'MOD' if name in o_getattribute(self,'mymoddedd')  else 'INIT'
        try:
            val.get_change = msg
            return val
        except (TypeError, AttributeError) as _:
            class wrapme(type(val)):
                get_change = msg
            return wrapme(val)
    cls.__getattribute__ =  new_getattribute
    
    def new_getattr(self, name):
        msg = 'DEL' if name in self.mydeleted else ''
        class ret():
            get_change = msg
            def __bool__(self):
                return False
        return ret()
    cls.__getattr__ =  new_getattr  
    
    return cls
#########################
import inspect
from typing import Any
import types
import copy


def _is_function(t):
    return isinstance(t, (types.FunctionType, types.BuiltinFunctionType, types.MethodType, types.BuiltinMethodType))


def _equals(a,b):
    if a is True or b is True:
        return a is b
    if a is False or b is False:
        return a is b
    return a == b
    

def change_detection(cls):
    def gen_change(value: Any, name: str):

        sub_class = type(value)
        if value is None:
            res  = copy.copy(NONE)
            res.get_change = name
            return res
        elif type(value) is bool:
            sub_class = Bool
        elif _is_function(value):
            value.get_change = name
            return value

        class Change(sub_class):

            def set_change(self, change):
                self.change = change

            @property
            def get_change(self):
                return self.change

        chng = Change(value) if sub_class != object else Change()
        chng.set_change(name)
        return chng

    class_attributes = {}

    class MetaClass(type):

        def __new__(metacls, name, bases, sad):
            for b in bases:
                attrs = [attr for attr in dir(b) if not attr.startswith("__")]
                for a in attrs:
                    val = getattr(b, a)
                    if not _is_function(val):
                        change = gen_change(val, 'INIT')
                        delattr(b, a)
                        class_attributes[a] = change

            return super().__new__(metacls, name, bases, dict(sad))

        def __setattr__(self, key, value):
            if key in class_attributes:
                if not _equals(class_attributes[key], value):
                    class_attributes[key] = gen_change(value, 'MOD')
            else:
                class_attributes[key] = gen_change(value, 'INIT')

        def __getattr__(self, item):
            if item in class_attributes:
                return class_attributes[item]

            return gen_change(NONE, '')

        def __delattr__(self, item):
            if item in class_attributes:
                class_attributes[item] = gen_change(NONE, 'DEL')

    class UserProxy(cls, metaclass=MetaClass):

        def __init__(self, *args, **kwargs):
            self._attributes = class_attributes.copy()
            super().__init__(*args, **kwargs)

        def __setattr__(self, key, value):
            if key == "_attributes":
                super().__setattr__(key, value)
                return

            if key in self._attributes:
                if not _equals(self._attributes[key], value):
                    self._attributes[key] = gen_change(value, 'MOD')
            else:
                self._attributes[key] = gen_change(value, 'INIT')

        def __getattr__(self, item):
            if item in self._attributes:
                return self._attributes[item]

            return gen_change(NONE, '')

        def __delattr__(self, item):
            if item in self._attributes:
                self._attributes[item] = gen_change(NONE, 'DEL')


    return UserProxy
################################
import types

def change_detection(cls):
    """ Decorator for get_change of class attributes """
    def _mc(obj,f):
        def _methodcall(*args, **kw):
            print(f'__metodcall called on {f} {args} {kw}\n')                
            val = f(*args, **kw)
            if callable(val):
                return _mc(val)
            else:
                pass
            return val
        return _methodcall   
    def _fg(f):
        def _getattrib(*args, **kw):
            class change_str(str):
                def get_change ():
                    pass
            class change_int(int): 
                def get_change():
                    pass
            class change_bool(Bool): 
                def get_change():
                    pass
                
                
            def get_wrapped(changes):
                
                def _get_change():
                    if len(changes) == 0:
                        return ''
                        
                    if changes[-1][0] == 'del':
                        change = 'DEL'    
                    else:
                        if len(changes) == 1:
                             change = 'INIT'
                        elif len(changes) > 1 :
                            change = 'MOD' if any([ (change[1] != changes[0][1]) or (type(change[1]) != type(changes[0][1])) for change in changes]) else 'INIT'
                    print(f"get change {change}")
                    return change

                result = None
                print(f"Changes {changes}")
                if len(changes) == 0:
                    result = change_str('')
                else:                    
                    val = changes[-1][1]
                    print(f"val {val} type {type(val)}")
                    if val is None:
                        print('val is none')
                        result = NONE
                    else:
                        if type(val) == int:
                            print('wrap int')
                            result = change_int(val)                        
                        elif type(val) == str:
                            print('wrap str')
                            result = change_str(val)
                        elif type(val) == bool:
                            print("wrap bool")
                            result = change_bool(val)
                        else:
                            print("wrap obj")
                            result = val
                                  
                result.get_change = _get_change()               
                return result
            
            if args[1] not in cls.__changes__:
                changes = []
                return get_wrapped(changes)
            else:
                changes = cls.__changes__[args[1]]
                print(f'get_ => {changes}')
                if changes[-1][0] == 'del':                
                    return get_wrapped(changes)
                
            val = f(*args, **kw)
            if callable(val):
                if not args[1].startswith("__"):
                    print({
                        'action': 'get',
                        'class': cls, # class object, not string
                        'attribute': args[1], # method name, string
                        'value': val
                    })  
                return _mc(args[0],val)
            else:
                 if not args[1].startswith("__"):
                    return get_wrapped(changes)
              
            return val
        return _getattrib
    def _fs(f):
        def __setattr(*args, **kw):
            #print(f'__setattrib called on {args} {kw} \n')
            val = f(*args, **kw)
            if args[1] not in cls.__changes__:
                cls.__changes__[args[1]]= []            
            cls.__changes__[args[1]].append(('set',args[2]))                
            return val
        return __setattr   
    def _del(f):
        def __delattr(*args, **kw):
            print(f" del '{args[1]}' from  {cls.__changes__}")
            if args[1] not in cls.__changes__ or cls.__changes__[args[1]][-1][0] == 'del':
               return NO_SUCH
            try:
                val = f(*args, **kw)
                print(val)
                if args[1] not in cls.__changes__:
                    cls.__changes__[args[1]]= []            
                #if args[1] not in cls.__class_attribs:
                cls.__changes__[args[1]].append(('del',None))                
                return val                
            except AttributeError as ex:
                print(f" del error {ex}")

        return __delattr         

    print(cls.__dict__) 
    cls.__changes__ = {}
    cls.__class_attribs = []
    for k,v in cls.__dict__.items():
        if not k.startswith('__'):
            cls.__changes__[k] = [('set',v)]
            cls.__class_attribs.append(k)
            
    cls.__getattribute__ = _fg(cls.__getattribute__)
    cls.__setattr__ = _fs(cls.__setattr__)   
    cls.__delattr__ = _del(cls.__delattr__) 

    return cls
################################
from collections import defaultdict

state = defaultdict(dict)

a = None
NONE_TYPE = a.__class__
b = False
BOOL_TYPE = b.__class__


class EmptyState:
    get_change = ""
    
    
class DeletedState:
    get_change = "DEL"
    
    def __bool__(self):
        return False
    

def get_new_type(old_type: type):
    class Foo(old_type):
        get_change = "INIT"
        origin = old_type
        
#         def __bool__(self):
#             if self.get_change == "DEL":
#                 return False
#             return super().__bool__()
        
    return Foo


def get_subclassed_value(value):
    type_ = value.__class__

    if type_ is NONE_TYPE:
        new_value = NONE.__class__()
        new_value.get_change = "INIT"
    elif type_ is BOOL_TYPE:
        new_value = Bool(value)
        new_value.get_change = "INIT"
    else:
        new_attr_type = get_new_type(type_)
        new_value = new_attr_type(value)
    return new_value
    
    
def equal(val1, val2):
    return val1 == val2 and getattr(type(val1), "origin", type(val1)) == getattr(type(val2), "origin", type(val2))

def change_detection(cls):
    """ Decorator for get_change of class attributes """
    
    for attr in [a for a in dir(cls) if not a.startswith("__")]:
        value = getattr(cls, attr)
        if callable(value):
            continue
        new_value = get_subclassed_value(value)
        setattr(cls, attr, new_value)
    
    def new__del_attr(self, item):
        print(item)
        attr = getattr(self, item, NO_SUCH)
        if attr is not NO_SUCH:
            attr.get_change = "DEL"
        object.__setattr__(self, item, DeletedState())
        
    def new__set_attr(self, name, value):
        new_value = get_subclassed_value(value)
        
        old_value = getattr(self, name, NO_SUCH)
        
        if old_value is not NO_SUCH \
        and getattr(old_value, "get_change", NO_SUCH) in ("INIT", "MOD"):
            if equal(old_value, new_value):
                new_value.get_change = old_value.get_change
            else:
                new_value.get_change = "MOD"

        print(name, new_value)
#         print(name, ': ', id(new_value), new_value, new_value.get_change, type_, '---', id(old_value), old_value, old_value.get_change, type(old_value), '\n')
        object.__setattr__(self, name, new_value)
        
        
    def new__get_attribute(self, name):
        """for unknown attrs"""
        
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return EmptyState()
        
    cls.__getattribute__ = new__get_attribute
    cls.__setattr__ = new__set_attr
    cls.__delattr__ = new__del_attr
    return cls
###########################################################
def change_detection(cls):
    class NonExistentAttribute(object):
        pass

    class JNoneMeta(type):
        def __subclasscheck__(currentCls, parentCls):
            return currentCls == JNone and parentCls == type(None)

    class JBoolMeta(type):
        def __subclasscheck__(currentCls, parentCls):
            return currentCls == JBool and parentCls == type(bool)

    class JInt(int):
        pass

    class JString(str):
        pass

    class JBool(object, metaclass = JBoolMeta):
        def __init__(self, value):
            self._value = value

        def __bool__(self):
            return type(self._value) == type(bool) and self._value

        def __eq__(self, value):
            return self._value == value

    class JNone(object, metaclass = JNoneMeta):
        def __bool__(self):
            return False

        def __eq__(self, value):
            return value == None

    class Journaled(cls):
        @staticmethod
        def createAttribute(value, state):
            if value == None:
                value = JNone()
            elif isinstance(value, bool):
                value = JBool(value)
            elif isinstance(value, int):
                value = JInt(value)
            elif isinstance(value, str):
                value = JString(value)

            try: # for functions/methods but allows for lambda
                value.get_change = state
            except AttributeError:
                pass

            return value

        def __init__(self, *args, **kwargs):
            super().__setattr__("__modified__", set())
            super().__setattr__("__deleted__", set())
            super().__init__(*args, **kwargs)

        def __getattribute__(self, name):
            try:
                v = super().__getattribute__(name)
            except AttributeError:
                v = NonExistentAttribute()

            if not name.startswith("__"):
                if name in self.__deleted__:
                    s = "DEL"
                elif name in self.__modified__:
                    s = "MOD"
                else:
                    s = "INIT" if type(v) != NonExistentAttribute else ""
                return Journaled.createAttribute(v, s)

            return v

        def __setattr__(self, name, value):
            if not name.startswith("__") or name not in self.__modified__:
                try:
                    v = self.__getattribute__(name)
                    if type(v) != NonExistentAttribute and (v != value or typesAreDifferent(type(v), type(value))): 
                        self.__modified__.add(name)
                except AttributeError:
                    pass
            #print('__setattr__: ', name, v, value)
            super().__setattr__(name, value)

        def __delattr__(self, name):
            if name in self.__modified__:
                self.__modified__.remove(name)
            if hasattr(self, name):
                self.__deleted__.add(name)
                super().__setattr__(name, None)

    def typesAreDifferent(subClass, parentClass):
        return not (issubclass(subClass, parentClass) or issubclass(parentClass, subClass))

    #copy original class attributes to Journaled class
    for clsAttr in filter(lambda x: not x.startswith("__"), dir(cls)):
        setattr(Journaled, clsAttr, cls.__dict__[clsAttr])

    return Journaled
#########################################
class BaseEq:
    def __init__(self, v):
        self.v = v
    
    def __eq__(self, other):
        return self.v == other
    
    def __bool__(self):
        return bool(self.v)

def change_detection(cls):
    def wrap(v, x):
        if callable(v):
            return v
        try:
            setattr(v, 'get_change', x)
            return v
        except:
            ty = type(v)
            if ty == bool:
                ty = Bool
            elif v == None:
                ty = BaseEq
            class Wrapper(ty):
                get_change = x
            return Wrapper(v)
    
    class ChangeDetector(cls):
        def __new__(k, *args, **kargs):
            obj = super().__new__(k)
            obj._changes = ({}, {})
            return obj
        
        def __getattribute__(self, name):
            _, st = super().__getattribute__('_changes')
            s = st.get(name, 'INIT')
            if s == 'DEL':
                return wrap(0, 'DEL')
            try:
                v = super().__getattribute__(name)
                return wrap(v, s)
            except AttributeError:
                return wrap(0, st.get(name, ''))
        
        def __setattr__(self, name, value):
            if name != '_changes':
                vals, st = super().__getattribute__('_changes')
                if name in vals and vals[name] is not value or hasattr(cls, name) and getattr(cls, name) is not value:
                    st[name] = 'MOD'
                elif st.get(name, 'DEL') == 'DEL':
                    st[name] = 'INIT'
                vals[name] = value
            super().__setattr__(name, value)
            
        def __delattr__(self, name):
            _, st = super().__getattribute__('_changes')
            st[name] = 'DEL'
            try:
                super().__delattr__(name)
            except:
                pass
    
    return ChangeDetector
####################################
def change_detection(cls):
    init = cls.__init__

    def _changed_value(value):
        _class = value.__class__
        if value is None: _class = NONE.__class__
        elif type(value) is bool: _class = Bool
        else: _class = type(_class.__name__, (_class,), {})
        return _class(value)

    def _init(self, *args, **kwargs):
        self.__dict__["__values__"] = {}
        self.__dict__["__changed__"] = {}
        init(self, *args, **kwargs)
        for key, value in cls.__dict__.items():
            if key.startswith("__") and key.endswith("__"): continue
            if callable(value): continue
            setattr(self, key, value)

    def _getattr(self, name):
        value = NO_SUCH.__class__(NO_SUCH)
        value.get_change = ""
        return value

    def _setattr(self, name, value):
        value = _changed_value(value)
        if name not in self.__values__:
            self.__values__[name] = value
            self.__changed__[name] = False
        if not self.__changed__[name] and self.__values__[name] == value:
            value.get_change = "INIT"
        else:
            self.__changed__[name] = True
            value.get_change = "MOD"
        self.__dict__[name] = value

    def _delattr(self, name):
        value = NO_SUCH.__class__(NO_SUCH)
        value.get_change = "DEL"
        self.__dict__[name] = value

    cls.__init__ = _init
    cls.__getattr__ = _getattr
    cls.__setattr__ = _setattr
    cls.__delattr__ = _delattr
    return cls
######################################
import functools

class III(int):
    def __init__(self, value):
        super().__init__()
        self._get_change = 'INIT'
    @property
    def get_change(self):
        return self._get_change
    @get_change.setter
    def get_change(self, value):
        self._get_change = value
    def __bool__(self):
        return self._get_change in ['INIT', 'MOD']

class SSS(str):
    def __init__(self, value):
        super().__init__()
        self._get_change = 'INIT'
    @property
    def get_change(self):
        return self._get_change
    @get_change.setter
    def get_change(self, value):
        self._get_change = value
    def __bool__(self):
        return self._get_change in ['INIT', 'MOD']

class DDD(object):
    def __init__(self, value):
        self._d = value
        self._get_change = 'INIT'
    def __eq__(self, other):
        if isinstance(other, DDD):
            return self._d == other._d
        else:
            return self._d == other
    @property
    def get_change(self):
        return self._get_change
    @get_change.setter
    def get_change(self, value):
        self._get_change = value
    def __bool__(self):
        return self._get_change in ['INIT', 'MOD']

class NNN(object):
    def __init__(self):
        super().__init__()
        self._get_change = ''
    @property
    def get_change(self):
        return self._get_change
    @get_change.setter
    def get_change(self, value):
        self._get_change = value
    def __bool__(self):
        return self._get_change in ['INIT', 'MOD']

def get_change(self):
    return self._get_change

def set_change(self, value):
    self._get_change = value

def change_detection(cls):

    @functools.wraps(cls, updated=())
    class S(cls):

        __dict = { k:v for k,v in cls.__dict__.items() if not (k.startswith('__') and k.endswith('__')) }
        _dict = { k:v for k,v in __dict.items() if not callable(v) }
        _dict1 = { k:III(v) for k,v in __dict.items() if type(v)==int}
        _dict2 = { k:SSS(v) for k,v in __dict.items() if type(v)==str}
        _dict3 = { k:DDD(v) for k,v in __dict.items() if type(v)==bool or v==None}
        _dict.update(_dict1)
        _dict.update(_dict2)
        _dict.update(_dict3)
        _status = { k:'INIT' for k in _dict}
        for k,v in _dict.items():
            if not hasattr(v, 'get_change'):
                print(f"*** {k} {v} has not get_change ***")
                type(v).get_change = property(get_change, set_change)
                v.get_change = 'INIT'
            result = setattr(cls, k, v)
            print(f"{k} {v} {result}")

        def __getattribute__(self, name: str):
            try:
                print(f"[inside 001] {name=}")
                value = super().__getattribute__(name)
                print(f"[inside 001] {value=}")
                return value
            except:
                return NNN()

        def __setattr__(self, name: str, value) -> None:
            print(f"[inside 003] {name=} {value=}")
            if name == "_status":
                return super().__setattr__(name, value)
            hasname = name in self._status
            hasstatus = True
            if type(value) == int:
                new_value = III(value)
            elif type(value) == str:
                new_value = SSS(value)
            elif type(value) == bool:
                new_value = DDD(value)
            elif type(value) == III:
                new_value = value
            elif type(value) == SSS:
                new_value = value
            elif value == None:
                new_value = DDD(value)
            else:
                new_value = value
                type(new_value).get_change = property(get_change, set_change)
                new_value.get_change = 'INIT'
            if hasname:
                cur_status = self._status[name]
                cur_value = self.__getattribute__(name)
                if  (new_value == cur_value) and (type(new_value)==type(cur_value) and cur_status!='DEL'):
                    pass
                else:
                    if cur_status == 'DEL':
                        new_status = 'INIT'
                    else:
                        new_status = 'MOD'
                    self._status[name] = new_status
                    cur_value = new_value
                    cur_value._get_change = new_status
                value = cur_value
            else:
                self._status[name] = 'INIT'
                value = new_value
            return super().__setattr__(name, value)
        
        def __delattr__(self, name: str) -> None:
            print(f"[inside 004] {name=}")
            if name == "_status":
                return super().__delattr__(name)
            hasname = hasattr(self, name)
            hasstatus = hasattr(self, '_status')
            print(f"[inside 004] {hasname=}")
            print(f"[inside 004] {hasstatus=}")
            if hasstatus:
                if hasname:
                    if name in self._status:
                        cur_value = self.__getattribute__(name)
                        cur_value._get_change = 'DEL'
                        self._status[name] = 'DEL'
                        if hasattr(type(self), name):

                            setattr(getattr(self, name), '_get_change', 'DEL')
                            self._status[name] = 'DEL'
                        return
            return super().__delattr__(name)
    return S
#####################################
def change_detection(cls):
    """ Decorator for get_change of class attributes """
    def W(x, status="INIT"):
        t = type(x)
        if isinstance(x, bool):
            arg = (x,)
            x = Bool(x)
        elif x is None:
            x = NONE
            arg = ()
        else:
            arg = (x,)
        class W(type(x)):
            get_change = status
            _WW_type = t
        return W(*arg)
    
    cache = {}
    class X(cls):
        def __init__(self, *args, **kw):
            super().__init__(*args, **kw)
            
        def __getattribute__(self, n):
            if n in cache:
                return cache[n]
            if not hasattr(super(), n):
                return W(NO_SUCH, "")
            t = super().__getattribute__(n)
            if callable(t):
                return t
            return cache.setdefault(n, W(t))
        
        def __setattr__(self, n, v):
            super().__setattr__(n, v)
            cache[n] = W(v, "INIT" if n not in cache or (cache[n] == v and cache[n]._WW_type is type(v) and cache[n].get_change == "INIT") else "MOD")
                
        def __delattr__(self, n):
            cache[n] = W(NO_SUCH, "DEL")
    return X
############################################
import re
import operator
from functools import update_wrapper, partial

class _MISSING:
    def __repr__(self):
        return '<MISSING>'
    def __bool__(self):
        return False
MISSING = _MISSING()

def define_proxy_binops(valueattr, modattr):
    def decorator(cls):
        def define_method(name, code, binop):
            globals = {
                'valueattr': valueattr,
                'modattr': modattr,
                'cls': cls,
                'binop': binop,
            }
            locals = {}
            exec('\n'.join(code), globals, locals)
            method = locals[name]
            method.__qualname__ = f'{cls.__qualname__}.{name}'
            setattr(cls, name, method)

        def add_binop(name):
            binop = getattr(operator, name)
            code = [
              f"def {name}(self, other):",
               "    value = getattr(self, valueattr)",
               "    other_value = getattr(other, valueattr) if isinstance(other, cls) else other",
               "    return binop(value, other_value)"]
            define_method(name, code, binop)

        def add_rbinop(rname):
            name = '__' + re.search(r'__r(.+)', rname)[1]
            binop = getattr(operator, name)
            code = [
              f"def {rname}(self, other):",
               "    value = getattr(self, valueattr)",
               "    other_value = getattr(other, valueattr) if isinstance(other, cls) else other",
               "    return binop(other_value, value)"]
            define_method(rname, code, binop)

        def add_ibinop(iname):
            name = '__' + re.search(r'__i(.+)', iname)[1]
            binop = getattr(operator, name)
            code = [
              f"def {iname}(self, other):",
               "    modify = getattr(self, modattr)",
               "    value = getattr(self, valueattr)",
               "    other_value = getattr(other, valueattr) if isinstance(other, cls) else other",
               "    result = binop(value, other_value)",
               "    modify(result)",
               "    return self"]
            define_method(iname, code, binop)

        binops = ['__add__', '__and__', '__concat__', '__contains__', '__eq__',
                  '__floordiv__', '__ge__', '__gt__', '__le__', '__lshift__',
                  '__lt__', '__matmul__', '__mod__', '__mul__', '__ne__', '__or__',
                  '__pow__', '__rshift__', '__sub__', '__truediv__', '__xor__']
        for name in binops:
            add_binop(name)
        rbinops = ['__radd__', '__rsub__', '__rmul__', '__rmatmul__', '__rtruediv__',
                   '__rfloordiv__', '__rmod__', '__rpow__', '__rlshift__',
                   '__rrshift__', '__rand__', '__rxor__', '__ror__']
        for name in rbinops:
            add_rbinop(name)
        ibinops = ['__iadd__', '__iand__', '__iconcat__', '__ifloordiv__', '__ilshift__',
                   '__imatmul__', '__imod__', '__imul__', '__ior__', '__ipow__', '__irshift__',
                   '__isub__', '__itruediv__', '__ixor__']
        for name in ibinops:
            add_ibinop(name)
        return cls
    return decorator

@define_proxy_binops('_value_', '_modify_')
class ProxyAttribute:
    def __init__(self, changeattr, value=MISSING):
        state = '' if value is MISSING else 'INIT'
        object.__setattr__(self, '_changeattr_', changeattr)
        object.__setattr__(self, '_value_', value)
        object.__setattr__(self, '_state_', state)

    def __repr__(self):
        value = self._value_
        state = self._state_
        return f'ProxyAttribute(value={value}, state={state or None})'

    def __getattr__(self, attr):
        if attr == self._changeattr_:
            return self._state_
        return getattr(self._value_, attr)

    def __setattr__(self, attr, value):
        if attr == self._changeattr_:
            raise AttributeError(f"can't set attribute '{self._changeattr_}' on ProxyAttribute")
        return setattr(self._value_, attr, value)

    def __delattr__(self, attr):
        if attr == self._changeattr_:
            raise AttributeError(f"can't delete attribute '{self._changeattr_}' on ProxyAttribute")
        return self._value_.__delattr__(attr)

    def __bool__(self):
        return bool(self._value_)
    
    def __call__(self, *args, **kwargs):
        return self._value_(*args, **kwargs)

    def _modify_(self, new_value):
        if self._value_ != new_value or type(self._value_) != type(new_value):
            new_state = 'MOD' if self._value_ is not MISSING else 'INIT'
            object.__setattr__(self, '_state_', new_state)
            object.__setattr__(self, '_value_', new_value)
        
    def _delete_(self):
        object.__setattr__(self, '_state_', 'DEL')
        object.__setattr__(self, '_value_', MISSING)

def change_detection(cls=None, /, changeattr='get_change'):
    """ Decorator for get_change of class attributes """
    Attribute = partial(ProxyAttribute, changeattr)

    def decorator(cls):
        class Wrapper(cls):
            def __getattribute__(self, attr):
                try:
                    attribute = super().__getattribute__(attr)
                    if not isinstance(attribute, ProxyAttribute):
                        # attribute isn't wrapped yet, initialize it
                        attribute = Attribute(attribute)
                        object.__setattr__(self, attr, attribute)
                    return attribute
                except AttributeError:
                    # non-existent attribute
                    attribute = Attribute()
                    object.__setattr__(self, attr, attribute)
                    return attribute

            def __setattr__(self, attr, value):
                if isinstance(value, ProxyAttribute):
                    value = value._value_
                try:
                    attribute = object.__getattribute__(self, attr)
                    if not isinstance(attribute, ProxyAttribute):
                        # We would get here if the user tries to set an instance attribute
                        # of the same name as a class attribute; attribute is the class
                        # attribute here
                        attribute = Attribute(attribute)
                    attribute._modify_(value)
                    return super().__setattr__(attr, attribute)
                except AttributeError:
                    # Initialize attr
                    attribute = Attribute(value)
                    return super().__setattr__(attr, attribute)

            def __delattr__(self, attr):
                try:
                    attribute = object.__getattribute__(self, attr)
                    attribute._delete_()
                    return None
                except AttributeError:
                    return super().__delattr__(attr)

        update_wrapper(Wrapper, cls, updated=())
        return Wrapper
    
    if cls is None:
        return decorator
    return decorator(cls)
