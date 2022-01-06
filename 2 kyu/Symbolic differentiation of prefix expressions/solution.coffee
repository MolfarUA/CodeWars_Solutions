

diff = (expr) ->
  console.log(expr)
  parsed = parse(expr)
  parsed.diff()

parse = (expr) ->
  parsed = undefined
  matchers.forEach (matcher) ->
    if matcher(expr)
      parsed = matcher(expr)
    return
  parsed

constant = (expr) ->
  if isNaN(parseInt(expr))
    return false
  {
    type: 'constant'
    expr: expr
    diff: ->
      '0'

  }

variable = (expr) ->
  if expr.length != 1
    return false
  if !isNaN(parseInt(expr))
    return false
  {
    type: 'variable'
    expr: expr
    diff: ->
      '1'

  }

sum = (expr) ->
  regex = /^\(\+ (.*)\)$/
  if !regex.test(expr)
    return false
  args = parseSub(regex.exec(expr)[1])
  arg1 = args[0]
  arg2 = args[1]
  {
    type: 'sum'
    expr: expr
    diff: ->
      diff1 = arg1.diff()
      diff2 = arg2.diff()
      cleanSum diff1, diff2

  }

cleanSum = (arg1, arg2) ->
  if parseInt(arg1) == 0
    return arg2
  if parseInt(arg2) == 0
    return arg1
  if !isNaN(parseInt(arg2)) and !isNaN(parseInt(arg1))
    return '' + (parseInt(arg1) + parseInt(arg2))
  '(+ ' + arg1 + ' ' + arg2 + ')'

remainder = (expr) ->
  regex = /^\(\- (.*)\)$/
  if !regex.test(expr)
    return false
  args = parseSub(regex.exec(expr)[1])
  arg1 = args[0]
  arg2 = args[1]
  {
    type: 'remainder'
    expr: expr
    diff: ->
      diff1 = arg1.diff()
      diff2 = arg2.diff()
      cleanRemainder diff1, diff2

  }

cleanRemainder = (arg1, arg2) ->
  if !isNaN(parseInt(arg2)) and !isNaN(parseInt(arg1))
    return '' + (parseInt(arg1) - parseInt(arg2))
  if parseInt(arg1) == 0
    return ''+ arg2
  if parseInt(arg2) == 0
    return '' + arg1
  '(- ' + arg1 + ' ' + arg2 + ')'

product = (expr) ->
  regex = /^\(\* (.*)\)$/
  if !regex.test(expr)
    return false
  args = parseSub(regex.exec(expr)[1])
  arg1 = args[0]
  arg2 = args[1]
  {
    type: 'product'
    expr: expr
    diff: ->
      diff1 = arg1.diff()
      diff2 = arg2.diff()
      prod1 = cleanProduct(diff1, arg2.expr)
      prod2 = cleanProduct(arg1.expr, diff2)
      cleanSum prod1, prod2

  }

cleanProduct = (arg1, arg2) ->
  if parseInt(arg1) == 0
    return '0'
  if parseInt(arg2) == 0
    return '0'
  if parseInt(arg1) == 1
    return arg2
  if parseInt(arg2) == 1
    return arg1
  if !isNaN(parseInt(arg2)) and !isNaN(parseInt(arg1))
    return '' + parseInt(arg1) * parseInt(arg2)
  '(* ' + arg1 + ' ' + arg2 + ')'

quotient = (expr) ->
  regex = /^\(\/ (.*)\)$/
  if !regex.test(expr)
    return false
  args = parseSub(regex.exec(expr)[1])
  arg1 = args[0]
  arg2 = args[1]
  {
    type: 'quotient'
    expr: expr
    diff: ->
      diff1 = arg1.diff()
      diff2 = arg2.diff()
      prod1 = cleanProduct(diff1, arg2.expr)
      prod2 = cleanProduct(arg1.expr, diff2)
      numerator = cleanRemainder(prod1, prod2)
      denominator = cleanPower(arg2.expr, '2')
      cleanQuotient numerator, denominator

  }

