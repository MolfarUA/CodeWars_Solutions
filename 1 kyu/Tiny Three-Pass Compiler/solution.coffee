5265b0885fda8eac5900093b



class Parser
  @parse: (program) ->
    parser = new Parser(program)
    parser.expr()

  constructor: (program) ->
    @tokens = program.match /[-+*/\(\)\[\]]|[A-Za-z]+|[0-9]+/g
    @args = {}
    @accept '['
    i = 0 ; while v = @accept /[a-z]+/ then @args[v] = i++
    @accept ']'

  accept: (re) ->
    if re instanceof RegExp and re.test(@tokens[0]) or re is @tokens[0]
      @tokens.shift()

  expr: () ->
    t = @term() ; while o = @accept /[+-/]/ then t = op: o, a: t, b: @term()
    t

  term: () ->
    t = @factor() ; while o = @accept /[*/]/ then t = op: o, a: t, b: @factor()
    t

  factor: () ->
    if @accept '('
      e = @expr() ; @accept ')' ; e
    else
      @number() or @variable()

  number: () ->
    if n = @accept(/\d+/) then op: 'imm', n: +n

  variable: () ->
    if v = @accept(/[a-z]+/) then op: 'arg', n: @args[v]

class Compiler
  compile: (program) ->
    @pass3(@pass2(@pass1(program)))

  pass1: (program) ->
    Parser.parse program

  pass2: (ast) ->
    if ast.n? then return ast

    a = @pass2 ast.a
    b = @pass2 ast.b

    if a.op is 'imm' and b.op is 'imm'
      op: 'imm', n: eval(a.n + ast.op + b.n)
    else
      op: ast.op, a: a, b: b

  pass3: (ast) ->
    if ast.op is 'imm'
      "IM #{ast.n}"
    else if ast.op is 'arg'
      "AR #{ast.n}"
    else
      [].concat(
        @pass3(ast.a), 'PU',
        @pass3(ast.b), 'SW', 'PO',
        {'+': 'AD', '-': 'SU', '*': 'MU', '/': 'DI'}[ast.op]
      )

_______________________________
Compiler = ->

Compiler::compile = (program) ->
  @pass3 @pass2(@pass1(program))

Compiler::tokenize = (program) ->
  regex = /\s*([-+*/\(\)\[\]]|[A-Za-z]+|[0-9]+)\s*/g
  program.replace(regex, ':$1').substring(1).split(':').map (tok) ->
    if isNaN(tok) then tok else tok | 0


Compiler::pass1 = (program) ->
  tokens = @tokenize(program)
  args = []
  token = tokens.shift()
  while `(token = tokens.shift()) != ']'`
    args.push token
  (`function parse(ts) {
  var op = function (ts, ops) {
    var b = 0, i = ts.length;
    while (i-- > 1)
      if (!(b += ('()'.indexOf(ts[i]) + 2) % 3 - 1) && ops.indexOf(ts[i]) >= 0)
        return {
          'op': ts[i],
          a: parse(ts.slice(0, i)),
          b: parse(ts.slice(i + 1))
        };
  };
  var node = op(ts, '+-') || op(ts, '*/');
  if (!node && ts.length > 1)
    node = parse(ts.slice(1, ts.length - 1));
  if (!node)
    node = typeof ts[0] == 'number' ? {
      op: 'imm',
      n: ts[0]
    } : {
      op: 'arg',
      n: args.indexOf(ts[0])
    };
  return node;
}`) tokens

Compiler::pass2 = (ast) ->
  (`function reduce(ast) {
  if ('+-*/'.indexOf(ast.op) >= 0) {
    var a = ast.a = reduce(ast.a), b = ast.b = reduce(ast.b);
    if (a.op + b.op == 'immimm')
      return {
        op: 'imm',
        n: eval(a.n + ast.op + b.n)
      };
  }
  return ast;
}`) ast

Compiler::pass3 = (ast) ->
  args = 
    arg: 'AR '
    imm: 'IM '
  ops = 
    '+': 'AD'
    '-': 'SU'
    '*': 'MU'
    '/': 'DI'
  (`function compile(ast) {
  var arg = args[ast.op];
  return arg ? [arg + ast.n] : [].concat(compile(ast.a), ['PU'], compile(ast.b), [
    'SW',
    'PO',
    ops[ast.op]
  ]);
}`) ast

