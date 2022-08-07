5571d9fc11526780a000011a


class ThingTuple(tuple):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.current = kwargs.get('current', None)

    def __new__(self, *args, **kwargs):
        return super().__new__(ThingTuple, *args, **kwargs)

    def __getattr__(self, attr):
        if attr == 'current':
            return object.__getattribute__(self, attr)
        if attr == 'each':
            return self
        elif attr in ['being_the', 'and_the']:
            self.current = 'property'
            p = []
            for i in self:
                p.append(i.__getattr__(attr))
            return ThingTuple(p, current=self.current)
        if self.current == 'property':
            self.current = 'property_value'
            p = []
            for i in self:
                p.append(i.__getattr__(attr))
            return ThingTuple(p, current=self.current)
        elif self.current == 'property_value':
            p = []
            for i in self:
                p.append(i.__getattr__(attr))
            return ThingTuple(p, current=self.current)
        elif self.current == 'having':
            p = []
            for i in self:
                i.has(self.count)
                p.append(i.__getattr__(attr))
            return ThingTuple(p, current=self.current)

    def having(self, num):
        self.count = num
        self.current = 'having'
        return self


class Thing(object):
    def __init__(self, name):
        self.name = name
        self.current = None

    def __getattr__(self, attr):
        if attr == 'is_a':
            self.current = '+bool'
            return self
        elif attr == 'is_not_a':
            self.current = '-bool'
            return self
        elif attr in ['is_the', 'being_the', 'and_the']:
            self.current = 'property'
            return self
        elif attr == 'can':
            self.current = 'verb'
            return self
        elif attr == 'verb':
            return object.__getattribute__(self, attr)

        if self.current == '+bool':
            self.__setattr__(f'is_a_{attr}', True)
        elif self.current == '-bool':
            self.__setattr__(f'is_a_{attr}', False)
        elif self.current == 'property':
            self.property_name = attr
            self.current = 'property_value'
        elif self.current == 'property_value':
            self.__setattr__(self.property_name, attr)
        elif self.current == 'has':
            n = f'{attr}' if not f'{attr}'.endswith('s') else f'{attr}'[:-1]
            if self.count == 1:
                self.__setattr__(attr, Thing(n))
            else:
                self.__setattr__(attr, ThingTuple([Thing(n) for _ in range(self.count)]))
            return self.__dict__[attr]
        elif self.current == 'verb':
            self.verb_name = attr
            return self.verb
        return self

    def verb(self, func, past=None):
        if past:
            func = self.past(func, self.name)
            self.__setattr__(past, func.results)
        func.__globals__['name'] = self.name
        self.__setattr__(self.verb_name, func)

    @staticmethod
    def past(func, name):

        def wrapper(*args, **kwargs):
            wrapper.results.append(func(*args, **kwargs))
            return wrapper.results[-1]

        wrapper.results = []
        return wrapper

    def __setattr__(self, attr, val):
        self.__dict__[attr] = val

    def has(self, num):
        self.count = num
        self.current = 'has'
        return self

    def having(self, num):
        return self.has(num)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

___________________________________________________
def return_child(thing, name, value):
    setattr(thing, name, value)
    return getattr(thing, name)


def return_parent(thing, name, value):
    setattr(thing, name, value)
    return thing


def apply_verb(thing, name):
    def verb(fn, tense=None):
        _fn = fn
        
        if tense is not None:
            past = []
            def wrapper(*args, **kwargs):
                out = fn(*args, **kwargs)
                past.append(out)
                return out
            
            _fn = wrapper
            setattr(thing, tense, past)
        
        _fn.__globals__['name'] = thing.name
        setattr(thing, name, _fn)
    
    return verb


class Defer:
    
    def __init__(self, fn):
        self.fn = fn
        
    def __getattr__(self, name):
        return self.fn(name)


class Accessor:
    
    def __getattr__(self, name):
        if name == 'is_a':
            return Defer(lambda n: setattr(self, 'is_a_' + n, True))
        elif name == 'is_not_a':
            return Defer(lambda n: setattr(self, 'is_a_' + n, False))
        elif name in {'is_the', 'being_the', 'and_the'}:
            return Defer(lambda n: Defer(lambda v: return_parent(self, n, v)))
        elif name == 'has' or name == 'having':
            return lambda i: Defer(lambda n: return_child(self, n, Things.from_has(i, n)))
        elif name == 'each':
            return self
        elif name == 'can':
            return Defer(lambda n: apply_verb(self, n))
        elif isinstance(self, Things):
            return Things([getattr(thing, name) for thing in self])


