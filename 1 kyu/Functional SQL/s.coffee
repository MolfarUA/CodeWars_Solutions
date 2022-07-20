545434090294935e7d0010ab


query = ->

  groupByRec = (arr, funcs) ->
    if funcs.length == 0
      return arr
    console.log arr, funcs
    res = Object.entries(arr.reduce(((rv, x, i) ->
      (rv[funcs[0](x)] = rv[funcs[0](x)] or []).push x
      rv
    ), {}))
    res.map (x) ->
      [
        +x[0] or x[0]
        groupByRec(x[1], funcs.slice(1))
      ]

  queryObj =
    selected: false
    selectFunc: (x) ->
      x
    fromed: false
    fromArr: []
    whereFuncs: []
    havingFuncs: []
    orderByFunc: (a, b) ->
      a - b
    orderByed: false
    groupByFuncs: null
    groupByed: false

  queryObj.select = (func) ->
    if queryObj.selected
      throw new Error('Duplicate SELECT')
    if func
      queryObj.selectFunc = func
    queryObj.selected = true
    queryObj

  queryObj.from = ->
    if queryObj.fromed
      throw new Error('Duplicate FROM')
    if arguments.length == 1
      queryObj.fromArr = arguments[0]
    else
      f = (a, b) ->
        [].concat(a.map((a) ->
          b.map((b) ->
            [].concat(a, b)))...)
      cartesian = (a, b, c...) ->
        if b
          return cartesian(f(a, b), c...)
        else
          return a
      queryObj.fromArr = cartesian(Array.from(arguments)...)
    queryObj.fromed = true
    queryObj

  queryObj.where = ->
    queryObj.whereFuncs.push Array.from(arguments)
    queryObj

  queryObj.having = ->
    queryObj.havingFuncs.push Array.from(arguments)
    queryObj

  queryObj.groupBy = ->
    if queryObj.groupByed
      throw new Error('Duplicate GROUPBY')
    queryObj.groupByFuncs = Array.from(arguments)
    queryObj.groupByed = true
    queryObj

  queryObj.orderBy = (condition) ->
    if queryObj.orderByed
      throw new Error('Duplicate ORDERBY')
    queryObj.orderByFunc = condition
    queryObj.orderByed = true
    queryObj

  queryObj.execute = ->
    resX = queryObj.fromArr
    console.log 'O', resX
    resX = resX.filter((x) ->
      ok = true
      funcs = queryObj.whereFuncs
      i = 0
      while i < funcs.length
        curOk = false
        j = 0
        while j < funcs[i].length
          curOk = curOk or funcs[i][j](x)
          ++j
        ok = ok and curOk
        i++
      ok
    )
    console.log 'W', resX
    if queryObj.groupByed
      resX = groupByRec(resX, queryObj.groupByFuncs)
    console.log 'G', resX
    resX = resX.sort(queryObj.orderByFunc)
    console.log 'S', resX
    resX = resX.filter((x) ->
      ok = true
      funcs = queryObj.havingFuncs
      i = 0
      while i < funcs.length
        curOk = false
        j = 0
        while j < funcs[i].length
          curOk = curOk or funcs[i][j](x)
          ++j
        ok = ok and curOk
        i++
      ok
    )
    resX = resX.map(queryObj.selectFunc)
    resX

  queryObj