____________________________________________
Compiler = ->

compileAST = (node) ->
  opInstr = 
    '/': 'DI'
    '*': 'MU'
    '+': 'AD'
    '-': 'SU'
  if node.op == 'arg'
    [
      'AR ' + node.n
      'PU'
    ]
  else if node.op == 'imm'
    [
      'IM ' + node.n
      'PU'
    ]
  else
    [].concat compileAST(node.a), compileAST(node.b), [
      'PO'
      'SW'
      'PO'
      opInstr[node.op]
      'PU'
    ]

# -,- []
# 8,- []
# -,- [8]
# r2,- [8]
# -,- [r2, 8]
# 3,- [r2, 8]
# -,- [3, r2, 8]
# 3,- [r2, 8]
# -,3 [r2, 8]

optimizeAST = (node) ->
  if node.op == 'arg' or node.op == 'imm'
    node
  else
    optA = optimizeAST(node.a)
    optB = optimizeAST(node.b)
    if optA.op == 'imm' and optB.op == 'imm'
      res = undefined
      switch node.op
        when '*'
          res = optA.n * optB.n
        when '/'
          res = optA.n / optB.n
        when '+'
          res = optA.n + optB.n
        when '-'
          res = optA.n - (optB.n)
        else
          throw new Error('unkonwn op')
      {
        op: 'imm'
        n: res
      }
    else
      {
        op: node.op
        a: optA
        b: optB
      }

parseTreeTransform = (node, argIndex) ->
  if typeof node.v == 'object'
    return {
      op: node.v.op
      a: parseTreeTransform(node.v.a, argIndex)
      b: parseTreeTransform(node.v.b, argIndex)
    }
  if typeof node.v == 'number'
    return {
      op: 'imm'
      n: node.v
    }
  if typeof node.v == 'string'
    return {
      op: 'arg'
      n: argIndex[node.v]
    }
  throw new Error('unknown parse tree transform', node)
  return

slrParser = (tokens, d) ->
  debug = if d then console.log else (->
  )
  debug tokens
  stack = []
  i = 0
  state = 0
  while tokens.length >= 0 and i < 100
    lookahead = parseRules[state][0][tokenType(tokens[0])]
    if lookahead == undefined
      lookahead = parseRules[state][0].rest
    if lookahead != undefined
      if lookahead == 'ACC'
        return stack
        break
      else if typeof lookahead == 'number'
        debug lookahead
        stack.push
          s: lookahead
          v: tokens.shift()
        state = lookahead
      else if typeof lookahead == 'function'
        debug lookahead.name
        A = lookahead(stack, tokens)
        s = stack[stack.length - 2].s
        state = parseRules[s][1][A]
        debug state
        stack[stack.length - 1].s = state
      else
        throw new Error('Unexpected lookahead', lookahead)
    i++
  throw new Error('did not parse tree in sufficient steps')
  return

r1 = (stack, tokens) ->
  stack.push
    t: 'AL'
    v: []
  'AL'

r2 = (stack, tokens) ->
  al = stack.pop()
  v = stack.pop()
  al.v.unshift v.v
  stack.push al
  'AL'

r3 = (stack, tokens) ->
  t = stack[stack.length - 1]
  stack[stack.length - 1] =
    t: 'E'
    v: t.v
  'E'

r4 = (stack, tokens) ->
  estar = stack.pop()
  e = stack.pop()
  v = estar.v
  v.a = e
  stack.push
    t: 'E'
    v: v
  'E'

r5 = (stack, tokens) ->
  t = stack.pop()
  plus = stack.pop()
  stack.push
    t: 'E*'
    v:
      op: '+'
      b: t
  'E*'

r6 = (stack, tokens) ->
  t = stack.pop()
  min = stack.pop()
  stack.push
    t: 'E*'
    v:
      op: '-'
      b: t
  'E*'

r7 = (stack, tokens) ->
  f = stack[stack.length - 1]
  stack[stack.length - 1] =
    t: 'T'
    v: f.v
  'T'