class Thing(Accessor):
    
    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)


class Things(tuple, Accessor):
    
    def __new__(cls, args):
        if len(args) == 1:
            return args[0]
        return super().__new__(cls, args)
    
    def __setattr__(self, name, value):
        for thing in self:
            setattr(thing, name, value)
        return self
    
    @classmethod
    def from_has(cls, amount, name):
        singular = name.rstrip('s')
        return cls([Thing(singular, **{'is_' + singular: True}) for _ in range(amount)])
      
___________________________________________________
class IsAThing(object):
    def __init__(self, thing):
        self.thing = thing

    def __getattr__(self, attr):
        setattr(self.thing, 'is_a_' + attr, True)


class IsNotAThing(object):
    def __init__(self, thing):
        self.thing = thing

    def __getattr__(self, attr):
        setattr(self.thing, 'is_a_' + attr, False)


class ObjectThing(object):
    def __init__(self, subject, predicate):
        self.subject = subject
        self.predicate = predicate

    def __getattr__(self, attr):
        setattr(self.subject, self.predicate, Thing(attr))
        return self.subject


class IsTheThing(object):
    def __init__(self, thing):
        self.thing = thing

    def __getattr__(self, attr):
        return ObjectThing(self.thing, attr)


class HasThing(object):
    def __init__(self, thing, number):
        self.thing = thing
        self.number = number

    def __getattr__(self, attr):
        if self.number == 1:
            result = Thing(str(attr))
            setattr(self.thing, attr, result)
        else:
            things = []
            for i in range(self.number):
                things.append(Thing(str(attr)[:-1]))

            result = ThingSet(things)
            setattr(self.thing, attr, result)

        return result
        # return self.thing


class FunctionThing(object):
    def __init__(self, thing, attr):
        self.thing = thing
        self.attr = attr

    def __call__(self, method, previous=''):
        setattr(self.thing, self.attr, lambda x: self.thing.save_and_return(method, previous, x))
        # setattr(self.thing, self.attr, method)


class CanThing(object):
    def __init__(self, thing):
        self.thing = thing

    def __getattr__(self, attr):
        return FunctionThing(self.thing, attr)


class Thing(object):
    # TODO: make the magic happen
    def __init__(self, name):
        self.name = name

        self.is_a = IsAThing(self)
        self.is_not_a = IsNotAThing(self)

        self.is_the = IsTheThing(self)
        self.has = lambda x: HasThing(self, x)
        self.having = lambda x: HasThing(self, x)

        setattr(self, 'is_' + self.name, True)

        self.can = CanThing(self)

    def __str__(self):
        return self.name

    def save_and_return(self, method, previous, x):
        method.__globals__['name'] = self.name
        # if previous != '':
        #     setattr(self, previous, method(x))

        if not hasattr(self, previous):
            setattr(self, previous, [])
        getattr(self, previous).append(method(x))

        return method(x)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        else:
            return self == other


class HasThings(object):
    def __init__(self, things, number):
        self.things = things
        self.number = number

    def __getattr__(self, attr):
        results = []
        if self.number == 1:
            for thing in self.things:
                result = Thing(str(attr))
                setattr(thing, attr, result)
                results.append(result)
        else:
            for thing in self.things:
                things = []
                for i in range(self.number):
                    things.append(Thing(str(attr)[:-1]))

                result = ThingSet(things)
                setattr(thing, attr, result)
                results += things

        return ThingSet(results)
        # return self.things


class ObjectThings(object):
    def __init__(self, subjects, predicate):
        self.subjects = subjects
        self.predicate = predicate

    def __getattr__(self, attr):
        results = []
        for subject in self.subjects:
            # results.append(Thing(attr))
            # setattr(subject, self.predicate, results[-1])
            setattr(subject, self.predicate, Thing(attr))

        return self.subjects


class IsTheThings(object):
    def __init__(self, things):
        self.things = things

    def __getattr__(self, attr):
        return ObjectThings(self.things, attr)