cleanQuotient = (n, d) ->
  if parseInt(n) == 0
    return '0'
  if parseInt(d) == 1
    return x
  if !isNaN(parseInt(n)) and !isNaN(parseInt(d))
    return '' + parseInt(n) / parseInt(d)
  '(/ ' + n + ' ' + d + ')'

power = (expr) ->
  regex = /^\(\^ (.*)\)$/
  if !regex.test(expr)
    return false
  args = parseSub(regex.exec(expr)[1])
  arg1 = args[0]
  arg2 = args[1]
  {
    type: 'power'
    expr: expr
    diff: ->
      diff1 = arg1.diff()
      diff2 = arg2.diff()
      exponent = cleanRemainder(arg2.expr, '1')
      pow = cleanPower(arg1.expr, exponent)
      cleanProduct arg2.expr, pow

  }

cleanPower = (x, k) ->
  if parseInt(x) == 0
    return '0'
  if parseInt(k) == 0
    return '1'
  if parseInt(k) == 1
    return x
  if !isNaN(parseInt(x)) and !isNaN(parseInt(k))
    return '' + parseInt(x) ** parseInt(k)
  '(^ ' + x + ' ' + k + ')'

cos = (expr) ->
  regex = /^\(cos (.*)\)$/
  if !regex.test(expr)
    return false
  arg = parse(regex.exec(expr)[1])
  {
    type: 'cos'
    expr: expr
    diff: ->
      `var diff`
      diff = arg.diff()
      cleanProduct diff, '(* -1 (sin ' + arg.expr + '))'

  }

sin = (expr) ->
  regex = /^\(sin (.*)\)$/
  if !regex.test(expr)
    return false
  arg = parse(regex.exec(expr)[1])
  {
    type: 'sin'
    expr: expr
    diff: ->
      `var diff`
      diff = arg.diff()
      cleanProduct diff, '(cos ' + arg.expr + ')'

  }

tan = (expr) ->
  regex = /^\(tan (.*)\)$/
  if !regex.test(expr)
    return false
  arg = parse(regex.exec(expr)[1])
  {
    type: 'tan'
    expr: expr
    diff: ->
      `var diff`
      diff = arg.diff()
      cleanProduct diff, '(+ 1 (^ (tan ' + arg.expr + ') 2))'

  }

exp = (expr) ->
  regex = /^\(exp (.*)\)$/
  if !regex.test(expr)
    return false
  arg = parse(regex.exec(expr)[1])
  {
    type: 'exp'
    expr: expr
    diff: ->
      `var diff`
      diff = arg.diff()
      cleanProduct diff, '(exp ' + arg.expr + ')'

  }

ln = (expr) ->
  regex = /^\(ln (.*)\)$/
  if !regex.test(expr)
    return false
  arg = parse(regex.exec(expr)[1])
  {
    type: 'exp'
    expr: expr
    diff: ->
      `var diff`
      diff = arg.diff()
      quot = cleanQuotient(1, arg.expr)
      cleanProduct quot, diff

  }

parseSub = (subExpr) ->
  exprs = []
  if subExpr.length == 3
    exprs = subExpr.split(' ')
  else if subExpr[0] != '('
    fs = subExpr.split(' ')
    f = fs[0]
    exprs.push f
    exprs.push subExpr.slice(f.length).trim()
  else
    n = undefined
    parantheses = 1
    i = 1
    while i < subExpr.length
      if subExpr[i] == '('
        parantheses++
      else if subExpr[i] == ')'
        parantheses--
      if parantheses == 0
        n = i
        break
      i++
    exprs.push subExpr.slice(0, n + 1)
    exprs.push subExpr.slice(n + 1).trim()
  if exprs.length == 0
    console.log subExpr
  exprs.map parse

