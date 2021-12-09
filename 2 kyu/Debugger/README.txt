Imagine you have a large project where is suddenly going something very messy. You are not able to guess what it is and don't want to debug all the code through. Your project has one base class.

In this kata you will write metaclass Meta for your base class, which will collect data about all attribute accesses and method calls in all project classes. From this data you can then better guess what is happening or which method call is bottleneck of your app.

We will use class Debugger to store the data. Method call collection should look like this:

Debugger.method_calls.append({
    'class': ..., # class object, not string
    'method': ..., # method name, string
    'args': args, # all args, including self
    'kwargs': kwargs
})
Attribute access collection should look like this:

Debugger.attribute_accesses.append({
    'action': 'set', # set/get
    'class': ..., # class object, not string
    'attribute': ..., # name of attribute, string
    'value': value # actual value
})
You should NOT log calls of getter/setter methods that you might create by meta class.

See the tests if in doubts.