class ThingSet(tuple):
    def __init__(self, things):
        self.things = things

        self.each = self
        self.having = lambda x: HasThings(self, x)
        self.being_the = IsTheThings(self)
        self.and_the = IsTheThings(self)

    def __getitem__(self, idx):
        return self.things[idx]

    def __len__(self):
        return len(self.things)
      
___________________________________________________
class Thing (object):
    class IsA:
        def __init__(self, parent):
            self.__parent = parent
            
        def __getattr__(self, name):
            setattr(self.__parent, f"is_a_{name}", True)
            
    class IsNotA:
        def __init__(self, parent):
            self.__parent = parent
            
        def __getattr__(self, name):
            setattr(self.__parent, f"is_a_{name}", False)
            
    class IsThe:
        def __init__(self, parent):
            self.__parent = parent
            
        def __getattr__(self, name):
            class What:
                def __init__(self, parent, what):
                    self.__parent = parent
                    self.__what = what
                def __getattr__(self, name):
                    setattr(self.__parent, self.__what, name)
                    return self.__parent
            return What(self.__parent, name)
            
    class Can:
        def __init__(self, parent):
            self.__parent = parent
            
        def __getattr__(self, name):
            def setCan(fnc, results=""):
                fnc.__globals__['name'] = self.__parent.name
                canFnc = fnc
                if len(results) > 0:
                    setattr(self.__parent, results, [])
                    def canWithTrack(*args, **kwargs):
                        res = fnc(*args, **kwargs)
                        getattr(self.__parent, results).append(res)
                        return res
                    canFnc = canWithTrack
                setattr(self.__parent, name, canFnc)
            return setCan
    
    class Tuple(tuple):
        class Each:
            def __init__(self, tup):
                self.__tup = tup
                
            def __getattr__(self, name):
                self.__tup = Thing.Tuple(getattr(e, name) for e in self.__tup)
                return self
            
            def __call__(self, *args):
                self.__tup = Thing.Tuple(e(*args) for e in self.__tup)
                return self
        
        def __new__ (cls, a):
            return super(Thing.Tuple, cls).__new__(cls, tuple(a))
        
        def __init__(self, _):
            self.each = Thing.Tuple.Each(self)

        
    class Has:
        def __init__(self, parent, n):
            self.__parent = parent
            self.__n = n
            
        def __getattr__(self, name):
            if self.__n > 1:
                attrName = name[:-1]
                attr = Thing.Tuple(Thing(attrName) for i in range(self.__n))
                for a in attr:
                    a.__setattr__(f"is_{attrName}", True)
            else:
                attr = Thing(name)
                attr.__setattr__(f"is_{name}", True)
            setattr(self.__parent, name, attr)
            return getattr(self.__parent, name)
            
    def __init__(self, name=""):
        self.name = name
        self.is_a = Thing.IsA(self)
        self.is_not_a = Thing.IsNotA(self)
        self.is_the = Thing.IsThe(self)
        self.being_the = Thing.IsThe(self)
        self.and_the = Thing.IsThe(self)
        self.can = Thing.Can(self)
        
    def has(self, n):
        return Thing.Has(self, n)
        
    def having(self, n):
        return self.has(n)
      
___________________________________________________
class ThingProperties(list):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        
    def __getattr__(self, attr):
        if attr not in self:
            self.append(attr)
        setattr(self._parent, attr, self)
        return ThingProperties(self._parent)
    
class ThingTuple(tuple):
    def __new__(cls, size, parent):
        tt = super().__new__(cls, size * (Thing(), ))
        tt.parent = parent
        return tt
    
    def __getattr__(self, attr):
        singular_attr = attr
        if len(self) > 1:
            singular_attr = attr[:-1]
        else:
            self[0].name = attr
            setattr(self.parent, attr, self[0])
            return self[0]

        for thing in self:
            thing.name = singular_attr
            getattr(thing.is_a, singular_attr)
        setattr(self.parent, attr, self)
        if attr == "each":
            # this each does not actually work
            return self[0]
        return self


class ThingProperty(object):
    def __init__(self, parent):
        self._parent = parent
        self._property = None
        
    def __getattr__(self, attr):
        self._property = attr
        return ThingPropertyValue(self)
        