matchers = [
  constant
  variable
  sum
  remainder
  product
  quotient
  power
  cos
  sin
  tan
  exp
  ln
]
______________________________________________
regex = (ctx, regex)->
  if reg_ret = regex.exec ctx.str
    ctx.str = ctx.str.substr reg_ret[0].length
    return reg_ret
  null

class Var
  name : ""
  toString : ()->"#{@name}"

class Const
  val : 0
  constructor : (@val = 0)->
  toString : ()->"#{@val}"
  
class Bin_op
  op : ""
  a : null
  b : null
  toString : ()->"(#{@op} #{@a} #{@b})"

class Fn_call
  name : ""
  arg : null
  toString : ()->"(#{@name} #{@arg})"


bra_parse = (ctx)->
  return null if !reg_ret = regex ctx, /^\(/
  
  loop
    if reg_ret = regex ctx, /^[-+*/^]/
      ret = new Bin_op
      ret.op = reg_ret[0]
      return null if !regex ctx, /^\s+/
      return null if !ret.a = parse ctx
      return null if !regex ctx, /^\s+/
      return null if !ret.b = parse ctx
      break
    
    if reg_ret = regex ctx, /^[a-z]+/i
      ret = new Fn_call
      ret.name = reg_ret[0]
      return null if !regex ctx, /^\s+/
      return null if !ret.arg = parse ctx
      break
    
    return null
  
  return null if !reg_ret = regex ctx, /^\)/
  
  ret

const_parse = (ctx)->
  return null if !reg_ret = regex ctx, /^-?\d+/
  new Const +reg_ret[0]

var_parse = (ctx)->
  return null if !reg_ret = regex ctx, /^[a-z]+/i
  ret = new Var
  ret.name = reg_ret[0]
  ret

parse = (ctx, final=false)->
  backup = ctx.str
  loop
    break if ret = bra_parse ctx
    ctx.str = backup
    break if ret = const_parse ctx
    ctx.str = backup
    break if ret = var_parse ctx
    return null
  if final and ctx.str
    console.log "unparsed #{ctx.str}"
    return null
  ret

reduce_walk = (root)->
  switch root.constructor.name
    when "Const", "Var"
      root
    
    when "Bin_op"
      ret = new Bin_op
      ret.op = root.op
      ret.a = reduce_walk root.a
      ret.b = reduce_walk root.b
      root = ret
      
      if root.a.constructor.name == "Const" and root.b.constructor.name == "Const"
        ret = new Const
        switch root.op
          when "+" then ret.val = root.a.val + root.b.val
          when "-" then ret.val = root.a.val - root.b.val
          when "*" then ret.val = root.a.val * root.b.val
          when "/" then ret.val = root.a.val / root.b.val
          when "^" then ret.val = Math.pow root.a.val, root.b.val
          else
            throw new Error "unknown Bin_op '#{root.op}'"
        return ret
      
      switch root.op
        when "+"
          return root.b if root.a.constructor.name == "Const" and root.a.val == 0
          return root.a if root.b.constructor.name == "Const" and root.b.val == 0
          # TODO associative step down
          # root.a.constructor.name == "Bin_op"
          # root.a.op == "+"
          # root.b.constructor.name == "Const"
          # root.a.a.constructor.name == "Const" OR root.a.b.constructor.name == "Const"
          
          # TODO flip: var should be first
          root
        
        when "-"
          # TODO ??? multiply to -1
          #return root.b if root.a.constructor.name == "Const" and root.a.val == 0
          return root.a if root.b.constructor.name == "Const" and root.b.val == 0
          
          # TODO associative step down
          
          # TODO flip: var should be first
          root
        
        when "*"
          if root.a.constructor.name == "Const"
            return root.b if root.a.val == 1
            return new Const 0 if root.a.val == 0
            
            if root.b.constructor.name == "Bin_op"
              if root.b.op == "*"
                if root.b.a.constructor.name == "Const"
                  ret = new Bin_op
                  ret.op = "*"
                  ret.a = new Const root.a.val * root.b.a.val
                  ret.b = root.b.b
                  return reduce_walk ret
          
          if root.b.constructor.name == "Const"
            return root.a if root.b.val == 1
            return new Const 0 if root.b.val == 0
          
          
          # TODO associative step down
          
          # TODO x * x^-1
          
          # TODO flip: var should be last
          root
        
        when "/"
          return new Const 0 if root.a.constructor.name == "Const" and root.a.val == 0
          return root.a if root.b.constructor.name == "Const" and root.b.val == 1
          
          root
        
        when "^"
          return new Const 1 if root.b.constructor.name == "Const" and root.b.val == 0
          return root.a if root.b.constructor.name == "Const" and root.b.val == 1
          root
        
        else
          throw new Error "unknown Bin_op '#{root.op}'"
    
    when "Fn_call"
      arg = reduce_walk root.arg
      if arg.constructor.name == "Const"
        ret = new Const
        switch root.name
          when "sin" then ret.val = Math.sin arg.val
          when "cos" then ret.val = Math.cos arg.val
          when "exp" then ret.val = Math.exp arg.val
          when "ln"  then ret.val = Math.log arg.val
          else
            throw new Error "unknown Fn_call '#{root.name}'"
        return ret
      
      ret = new Fn_call
      ret.name = root.name
      ret.arg = arg
      ret
    
    else
      throw new Error "unknown type '#{root.constructor.name}'"

