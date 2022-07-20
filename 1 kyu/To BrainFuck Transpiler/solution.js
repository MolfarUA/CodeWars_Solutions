59f9cad032b8b91e12000035



function kcuf(code) {
  let q = false
  let statements = [...code]  // for each character
    .map(c => /"|'/.test(c) ? (q=!q,c) : q ? c : c.toUpperCase())
    .join``.split`\n`
    .map(i=>i  // for each statement
      .replace(/^\s+|("[^"]*")|(\/\/|--|#).*$/g,m=>m[0]=='"'?m:'')
      .match(/("[^"]*")|('[^']')|-?\d+|[$_A-Za-z][$\w]*(\s*\[\s*\d+\s*\])?/g)
    )
    .filter(i=>i)
  
  let procs = {}
  for (let i=0; i<statements.length; i++) if (statements[i][0] == 'PROC') for (let lvl=0, j=i+1; j<statements.length; j++) switch(statements[j][0]) {
    case 'PROC': case 'VAR': throw Error(`'proc' and 'var' not allowed inside 'proc'`)
    case 'IFEQ': case 'IFNEQ': case 'WNEQ': lvl++; break
    case 'END': if (!(lvl--)) {
      let proc = statements.splice(i, j-i+1).slice(0,-1)
      let params = proc.shift().slice(1)
      let name = params.shift()
      if (procs[name]) throw Error(`proc '${name}' not defined`)
      if (params.some((d,i)=>i!=params.indexOf(d))) throw Error(`wrong number of arguments in proc call`)
      procs[name] = {proc, params}
      j = statements.length
      i--
    }
  }
  let i, n = 0
  while ((i = statements.findIndex(s => s[0] == 'CALL')) > -1) {
    let input = statements[i].slice(2)
    let {proc, params} = procs[statements[i][1]]
    if (input.length != params.length) throw Error(`wrong number of arguments for instruction`)
    statements.splice(i, 1, ...proc.map(cmd => cmd.map(a => (i = params.indexOf(a)) > -1 ? input[i] : a)))
    if (n++ > 30) throw Error(`stack overflow`)
  }
  
  let bf = '', Z = '[-]', P = '+', M = '-', varDict = {}, ptr = 0, stack = [], mem = [], temps = 0
  let temp = (n=0) => {
    let name = 'temp' + temps++
    cmds.var(name + (n ? `[${n}]` : ''))
    return name
  }
  let del = (...names) => {
    names.forEach(name => {
      let i = varDict[name]
      let n = mem[i] + i
      for (; i < n; i++) mem[i] = 0
      delete varDict[name]
    })
    mem.reverse()
    while (mem[0]==0) mem.shift()
    mem.reverse()
  }
  
  let num = val => /^'.'$/.test(val) ? val.charCodeAt(1) : val
  let varTest = name => { if (mem[varDict[name]]>1) throw Error(`expected non-list var`) }
  let godo = (varName, ins) => {
    if (!varDict.hasOwnProperty(varName)) throw Error(`var '${varName}' not defined`)
    let t = varDict[varName] - ptr
    bf += (t>0 ? '>' : '<').repeat(Math.abs(t))
    ptr = varDict[varName]
    bf += ins || ''
  }
  let loop = (test, ...rest) => {
    godo(test, '[')
    while (rest.length) godo(...rest.splice(0,2))
    godo(test, M)
    bf += ']'
  }
  let prepareList = (a,b) => {
    if (mem[varDict[a]] <= 1) throw Error('expecting list')
    godo(a, '[-]>[-]>[-]<<')
    if (isNaN(b)) {
      loop(b, a, '+>+>+<<')
      loop(a, b, P)
    } else {
      bf += '>'+P.repeat(b)+'>'+P.repeat(b)+'<<'
    }
  }
  let onList = (l,r) => godo(l, `>>>>${r}<<<<`)  // pointer should be at list init and will end at list init
    
  let cmds = {
    'var': (...names) => names.forEach(name => {
      let [_, n, size] = name.match(/^([$_A-Za-z][$\w]*)(?:\s*\[\s*(\d+)\s*\])?$/) || []
      if (!_) throw Error(`var '${name}' invalid syntax`)
      if (varDict.hasOwnProperty(n)) throw Error(`var '${n}' already declared`)
      
      if (size) {
        let len = +size+4
        let next = ((mem.join`,`.indexOf(Array(len).fill('0').join`,`) + 1) || (mem.length + 1)) - 1
        varDict[n] = next
        mem.splice(next, len, len, ...Array(len-1).fill(1))
        godo(n, '[-]>'.repeat(len) + '<'.repeat(len))
      } else {
        let next = ((mem.findIndex(c => !c) + 1) || (mem.length + 1)) - 1
        mem[next] = 1
        varDict[n] = next
      }
    }),
    'set': (name, val) => {
      val = num(val)
      if (isNaN(val)) {
        varTest(val)
        let t = temp()
        godo(t, Z)
        godo(name, Z)
        loop(val, name, P, t, P)
        loop(t, val, P)
        del(t)
      } else {
        val = +val
        while (val<0) val+=256
        godo(name, Z + P.repeat(val%256))
      }
    },
    'inc': (a,b) => {
      let t = temp()
      cmds.set(t, b)
      loop(t, a, P)
      del(t)
    },
    'dec': (a,b) => {
      let t = temp()
      cmds.set(t, b)
      loop(t, a, M)
      del(t)
    },
    
    'add': (a,b,c) => {
      let t1 = temp(), t2 = temp()
      cmds.set(t1, a)
      cmds.set(t2, b)
      godo(c, Z)
      loop(t1, c, P)
      loop(t2, c, P)
      del(t1,t2)
    },
    'sub': (a,b,c) => {
      let t1 = temp(), t2 = temp()
      cmds.set(t1, a)
      cmds.set(t2, b)
      godo(c, Z)
      loop(t1, c, P)
      loop(t2, c, M)
      del(t1,t2)
    },
    'mul': (a,b,c) => {
      if (b===c) [a,b] = [b,a]  // Necessary due to order of nested loops
      let t1 = temp(), t2 = temp(), t3 = temp()
      cmds.set(t1, a)
      cmds.set(t2, b)
      godo(c, Z)
      godo(t1, '[')
        cmds.set(t3, t2)
        loop(t3, c, P)
        godo(t1, M)
      bf += ']'
      del(t1,t2,t3)
    },
    'divmod': (a,b,c,d) => {
      let t = temp(9)
      cmds.lset(t,0,b)
      cmds.lset(t,1,1)
      cmds.lset(t,2,0)
      cmds.lset(t,3,a)
      cmds.lset(t,4,b)    // below turns `d 1 0 n d` into `0 0 0 0 d-n%d n%d n/d` - works for d=1
      onList(t, '-[>->+<<[-]]>[>>[>>>+<<<-]<<-]>[>[->-[>+>>]>[+[-<+>]>+>>]<<<<<]<-]<<')    // custom-made
      if (c!==undefined) cmds.lget(t,6,c)
      if (d!==undefined) cmds.lget(t,5,d)
      del(t)
    },
    'div': (a,b,c) => cmds.divmod(a,b,c),
    'mod': (a,b,c) => cmds.divmod(a,b,undefined,c),      
    
    'cmp': (a,b,c) => {
      let t = temp(6)
      cmds.lset(t,1,a)
      cmds.lset(t,3,b)
      let compare = '[[>+<-]>>[[>+<-]>>+<<]<<]>[<+>-]>>[<+>-]>'  // must start at i=1, ends at i=5
      onList(t, '>'+compare+'[-<<-<<-'+compare+']<<[<<<->>>[-]]<<[<+>[-]]<')    // custom-made
      cmds.lget(t,0,c)
    },
    
    'a2b': (a,b,c,d) => {
      let t1 = temp(), t2 = temp()
      cmds.set(t1,b)
      cmds.set(t2,c)
      cmds.sub(a,48,d)
      cmds.mul(d,100,d)
      cmds.sub(t1,48,t1)
      cmds.mul(t1,10,t1)
      cmds.add(d,t1,d)
      cmds.sub(t2,48,t2)
      cmds.add(d,t2,d)
      del(t1,t2)
    },
    
    'b2a': (a,b,c,d) => {
      let t = temp()
      cmds.set(t,a)
      cmds.div(t,100,b)
      cmds.add(b,48,b)
      cmds.div(t,10,c)
      cmds.mod(c,10,c)
      cmds.add(c,48,c)
      cmds.mod(t,10,d)
      cmds.add(d,48,d)
      del(t)
    },
    
    'lset': (a,b,c) => {
      prepareList(a,b)
      c = num(c)
      if (isNaN(c)) {
        varTest(c)
        loop(c, a, '+>>>+<<<')
        loop(a, c, P)
      } else {
        bf += '>>>'+P.repeat(c)+'<<<'
      }
      godo(a, '[-]>[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]>>>[-]<[->+<]<[[-<+>]<<<[->>>>+<<<<]>>-]<<')    // Credit: Konstantinos Asimakis
    },
    
    'lget': (a,b,c) => {
      prepareList(a,b)
      godo(a, '[-]>[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]>>>[-<+<<+>>>]<<<[->>>+<<<]>[[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-] >[<<<+>>>-]<<<')    //<< Credit: Konstantinos Asimakis
      godo(c, Z)
      loop(a, c, P)
    },
    
    'ifeq': (a,b) => {
      let t1 = temp(2), t2 = temp()
      cmds.sub(a,b,t2)
      cmds.lset(t1,0,t2)
      onList(t1, '[[-]>+<]+>[<->-]<')    // Credit: igor @ http://shygypsy.com/bflib.txt
      cmds.lget(t1,0,t2)
      del(t1)
      godo(t2, '[')
      stack.push(() => {
        godo(t2, Z)
        del(t2)
        bf += ']'
      })
    },
    'ifneq': (a,b) => {
      let t = temp()
      cmds.sub(a,b,t)
      godo(t, '[')
      stack.push(() => {
        godo(t, Z)
        del(t)
        bf += ']'
      })
    },
    'wneq': (a,b) => {
      let t = temp()
      cmds.sub(a,b,t)
      godo(t, '[')
      stack.push(() => {
        cmds.sub(a,b,t)
        godo(t,'')
        bf += ']'
        del(t)
      })
    },
    'end': () => stack.pop()(),
    
    'read': name => godo(name, ','),
    'msg': (...parts) => {
      let t = temp()
      parts.forEach(part => /^"[^"]*"$/.test(part)
        ? [...part.slice(1,-1).replace(/\\n/g, '\n')].forEach(c => godo(t, Z + P.repeat(c.charCodeAt()) + '.') )
        : godo(part, '.')
      )
      del(t)
    },
    'rem': (...a) => {}
  }
  
  statements.forEach(([cmd, ...args]) => {
    let ins = cmds[cmd.toLowerCase()]
    if (!ins) throw Error(`cmd '${cmd}' not recognized`)
    if (ins.length && ins.length != args.length) throw Error(`wrong number of arguments for '${cmd}'`)
    ins(...args)
  })
  if (stack.length) throw Error(`unclosed block`)
  
  return bf
}

############################################
function kcuf(code, vars = new Map()){
  let a, b, mem = 8, ptr = 0, nest = 0, loops = [],
    proc = ([s, ...r]) => (assert(!b && !vars.has(s) && new Set(r).size == r.length), b = [], nest++, vars.set(s, {r, b}), 0),
    take = (p = /\s/, f, r = a) => r[0] && (x = f ? p(r) : p.test(r[0])) ? (f ? f(x) : r.shift()) + take(p, f, r) : "",
    v = () => (take(), assert(a.length && /[$_a-z]/i.test(a[0])), (a.shift() + take(/[$_\w]/)).toLowerCase()),
    cn = () => (a.shift(), pc(a) + (assert(a.shift() == "'") || 0)),
    vn = () => (take(), a[0] == "'" ? cn() : /[\-\d]/.test(a[0]) ? +((a[0] == "-" ? a.shift() : "") + take(/\d/)) : v()),
    vs = () => (take(), !a.length ? "" : a[0] != "\"" ? v() : a.shift() + take(/[^"]/) + (assert(a[0] == "\""), a.shift())),
    rn = () => (take(), a[0] == "[" && (assert(a.includes("]")), +a.splice(0, a.indexOf("]") + 1).slice(1, -1).join("") + 4)),
    pc = r => (r[0] != "\\" ? r.shift() : r.splice(0, 2)[1].replace(/[nrt]/g, x => ({n:"\n", r:"\r", t:"\t"}[x]))).charCodeAt(0),
    get = (x, r) => (e = vars.get(x), x.map ? get(x[0], 1) + x[1] : x.trim ? (assert(e && e[1] == r), e[0]) : x),
    fill = (x, s = "-+") => Array(Math.abs(s == "-+" ? x % 256 : x)).fill(s[+(x > 0)]).join(""),
    jmp = x => (d = get(x, 0), fill(d - ptr, "<>") + (ptr = d, "")),
    inc = (x, y = 1, n = 0) => y.trim ? add(x, y, n) : !y ? "" : jmp(x) + fill(y * (-1) ** n),
    clr = (x, f, n, d) => jmp(x) + "[" + (d > 0 ? "<" : "") + (f ? f() : "") + (d < 0 ? ">" : "") + (n ? clr(x) : inc(x, -1)) + "]",
    loop = (n = 0) => (loops.push(() => inc(3, n) + jmp(4) +  (n ? "]" + jmp(3) : "") + "]"), jmp(4) + "[" + clr(4)),
    set = (y, x = v(), n) => clr(x) + clr(y, () => inc(x, n)),
    prp = (...r) => r.reduce((s, x) => s + inc(Math.abs(x), vn(), x < 0), ""),
    add = (x, y, n) => set(y, 0) + clr(0, () => inc(y) + inc(x, 1, n)),
    eql = n => clr(3, () => inc(4, (-1) ** !n), 1),
    div = () => clr(1, () => inc(5) + add(3, 2) + add(3, 5, 1) + eql() + inc(4) + clr(4, () => clr(5) + inc(6))) + clr(2),
    swp = (r, n, ...p) => clr([r, 1 + (n > 0)], () => p.reduce((s, x) => s + set([r, (x + n + 5) % 5], [r, x], 1), ""), 0, n),
    arr = (r, x, y) => inc([r, 1], x) + inc([r, 2], x) + inc([r, 3], y || 0) + swp(r, -1, 0, 4, 3, 2) + clr([r, 4], !y && 
      (() => inc([r, 3]) + inc([r, 1]))) + set([r, y ? 3 : 1], [r, 4]) + swp(r, 1, 2, 3, 4) + (!y ? set([r, 3]) : "");
  return code.split("\n").map(s => s.match(/^\s*(\w*)\s*((-[^-]|\/[^/]|"[^"]*"|[^-/#])*)/)).filter(([s, i, r]) => (
    /proc/i.test(i) ? proc(r.toLowerCase().split(/\s+/)) : i && (!b || (assert(!/var/i.test(i)), 
    /end/i.test(i) && !--nest ? b = 0 : (/eq/i.test(i) && nest++, b.push(s), 0)))
  )).reduce((s, [_, inst, args]) => (a = [...args], s + ({
    rem: () => (a = [], ""),
    read: () => jmp(v()) + ",",
    lget: () => arr(v(), vn()),
    lset: () => arr(v(), vn(), vn()),
    inc: () => inc(v(), vn()),
    dec: () => inc(v(), vn(), 1),
    set: () => clr(v()) + prp(ptr),
    add: () => prp(1, 1) + set(1),
    sub: () => prp(1, -1) + set(1),
    div: () => prp(1, 2) + div() + set(6) + clr(5),
    mod: () => prp(1, 2) + div() + set(5) + clr(6),
    divmod: () => prp(1, 2) + div() + set(6) + set(5),
    mul: () => prp(1, 2) + clr(1, () => add(3, 2)) + clr(2) + set(3),
    ifeq: () => add(3, v()) + prp(-3) + eql() + inc(4) + loop(),
    ifneq: () => add(3, v()) + prp(-3) + eql(1) + loop(),
    wneq: () => inc(3) + jmp(3) + "[" + clr(3) + add(3, v()) + prp(-3) + eql(1) + loop(1), 
    end: () => (assert(loops.length), loops.pop()()),
    var: () => take(v, (x, l = rn()) => (assert(!vars.has(x)), vars.set(x, [mem, !!l]), mem += l || 1, "")),
    msg: () => take(vs, x => x[0] != "\"" ? jmp(x) + "." : jmp(0) + take(pc, y => fill(y) + "." + clr(0), [...x.slice(1, -1)])),
    cmp: () => prp(2, 3) + clr(2, () => inc(5, 2) + clr(3, () => clr(5) + inc(6)) + add(4, 5) + set(6, 3) + inc(3, -1)) + eql() + set(4),
    a2b: () => [100, 10, 1].reduce((s, x) => s + prp(1) + inc(1, -48) + clr(1, () => inc(4, x)), "") + set(4),
    b2a: () => prp(7) + [100, 10, 1].reduce((s, y, i) => s + add(1, 7) + inc(2, y) + div() + set(6, 1) + 
      clr(5) + inc(2, !i ? 100 : 10) + div() + clr(6) + inc(5, 48) + set(5), "") + clr(7),
    call: () => ({b, r} = vars.get(v()), n = [], take(v, x => n.push([r[n.length], vars.get(x)])), 
      assert(n.length == r.length), jmp(0) + kcuf(b.join("\n"), new Map([...vars, ...n])))
  }[inst.toLowerCase()] || assert)() + (take(), assert(!a.length), "")), "") + jmp(0);
}
###########################
function kcuf(code, vars = new Map()){
  let a, b, ptr = 0, mem = 8, nest = 0, loops = [],
    proc = ([s, ...r]) => (assert(!b && !vars.has(s) && new Set(r).size == r.length), b = [], nest++, vars.set(s, {r, b}), 0),
    take = (p = /\s/, f, r = a) => {for(var o = "", x; r[0] && (x = f ? p(r) : p.test(r[0])); o += f ? f(x) : r.shift()); return o},
    v = () => (take(), assert(a.length && /[$_a-z]/i.test(a[0])), (a.shift() + take(/[$_\w]/)).toLowerCase()),
    vn = () => (take(), a[0] == "'" ? (a.shift(), pc(a) + (assert(a.shift() == "'") || 0)) : 
      /[\-\d]/.test(a[0]) ? +((a[0] == "-" ? a.shift() : "") + take(/\d/)) : v()),
    vs = () => (take(), !a.length ? "" : a[0] != "\"" ? v() : a.shift() + take(/[^"]/) + (assert(a[0] == "\""), a.shift())),
    rn = () => (take(), a[0] == "[" && (assert(a.includes("]")), +a.splice(0, a.indexOf("]") + 1).slice(1, -1).join("") + 4)),
    pc = r => (x = r.shift(), (x != "\\" ? x : r.shift().replace("n", "\n").replace("r", "\r").replace("t", "\t")).charCodeAt(0)),
    get = (x, g, h = vars.get(x)) => x.map ? get(x[0], 1) + x[1] : x.trim ? (assert(h && h[1] == g), h[0]) : x,
    loop = f => (loops.push(() => (f ? f() : j(2)) + "]"), j(2) + "[" + c(2)),
    aa = (x, s = "-+") => Array(Math.abs(x)).fill(s[+(x > 0)]).join(""),
    j = (x, d = get(x, 0)) => aa(d - ptr, "<>") + (ptr = d, ""),
    addn = (x, y, n) => y.trim ? add(x, y, n) : !y ? "" : j(x) + aa(y * (-1) ** !!n % 256),
    c = (x, f, n) => j(x) + "[" + (f ? f() : "") + addn(x, -1 * !n) + "]",
    set = (x, y, z) => z ? "" : c(x) + c(y, () => addn(x, 1)),
    add = (x, y, n) => c(y, () => addn(0, 1)) + c(0, () => addn(y, 1) + addn(x, 1, n)),
    eq = n => c(1, () => addn(2, (-1) ** !n) + c(1), 1) + addn(2, !n),
    divmod = (q, r) => addn(3, 1) + c(1, () => addn(2, -1) + c(2, () => (ptr -= 3, addn(0, 1) + j(2)), 1) + 
      c(3, () => set(2, 3) + addn(3, 1) + addn(4, 1) + j(6), 1)) + c(2) + addn(3, -1),
    lHelp = (r, x, y, yy = y == undefined, z = yy && v()) => 
      addn([r, 1], x) + addn([r, 2], x) + addn([r, 3], y || 0) + c([r, 1], () => (ptr--, 
      set([r, -1], [r, 3]) + set([r, 3 - yy], [r, 2 - yy]) + set([r, 2 - yy], [r, 1 - yy]) + set([r, 1], [r, 0], yy) 
      )) + c([r, 4], yy && (() => addn([r, 3], 1) + addn([r, 1], 1))) + set([r, 4], [r, 3 - 2 * yy]) + 
      c([r, 2], () => (ptr++, set([r, 2], [r, 3]) + set([r, 3], [r, 4], !yy) + set([r, 4], [r, 0]))) + set(z, [r, 3], !yy),
    call = ({b, r}, args) => (assert(args.length == r.length), j(0) + kcuf(b.join("\u000A"), new Map([...vars, ...args.map((x, i) => [r[i], x])]))),
    b22a = (x) => addn(7, x) + [100, 10, 1].reduce((s, y) => s + add(1, 7) + addn(2, y) + divmod() + set(1, 4) + c(3) + addn(2, y == 100 ? 100 : 10) + divmod() + c(4) + addn(3, 48) + set(v(), 3), "") + c(7),
    cmp = () => c(3, () => addn(5, 1) + add(4, 1) + c(4, () => c(5)) + add(6, 5) + addn(1, -1)) + add(6, 6) + eq(1) + add(6, 2, 1) + c(1) + c(2);
  return code.split("\u000A").map(s => s.match(/^\s*(\w*)\s*((-[^-]|\/[^/]|"[^"]*"|[^-/#])*)/)).filter(([s, i, r]) => (
    /proc/i.test(i) ? proc(r.toLowerCase().split(/\s+/)) : i && (!b || (assert(!/var/i.test(i)), 
    /end/i.test(i) && !--nest ? b = 0 : (/eq/i.test(i) && nest++, b.push(s), 0)))
  )).reduce((s, [_, inst, args]) => (a = [...args], s + ({
    rem: () => (a = [], ""),
    read: () => j(v()) + ",",
    lget: () => lHelp(v(), vn()),
    lset: () => lHelp(v(), vn(), vn()),
    inc: () => addn(v(), vn()),
    dec: () => addn(v(), vn(), 1),
    set: () => c(v()) + addn(ptr, vn()),
    add: () => addn(1, vn()) + addn(1, vn()) + set(v(), 1),
    sub: () => addn(1, vn()) + addn(1, vn(), 1) + set(v(), 1),
    mul: () => addn(1, vn()) + addn(2, vn()) + c(1, () => add(3, 2)) + c(2) + set(v(), 3),
    div: () => addn(1, vn()) + addn(2, vn()) + divmod() + set(v(), 4) + c(3),
    mod: () => addn(1, vn()) + addn(2, vn()) + divmod() + set(v(), 3) + c(4),
    divmod: () => addn(1, vn()) + addn(2, vn()) + divmod() + set(v(), 4) + set(v(), 3),
    cmp: () => addn(3, vn()) + addn(1, vn()) + cmp() + set(v(), 6),
    ifeq: () => add(1, v()) + addn(1, vn(), 1) + eq() + loop(),
    ifneq: () => add(1, v()) + addn(1, vn(), 1) + eq(1) + loop(),
    wneq: () => addn(1, 1) + j(1) + "[" + c(1) + add(1, v()) + addn(1, vn(), 1) + eq(1) + loop(() => addn(1, 1) + j(2) + "]" + j(1)), 
    end: () => (assert(loops.length), loops.pop()()),
    call: () => call(vars.get(v()), (r = [], take(v, x => r.push(vars.get(x))), r)),
    var: () => take(v, (x, l = rn()) => (assert(!vars.has(x)), vars.set(x, [mem, !!l]), mem += l || 1, "")),
    msg: () => take(vs, x => x[0] != "\"" ? j(x) + "." : j(0) + take(pc, y => aa(y % 256) + "." + c(0), [...x.slice(1, -1)])),
    a2b: () => [100, 10, 1].reduce((s, x) => s + addn(1, vn()) + addn(1, -48) + c(1, () => addn(4, x)), "") + set(v(), 4),
    b2a: () => b22a(vn())
  }[inst.toLowerCase()] || assert)() + (take(), assert(!a.length), "")), "") + j(0);
}

############################################
function kcuf(code, vars = new Map()){
  let a, b, ptr = 0, mem = 10, nest = 0, loops = [];
  let aa = (x, s = "-+") => Array(Math.abs(x)).fill(s[+(x > 0)]).join("");
  let loop = f => (loops.push(() => (f ? f() : j(1)) + "]"), j(1) + "[" + c(1));
  let get = (x, g, h = vars.get(x)) => x.map ? get(x[0], 1) + x[1] : x.trim ? (assert(h && h[1] == g), h[0]) : x;
  let j = (x, d = get(x, 0)) => aa(d - ptr, "<>") + (ptr = d, "");
  let addn = (x, y, n) => y.trim ? add(x, y, n) : !y ? "" : j(x) + aa(y * (-1) ** !!n % 256);
  let c = (x, f, n) => j(x) + "[" + (f ? f() : "") + addn(x, -1 * !n) + "]";
  let set = (x, y, z) => z ? "" : c(x) + c(y, () => addn(x, 1));
  let add = (x, y, n) => c(y, () => addn(0, 1)) + c(0, () => addn(y, 1) + addn(x, 1, n));
  let eq = (x, y, n) => add(2, x) + addn(2, y, 1) + c(1) + c(2, () => addn(1, (-1) ** !n) + c(2), 1) + addn(1, !n);
  let divmod = (q, r) => addn(3, 1) + c(1, () => addn(2, -1) + c(2, () => (ptr -= 3, addn(0, 1) + j(2)), 1) + 
    c(3, () => set(2, 3) + addn(3, 1) + addn(4, 1) + j(6), 1)) + c(2) + addn(3, -1);
  let lHelp = (r, x, y, yy = y == undefined, z = yy && v()) => 
    addn([r, 1], x) + addn([r, 2], x) + addn([r, 3], y || 0) + c([r, 1], () => (ptr--, 
      set([r, -1], [r, 3]) + set([r, 3 - yy], [r, 2 - yy]) + set([r, 2 - yy], [r, 1 - yy]) + set([r, 1], [r, 0], yy) 
    )) + c([r, 4], yy && (() => addn([r, 3], 1) + addn([r, 1], 1))) + set([r, 4], [r, 3 - 2 * yy]) + 
    c([r, 2], () => (ptr++, set([r, 2], [r, 3]) + set([r, 3], [r, 4], !yy) + set([r, 4], [r, 0]))) + set(z, [r, 3], !yy);
  let take = (p = /\s/, f, r = a, x, o = "") => {while(r[0] && (x = f ? p(r) : p.test(r[0]))) o += f ? f(x) : r.shift(); return o};
  let v = () => (take(), assert(a.length && /[$_a-z]/i.test(a[0])), (a.shift() + take(/[$_\w]/)).toLowerCase());
  let pc = (r, x = r.shift()) => (x != "\\" ? x : r.shift().replace("n", "\n").replace("r", "\r").replace("t", "\t")).charCodeAt(0);
  let vn = () => (take(), a[0] == "'" ? (a.shift(), pc(a) + (assert(a.shift() == "'") || 0)) : 
    /[\-\d]/.test(a[0]) ? +((a[0] == "-" ? a.shift() : "") + take(/\d/)) : v());
  let vs = () => (take(), !a.length ? "" : a[0] != "\"" ? v() : a.shift() + take(/[^"]/) + (assert(a[0] == "\""), a.shift()));
  let rn = () => (take(), a[0] == "[" && (assert(a.includes("]")), +a.splice(0, a.indexOf("]") + 1).slice(1, -1).join("") + 4));
  return code.split("\u000A").map(s => s.match(/^\s*(\w*)\s*((-[^-]|\/[^/]|"[^"]*"|[^-/#])*)/)).filter(([s, inst, r]) => 
    (inst = inst.toLowerCase(), inst == "proc" ? ([s, ...r] = r.toLowerCase().split(/\s+/), 
    assert(!b && !vars.has(s) && new Set(r).size == r.length), b = [], nest++, vars.set(s, {r, b}), 0) : 
    inst && (!b || (assert(inst != "var"), inst == "end" && !--nest ? b = 0 : inst.slice(-1) == "eq" ? nest++ : b.push(s), 0))
  )).reduce((s, [_, inst, [...args] = ""]) => (a = args, s + ({
    rem: () => (a = [], ""),
    read: () => j(v()) + ",",
    inc: () => addn(v(), vn()),
    dec: () => addn(v(), vn(), 1),
    lget: () => lHelp(v(), vn()),
    lset: () => lHelp(v(), vn(), vn()),
    ifeq: () => eq(v(), vn()) + loop(),
    ifneq: () => eq(v(), vn() ,1) + loop(),
    set: (x = v()) => addn(1, vn()) + set(x, 1),
    add: () => addn(1, vn()) + addn(1, vn()) + set(v(), 1),
    sub: () => addn(1, vn()) + addn(1, vn(), 1) + set(v(), 1),
    mul: () => addn(1, vn()) + addn(2, vn()) + c(1, () => add(3, 2)) + c(2) + set(v(), 3),
    div: () => addn(1, vn()) + addn(2, vn()) + divmod() + set(v(), 4) + c(3),
    mod: () => addn(1, vn()) + addn(2, vn()) + divmod() + set(v(), 3) + c(4),
    divmod: () => addn(1, vn()) + addn(2, vn()) + divmod() + set(v(), 4) + set(v(), 3),
    wneq: () => addn(2, 1) + j(2) + "[" + c(2) + eq(v(), vn(), 1) + loop(() => addn(2, 1) + j(1) + "]" + j(2)), 
    end: () => (assert(loops.length), loops.pop()()),
    var: () => take(v, (x, l = rn()) => (assert(!vars.has(x)), vars.set(x, [mem, !!l]), mem += l || 1, "")),
    msg: () => take(vs, x => x[0] != "\"" ? j(x) + "." : j(0) + take(pc, y => aa(y % 256) + "." + c(0), [...x.slice(1, -1)])),
    a2b: () => [100, 10, 1].reduce((s, x) => s + addn(1, vn()) + addn(1, -48) + c(1, () => addn(4, x)), "") + set(v(), 4),
    b2a: () => addn(9, vn()) + [100, 10, 1].reduce((s, x) => s + add(1, 9) + addn(2, x) + divmod() + set(1, 4) + c(3) + 
      addn(2, x == 100 ? 100 : 10) + divmod() + c(4) + addn(3, 48) + set(v(), 3), "") + c(9),
    cmp: () => addn(3, vn()) + addn(4, vn()) + c(3, () => addn(1, 1) + add(2, 4) + c(2, () => c(1)) + add(5, 1) + 
      addn(4, -1)) + add(5, 5) + c(4, () => addn(5, -1) + c(4), 1) + set(v(), 5),
    call: ({r, b} = vars.get(v()), args = []) => (take(v, x => args.push([r[args.length], vars.get(x)])), 
      assert(args.length == r.length), j(0) + kcuf(b.join("\u000A"), new Map([...vars, ...args]))),
  }[inst.toLowerCase()] || assert)() + (take(), assert(!a.length), "")), "") + j(0);
}