class ThingPropertyValue(object):
    def __init__(self, parent):
        self._parent = parent
        
    def __getattr__(self, attr):
        setattr(self._parent._parent, self._parent._property, attr)
        return self._parent._parent
    

class CanMethod(object):
    def __init__(self, parent):
        self._parent = parent
        self._method = None
        self._past = None
        
    def __getattr__(self, attr):
        self._method = ThingFunction(self, attr)
        return self._method
    
    def __call__(self, func, past=None, **kwargs):
        setattr(self._parent, self._method, func)
    

class ThingFunction(object):
    def __init__(self, parent, method_name):
        self._parent = parent
        self._function = method_name
        
    def __call__(self, func, past=None, *args, **kwargs):
        func.__globals__["name"] = self._parent._parent.name
        if past:
            setattr(self._parent._parent, past, [])
        def loggin_func(*args, **kwargs):
            res = func(*args, **kwargs)
            if past:
                getattr(self._parent._parent, past).append(res)
            return res
        setattr(self._parent._parent, self._function, loggin_func)
        

class Thing (object):
    def __init__(self, name=None):
        self.name = name
        self._properties = {True: ThingProperties(self), False: ThingProperties(self)}
        
    def __getattr__(self, attr):
        if attr == "is_a":
            return self._properties[True]
        if attr == "is_not_a":
            return self._properties[False]
        if attr == "is_the" or attr == "being_the" or attr == "and_the":
            return ThingProperty(self)
        if attr.startswith("is_a_"):
            return attr[5:] in self._properties[True]
        if attr.startswith("is_not_a_"):
            return attr[9:] in self._properties[False]
        if attr.startswith("is_"):
            return attr[3:] in self._properties[True]
        if attr.startswith("is_not_"):
            return attr[7:] in self._properties[False]
        if attr == "can":
            return CanMethod(self)

    def has(self, count):
        return ThingTuple(count, self)
    
    def having(self, count):
        return ThingTuple(count, self)
      
___________________________________________________
from collections import defaultdict


class Thing:
    def __init__(self, name):
        self.name = name
        self.method_call_tracker = defaultdict(list)

    def __getattr__(self, name):
        if name in self.method_call_tracker:
            return self.method_call_tracker[name]
        return super().__getattr__(self, name)

    @property
    def is_a(self):
        return BoolBuilder(self, True)

    @property
    def is_not_a(self):
        return BoolBuilder(self, False)

    @property
    def is_the(self):
        return PropertyBuilderPhase1(self)
    
    @property
    def being_the(self):
        return PropertyBuilderPhase1(self)

    @property
    def and_the(self):
        return PropertyBuilderPhase1(self)
    
    @property
    def can(self):
        return MethodBuilderPhase1(self)

    def has(self, amount):
        return ChildBuilder(self, amount)

    def having(self, amount):
        return ChildBuilder(self, amount)


class ThingTuple(tuple):
    def __new__(cls, *args):
        return super().__new__(cls, *args)

    @property
    def each(self):
        return EachBuilder(self)


class BoolBuilder:
    def __init__(self, target, value):
        self.target = target
        self.value = value

    def __getattr__(self, name):
        setattr(self.target, f'is_a_{name}', self.value)
        return self.target


class ChildBuilder:
    def __init__(self, target, value):
        self.target = target
        self.value = value
        
    def __getattr__(self, name):

        def create_thing():
            singular_name = name[:-1] if self.value > 1 else name
            thing = Thing(singular_name)
            setattr(thing, f'is_{singular_name}', True)
            return thing

        if self.value > 1:
            value = ThingTuple(create_thing() for _ in range(self.value))
        else:
            value = create_thing()

        setattr(self.target, name, value)

        return value


class PropertyBuilderPhase1:
    def __init__(self, target):
        self.target = target

    def __getattr__(self, name):
        return PropertyBuilderPhase2(self.target, name)


class PropertyBuilderPhase2:
    def __init__(self, target, property):
        self.target = target
        self.property = property

    def __getattr__(self, property_value):
        setattr(self.target, self.property, property_value)
        return self.target


class MethodBuilderPhase1:
    def __init__(self, target):
        self.target = target

    def __getattr__(self, name):
        return MethodBuilderPhase2(self.target, name)


