assemblerInterpreter=(a)->
  p=fl=0
  st={}
  cs=[]
  o =[]
  v=(a)-> unless isNaN a then +a else
    if a[0] isnt "'" then st[a] ?0
    else a.replace /^'|'$/g, ''
  ins =
    mov : ( a, b )-> -> st[a] = v b
    inc : ( a    )-> -> st[a] =  1 + st[a] ?0
    dec : ( a    )-> -> st[a] = -1 + st[a] ?0
    jnz : ( a, b )-> -> if v a then i += -1 + v b
    add : ( a, b )-> -> st[a] = v(a) + v b
    sub : ( a, b )-> -> st[a] = v(a) - v b
    mul : ( a, b )-> -> st[a] = v(a) * v b
    div : ( a, b )-> -> st[a] = v(a) // v b
    jmp : ( a    )-> -> p = ls[a]
    cmp : ( a, b )-> -> fl = v(a) - v b
    jne : ( a    )-> -> if  fl    then p=ls[a]
    je  : ( a    )-> -> if !fl    then p=ls[a]
    jge : ( a    )-> -> if fl >=0 then p=ls[a]
    jg  : ( a    )-> -> if fl > 0 then p=ls[a]
    jle : ( a    )-> -> if fl <=0 then p=ls[a]
    jl  : ( a    )-> -> if fl < 0 then p=ls[a]
    call: ( a    )-> -> cs.push p; p=ls[a]
    ret : (      )-> -> p = cs.pop()
    msg : ( a... )-> -> o.push v b for b in a
    end : (      )-> -> p = undefined

  # "compile"
  ls = {}
  m = for s,i in a.split '\n'
    ts=s.trim().replace(/;.*$/gm,'').match /'[^']*'|[^,\s]+/g
    if ts?[0]?[-1..] is ':'
      ls[ts[0][...-1]]=i
      undefined
    else if ts?.length
      cc = ins[ts[0]]? ts[1..]...
      if not cc?
        throw new Error 'unsupported instruction:'+ts
      cc

  # execute
  while 0<=p<m.length
    m[p]?()
    ++p
  if isNaN p then o.join '' else -1