r8 = (stack, tokens) ->
  tstar = stack.pop()
  t = stack.pop()
  v = tstar.v
  v.a = t
  stack.push
    t: 'T'
    v: v
  'T'

r9 = (stack, tokens) ->
  f = stack.pop()
  mul = stack.pop()
  stack.push
    t: 'T*'
    v:
      op: '*'
      b: f
  'T*'

r10 = (stack, tokens) ->
  f = stack.pop()
  div = stack.pop()
  stack.push
    t: 'T*'
    v:
      op: '/'
      b: f
  'T*'

r11 = (stack, tokens) ->
  v = stack[stack.length - 1]
  stack[stack.length - 1] =
    t: 'V'
    v: v.v
  'F'

r12 = (stack, tokens) ->
  f = stack[stack.length - 1]
  stack[stack.length - 1] =
    t: 'F'
    v: f.v
  'F'

r13 = (stack, tokens) ->
  stack.pop()
  # ')'
  e = stack.pop()
  stack.pop()
  # '('
  stack.push
    t: 'F'
    v: e.v
  'F'

r14 = (stack, tokens) ->
  v = stack[stack.length - 1]
  stack[stack.length - 1] =
    t: 'V'
    v: v.v
  'V'

tokenType = (token) ->
  if token == '[' or token == ']' or token == '+' or token == '-' or token == '*' or token == '/' or token == '(' or token == ')'
    return token
  if typeof token == 'undefined'
    return 'EOF'
  if typeof token == 'number'
    return 'N'
  'V'

Compiler::compile = (program) ->
  @pass3 @pass2(@pass1(program))

Compiler::tokenize = (program) ->
  # Turn a program string into an array of tokens.  Each token
  # is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
  # name or a number (as a string)
  regex = /\s*([-+*/\(\)\[\]]|[A-Za-z]+|[0-9]+)\s*/g
  program.replace(regex, ':$1').substring(1).split(':').map (tok) ->
    if isNaN(tok) then tok else tok | 0

Compiler::pass1 = (program) ->
  tokens = @tokenize(program)
  stack = slrParser(tokens, false)
  args = stack[1]
  argIndex = {}
  i = 0
  while i < args.v.length
    argIndex[args.v[i]] = i
    i++
  ast = parseTreeTransform(stack[3], argIndex)
  ast

Compiler::pass2 = (ast) ->
  opt = optimizeAST(ast)
  opt

Compiler::pass3 = (ast) ->
  # return assembly instructions
  instr = compileAST(ast)
  instr

parseRules = 
  0: [
    { '[': 1 }
    {}
  ]
  1: [
    {
      ']': r1
      'V': 4
    }
    {
      'AL': 2
      'V': 3
    }
  ]
  2: [
    { ']': 5 }
    {}
  ]
  3: [
    {
      ']': r1
      'V': 4
    }
    {
      'AL': 6
      'V': 3
    }
  ]
  4: [
    { 'rest': r14 }
    {}
  ]
  5: [
    {
      '(': 12
      'N': 11
      'V': 4
    }
    {
      'F': 9
      'T': 8
      'E': 7
      'V': 10
    }
  ]
  6: [
    { ']': r2 }
    {}
  ]
  7: [
    {
      '+': 14
      '-': 15
      'EOF': 'ACC'
    }
    { 'E*': 13 }
  ]
  8: [
    {
      '*': 17
      '/': 18
      'rest': r3
    }
    { 'T*': 16 }
  ]
  9: [
    { 'rest': r7 }
    {}
  ]
  10: [
    { 'rest': r11 }
    {}
  ]
  11: [
    { 'rest': r12 }
    {}
  ]
  12: [
    {
      'N': 11
      '(': 12
      'V': 4
    }
    {
      'E': 19
      'T': 8
      'F': 9
      'V': 10
    }
  ]
  13: [
    { 'rest': r4 }
    {}
  ]
  14: [
    {
      'N': 11
      '(': 12
      'V': 4
    }
    {
      'T': 20
      'F': 9
      'V': 10
    }
  ]
  15: [
    {
      'N': 11
      '(': 12
      'V': 4
    }
    {
      'T': 21
      'F': 9
      'V': 10
    }
  ]
  16: [ { 'rest': r8 } ]
  17: [
    {
      'N': 11
      '(': 12
      'V': 4
    }
    {
      'F': 22
      'V': 10
    }
  ]
  18: [
    {
      'N': 11
      '(': 12
      'V': 4
    }
    {
      'F': 23
      'V': 10
    }
  ]
  19: [
    {
      '+': 14
      '-': 15
      ')': 24
    }
    { 'E*': 13 }
  ]
  20: [
    {
      '*': 17
      '/': 18
      'rest': r5
    }
    { 'T*': 16 }
  ]
  21: [
    {
      '*': 17
      '/': 18
      'rest': r6
    }
    { 'T*': 16 }
  ]
  22: [
    { 'rest': r9 }
    {}
  ]
  23: [
    { 'rest': r10 }
    {}
  ]
  24: [
    { 'rest': r13 }
    {}
  ]