class MethodBuilderPhase2:
    def __init__(self, target, funcname):
        self.target = target
        self.funcname = funcname

    def __call__(self, func, past=None):
        setattr(self.target, self.funcname, self.wrapper(self.target, func, past))
        return self.target

    @staticmethod
    def wrapper(target, func, past=None):
        def decorator(*args, **kwargs):
            func.__globals__['name'] = target.name
            r = func(*args, **kwargs)
            if past is not None:
                target.method_call_tracker[past].append(r)
            return r
        return decorator


class EachBuilder:
    def __init__(self, target_tuple):
        self.target_tuple = target_tuple

    @property
    def being_the(self):
        return TuplePropertyBuilderPhase1(self.target_tuple)

    @property
    def and_the(self):
        return TuplePropertyBuilderPhase1(self.target_tuple)

    def having(self, amount):
        return TupleChildBuilder(self.target_tuple, amount)


class TupleChildBuilder:
    def __init__(self, target_tuple, value):
        self.target_tuple = target_tuple
        self.value = value

    def __getattr__(self, name):

        def create_thing():
            singular_name = name[:-1] if self.value > 1 else name
            thing = Thing(singular_name)
            setattr(thing, f'is_{singular_name}', True)
            return thing

        values = []

        for target in self.target_tuple:
            if self.value > 1:
                value = ThingTuple(create_thing() for _ in range(self.value))
            else:
                value = create_thing()

            setattr(target, name, value)

            values.append(value)

        return EachBuilder(values)


class TuplePropertyBuilderPhase1:
    def __init__(self, target_tuple):
        self.target_tuple = target_tuple

    def __getattr__(self, name):
        return TuplePropertyBuilderPhase2(self.target_tuple, name)


class TuplePropertyBuilderPhase2:
    def __init__(self, target_tuple, property):
        self.target_tuple = target_tuple
        self.property = property

    def __getattr__(self, property_value):
        for target in self.target_tuple:
            setattr(target, self.property, property_value)
        return EachBuilder(self.target_tuple)
      
___________________________________________________
import functools
from typing import Any, Callable, List, Union


class Can:
    def __init__(self, thing: 'Thing', set_attr):
        self._thing = thing
        self._set_thing_attr = set_attr
        self._methods_registry = {}
        self._tracked_calls = []

    def _skill_decorator(self, skill: Callable):
        @functools.wraps(skill)
        def wrapper(*args, **kwargs):
            thing_attrs = {
                k: v for k, v in vars(self._thing).items()
                if not k.startswith('_')
            }

            func_globals = skill.__globals__
            saved_values = func_globals.copy()
            func_globals.update(thing_attrs)

            try:
                result = skill(*args, **kwargs)
            finally:
                func_globals = saved_values

            self._tracked_calls.append(result)
            return result

        return wrapper

    def __getattr__(self, item: str):
        def add_skill(skill: Callable, past=''):
            setattr(self._thing, item, self._skill_decorator(skill))

            if past:
                def skill_history():
                    return self._tracked_calls
                self._set_thing_attr(past, skill_history())

        return add_skill


class Is:
    def __init__(self, thing: 'Thing', set_thing_attr: Callable):
        self.__thing = thing
        self.__set_thing_attr = set_thing_attr
        self.__state: bool = True

    def __call__(self, state=True):
        self.__state = state
        return self

    def __getattr__(self, item: str):
        self.__set_thing_attr(f'is_a_{item}', self.__state)


class IsTheSetter:
    def __init__(self, attr_name: str, set_thing_attr: Callable):
        self.__set_thing_attr = set_thing_attr
        self.__attr_name = attr_name

    def __getattr__(self, item: str):
        self.__set_thing_attr(self.__attr_name, item)


class IsThe:
    def __init__(self, thing: 'Thing', set_thing_attr: Callable):
        self.__thing = thing
        self.__set_thing_attr = set_thing_attr

    def __getattr__(self, item: str):
        return IsTheSetter(item, self.__set_thing_attr)


class BeingTheSetter:
    def __init__(self,
                 attr_name: str,
                 things_chain: 'ThingsChain',
                 things: List['Thing']):
        self.__name = attr_name
        self.__things_chain = things_chain
        self.__things = things

    def __getattr__(self, item: str):
        for thing in self.__things:
            setattr(thing, self.__name, item)
        return self.__things_chain