____________________________________________________
assemblerInterpreter = (program) ->
  prog=program.split('\n').map((x)->x.replace(/(.*?)(;.*)/,"$1").trim())
  register={}
  labels={}
  calls=[]
  l=prog.length
  getReg=(v)->if register[v]==undefined then parseInt(v) else register[v]
  for i in [0..l-1]
    k=prog[i]
    if k.slice(-1)==':' then labels[k.slice(0,-1)]=i+1
    
  i=0
  output=""
  cmp=null
  reg=null
  while i<l
    if prog[i]=="end" then return output
  
    line=prog[i].split(/ +/).map((x)->x.trim().replace(/,$/,""))
    cmd=line[0]
    console.log(line)
    console.log(register)
    if cmd=="inc"
      register[line[1]]++
    else if cmd=="dec"
        register[line[1]]--
    else if cmd=="mul"
        register[line[1]]*=getReg(line[2])
    else if cmd=="div"
        register[line[1]]=Math.floor(register[line[1]]/getReg(line[2]))
    else if cmd=="add"
        register[line[1]]+=getReg(line[2])
    else if cmd=="sub"
        register[line[1]]-=getReg(line[2])
    else if cmd=="mov"
        register[line[1]]=getReg(line[2])
    else if cmd =="jmp"
        i=labels[line[1]]-1
    else if cmd=="ret"
        i=calls.pop()-1
    else if cmd=="je"
        if cmp=="eq"
          i=labels[line[1]]
    else if cmd=="jne"
      if cmp!="eq"
        i=labels[line[1]]-1
    else if cmd=="jge"
      if ["eq","sup"].includes(cmp)
        i=labels[line[1]]-1
    else if cmd=="jg"
      if cmp=="sup"
        i=labels[line[1]]-1
    else if cmd=="jle"
        if ["eq","inf"].includes(cmp)
          i=labels[line[1]]-1
    else if cmd=="jl"
      if cmp=="inf"
        i=labels[line[1]]-1
    else if cmd=="cmp"
        [reg1,reg2]=line.slice(1).map((x)->getReg(x.replace(/,$/,"")))
        sign=Math.sign(reg1-reg2)
        if sign==-1
          cmp="inf"
        else if sign
            cmp="sup"
        else
          cmp="eq"
    else if cmd=="call"
        calls.push(i+1)
        i=labels[line[1]]-1
    else
      L=prog[i].slice(3).split(/'/)
      output=""
      for s in L
        k=register[s.replace(/ /g,'').replace(/(^,)|(,$)/g,"")]
        console.log(k,k==undefined,s)
        if k==undefined
          output+=s
        else
          output+=k.toString()

      output=output.trim()
          
    i++
    
  -1
  
____________________________________________________
assemblerInterpreter = (program) ->
  cmd_list = []
  label_hash = {}
  for line in program.split("\n")
    line = line.replace /\s+/g, " "
    line = line.trim()
    if !line.startsWith "msg"
      line = line.replace /;.*$/, "" # NOTE msg and string token
    line = line.trim()
    continue if line == ""
    if reg_ret = /^(\w+):$/.exec line
      [_skip, label] = reg_ret
      label_hash[label] = cmd_list.length
      continue
    
    cmd_list.push line
  
  
  call_stack = []
  reg_hash = {}
  cmp_res = 0
  exec_ptr = 0
  extract = (t)->
    if /^-?\d+$/.test t
      +t
    else
      reg_hash[t]
  
  stdout_list = []
  
  loop
    cmd = cmd_list[exec_ptr]
    return -1 if !cmd # bad program
    
    if reg_ret = /^mov (.*)\s*,\s*(.*)$/.exec cmd
      [_skip, dst, src] = reg_ret
      reg_hash[dst] = extract src
    else if reg_ret = /^inc (.*)$/.exec cmd
      [_skip, dst] = reg_ret
      reg_hash[dst]++
    else if reg_ret = /^dec (.*)$/.exec cmd
      [_skip, dst] = reg_ret
      reg_hash[dst]--
    else if reg_ret = /^add (.*)\s*,\s*(.*)$/.exec cmd
      [_skip, dst, src] = reg_ret
      src = extract src
      reg_hash[dst] += src
    else if reg_ret = /^sub (.*)\s*,\s*(.*)$/.exec cmd
      [_skip, dst, src] = reg_ret
      src = extract src
      reg_hash[dst] -= src
    else if reg_ret = /^mul (.*)\s*,\s*(.*)$/.exec cmd
      [_skip, dst, src] = reg_ret
      src = extract src
      reg_hash[dst] *= src
    else if reg_ret = /^div (.*)\s*,\s*(.*)$/.exec cmd
      [_skip, dst, src] = reg_ret
      src = extract src
      reg_hash[dst] = reg_hash[dst] // src
    else if reg_ret = /^cmp (.*)\s*,\s*(.*)$/.exec cmd
      [_skip, a, b] = reg_ret
      cmp_res = extract(a) - extract(b)
    else if reg_ret = /^(j.*) (.*)$/.exec cmd
      [_skip, cond_type, label] = reg_ret
      cond = false
      switch cond_type
        when "jne" then cond = cmp_res != 0
        when "je"  then cond = cmp_res == 0
        when "jl"  then cond = cmp_res <  0
        when "jle" then cond = cmp_res <= 0
        when "jg"  then cond = cmp_res >  0
        when "jge" then cond = cmp_res >= 0
        when "jmp" then cond = true
      if cond
        return -1 if !(ptr = label_hash[label])? # bad program
        exec_ptr = ptr
        continue
    else if reg_ret = /^end$/.exec cmd
      break
    else if reg_ret = /^call (.*)$/.exec cmd
      [_skip, label] = reg_ret
      return -1 if !(ptr = label_hash[label])? # bad program
      call_stack.push exec_ptr+1
      exec_ptr = ptr
      continue
    else if reg_ret = /^ret$/.exec cmd
      return -1 if call_stack.length == 0 # bad program
      exec_ptr = call_stack.pop()
      continue
    else if reg_ret = /^msg (.*)$/.exec cmd
      [_skip, str] = reg_ret
      regex = (reg_exp)->
        if reg_ret = reg_exp.exec str
          str = str.substr reg_ret[0].length
          return reg_ret
        null
      while str != ""
        break if reg_ret = regex /^;/
        continue if reg_ret = regex /^,/
        continue if reg_ret = regex /^\s+/
        if reg_ret = regex /^'(.*?)'/
          [_skip, val] = reg_ret
          stdout_list.push val
          continue
        if reg_ret = regex /^\w+/
          stdout_list.push extract reg_ret[0]
          continue
        if reg_ret = regex /^\d+/
          stdout_list.push +reg_ret[0]
          continue
        
        break
      
    else
      throw new Error "bad command #{cmd}"
    exec_ptr++
  
  stdout_list.join ""

____________________________________________________
parseArgs = (args) ->
  parsed = []
  tokens = {} =
    number: /^[\-\.\d]+/i
    string: /^'(?:[^']|'')*'/
    name:   /^[\w\.]+/
    comma:  /^,\s?/
  fetchToken = ->
    args = (args ? '').trim()
    for k, re of tokens
      if m = args.match(re)
        args = args.substr(m[0].length)
        return [k, m[0]]
  loop
    [k, v] = fetchToken() ? []
    continue if k == 'comma'
    break unless v
    parsed.push([k, v])
  parsed