___________________________________________
class Engine
  filter_fn_list        : []
  input_list_list       : null # once set
  group_by_fn_list      : null # once set
  grouped_filter_fn_list: []
  select_fn             : null # once set
  order_by_fn           : null # once set
  res_list_list         : null # once set
  
  constructor:()->
    @filter_fn_list        = []
    @grouped_filter_fn_list= []
  
  # ###################################################################################################
  #    API
  # ###################################################################################################
  select:(fn)->
    throw new Error "Duplicate SELECT" if @select_fn
    @select_fn = fn || (x) -> x
    @
  
  from:(input_list_list...)->
    throw new Error "Duplicate FROM" if @input_list_list
    @input_list_list = if input_list_list.length <= 1
      input_list_list[0].slice()
    else
      res_list_list = []
      input_list_list.reverse()
      for v in input_list_list[0]
        res_list_list.push [v]
      
      for i in [1 ... input_list_list.length] by 1
        new_res_list_list = []
        for v in input_list_list[i]
          for res_list in res_list_list
            new_res_list_list.push [v].concat res_list
        res_list_list = new_res_list_list
      
      res_list_list
    @
  
  where:(filter_fn_list...)->
    @filter_fn_list.push @_or filter_fn_list
    @
  
  orderBy:(fn)->
    throw new Error("Duplicate ORDERBY") if @order_by_fn
    @order_by_fn = fn
    @
  
  groupBy:(group_by_fn_list...)->
    throw new Error("Duplicate GROUPBY") if @group_by_fn_list
    @group_by_fn_list = group_by_fn_list
    @
  
  having:(filter_fn_list...)->
    @grouped_filter_fn_list.push @_or filter_fn_list
    @
  
  execute:()->
    return @res_list_list if @res_list_list
    res_list_list = @input_list_list || []
    
    res_list_list = @filter res_list_list, @filter_fn_list
    if @group_by_fn_list
      res_list_list = @apply_group_by res_list_list, 0
    else 
      res_list_list.sort @order_by_fn               if @order_by_fn
      res_list_list = res_list_list.map @select_fn  if @select_fn
    
    @res_list_list = res_list_list
  
  # ###################################################################################################
  #    internal
  # ###################################################################################################
  _or:(fn_list)->
    return fn_list[0] if fn_list.length == 1
    (in_list)->
      for fn in fn_list
        return true if fn in_list
      false
  
  filter:(res_list_list, filter_fn_list)->
    new_res_list_list = []
    for res_list in res_list_list
      found = false
      for fn in filter_fn_list
        if !fn res_list
          found = true
          break
      new_res_list_list.push res_list if !found
    new_res_list_list
  
  apply_group_by:(in_list_list, i)->
    last = i == @group_by_fn_list.length - 1
    fn = @group_by_fn_list[i]
    key_to_pair_hash = {}
    for v in in_list_list
      key = fn v
      key_to_pair_hash[key] ?= [key, []]
      key_to_pair_hash[key][1].push v
    
    res_list_list = []
    for _k,v of key_to_pair_hash
      [key,list] = v
      res_list_list.push [
        key
        if last then list else @apply_group_by list, i + 1
      ]
    
    if last
      res_list_list = @filter res_list_list, @grouped_filter_fn_list
      res_list_list.sort @order_by_fn               if @order_by_fn
      res_list_list = res_list_list.map @select_fn  if @select_fn
    
    res_list_list

query = ()->new Engine

___________________________________________
query = () ->
  return new Query()

guard = (condition, message) ->
  if !condition
    throw new Error(message)
  return

cartesian = (arr) ->
  arr.reduce ((a, b) ->
    return a.map((x) ->
      return b.map (y) ->
        return x.concat [ y ]
    ).reduce ((a, b) ->
      return a.concat b
    ), []
  ), [ [] ]

identity = (e) ->
  e

pass = (e) ->
  true
  
typeIsArray = Array.isArray || ( value ) -> 
  return {}.toString.call( value ) is '[object Array]'
  