class BeingThe:
    def __init__(self,
                 things_chain: 'ThingsChain',
                 things: List['Thing']):
        self.__things_chain = things_chain
        self.__things = things

    def __getattr__(self, item: str):
        return BeingTheSetter(item, self.__things_chain, self.__things)


class Having:
    def __init__(self,
                 count: int,
                 things_chain: 'ThingsChain',
                 things: List['Thing']):
        assert count >= 1, "Invalid things count"
        self.__count = count
        self.__things_chain = things_chain
        self.__things = things

    def __getattr__(self, item: str):
        if self.__count == 1:
            new_individual_things = []
            for thing in self.__things:
                new_thing = Thing(f'{item}')
                setattr(thing, item, new_thing)
                new_individual_things.append(new_thing)
            return ThingsChain(new_individual_things)
        else:
            new_thing_groups = []
            for thing in self.__things:
                new_things = Things(
                    Thing(f'{item[:-1]}')
                    for i in range(self.__count)
                )
                setattr(thing, item, new_things)
                new_thing_groups.append(new_things)
            return Things(new_thing_groups)


class ThingsChain:
    def __init__(self, things: List[Union['Thing', 'Things']]):
        all_things = []
        for t in things:
            if isinstance(t, Thing):
                all_things.append(t)
            else:  # Things
                all_things.extend(t)
        self.__things = all_things

    def having(self, count: int):
        return Having(count, self, self.__things)

    @property
    def being_the(self):
        return BeingThe(self, self.__things)

    @property
    def and_the(self):
        return self.being_the


class Things(tuple):
    @functools.cached_property
    def each(self):
        return ThingsChain(list(self))


class Has:
    def __init__(self, count: int, thing: 'Thing'):
        assert count >= 1, "Invalid things count"
        self.__count = count
        self.__thing = thing

    def __getattr__(self, item: str):
        if self.__count == 1:
            new_thing = Thing(f'{item}')
            setattr(self.__thing, item, new_thing)
            return ThingsChain([new_thing])
        else:
            new_things = Things(
                Thing(f'{item[:-1]}')
                for i in range(self.__count)
            )
            setattr(self.__thing, item, new_things)
            return new_things


class Thing(object):
    def __init__(self, thing_name: str):
        self.name = thing_name
        self.__attrs = {}
        self.__is = Is(self, self.__set_attr)
        self.__is_the = IsThe(self, self.__set_attr)

    def __str__(self):
        return f"Thing('{self.name}')"

    def __repr__(self):
        return self.__str__()

    def has(self, count: int):
        return Has(count, self)

    def having(self, count: int):
        things = [self]
        return Having(count, ThingsChain(things), things)

    @property
    def is_a(self):
        return self.__is(True)

    @property
    def is_not_a(self):
        return self.__is(False)

    @property
    def is_the(self):
        return self.__is_the

    def __getattr__(self, item):
        if item in self.__attrs:
            if callable(self.__attrs[item]):
                return self.__attrs[item]()
            return self.__attrs[item]
        return item

    def __set_attr(self, attr_name: str, value: Any):
        self.__attrs[attr_name] = value

    @property
    def can(self):
        return Can(self, self.__set_attr)
      
___________________________________________________
class ThingTuple(tuple):
    @property
    def each(self):
        class Each:
            def __init__(lself, underlying):
                lself.underlying = underlying

            def having(lself, n):
                class Having:
                    def __getattr__(_, attr):
                        return Each(ThingTuple(getattr(i.having(n), attr) for i in lself.underlying))
                return Having()

            @property
            def being_the(lself):
                class BeingThe:
                    def __getattr__(_, attr):
                        class Value:
                            def __getattr__(_, val):
                                for i in lself.underlying:
                                    getattr(getattr(i.being_the, attr), val)
                                return lself
                        return Value()
                return BeingThe()
            and_the = being_the
        return Each(self)