______________________________________________
U = undefined

class Compiler

  compile: (program) ->
    @pass3(@pass2(@pass1(program)))
  
  tokenize: (program) ->
    regex = /\s*([-+*/\(\)\[\]]|[A-Za-z]+|[0-9]+)\s*/g;
    program.replace(regex, ":$1").substring(1).split(':').map( (tok) ->
      if isNaN(tok) then tok else tok|0
    )
  
  pass1: (program) ->
    ts = @tokenize(program)
    t = ts.shift(); # [
    arg = {}
    i=0
    loop
      t = ts.shift()
      break if t == ']'
      arg[t] = i++
    par = 0
    tree = 0
    loop
      t = ts.shift()
      break if t == U
      next = U
      prec = 0
      switch t
        when '(' then par++
        when ')' then par--
        when '/', '*'
          prec = 1
          next = { op: t, a:U, b:U }
        when '+', '-'
          prec = 0
          next = { op: t, a:U, b:U }
        else
          prec = 2
          if !isNaN(t)
            next = { op: 'imm', n: t }
          else if arg.hasOwnProperty(t)
            next = { op: 'arg', n: arg[t] }
          else
            throw "parse error at token '"+t+"'"
        
      if !next then continue
      next['p'] = par*10+prec
      
      if !tree
        tree = next
      else
        node = tree
        parent = U
        while node.p < next.p && node.b
          parent = node
          node = node.b

        if next.hasOwnProperty('n')
          node.b = next
        else
          next.a = node
          node = next
        
        if parent
          parent.b = node
        else
          tree = node
    
    cleanup = (node) ->
      delete node.p
      return if node.hasOwnProperty('n')
      throw "syntax error" if node.a == U || node.b == U
      cleanup(node.a)
      cleanup(node.b)
      node
    cleanup(tree)
  
  pass2: (ast) ->
    resolve = (node) ->
      return if node.hasOwnProperty('n')
      resolve(node.a)
      resolve(node.b)
      if node.a.op == 'imm' && node.b.op == 'imm'
        switch node.op
          when '*' then node.n = node.a.n * node.b.n
          when '/' then node.n = node.a.n / node.b.n
          when '+' then node.n = node.a.n + node.b.n
          when '-' then node.n = node.a.n - node.b.n
        node.op = 'imm'
        delete node.a
        delete node.b
      
      node
    resolve(ast)

  pass3: (ast) ->
    resolve = (node) ->
      code = []
      if !node.hasOwnProperty('n')
        code = code.concat(resolve(node.a),resolve(node.b))
      switch node.op
        when 'imm' then code = code.concat(['IM '+node.n, 'PU'])
        when 'arg' then code = code.concat(['AR '+node.n, 'PU'])
        when '+' then code = code.concat(['PO', 'SW', 'PO', 'AD', 'PU'])
        when '-' then code = code.concat(['PO', 'SW', 'PO', 'SU', 'PU'])
        when '*' then code = code.concat(['PO', 'SW', 'PO', 'MU', 'PU'])
        when '/' then code = code.concat(['PO', 'SW', 'PO', 'DI', 'PU'])
    
      code
    resolve(ast)
