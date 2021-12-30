String::map?=(f)->[].map.call @,f

unb = (n,l=0) ->
  n.map((a)-> {' ':'s','\t':'t','\n':'n'}[a] ?a[...l]).join ''

get = (s,m,p)->
  return [v,k,p+k.length] for k,v of s when k is m[p...p+k.length]

ch = (a)-> throw new Error unless a; a
num = (m,p)->
  ch m[p] isnt 'n'
  s={s:1,t:-1}[m[p++]]
  n=0
  until 'n' is c=m[p++]
    n=(n<<1)+{s:0,t:1}[c]
  [s*n,p]

lab = (m,p)->
  l=''
  until 'n' is c=m[p++]
    l+=c
  [l,p]

whitespace = (m,i,u) ->
  m = unb m unless u
  o = ''
  s = []
  h = {}
  p = 0
  cs = []
  cl = {}
  cs_pop = -> ch cs.length; cs.pop()
  s_push = (a)-> s.unshift a
  s_pop = -> ch s.length; s.shift()
  cmds =
    s :
        __ : stack    : 6
        s  : push     : -> [n,p] = num m,p; [p, -> s_push n]
        ts : dupe     : -> [n,p] = num m,p; [p, -> ch 0<=n<s.length; s_push s[n]]
        tn : discard  : -> [n,p] = num m,p; [p, -> s[1..] = 0<n<=s.length and s[n+1..] or []]
        ns : dupe0    : -> [p, -> ch s.length; s_push s[0]]
        nt : swap     : -> [p, -> ch s.length>1; [s[1],s[0]] = s[0..1]]
        nn : discard0 : -> [p, -> s_pop()]
    ts:
        __ : arith    : 5
        ss : add      : -> [p, -> a=s_pop(); s_push s_pop()+ a]
        st : sub      : -> [p, -> a=s_pop(); s_push s_pop()- a]
        sn : mul      : -> [p, -> a=s_pop(); s_push s_pop()* a]
        ts : div      : -> [p, -> ch a=s_pop(); s_push s_pop()// ch a]
        tt : mod      : -> [p, -> a=s_pop(); s_push s_pop()%% ch a]
    tt:
        __ : heap     : 2
        s  : set      : -> [p, -> a=s_pop(); h[s_pop()] = a]
        t  : get      : -> [p, -> s_push h[s_pop()]]
    tn:
        __ : io       : 4 
        ss : outc     : -> [p, -> o += String.fromCharCode s_pop()]
        st : outn     : -> [p, -> o += s_pop().toString()]
        ts : in_c     : -> [p, -> ch i.length; h[s_pop()] = i.charCodeAt(); i=i[1..]]
        tt : in_n     : -> [p, -> ch i.length; np = i.indexOf '\n'; ch np?; h[s_pop()] = parseInt i[...np]; i=i[np+1..]]
    n :
        __ : flow     : 7
        ss : label    : -> [l,p] = lab m,p; ch not cl[l]?; cl[l] = p; [p, -> ]
        st : call     : -> [l,p] = lab m,p; [p, -> cs.push p; p = cl[l]]
        sn : jmp      : -> [l,p] = lab m,p; [p, -> p = cl[l]]
        ts : jz       : -> [l,p] = lab m,p; [p, -> p = cl[l] unless s_pop()]
        tt : jlz      : -> [l,p] = lab m,p; [p, -> p = cl[l] if 0>s_pop()]
        tn : ret      : -> [p, -> p = cs_pop()]
        nn : exit     : -> [p, -> p = -1]

  cc = {}
  while 0<=p<m.length
    p0 = p
    [imp,k,p] = get cmds, m,p
    [cmd,c,p] = get imp, m,p
    [p,_] = cc[p0] = cmd[Object.keys(cmd)[0]]()

  p=0
  until p<0
    [p,f] = cc[p]
    f()

  o

___________________________________________________
whitespace = (code, input) ->
  code = code.replace(/[^ \t\n]/g, '').replace(/ /g, 'S').replace(/\t/g, 'T').replace(/\n/g, 'N')
  input = input?.split ''

  line = 0
  stack = []
  heap = {}
  output = []
  labels = {}
  pc = 0
  subroutines = []

  patterns =
    imp:    /^(S|T[STN]|N)/
    stack:  /^(S|T[SN]|N[STN])/
    arithmetic: /^(S[STN]|T[ST])/
    heap:   /^([ST])/
    io:     /^([ST]{2})/
    'flow control': /^([ST][STN]|NN)/
    number: /^([ST]+)N/
    label:  /^([ST]*)N/
    
  imps =
    S:  'stack'
    TS: 'arithmetic'
    TT: 'heap'
    TN: 'io'
    N:  'flow control'

  args = {stack: {}, 'flow control': {}}
  args.stack[cmd] = 'number' for cmd in ['S', 'TS', 'TN']
  args['flow control'][cmd] = 'label' for cmd in ['SS', 'ST', 'SN', 'TS', 'TT']

  pop = -> if stack.length then stack.pop() else throw 'error : empty stack'
  push = (v) -> stack.push v

  printc = (c) -> output.push String.fromCharCode c
  printn = (i) -> output.push i

  read = -> if (c = input.shift())? then c else throw 'error : input'
  readc = -> read().charCodeAt(0)
  readn = -> parseInt (c until (c = read()) is '\n').join('')

  declare = (l) -> if not labels[l]? then labels[l] = line else throw 'error : label "' + l + '" already exists' 

  jump = (l) -> if labels[l]? then pc = labels[l] else throw 'error : label "' + l + '" does not exist'
  
  call = (l) -> subroutines.push pc; jump l
  return_ = -> if subroutines.length then pc = subroutines.pop() else throw 'error : return'

  functions =
    stack:
      S:  (arg) -> -> push arg
      TS: (arg) -> -> id = stack.length-1-arg; if stack[id]? then push stack[stack.length-1-arg] else throw 'error : stack out of bound'
      TN: (arg) -> -> a = pop(); stack = (if 0 <= arg < stack.length then stack[0...stack.length-arg] else []); push a
      NS: -> -> a = pop(); push a; push a
      NT: -> -> a = pop(); b = pop(); push a; push b
      NN: -> -> pop()
    arithmetic:
      SS: -> -> a = pop(); b = pop(); push b + a
      ST: -> -> a = pop(); b = pop(); push b - a
      SN: -> -> a = pop(); b = pop(); push b * a
      TS: -> -> a = pop(); b = pop(); if a then push b // a else throw 'error : division by 0'
      TT: -> -> a = pop(); b = pop(); if a then push b %% a else throw 'error : division by 0'
    heap:
      S: -> -> a = pop(); b = pop(); heap[b] = a
      T: -> -> a = pop(); if heap[a] then push heap[a] else throw 'error : heap access'
    io:
      SS: -> -> printc pop()
      ST: -> -> printn pop()
      TS: -> -> a = readc(); b = pop(); heap[b] = a
      TT: -> -> a = readn(); b = pop(); heap[b] = a
    'flow control':
      SS: (arg) -> declare arg; ->
      ST: (arg) -> -> call arg
      SN: (arg) -> -> jump arg
      TS: (arg) -> -> a = pop(); if a is 0 then jump arg
      TT: (arg) -> -> a = pop(); if a < 0 then jump arg
      TN: -> -> pc = return_()
      NN: -> -> pc = prog.length
    
  next = (type) ->
    res = code.match patterns[type]
    if not res? then throw 'parsing error : ' + type
    code = code.slice res[0].length
    res[1]

  hasNext = -> code.length > 0

  parseNumber = (str) ->
    sign = if str[0] is 'S' then 1 else -1
    num = parseInt(str[1..].replace(/S/g, '0').replace(/T/g, '1') or '0', 2)
    sign * num
    
  readImp = ->
    imp = imps[next 'imp']
    cmd = next imp
    arg = switch args[imp]?[cmd]
      when 'number' then parseNumber(next 'number')
      when 'label' then next 'label'
      else null
    instruction = functions[imp][cmd](arg)

    line++
    instruction

  # compilation
  prog = (readImp() while hasNext())

  # execution
  (prog[pc](); pc++) while pc < prog.length
  
  if pc is prog.length then throw 'error : exit'
  
  output.join('')
  
___________________________________________________
unbleach = (n) ->
  if n
    return n.replace(RegExp(' ', 'g'), 's').replace(/\t/g, 't').replace(/\n/g, 'n')
  return

# solution
tokenize = (code) ->
  labels = {}
  tokens = []
  a = undefined

  consume = ->
    char = code.charAt(0)
    code = code.substr(1)
    char

  getNumber = ->
    result = 0
    if code.charAt(0) == 'n'
      throw new Error('Invalid number')
    code = code.replace(/^([st])([st]*)n/, (all, sign, number) ->
      result = (if sign == 't' then -1 else 1) * parseInt(number.replace(/s/g, '0').replace(/t/g, '1') or '0', 2)
      ''
    )
    result

  getLabel = ->
    result = 0
    if code.charAt(0) == 'n'
      code = code.substr(1)
      return -1
    code = code.replace(/^([st]*)n/, (all, number) ->
      result = parseInt(number.replace(/s/g, '0').replace(/t/g, '1') or '0', 2)
      ''
    )
    result

  addToken = ->
    tokens.push [].slice.call(arguments)
    return

  while code.length
    switch consume()
      when 's'
        switch consume()
          when 's'
            if code.charAt(0) == 'n'
              throw new Error('Missing number')
            addToken 'stack-push', getNumber()
          when 't'
            switch consume()
              when 's'
                addToken 'stack-duplicate-nth', getNumber()
              when 'n'
                addToken 'stack-discard', getNumber()
              else
                throw new Error('Unknown statement t after st')
          when 'n'
            switch consume()
              when 's'
                addToken 'stack-duplicate'
              when 't'
                addToken 'swap-top-two'
              when 'n'
                addToken 'stack-pop'
      when 't'
        switch consume()
          when 's'
            switch consume()
              when 's'
                # IMP [tab][space] - Arithmetic [space]
                switch consume()
                  when 's'
                    addToken 'add'
                  when 't'
                    addToken 'subtract'
                  when 'n'
                    addToken 'multiply'
              when 't'
                # IMP [tab][space] - Arithmetic [tab]
                switch consume()
                  when 's'
                    addToken 'divide'
                  when 't'
                    addToken 'modulus'
                  else
                    throw new Error('Unknown statement n after tst')
              else
                throw new Error('Unknown statement n after ts')
          when 't'
            # Heap Access
            switch consume()
              when 's'
                addToken 'heap-set'
              when 't'
                addToken 'heap-get'
              else
                throw new Error('Unknown statement n after tst')
          when 'n'
            # Input/Output
            switch consume()
              when 's'
                switch consume()
                  when 's'
                    addToken 'output-char'
                  when 't'
                    addToken 'output-number'
                  else
                    throw new Error('Unknown statement n after tns')
              when 't'
                switch consume()
                  when 's'
                    addToken 'input-char'
                  when 't'
                    addToken 'input-number'
                  else
                    throw new Error('Unknown statement n after tnt')
              else
                throw new Error('Unknown statement n after tn')
      when 'n'
        # Flow Control
        switch consume()
          when 's'
            switch consume()
              when 's'
                a = '' + getLabel()
                if typeof labels[a] != 'undefined'
                  throw new Error('Label ' + a + ' already defined')
                labels[a] = tokens.length
                addToken 'label', a
              when 't'
                addToken 'call', '' + getLabel()
              when 'n'
                addToken 'go', '' + getLabel()
          when 't'
            switch consume()
              when 's'
                addToken 'go-if-zero', '' + getLabel()
              when 't'
                addToken 'go-if-negative', '' + getLabel()
              when 'n'
                addToken 'exit'
          when 'n'
            if consume() == 'n'
              addToken 'exit-program'
              break
            throw new Error('Unknown statement t/s after nnn')
  {
    labels: labels
    tokens: tokens
  }

parse = (code, stack, heap, input) ->
  _a = undefined
  tokensBag = tokenize(code)
  labels = tokensBag.labels
  tokens = tokensBag.tokens
  routines = []
  output = ''
  a = undefined
  b = undefined

  stackPop = ->
    if !stack.length
      throw new Error('Unexpected end of stack')
    stack.pop()

  getStackValue = (index) ->
    if index < 0 or index >= stack.length
      throw new Error('Unexpected [' + index + '] index in stack')
    stack[index]

  findLabel = (name, index) ->
    name = '' + name
    if !labels.hasOwnProperty(name)
      throw new Error('Unknown label')
    labels[name]

  console.log tokens
  index = 0
  while index < tokens.length
    _b = tokens[index]
    command = _b[0]
    parameter = _b[1]
    label = undefined
    switch command
      when 'stack-push'
        stack.push parameter
      when 'stack-duplicate-nth'
        stack.push getStackValue(stack.length - 1 - parameter)
      when 'stack-discard'
        if parameter < 0 or parameter >= stack.length
          stack.splice 0, stack.length - 1
        else if parameter > 0
          stack.splice stack.length - 1 - parameter, parameter
      when 'stack-duplicate'
        stack.push getStackValue(stack.length - 1)
      when 'swap-top-two'
        _a = [
          getStackValue(stack.length - 2)
          getStackValue(stack.length - 1)
        ]
        stack[stack.length - 1] = _a[0]
        stack[stack.length - 2] = _a[1]
      when 'stack-pop'
        stackPop()
      when 'add'
        stack.push stackPop() + stackPop()
      when 'subtract'
        stack.push -stackPop() + stackPop()
      when 'multiply'
        stack.push stackPop() * stackPop()
      when 'divide'
        a = stackPop()
        if a == 0
          throw new Error('Division by 0 not permitted')
        stack.push Math.floor(stackPop() / a)
      when 'modulus'
        a = stackPop()
        if a == 0
          throw new Error('Modulus 0 not permitted')
        b = stackPop()
        stack.push Math.round(a * (b / a - Math.floor(b / a)))
      when 'heap-set'
        a = stackPop()
        heap[stackPop()] = a
      when 'heap-get'
        a = stackPop()
        if !heap.hasOwnProperty(a)
          throw new Error('Missing value at [' + a + '] in the heap')
        stack.push heap[a]
      when 'output-char'
        output += String.fromCharCode(stackPop())
      when 'output-number'
        output += '' + stackPop()
      when 'input-char'
        if !input.length
          throw new Error('No character to read.')
        # Read a character from input, a, Pop a value off the stack, b, then store the ASCII value of a at heap address b.
        a = input.charAt(0).charCodeAt(0)
        input = input.substr(1)
        heap[stackPop()] = a
      when 'input-number'
        # Read a number from input, a, Pop a value off the stack, b, then store a at heap address b.
        inputLines = input.split('\n')
        if inputLines.length < 2
          throw new Error('Expected a number then a new line.')
        a = inputLines.shift().replace(/0x([0-9a-f]+)/gi, (all, number) ->
          parseInt(number, 16).toString()
        )
        input = inputLines.join('\n')
        if !a.length
          throw new Error('Empty string cannot be a number.')
        heap[stackPop()] = a
      when 'label'
        break
      when 'call', 'go'
        # (label)
        # Jump unconditionally to the position specified by label n.
        routines.push index
        index = findLabel(parameter, index) - 1
      when 'go-if-zero'
        # (label)
        #  Pop a value off the stack and jump to the label specified by n if the value is zero.
        label = findLabel(parameter, index)
        if stackPop() == 0
          index = label - 1
      when 'go-if-negative'
        # (label)
        # Pop a value off the stack and jump to the label specified by n if the value is less than zero.
        label = findLabel(parameter, index)
        if stackPop() < 0
          index = label - 1
      when 'exit'
        # Exit a subroutine and return control to the location from which the subroutine was called.
        if !routines.length
          throw new Error('No subroutine to exit.')
        index = routines.pop()
      when 'exit-program'
        return output
      else
        throw new Error('Unknown statement [' + command + ']')
    index++
  throw new Error('Unexpected end of program.')
  return

# solution

whitespace = (code, input) ->
  output = ''
  stack = []
  heap = {}

  parse unbleach(code.replace(/[^ \n\t]/g, '')) or '', stack, heap, input or ''
  
___________________________________________________
unbleach = (n) ->
  n?.replace(RegExp(' ', 'g'), 's').replace(/\t/g, 't').replace(/\n/g, 'n')

bleach = (n) ->
  n.replace(/s/g, ' ').replace(/t/g, '\t').replace(/n/g, '\n')

whitespace = (code, input) ->
  output = ''
  stack = []
  heap = {}
  index = 0
  inputIndex = 0
  callStack = []
  labels = {}

  tokens =
    ' ': true
    '\t': true
    '\n': true

  incr = -> ++index

  curr = ->
    fatal 'unexpected EOF' if finished()
    until tokens[code[index]]
      fatal 'unexpected EOF' if incr() and finished()
    code[index]

  finished = -> index >= code.length

  untilCurr = (c, fn) ->
    while not finished() and curr() isnt c
      fn curr()
      incr()

  fatal = (message) ->
    throw new Error message

  assertTop = (message) ->
    fatal 'empty stack' + (message or '') unless stack.length

  parseNumber = ->
    number = 0
    isNegative = curr() is '\t'
    fatal 'invalid sign' if not isNegative and curr() isnt ' '
    incr()
    untilCurr '\n', (c) ->
      number = number << 1 | if c is '\t' then 1 else 0
    incr()
    if isNegative then -number else number

  parseLabel = ->
    label = ''
    untilCurr '\n', (c) ->
      label += c
    incr()
    label

  dodgeArgument = ->
    incr() while curr() isnt '\n'
    incr()

  pushStack = ->
    stack.push parseNumber()

  duplicateNthStack = ->
    n = parseNumber()
    fatal 'invalid duplicate number' if n < 0
    n = stack.length - 1 - n
    fatal 'stack too short' if n < 0
    stack.push stack[n]

  popNStack = ->
    n = parseNumber()
    top = popStack()
    n = stack.length if n < 0 or n >= stack.length
    fatal 'stack too short' if n > stack.length
    popStack() while n--
    stack.push top

  duplicateTopStack = ->
    assertTop ' to duplicate'
    stack.push stack[stack.length - 1]

  swapStack = ->
    fatal 'stack too short to swap' unless stack.length > 1
    [stack[stack.length - 2], stack[stack.length - 1]] =
      [stack[stack.length - 1], stack[stack.length - 2]]

  popStack = ->
    assertTop()
    stack.pop()

  add = ->
    a = popStack()
    assertTop()
    stack[stack.length - 1] += a

  subtract = ->
    a = popStack()
    assertTop()
    stack[stack.length - 1] -= a

  multiply = ->
    a = popStack()
    assertTop()
    stack[stack.length - 1] *= a

  divideNumbers = (b, a) ->
    fatal 'division by zero' unless a
    Math.floor b / a

  divide = ->
    a = popStack()
    assertTop()
    stack[stack.length - 1] =
      divideNumbers stack[stack.length - 1], a

  modulo = ->
    a = popStack()
    assertTop()
    b = stack[stack.length - 1]
    stack[stack.length - 1] = b - (a * divideNumbers b, a)

  popStoreHeap = ->
    a = popStack()
    b = popStack()
    heap[b] = a

  popPushFromHeap = ->
    address = heap[popStack()]
    fatal 'undefined heap address' if address is undefined
    stack.push address

  outputCharacter = ->
    output += String.fromCharCode popStack()

  outputNumber = ->
    output += popStack()

  inputCharacter = ->
    fatal 'input too short' if inputIndex is input.length
    heap[popStack()] = input[inputIndex++].charCodeAt 0

  inputNumber = ->
    number = ''
    while inputIndex < input.length and input[inputIndex] isnt '\n'
      number += input[inputIndex++]
    fatal 'invalid input number' if inputIndex is input.length
    heap[popStack()] = parseInt number
    ++inputIndex

  defineLabel = ->
    label = parseLabel()
    fatal "label [#{unbleach label}] already defined" if labels[label]
    labels[label] = index

  jumpToLabel = (label) ->
    fatal "undefined label [#{unbleach label}]" unless labels[label]
    index = labels[label]

  callSubroutine = ->
    label = parseLabel()
    callStack.push index
    jumpToLabel label

  jumpLabel = ->
    label = parseLabel()
    jumpToLabel label

  jumpIfZero = ->
    label = parseLabel()
    jumpToLabel label if popStack() is 0

  jumpIfNegative = ->
    label = parseLabel()
    jumpToLabel label if popStack() < 0

  returnSubroutine = ->
    fatal 'unexpected return outside routine' unless callStack.length
    index = callStack.pop()

  exitProgram = ->
    index = code.length

  stackInstructions =
    ' ': [dodgeArgument, pushStack]
    '\t':
      ' ': [dodgeArgument, duplicateNthStack]
      '\n': [dodgeArgument, popNStack]
    '\n':
      ' ': [null, duplicateTopStack]
      '\t': [null, swapStack]
      '\n': [null, popStack]

  arithmeticInstructions =
    ' ':
      ' ': [null, add]
      '\t': [null, subtract]
      '\n': [null, multiply]
    '\t':
      ' ': [null, divide]
      '\t': [null, modulo]

  heapInstructions =
    ' ': [null, popStoreHeap]
    '\t': [null, popPushFromHeap]

  ioInstructions =
    ' ':
      ' ': [null, outputCharacter]
      '\t': [null, outputNumber]
    '\t':
      ' ': [null, inputCharacter]
      '\t': [null, inputNumber]

  flowInstructions =
    ' ':
      ' ': [defineLabel, dodgeArgument]
      '\t': [dodgeArgument, callSubroutine]
      '\n': [dodgeArgument, jumpLabel]
    '\t':
      ' ': [dodgeArgument, jumpIfZero]
      '\t': [dodgeArgument, jumpIfNegative]
      '\n': [null, returnSubroutine]
    '\n': '\n': [null, exitProgram]

  imp =
    ' ': stackInstructions
    '\t':
      ' ': arithmeticInstructions
      '\t': heapInstructions
      '\n': ioInstructions
    '\n': flowInstructions

  walkTree = (node, phase) ->
    if node.constructor is Array
      node[phase] and node[phase]()
      return node[phase]
    currentChar = curr()
    for char, childNode of node when char is currentChar
      return incr() and walkTree childNode, phase
    fatal 'invalid command'

  walkTree imp, 0 until finished()

  index = 0
  lastInstruction = null
  lastInstruction = walkTree imp, 1 until finished()
  fatal 'unclean termination' unless lastInstruction is exitProgram

  output
  
___________________________________________________
whitespace = do ->
  unbleach = (str) ->
    str
    .replace /\S/g, ''
    .replace /\ /g, 's'
    .replace /\t/g, 't'
    .replace /\n/g, 'n'
  instructionTable = do ->
    bin2dec = do ->
      [sign, values] = [{t: -1, s: +1}, {s: 0, t: 1}]
      (blob) ->
        throw 'Invalid binary number.' unless blob.length > 0
        return 0 if blob.length is 1
        d = blob.slice()
        sign[d.shift()] * do ->
          d.reverse()
          .map (char) -> values[char]
          .reduce (sum, v, i) ->
            sum + v * 2 ** i
          , 0
    bin2label = (blob) -> ":#{blob.join ''}"
    destination = (blob, instruction) -> instruction.value =  bin2label blob
    integer = (blob, instruction) -> instruction.value = bin2dec blob
    label = (blob, instruction, rte) ->
      console.log blob, instruction, rte
      instruction.value = k = bin2label blob
      throw "Label already used: #{k}." if rte.labels[k]?
      rte.labels[k] = instruction
    validate = (address) -> throw "Invalid address #{address}." if address < 0

    [ # STACK
      ['ss', 'Push', integer, (value) -> @push value]
      ['sts', 'Fish', integer, (depth) ->
        index = @stack.length - 1 - depth
        if index < 0 or index > @stack.length or depth < 0
          throw "Invalid stack index #{index} at #{depth}."
        @push @stack[index]]
      ['stn', 'Discard', integer, (depth) ->
        top = @pop()
        if depth > 0 and depth < @stack.length
          @pop() while depth-- > 0
        else @stack = []
        @push top]
      ['sns', 'Duplicate', ->
        @push top = @pop()
        @push top]
      ['snt', 'Swap', ->
        [@pop(), @pop()].forEach (number) =>
          @push number]
      ['snn', 'Discard top', -> @pop()]
      # Math
      ['tsss', 'Add', -> @push @pop() + @pop()]
      ['tsst', 'Subtract', -> @push -@pop() + @pop()]
      ['tssn', 'Multiply', -> @push @pop() * @pop()]
      ['tsts', 'Divide',  ->
        [top, second] = [@pop(), @pop()]
        throw 'Division by zero.' if top is 0
        @push Math.floor second / top]
      ['tstt', 'Modulo', ->
        [top, second] = [@pop(), @pop()]
        throw 'Division by zero.' if top is 0
        @push Math.floor second %% top]
      # Heap
      ['tts', 'Store', ->
        [top, address] = [@pop(), @pop()]
        validate address
        @heap[address] = top]
      ['ttt', 'Read', ->
        validate address = @pop()
        @push v = @heap[address]
        throw "Undefined value at heap[#{address}]." unless v?]
      # Output
      ['tnss', 'PutChar', -> @output.push String.fromCharCode @pop()]
      ['tnst', 'PutNumber', -> @output.push @pop()]
      # Input
      ['tnts', 'ReadChar', ->
        validate address = @pop()
        @heap[address] = do =>
          throw "Empty Input" unless @input.length > 0
          v = @input[0].charCodeAt 0
          @input = @input.slice 1
          v]
      ['tntt', 'ReadNumber', ->
        validate address = @pop()
        @heap[address] = do =>
          throw "Empty Input" unless @input.length > 0
          match = (/^.*\n/.exec @input)[0]
          throw 'Not a number.' unless match?
          n = parseInt match
          throw 'Not a number.' if n is Number.NaN
          @input = @input.replace match, ''
          n]
      # Flow control
      ['nss', 'Label', label, ->]
      ['nst', 'Call', destination, (subroutine)->
        @calls.push @current
        @jmp subroutine]
      ['nsn', 'Jump', destination, (label) -> @jmp label]
      ['nts', 'JumpZero', destination, (label) ->
        @jmp label if @pop() is 0]
      ['ntt', 'JumpNegative', destination, (label) ->
        @jmp label if @pop() < 0]
      ['ntn', 'Return', ->
        throw 'Cannot return from empty callstack.' unless @calls.length > 0
        @goto @calls.pop()]
      ['nnn', 'End', -> @done = true]]
    .reduce (map, arr) ->
      if arr.length is 4
        [path, name, binding, effect] = arr
      else
        [path, name, effect] = arr
        binding = null
      p = map
      path.split ''
      .forEach (char) ->
        p[char] ?= {}
        p = p[char]
      p.match = {path, name, binding, effect}
      map
    , {}

  class RTE
    jmp: (label) ->
      throw 'Invalid Label.' unless @labels[label]?
      @goto @labels[label]
    goto: (instruction) ->
      throw 'Cant jump to empty instruction.' unless instruction
      @current = instruction
    pop: ->
      throw 'Empty Stack.' unless @stack.length > 0
      @stack.pop()
    push: (v) -> @stack.push v

    constructor: (@input) ->
      @reset()
      this
    reset: ->
      [@stack, @heap, @calls, @output] = [0...4].map -> []
      [@labels, @done] = [{}, false]
    run: (@current) ->
      until @done
        throw 'Code Ended.' unless @current?
        instruction = @current
        @current = instruction.next
        instruction.type.effect.call this, instruction.value
      this

  (code, input) ->
    code = unbleach code
    throw 'Invalid program.' unless code.length > 0
    (env = new RTE input)
    .run firstInstruction =
      code
      .split ''
      .reduce (pass, char, pointer) ->
        pass.read char, pointer
        pass
      ,
        list: []
        reading: 'Instructions'
        s: instructionTable
        read: (char, pointer) ->
          if @reading is 'Instructions'
            @s = @s[char]
            throw 'Malformed program' unless @s?
            if @s.match?
              @list.push @instruction =
                type: @s.match
                pointer: pointer
              @s = instructionTable
              if @instruction.type.binding?
                @reading = 'Blob'
                @blob = []
          else #blob
            if char is 'n'
              @reading = 'Instructions'
              @instruction.type.binding @blob, @instruction, env
            else @blob.push char
        process: ->
          @list.forEach (instruction, i, list) ->
            instruction.next = list[i + 1]
          @list[0]
      .process()
    .output.join ''