class Thing:
    __slots__ = 'name', '_things_being', '_entities', '_ofs', '_funs', '_hists'

    def __init__(self, name):
        self.name = name
        self._things_being = set()
        self._entities = {}
        self._funs = {}
        self._hists = {}
        self._ofs = {}

    @property
    def is_a(self):
        class IsA:
            def __getattribute__(_, attr):
                self._things_being.add(attr)
        return IsA()

    @property
    def is_not_a(self):
        class IsNotA:
            def __getattribute__(_, attr):
                if attr in self._things_being:
                    self._things_being.remove(attr)
        return IsNotA()

    @property
    def is_the(self):
        class IsThe:
            def __getattribute__(_, attr):
                if not attr.endswith('_of'):
                    raise AttributeError
                class Of:
                    def __getattribute__(_, what):
                        self._ofs[attr[:-3]] = what
                return Of()
        return IsThe()

    def has(self, n):
        class Has:
            def __getattribute__(_, attr):
                if n == 1:
                    thing = Thing(attr)
                else:
                    thing = ThingTuple(Thing(attr[:-1]) for _ in range(n))
                self._entities[attr] = thing
                return thing
        return Has()

    having = has

    @property
    def being_the(self):
        class BeingThe:
            def __getattr__(_, attr):
                class Value:
                    def __getattr__(_, val):
                        self._entities[attr] = val
                        return self
                return Value()
        return BeingThe()
    and_the = being_the

    @property
    def can(self):
        class Can:
            def __getattr__(_, attr):
                def def_fun(method, history_name=None):
                    def myfun(*args, **kwargs):
                        method.__globals__['name'] = self.name
                        v = method(*args, **kwargs)
                        if history_name is not None:
                            self._hists[history_name].append(v)
                        return v
                    if history_name is not None:
                        self._hists[history_name] = []
                    self._funs[attr] = myfun
                return def_fun
        return Can()

    def __getattr__(self, attr):
        if attr.startswith('is_a_'):
            return attr[5:] in self._things_being
        elif attr.startswith('is_'):
            return attr[3:] == self.name
        elif attr.endswith('_of') and attr[:-3] in self._ofs:
            return self._ofs[attr[:-3]]
        elif attr in self._entities:
            return self._entities[attr]
        elif attr in self._funs:
            return self._funs[attr]
        elif attr in self._hists:
            return self._hists[attr]
        raise AttributeError(attr)
        
___________________________________________________
class PropertyCollector:
    def __init__(self, start):
        self.property_chain = [start]
        
    def __getattr__(self, name):
        self.property_chain.append(name)
        return self
    
    def __call__(self, *args):
        self.property_chain.append(args)
        return self

name = "Jane"
class Thing (object):
    def __init__(self, name):
        self.name = name
        self.properties = None
        
    def __getattr__(self, name):
        if self.properties is not None:
            self.parse_properties(self.properties.property_chain)
        
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            self.properties = PropertyCollector(name)
            return self.properties
    
    def no_log_calls(self, func):
        def _(*args):
            name = self.name
            return func(*args)
        return _
    
    def log_calls(self, func, cname):
        def log(*args):
            name = self.name
            print(name)
            n = func(*args)
            self.__dict__[cname].append(n)
            return n
        return log
        
    def parse_properties(self, chain):
        if chain[0] in ["is_a", "is_not_a"]:
            self.__dict__["is_a_" + chain[1]] = (chain[0] == "is_a")
        elif chain[0] in ["has", "having"]:
            print(chain, len(chain))
            thing = Thing(chain[2] if chain[1][0] == 1 else chain[2][:-1])
            if len(chain) > 3:
                thing.parse_properties(chain[3:])
                
            if chain[1][0] == 1:
                self.__dict__[chain[2]] = thing
            else:
                self.__dict__[chain[2]] = (thing,) * chain[1][0]
        elif chain[0] in ["being_the", "and_the"]:
            self.__dict__[chain[1]] = chain[2]
            if len(chain) > 3:
                self.parse_properties(chain[3:])
        elif chain[0] == "each":
            self.parse_properties(chain[1:])
        elif chain[0] == "is_the":
            self.__dict__[chain[1]] = chain[2]
        elif chain[0] == "can":
            if len(chain[2]) == 2:
                self.__dict__[chain[1]] = self.log_calls(
                    chain[2][0], chain[2][1])
                self.__dict__[chain[2][1]] = []
            else:
                self.__dict__[chain[1]] = self.no_log_calls(chain[2][0])
        