ast_neg = (root)->
  ret = new Bin_op
  ret.op = "*"
  ret.a = new Const -1
  ret.b = root
  ret
  
diff_walk = (root)->
  switch root.constructor.name
    when "Const"
      new Const 0
    
    when "Var"
      new Const 1
    
    when "Bin_op"
      switch root.op
        when "+", "-"
          ret = new Bin_op
          ret.op = root.op
          ret.a = diff_walk root.a
          ret.b = diff_walk root.b
          reduce_walk ret
        
        when "*"
          ret = new Bin_op
          ret.op = "+"
          ret.a = r0 = new Bin_op
          r0.op = "*"
          r0.a = diff_walk root.a
          r0.b = root.b
          
          ret.b = r1 = new Bin_op
          r1.op = "*"
          r1.a = root.a
          r1.b = diff_walk root.b
          reduce_walk ret
        
        when "/"
          ret = new Bin_op
          ret.op = "/"
          ret.a = top = new Bin_op
          ret.b = bot = new Bin_op
          
          top.op = "-"
          top.a = r0 = new Bin_op
          r0.op = "*"
          r0.a = diff_walk root.a
          r0.b = root.b
          
          top.b = r1 = new Bin_op
          r1.op = "*"
          r1.a = root.a
          r1.b = diff_walk root.b
          
          bot.op = "^"
          bot.a = root.b
          bot.b = new Const 2
          
          reduce_walk ret
        
        when "^"
          if root.b.constructor.name == "Const"
            c = new Const root.b.val
            
            ret = new Bin_op
            ret.op = "*"
            ret.a = c
            ret.b = new Bin_op
            ret.b.op = "*"
            ret.b.a = diff_walk root.a
            ret.b.b = pow = new Bin_op
            pow.op = "^"
            pow.a = root.a
            pow.b = new Const root.b.val - 1
            
            return reduce_walk ret
          throw new Error "pow for non-const is not implemented"
        
        else
          throw new Error "unknown Bin_op '#{root.op}'"
    
    when "Fn_call"
      switch root.name
        when "exp"
          ret = new Bin_op
          ret.op = "*"
          
          ret.a = diff_walk root.arg
          
          ret.b = new Fn_call
          ret.b.name = "exp"
          ret.b.arg = root.arg
          
          reduce_walk ret
        
        when "ln"
          ret = new Bin_op
          ret.op = "/"
          
          ret.a = diff_walk root.arg
          ret.b = root.arg
          
          reduce_walk ret
        
        when "sin"
          ret = new Bin_op
          ret.op = "*"
          
          ret.a = diff_walk root.arg
          
          ret.b = new Fn_call
          ret.b.name = "cos"
          ret.b.arg = root.arg
          
          reduce_walk ret
        
        when "cos"
          ret = new Bin_op
          ret.op = "*"
          
          ret.a = diff_walk root.arg
          
          ret.b = new Fn_call
          ret.b.name = "sin"
          ret.b.arg = root.arg
          
          reduce_walk ast_neg ret
        
        when "tan"
          ret = new Bin_op
          ret.op = "*"
          ret.a = diff_walk root.arg
          
          ret.b = payload = new Bin_op
          payload.op = "+"
          payload.a = new Const 1
          payload.b = new Bin_op
          payload.b.op = "^"
          payload.b.a = fn = new Fn_call
          payload.b.b = new Const 2
          fn.name = "tan"
          fn.arg = root.arg
          
          reduce_walk ret
        
        when "tan"
        
        else
          throw new Error "unknown Fn_call '#{root.name}'"
    
    else
      throw new Error "unknown type '#{root.constructor.name}'"