class Query
  constructor: () ->
    @fromExp = null
    @selectExp = null
    @whereExp = null
    @groupByExp = null
    @havingExp = null
    @orderByExp = null
  select: (selector) ->
    guard(@selectExp == null, "Duplicate SELECT")
    @selectExp = new SelectExp(selector)
    return this
  from: (clauses...) ->
    guard(@fromExp == null, "Duplicate FROM")
    @fromExp = new FromExp(clauses)
    return this
  where: (clauses...) ->
    if @whereExp == null
      @whereExp = new FilterExp()
    @whereExp.add((e) -> new FilterExp(clauses).any(e))
    return this
  groupBy: (clauses...) ->
    guard(@groupByExp == null, "Duplicate GROUPBY")
    @groupByExp = new GroupByExp(clauses)
    return this
  having: (clauses...) ->
    if @havingExp == null
      @havingExp = new FilterExp()
    @havingExp.add((e) -> new FilterExp(clauses).any(e))
    return this
  orderBy: (comparer) ->
    guard(@orderByExp == null, "Duplicate ORDERBY")
    @orderByExp = new OrderByExp(comparer)
    return this
  execute: () ->
    fromExp = @fromExp || new FromExp()
    whereExp = @whereExp || new FilterExp()
    groupByExp = @groupByExp
    havingExp = @havingExp || new FilterExp()
    selectExp = @selectExp || new SelectExp()
    orderByExp = @orderByExp
    records = whereExp.filterAll(fromExp.from())
    results = null
    if groupByExp != null
      results = selectExp.select(havingExp.filterAll(groupByExp.groupBy(records)))
    else
      results = selectExp.select(records)
    if orderByExp != null
      results = orderByExp.orderBy(results)
    return results
  
class SelectExp
  constructor: (selector) ->
    if (selector == null || typeof selector == 'undefined' ) 
      selector = identity
    @selector = selector
  select: (source) ->
    return source.map(@selector)
  
class FromExp
  constructor: (source) ->
    if source == null || typeof source == 'undefined' || source.length == 0
      source = [[]]
    @source = source
  from: () ->
    if @source.length == 1
      return @source[0]
    return cartesian(@source)
  
class FilterExp
  constructor: (filters) ->
    if filters == null || typeof filters == 'undefined'
      filters = []
    if !typeIsArray filters
      filters = [filters]
    @filters = filters
  add: (filter) ->
    @filters.push filter
  all: (e) ->
    filters = @filters
    if filters.length == 0
      filters = [pass]
    return (filters.every (fn) ->
      fn e)
  any: (e) ->
    filters = @filters
    if filters.length == 0
      filters = [pass]
    return (filters.some (fn) ->
      fn e)
  filterAll: (source) ->
    filters = @filters
    if filters.length == 0
      filters = [pass]
    return (source.filter (e) ->
      return (filters.every (fn) ->
        fn e))
  filterAny: (source) ->
    filters = @filters
    if filters.length == 0
      filters = [pass]
    return (source.filter (e) ->
      return (filters.some (fn) ->
        fn e))

class OrderByExp 
  constructor: (comparer) ->
    if comparer == null || typeof comparer == 'undefined'
      comparer = (a, b) -> a - b
    @comparer = comparer
  orderBy: (source) ->
    return source.sort(@comparer)
  
class GroupByExp 
  constructor: (keySelector) ->
    if keySelector == null || typeof keySelector == 'undefined' || keySelector.length == 0
      keySelector = [identity]
    @keySelector = keySelector
  groupBy: (source) ->
    tree = []
    i = 0
    while i < source.length
      item = source[i]
      node = tree
      j = 0
      while j < @keySelector.length
        selector = @keySelector[j]
        key = selector(item)
        nextNode = node.find((e) ->
          e[0] == key
        )
        if typeof nextNode == 'undefined'
          nextNode = [
            key
            []
          ]
          node.push nextNode
        node = nextNode[1]
        j++
      node.push item
      i++
    return tree

___________________________________________
is_f = (f) -> typeof f == 'function'

