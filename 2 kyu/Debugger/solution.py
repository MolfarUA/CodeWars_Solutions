from time import time

class Debugger(object):
  attribute_acceses = []
  method_calls = []

class Meta(type):
  def __new__(cls, name, bases, atts):
    for k,v in atts.items():
      if callable(v): atts[k] = wrapped_method(cls, v)
    atts['__getattribute__'] = wrapped_getattribute(cls) 
    atts['__setattr__'] = wrapped_setattr(cls) 
    return type.__new__(cls, name, bases, atts)

def wrapped_method(c, f):
  def w(*args, **kwargs):
    a = time()
    r = f(*args, **kwargs)
    b = time()
    Debugger.method_calls.append({'class':c,'mehod':f.__name__,'args':args,'kwargs':kwargs,'time':b-a}) 
  return w

def wrapped_setattr(c):
  def s(self, k, v):
    object.__setattr__(self, k, v)
    Debugger.attribute_acceses.append({'action':'set','class':c,'attribute':k,'value':v})
  return s

def wrapped_getattribute(c):
  def g(self, k):
    v = object.__getattribute__(self, k)
    Debugger.attribute_acceses.append({'action':'get','class':c,'attribute':k,'value':v})
    return v
  return g
##################
import inspect
class Debugger(object):
    attribute_accesses, method_calls = [], []

class Meta(type):
    def __new__(cls, name, bases, d):
        x = super(Meta,cls).__new__(cls, name, bases, d)
        for i, j in d.items():
            if callable(j) : setattr(x, i, method_call(j))

        def getattribute(self, item):
            Debugger.attribute_accesses.append({'action': 'get', 'class': x, 'attribute': item, 'value': object.__getattribute__(self, item)})
            return object.__getattribute__(self, item)

        def setattribute(self, key, value):
            Debugger.attribute_accesses.append({'action': 'set', 'class': x, 'attribute': key, 'value': value})
            object.__setattr__(self, key, value)

        x.__getattribute__ = lambda self, item: getattribute(self, item)
        x.__setattr__ = lambda self, key, value: setattribute(self, key, value)
        return x

def method_call(f):
    def another(*args, **kwargs):
        Debugger.method_calls.append({'class': args[0], 'method': f.__name__, 'args': args, 'kwargs': kwargs})
        return f(*args)
    return another
###########################
class Debugger(object):
    attribute_accesses = []
    method_calls = []
    
class Meta(type):
    def __new__(cls, name, bases, dct):
        instance = super().__new__(cls, name, bases, dct)
        
        for attr_name in instance.__dict__: 
            attr = getattr(instance, attr_name)
            
            if callable(attr):
                setattr(instance, attr_name, Meta.track_methods(attr))
            
        setattr(instance, '__setattr__', Meta.track_setter(instance.__setattr__))
        setattr(instance, '__getattribute__', Meta.track_getter(instance.__getattribute__))
                
        return instance
    
    @staticmethod
    def track_methods(method):
        def wrapper(*args, **kwargs):
            this = args[0]
            
            Debugger.method_calls.append({
                'class': this.__class__,
                'method': method.__name__,
                'args': args,
                'kwargs': kwargs,
            })
            
            return method(*args, **kwargs)
            
        return wrapper
        
    @staticmethod
    def track_setter(setter):
        def wrapper(*args, **kwargs):            
            this = args[0]
            attr_name = args[1]
            value = args[2]
            
            if attr_name != '__class__':            
                Debugger.attribute_accesses.append({
                    'action': 'set',
                    'class': this.__class__,
                    'attribute': attr_name,
                    'value': value,
                })
            
            return setter(*args, **kwargs)
            
        return wrapper
        
    @staticmethod
    def track_getter(getter):
        def wrapper(*args, **kwargs):
            this = args[0]
            attr_name = args[1]
            
            if attr_name != '__class__': 
                Debugger.attribute_accesses.append({
                    'action': 'get',
                    'class': this.__class__,
                    'attribute': attr_name,
                })
            
            return getter(*args, **kwargs)
            
        return wrapper
#########################################
import types
import inspect

class Debugger(object):
    attribute_accesses = []
    method_calls = []



# Function that prints the name of a passed in function, and returns a new function
# encapsulating the behavior of the original function
def call_method(fn, *args, **kwargs):
    def fncomposite(*args, **kwargs):
        Debugger.method_calls.append({
            'class': args[0],
            'method': fn,
            'args': args,
            'kwargs': kwargs
        })
        rt = fn(*args, **kwargs)
        return rt
    
    return fncomposite

def get_attr(*args):
    Debugger.attribute_accesses.append({
        'action': 'get',
        'class': args[0],
        'attribute': args[1],
        'value': ''
    })
    return object.__getattribute__(*args)
    
def set_attr(*args):
    Debugger.attribute_accesses.append({
        'action': 'set',
        'class': args[0],
        'attribute': args[1],
        'value': args[2]
    })
    return object.__setattr__(*args)