parseProgram = (program) ->
  parsed = []
  labels = {}
  cmdRe   = /^\s*(\w+)(?:\s+([^;]+))?(\s*;.*)?$/
  labelRe = /^\s*(\w+)\:\s*$/
  for str in program.split('\n')
    if m = str.match(cmdRe)
      cmd = m[1..]
      cmd[1] = parseArgs(cmd[1])
      parsed.push(cmd)
    else if m = str.match(labelRe)
      parsed.push([])
      labels[m[1]] = parsed.length - 1
  [parsed, labels]

assemblerInterpreter = (program) ->
  callstack = []
  output = ''
  regs = {}
  cursor = 0
  cmpRes = null

  regOrInt = (a) ->
    return parseInt(a[1]) if a[0] == 'number'
    return regs[a[1]]     if a[0] == 'name'

  [commands, labels] = parseProgram(program)
  loop
    cmd = commands[cursor]
    break if undefined == cmd
    [cmnd, args] = cmd
    [a, b] = args if args
    switch cmnd
      when 'end' then return output
      when 'mov' then regs[a[1]] = regOrInt(b)

      when 'inc' then regs[a[1]] += 1
      when 'dec' then regs[a[1]] -= 1
      when 'add' then regs[a[1]] += regOrInt(b)
      when 'sub' then regs[a[1]] -= regOrInt(b)
      when 'mul' then regs[a[1]] *= regOrInt(b)
      when 'div' then regs[a[1]] = Math.floor(regs[a[1]] / regOrInt(b))

      when 'cmp' then cmpRes = regOrInt(a) - regOrInt(b)
      when 'jmp'
        cursor = labels[a[1]]
        continue
      when 'jne'
        if cmpRes != 0
          cursor = labels[a[1]]
          continue
      when 'je'
        if cmpRes == 0
          cursor = labels[a[1]]
          continue
      when 'jge'
        if cmpRes >= 0
          cursor = labels[a[1]]
          continue
      when 'jg'
        if cmpRes > 0
          cursor = labels[a[1]]
          continue
      when 'jle'
        if cmpRes <= 0
          cursor = labels[a[1]]
          continue
      when 'jl'
        if cmpRes < 0
          cursor = labels[a[1]]
          continue
      when 'call'
        callstack.push(cursor)
        cursor = labels[a[1]]
        continue
      when 'ret'
        cursor = callstack.pop()
      when 'msg'
        output += args.map((a) ->
          switch a[0]
            when 'string' then a[1].replace(/^'((?:[^']|'')*)'/, '$1').replace(/''/g, '\'')
            when 'name'   then regs[a[1]]
            when 'number' then a[1]
        ).join('')
    cursor += 1
  -1
  
