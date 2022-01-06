function parseRegExp(s) {
  // simple recursive descent parser
  let i = 0;

  const parse_normal = () => /^[^\*\|\(\)]$/.test(s[i]) ? new Normal(s[i++]) : null;
  const parse_any = () => s[i] === '.' ? new Any(s[i++]) : parse_normal();
  
  const parse_group = () => {
    if (s[i] === '(') {
      i++;
      const next = parse_or();
      if (s[i++] !== ')') throw new Error('Unclosed group');
      return next;
    } else {
      return parse_any();
    }
  };
  
  const parse_zero_or_more = () => {
    const next = parse_group();
    if (s[i] === '*') {
      i++;
      return new ZeroOrMore(next);
    }
    return next;
  };

  const parse_str = () => {
    const set = [];
    let r;
    while ( r = parse_zero_or_more() ) set.push(r);
    if (set.length === 0) return null;
    return (set.length === 1) ? set[0] : new Str(set);
  };

  const parse_or = () => {
    const next = parse_str();
    if (s[i] === '|') {
      i++;
      return new Or(next, parse_str());
    } else {
      return next;
    }
  };
  
  try {
    const ast = parse_or();
    if (i !== s.length) throw new Error('Could not parse');
    return ast;
  } catch (e) {
    return null;  // invalid
  }
}
____________________________________________________________
function parseRegExp(s) {
  const eof = () => ! tokens.length ;
  const satisfy = pred => pred(tokens[0]) && tokens.shift() ;
  const char = c => satisfy( v => v===c ) ;
  const pParen = (e) => char('(') && ( e = pOr() || _|_ ) && ( char(')') || _|_ ) && e ;
  const pNormal = (e) => ( e = satisfy( v => ! "()*|.".includes(v) ) ) && new Normal(e) ;
  const pAny = () => char('.') && new Any ;
  const pMany = (e) => ( e = pParen() || pNormal() || pAny() ) && char('*') ? new ZeroOrMore(e) : e ;
  const pStr = (e,f) => { for ( e = []; f = pMany(); e.push(f) ); return e.length && ( e.length===1 ? e[0] : new Str(e) ) ; } ;
  const pOr = (e,f) => ( e = pStr() ) && char('|') ? ( f = pStr() ) && new Or(e,f) : e ;
  const pRegex = (e) => ( e = pOr() ) && eof() && e ;
  let tokens = s.split("");
  try      { return pRegex() || null ; }
  catch(_) { return null; } // pParen should not eat tokens if it's going to fail later. use an index instead of `.shift()` ?
}
____________________________________________________________
var parseRegExp = (function() {
    var flatred = (r,v,i,a) => r.concat(v);
    return function parseRegExp(str) {
        var z, s, g, i, j, b, a = splitRegExp(str);
        if (!a) return null;
        for (g=a[i=0]; i<a.length; g=a[++i]) {
            for (s=g[j=0]; j<g.length; s=g[++j]) {
                b = s[0]=='(', z = b && s[s.length-1]=='*';
                s = b ? parseRegExp(s.slice(+b,-b-z)) : parseStr(s);
                if (!s) return null;
                if (z) s = new ZeroOrMore(s);
                g[j] = s;
            }
            if (g.some(Array.isArray)) g = g.reduce(flatred,[]);
            a[i] = g.length==1 ? g[0] : new Str(g);
        }
        a = a.or ? new Or(...a) : a[0];
        return a;
    };
    function parseStr(str) {
        var c, i = 0, r = [];
        for (c=str[i]; i<str.length; c=str[++i]) {
            if (c=='*') return null;
            c = c=='.' ? new Any() : new Normal(c);
            if (str[i+1]=='*') ++i, c = new ZeroOrMore(c);
            r.push(c);
        }
        return r;
    }
    function splitRegExp(str) {
        var r = [[]], i = 0, j = 0;
        if (!str || '|*)'.indexOf(str[0])!=-1) return null; else r.or = 0;
        do {
            if (str[j]==')') return null;
            j = indexFrom(str,'()|',j-1);
            if (j!=-1) {
                if (i!=j) r[r.length-1].push(str.slice(i,i=j));
                if (str[j]=='(') {
                    j = matchBraces(str,j);
                    if (j==-1 || j==i+1) return null;
                    if (str[++j]=='*') ++j;
                    r[r.length-1].push(str.slice(i,j));
                }
                else if (str[j]=='|') r.or = 1, r.push([]), ++j;
            }
            else r[r.length-1].push(str.slice(i));
        } while ((i=j)!=-1 && i<str.length);
        return r.length==1+r.or && r.every(g => g.length) ? r : null;
    }
    function indexFrom(str,chr,i) {
        while (++i<str.length && chr.indexOf(str[i])==-1);
        return i<str.length ? i : -1;
    }
    function matchBraces(str,i) {
        var b = 1;
        while (b && ++i<str.length) str[i]=='(' && ++b, str[i]==')' && --b;
        return !b && i<str.length ? i : -1;
    }
})();
____________________________________________________________
const parseRegExp = str => {
    
    try {
        
        const matchingParen = tokens => {
            for(let i = 0, balance = 1; i < tokens.length; i++) {
                balance += tokens[i] === '('; balance -= tokens[i] === ')'
                if(!balance) return i
            }
            throw Error('No matching parenthesis.')
        }
        
        const createTree = tokens => {
        
            if(!tokens.length) throw Error('Nothing to parse.')
            
            let stack = [], ops = [], ast = [], seq = [], arg, arg2
            
            while(tokens.length) {
                let curr = tokens.shift()
                if(curr === '(') {
                    let subExpr = tokens.splice(0, matchingParen(tokens))
                    tokens.shift()
                    seq.push(createTree(subExpr))
                }
                if(curr === ')')
                    throw Error('Invalid parentheses.')
                if(curr === '*') {
                    arg = seq.length ? seq.pop() : stack.pop()
                    if(arg instanceof ZeroOrMore) throw Error('Syntax Error (ZeroOrMore).')
                    seq.push(new ZeroOrMore(arg))
                }
                if(curr === '|') {
                    stack.push(seq.length > 1 ? new Str(seq) : seq[0])
                    seq = []
                    ops.push(curr)
                }
                if(!'()*|'.includes(curr))
                    seq.push(curr === '.' ? new Any() : new Normal(curr))
            }
            stack.push(seq.length > 1 ? new Str(seq) : seq[0])
            
            if(ops.length) {
                while(ops.length) {
                    arg2 = stack.pop(); arg = stack.pop()
                    if(!arg || !arg2) throw Error('Syntax error (Or).')
                    ast.push(new Or(arg, arg2))
                    ops.pop()
                }
            }
            else ast = stack
            
            return ast.length > 1 ? new Str(ast) : ast.pop()
        }
        
        return createTree([...str])
    }

    catch (e) { return null }

}
____________________________________________________________
const parseRegExp = ([...arr]) => (p = n => {
  for(var v, ret = [[]]; v = arr.shift();){
    if(v == ")"){n = !n; break}
    if(v == "*" || (v == "|" && (ret[1] || !ret[0][0]))) return null;
    if(v == "|"){ret.unshift([]); continue}
    v = v == "(" ? p(1) : v == "." ? new Any(): new Normal(v);
    if(v == null) return null;
    ret[0].push(arr[0] == "*" ? arr.shift() && new ZeroOrMore(v) : v);
  } 
  let f = ret.map(a => a[1] ? new Str(a) : a[0]);
  return n || !ret[0][0] ? null : f[1] ? new Or(f[1], f[0]) : f[0];
})();