class Meta(type):        
    def __call__(cls, *args, **kw):
        new_class = super(Meta, cls).__call__(*args, **kw)
        return new_class
        
    def __new__(cls, name, bases, attr):
        # Add debugging for methods
        for name, value in attr.items():
            if type(value) is types.FunctionType or type(value) is types.MethodType:
                attr[name] = call_method(value)

        new_class = super(Meta, cls).__new__(cls, name, bases, attr)
        # Add debugging for attributes
        new_class.__getattribute__ = get_attr
        new_class.__setattr__ = set_attr
        return new_class
#######################################
class Debugger(object):
    attribute_accesses = []
    method_calls = []

class Meta(type):
    def __new__(cls, name, bases, clsdict):

        # Decorate class/instance method
        def wrap(cls, method):
            def wrapper(*args, **kwargs):
                Debugger.method_calls.append({
                    'class': cls,
                    'method': method.__name__,
                    'args': args,
                    'kwargs': kwargs
                })
                return method(*args, **kwargs)
            return wrapper

        # Intercept get attribute
        def _getattribute(self, attr):
            Debugger.attribute_accesses.append({
                'action': 'get',
                'class': type(self),
                'attribute': attr,
                'value': self
            })

            return super(type(self), self).__getattribute__(attr)

        # Intercept set attribute
        def _setattr(self, attr, value):
            Debugger.attribute_accesses.append({
                'action': 'set',
                'class': type(self),
                'attribute': attr,
                'value': value
            })
            super(type(self), self).__setattr__(attr, value)

        for attr, val in clsdict.items():
            if callable(val):
                clsdict[attr] = wrap(cls, val)
        clsdict['__getattribute__'] = _getattribute
        clsdict['__setattr__'] = _setattr

        return type.__new__(cls, name, bases, clsdict)
##############################
class Debugger(object):
    attribute_accesses = []
    method_calls = []
    
class Meta(type):
    @staticmethod
    def __getattribute(self, item):
        value = object.__getattribute__(self, item)
        Debugger.attribute_accesses.append({
            'action': 'get',  # set/get
            'class': type(self),  # class object, not string
            'attribute': item,  # name of attribute, string
            'value': value  # actual value
        })

        if item in object.__getattribute__(self, "__dict__"):
            return value

        def method(*args, **kwargs):
            Debugger.method_calls.append({
                'class': self,  # class object, not string
                'method': item,  # method name, string
                'args': (self, ) + args,  # args,  # all args, including self
                'kwargs': kwargs  # kwargs

            })

            return value(*args, **kwargs)

        return method

    @staticmethod
    def __setattr(self, key, value):
        object.__setattr__(self, key, value)
        print("set debug")
        Debugger.attribute_accesses.append({
            'action': 'set',  # set/get
            'class': type(self),  # class object, not string
            'attribute': key,  # name of attribute, string
            'value': value  # actual value

        })

    def __call__(cls, *args, **kwargs):
        cls.__getattribute__ = Meta.__getattribute
        cls.__setattr__ = Meta.__setattr
        instance = super().__call__(*args, **kwargs)
        Debugger.method_calls.append({
            'class': instance,  # class object, not string
            'method': "__init__",  # method name, string
            'args': (instance,) + args,  # args,  # all args, including self
            'kwargs': kwargs  # kwargs
        })
        return instance
##########################################
from types import MethodType, FunctionType


class Debugger(object):
    attribute_accesses = []
    method_calls = []


def method_dec(func):
    def inner(self, *args, **kwargs):
        Debugger.method_calls.append({
            'class': type(self),
            'method': func.__name__,
            'args': (self,) + args,
            'kwargs': kwargs
        })
        return func(self, *args, **kwargs)

    return inner


def get_attr_dec(func):
    def inner(self, item):
        res = func(self, item)
        # if not isinstance(res, MethodType) and not isinstance(res, FunctionType):
        Debugger.attribute_accesses.append({
            'action': 'get',
            'class': type(self),  # class object, not string
            'attribute': item,  # name of attribute, string
            'value': res  # actual value
        })
        return res

    return inner


def set_attr_dec(func):
    def inner(self, key, value):
        func(self, key, value)
        Debugger.attribute_accesses.append({
            'action': 'set',
            'class': type(self),  # class object, not string
            'attribute': key,  # name of attribute, string
            'value': value  # actual value
        })

    return inner


class Meta(type):

    def __new__(mcs, clsname, bases, attrs):
        attrs = {
            key: method_dec(value) if (
                    isinstance(value, MethodType) or isinstance(value, FunctionType)) else value
            for key, value in attrs.items()
        }
        attrs["__getattribute__"] = get_attr_dec(super(type, mcs).__getattribute__)
        attrs["__setattr__"] = set_attr_dec(super(type, mcs).__setattr__)
        return type.__new__(mcs, clsname, bases, attrs)
