5571d9fc11526780a000011a


the_context = null
being_the = null
name = null

has = having = (length) ->
  the_context.having(length)

makeProxy = (obj, getFn) -> new Proxy({obj}, get: (target, fldName) ->
  return Reflect.get(target, fldName) if fldName in ['__lookupGetter__', '__lookupSetter__']
  return Reflect.get(target, fldName) unless 'string' == typeof fldName # Prevent Node inspection issues
  getFn(target, fldName)
)

is_a_proxy = (obj, val) -> makeProxy(obj, (target, fldName) -> target.obj["is_a_#{fldName}"] = val)

is_the_proxy = (obj) ->
  makeProxy obj, (target, fieldName) ->
    makeProxy obj, (target, fldName) ->
      target.obj[fieldName] = fldName
      target.obj

has_proxy = (obj, length) ->
  makeProxy obj, (target, fldName) ->
    if length == 1
      target.obj[fldName] = new Thing(fldName)
    else
      target.obj[fldName] = []
      target.obj[fldName].each = (a) ->
        for item in target.obj[fldName]
          the_context = item
          being_the = item.is_the
          a(item)
      for i in [1..length]
        target.obj[fldName].push(new Thing(fldName.replace(/(\w)s?$/, '$1')))
    return target.obj[fldName]

can_proxy = (obj) ->
  makeProxy obj, (target, fldName) ->
    (log, fn) ->
      [fn, log] = [log, null] unless fn
      return unless 'function' == typeof fn
      obj[log] = [] if log
      obj[fldName] = ->
        name = obj.name
        res = fn(arguments...)
        obj[log].push(res) if log
        res


class Thing
  constructor: (@name) ->
    @is_a     = is_a_proxy(@, true)
    @is_not_a = is_a_proxy(@, false)
    @can      = can_proxy(@)
    @is_the   = is_the_proxy(@)
    @and_the  = @is_the
  
  has: (length) -> has_proxy(@, length)

Thing::having = Thing::has

___________________________________________________
the_context = null
being_the = null
name = null

has = having = (length) ->
  the_context.having(length)

is_a_proxy = (obj, val) ->
  new Proxy({obj}, {
    get: (target, fldName) ->
      target.obj["is_a_#{fldName}"] = val
  })

is_the_proxy_lvl2 = (obj, fieldName) ->
  new Proxy({obj}, {
    get: (target, fldName) ->
      target.obj[fieldName] = fldName
      target.obj._proxy
  })

is_the_proxy = (obj) ->
  new Proxy({obj}, {
    get: (target, fldName) ->
      is_the_proxy_lvl2(obj, fldName)
  })

has_proxy = (obj, length) ->
  new Proxy({obj}, {
    get: (target, fldName) ->
      if length == 1
        target.obj[fldName] = new Thing(fldName)
      else
        target.obj[fldName] = []
        target.obj[fldName].each = (a) ->
          for item in target.obj[fldName]
            the_context = item
            being_the = item.is_the
            a(item)
        for i in [1..length]
          target.obj[fldName].push(new Thing(fldName.replace(/(\w)s?$/, '$1')))
      return target.obj[fldName]
  })


can_proxy = (obj) ->
  new Proxy({obj}, {
    get: (target, fldName) ->
      return (args...) ->
        args.unshift(null) if args.length == 1
        [log, fn] = args
        obj[log] = [] if log
        obj[fldName] = ->
          name = obj.name
          res = fn(arguments...)
          obj[log].push(res) if log
          res
  })


handler =
  get: (target, fieldName) ->
    return is_a_proxy(target, true) if fieldName == 'is_a'
    return is_a_proxy(target, false) if fieldName == 'is_not_a'
    return is_the_proxy(target) if fieldName in ['is_the', 'and_the']
    return can_proxy(target) if fieldName in ['can']
    return has_proxy.bind(target, target) if fieldName in ['has', 'having']
    return Reflect.get(target, fieldName)

Thing = (name) ->
  thing = {name}
  p = new Proxy(thing, handler)
  thing._proxy = p
  p.__proto__ = Thing.prototype
  p.__proto__.constructor = Thing
  p

___________________________________________________
$ = (fn)-> new Proxy {}, get: (_,id)-> fn id

Array::each = (fn)->
  fn(t) t for t,i in @
  @

things = (n,k)-> if n==1 then new Thing k else (new Thing k[...-1] for [0...n])
having = (n)-> $ (k)-> (t)-> t[k] = things n,k
being_the = $ (k)-> $ (v)->
  f = (t)-> t[k] = v
  f.and_the = $ (k)-> $ (v)-> (t)-> f t; t[k] = v
  f

class Thing
  constructor: (@name)->
  has:    (n)-> $ (k)=> @[k] = things n,k
  having: (n)-> @has n

Object.defineProperties Thing::,
  is_a    : get: -> $ (k)=> @['is_a_'+k]=yes
  is_not_a: get: -> $ (k)=> @['is_a_'+k]=no
  is_the  : get: -> $ (k)=> $ (v)=> @[k]=v
  can     : get: -> $ (k)=> (st,fn)=>
    if fn? then @[st]=[]
    else [fn,st] = [st,fn] # skip typeof
    @[k]=->
      global.name = @name # unsafe
      o = fn.apply @, arguments
      @[st]?.push o
      o