diff = (str)->
  ctx = {str}
  ret = parse ctx, true
  ret = reduce_walk ret
  ret = diff_walk ret
  ""+ret
______________________________________________
diff = (e)->
  # 1. tokenize
  ts = e.match(/-?(\d*\.)?\d+|\w+|[-+*/^]/g).map (t)->if isNaN t then t else +t

  # 2. parse ast
  i = 0
  ast = do o = ->
    t = ts[i++]
    switch 
      when t is 'x' or !isNaN t
        [t]
      when t in '-+*/^'
        [t, o(), o()]
      else
        [t, o()]

  # 3. diff
  ast = do o = (n = ast)->
    switch n[0]
      when 'x'
        [1]
      when '+'
        ['+',o(n[1]),o(n[2])]
      when '-'
        ['-',o(n[1]),o(n[2])]
      when '*'
        ['+',['*',o(n[1]),n[2]],['*',n[1],o n[2]]]
      when '/'
        ['/',['-',['*',o(n[1]),n[2]],['*',n[1],o n[2]]],['^',n[2],[2]]]
      when '^' # a*f'(x)*f(x)^(a-1)
        ['*',n[2],['*',o(n[1]),['^',n[1],['-',n[2],[1]]]]]
      when 'sin'
        ['*',o(n[1]),['cos',n[1]]]
      when 'cos'
        ['*',o(n[1]),['*',[-1],['sin',n[1]]]]
      when 'tan'
        ['*',o(n[1]),['+',[1],['^',['tan',n[1]],[2]]]]
      when 'exp'
        ['*',o(n[1]),['exp',n[1]]]
      when 'ln'
        ['/',o(n[1]),n[1]]
      else
        [0]

  # 4. simplify
  o = (n)->
    l=(L=n[1])?[0]
    r=(R=n[2])?[0]
    d=!isNaN(l-r)
    switch n[0]
      when '+'
        if l is 0
          return up R
        if r is 0
          return up L
        if d
          return up [l+r]
      when '-'
        if r is 0
          return up L
        if d
          return up [l-r]
      when '*'
        if 0 in [l,r]
          return up [0]
        if l is 1
          return up R
        if r is 1
          return up L
        if d
          return up [l*r]
      when '/'
        if r is 1
          return up L
        if d
          return up [l/r]
      when '^'
        if r is 0
          return [1]
        if r is 1
          return up L
        if d
          return up [l**r]
    [n[0]].concat n[1..].map o
  upd = yes
  up = (v)-> upd = yes; v
  while upd
    upd = no
    ast = o ast

  # 5. convert to prefix notation.
  do o = (n = ast)->
    if n[1]? then "(#{n[0]} #{n[1..].map(o).join ' '})" else "#{n[0]}"