class SqlQuery
  constructor: ->
    @_select  = undefined
    @_from    = undefined
    @_where   = []
    @_orderBy = undefined
    @_groupBy = undefined
    @_having  = []

  select: (select = null) ->
    throw Error('Duplicate SELECT') unless 'undefined' == typeof @_select
    @_select = select
    @

  from: (args...) ->
    throw Error('Duplicate FROM') unless 'undefined' == typeof @_from
    @_from = args.shift()
    if args.length > 0
      @_from = @_from.map((a) -> [a])
    while args.length > 0
      _from = []
      from = args.shift()
      for row in @_from
        for f in from
          r = row[..]
          r.push(f)
          _from.push(r)
      @_from = _from
    @

  where: (where...) ->
    @_where.push(where)
    @

  orderBy: (orderBy) ->
    throw Error('Duplicate ORDERBY') unless 'undefined' == typeof @_orderBy
    @_orderBy = orderBy
    @

  groupBy: (groupBy...) ->
    throw Error('Duplicate GROUPBY') unless 'undefined' == typeof @_groupBy
    @_groupBy = groupBy
    @

  having: (having...) ->
    @_having.push(having)
    @

  executeGroupBy: (res) ->
    groupBy = @_groupBy[0]
    doGroupBy = (res, groupBy) ->
      ress = {}
      for rez in res
        k = groupBy(rez)
        ress[k] ?= [k, []]
        ress[k][1].push(rez)
      Object.values(ress)
    walk = (groups, d, l) =>
      for group in groups
        if d == l
          group[1] = doGroupBy(group[1], @_groupBy[l])
        else
          group[1] = walk(group[1], d + 1, l)
      groups
    groups = doGroupBy(res, groupBy)
    for l in [1...@_groupBy.length]
      groups = walk(groups, 1, l)
    groups


  filter: (res, where) ->
    f = (x) ->
      where.reduce(((andWhere, a) ->
        andWhere and a.reduce(((orWhere, b) ->
          orWhere or b(x)
        ), false)
      ), true)
    res.filter(f)

  execute: ->
    res = @_from ? []

    res = @filter(res, @_where) if @_where.length

    if @_groupBy and is_f @_groupBy[0]
      res = @executeGroupBy(res)

    if is_f @_orderBy
      ob = if @_groupBy then (a, b) => @_orderBy(a[0], b[0]) else @_orderBy
      res = res[..].sort(ob)

    res = @filter(res, @_having) if @_having.length

    if is_f @_select
      res = res.map(@_select)
    res


query = ->
  new SqlQuery()
_______________________________________
ID  = (x  ) -> (x)
AND = (fns) -> (x) -> fns.every (fn) -> fn x
OR  = (fns) -> (x) -> fns.some  (fn) -> fn x

product = (arr) -> arr.reduce ((res, x) -> [].concat(y.concat [z] for z in x for y in res...)), [[]]
grouper = (arr, fns) -> arr.reduce ((res, x) ->
    (fns.reduce ((groups, fn) ->
      key = fn(x); idx = groups.findIndex (group) -> key is group[0]
      groups[idx = groups.length] = [key, []] if idx < 0
      groups[idx][1]), res).push(x)
    res), []

set = (object, property, value) -> if property of object then throw Error("Duplicate #{property}") else object[property] = value

query = ->
  sms = WHERE: [], HAVING: [] # SQL Statements
  qry =
    select:  (fn  =  ID) -> set sms, "SELECT",  fn ; qry
    from:    (a, arr...) -> set sms, "FROM", (if arr.length then product [a].concat arr else a); qry
    orderBy: (fn       ) -> set sms, "ORDERBY", fn ; qry
    groupBy: (   fns...) -> set sms, "GROUPBY", fns; qry
    where:   (   fns...) -> sms.WHERE .push OR fns;  qry
    having:  (   fns...) -> sms.HAVING.push OR fns;  qry
    execute:             ->
      res = sms.FROM ? [];
      res = res.filter AND sms.WHERE   if sms.WHERE.length
      res = grouper res,   sms.GROUPBY if sms.GROUPBY
      res = res.filter AND sms.HAVING  if sms.HAVING.length
      res = [res...].sort  sms.ORDERBY if sms.ORDERBY
      if sms.SELECT then res.map sms.SELECT else res