____________________________________________________
config = undefined
utils = 
  run: (x) ->
    utils.start x
    while config.online
      if !config.mem[config.pc]
        break
      utils.filter config.mem[config.pc++]
    if config.online then -1 else config.res
  start: (x) ->
    is_eq = undefined
    x.split('\n').forEach (i) ->
      i = i.trim()
      i = i.replace(/;.*$/, '').trim()
      if !i
        return
      if is_eq = i.match(/(.*)\:$/)
        config.lbl[is_eq[1]] = config.mem.length
        return
      config.mem.push i
      return
    return
  test_reg: (x) ->
    x.match /^\D/
  get_val: (x) ->
    if utils.test_reg(x) then +config.reg[x] else +x
  get_args: (s) ->
    arr = []
    reg = /\s*('(.+?)'|([^,]+))\s*\,?/g
    while `m = reg.exec(s)`
      arr.push m[1]
    arr
  filter: (instrucion) ->
    is_eq = instrucion.match(/(\S+)\s*(.*)$/)
    arr = utils.get_args(is_eq[2])
    if `is_eq[1] == 'mov'`
      config.reg[arr[0]] = utils.get_val(arr[1])
    else if `is_eq[1] == 'add'`
      config.reg[arr[0]] += utils.get_val(arr[1])
    else if `is_eq[1] == 'sub'`
      config.reg[arr[0]] -= utils.get_val(arr[1])
    else if `is_eq[1] == 'call'`
      config.items.push config.pc
      config.pc = config.lbl[arr[0]]
    else if `is_eq[1] == 'jmp'`
      config.pc = config.lbl[arr[0]]
    else if `is_eq[1] == 'inc'`
      config.reg[arr[0]]++
    else if `is_eq[1] == 'mul'`
      config.reg[arr[0]] *= utils.get_val(arr[1])
    else if `is_eq[1] == 'div'`
      config.reg[arr[0]] = Math.floor(config.reg[arr[0]] / utils.get_val(arr[1]))
    else if `is_eq[1] == 'dec'`
      config.reg[arr[0]]--
    else if `is_eq[1] == 'cmp'`
      a = utils.get_val(arr[0])
      b = utils.get_val(arr[1])
      config.eq = `a == b`
      config.lt = a < b
    else if `is_eq[1] == 'jne'`
      if !config.eq
        config.pc = config.lbl[arr[0]]
    else if `is_eq[1] == 'jg'`
      if !config.eq and !config.lt
        config.pc = config.lbl[arr[0]]
    else if `is_eq[1] == 'jle'`
      if config.eq or config.lt
        config.pc = config.lbl[arr[0]]
    else if `is_eq[1] == 'ret'`
      if !config.items.length
        throw 'Empty config.items'
      config.pc = config.items.pop()
    else if `is_eq[1] == 'msg'`
      arr.map (arg) ->
        is_eq = arg.match(/^\'(.*)\'$/)
        if is_eq
          config.res += is_eq[1]
        else
          config.res += utils.get_val(arg)
        return
    else if `is_eq[1] == 'je'`
      if config.eq
        config.pc = config.lbl[arr[0]]
    else if `is_eq[1] == 'jge'`
      if !config.lt
        config.pc = config.lbl[arr[0]]
    else if `is_eq[1] == 'jl'`
      if !config.eq and config.lt
        config.pc = config.lbl[arr[0]]
    else if `is_eq[1] == 'end'`
      config.online = false
    return

assemblerInterpreter = (x) ->
  config =
    online: true
    items: []
    mem: []
    lbl: {}
    reg: {}
    eq: 0
    lt: 0
    pc: 0
    res: ''
  utils.run x

____________________________________________________
parseProg = (program) ->
  #break by line
  program = program.split('\n')
  
  #eliminate comments
  program = (line.split('\'') for line in program)
  relevant = (Math.max((i for i in [0..line.length - 1] by 2)...) for line in program)
  program = (program[i][0...relevant[i] + 1] for i in [0..program.length - 1])
  program = (line.join('\'') for line in program)
  program = (line.replace(/;[^']*$/, '') for line in program)
  
  #tokenize, eliminate blank lines
  program = (line.match(/('[^']*')|[^,\s]+/g) for line in program)
  nprog = []
  for line in program
    nprog.push(line) if line isnt null
  program = nprog
  
  #strip commas from args
  program = ((token.replace(/,$/, '') for token in line) for line in program)

funcPoints = (program) ->
  points = {}
  for line, i in program
    points[line[0].slice(0, -1)] = i if line[0].slice(-1) is ':'
  points

interpInp = (inp, regs) -> if inp in (key for key of regs) then regs[inp] else parseInt(inp)

msg = (args, regs) ->
  out = ''
  for arg in args
    console.log(arg)
    inst = regs[arg]
    if inst == undefined
      out += arg.slice(1, arg.length - 1)
    else
      out += "#{inst}"
  out

div = (a, b) ->
  (a - (a % b)) / b

assemblerInterpreter = (program) ->
  #grunt work
  program = parseProg program
  points = funcPoints program
  
  inWrongFunc = false
  regs = {}
  cmp = []
  recRet = []
  end = false
  outStr = ''
  
  i = 0
  while i < program.length
    line = program[i]
    
    if inWrongFunc
      if line[0] == 'ret'
        inWrongFunc = false
        if recRet.length > 0
          i = recRet.pop()
    else
      if line[0] == 'mov'
        regs[line[1]] = interpInp(line[2], regs)
      else if line[0] == 'inc'
        regs[line[1]] += 1
      else if line[0] == 'dec'
        regs[line[1]] -= 1
      else if line[0] == 'add'
        regs[line[1]] += interpInp(line[2], regs)
      else if line[0] == 'sub'
        regs[line[1]] -= interpInp(line[2], regs)
      else if line[0] == 'mul'
        regs[line[1]] *= interpInp(line[2], regs)
      else if line[0] == 'div'
        regs[line[1]] = div(regs[line[1]], interpInp(line[2], regs))
      else if line[0] == 'cmp'
        cmp = [interpInp(line[1], regs), interpInp(line[2], regs)]
      else if line[0] == 'call'
        recRet.push(i)
        i = points[line[1]]
      else if line[0] == 'ret'
        if recRet.length > 0
          i = recRet.pop()
      else if line[0] == 'jmp'
        i = points[line[1]]
      else if line[0] == 'jne'
        i = points[line[1]] if cmp[0] != cmp[1]
      else if line[0] == 'je'
        i = points[line[1]] if cmp[0] == cmp[1]
      else if line[0] == 'jge'
        i = points[line[1]] if cmp[0] >= cmp[1]
      else if line[0] == 'jg'
        i = points[line[1]] if cmp[0] > cmp[1]
      else if line[0] == 'jle'
        i = points[line[1]] if cmp[0] <= cmp[1]
      else if line[0] == 'jl'
        i = points[line[1]] if cmp[0] < cmp[1]
      else if line[0].slice(-1) == ':'
        inWrongFunc = true
      else if line[0] == 'end'
        end = true
        break
      else if line[0] == 'msg'
        outStr = msg(line.slice(1, line.length), regs)
    i += 1
  
  if end then outStr else -1
