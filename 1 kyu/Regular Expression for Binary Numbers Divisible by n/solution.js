function regexDivisibleBy(n) {
  if (n==1) return '^[01]+$'  // Special case
  let a = []  // List of nodes
  for (let i=0; i<n; i++) a[i] = {}  // Node
  for (let i=0; i<n; i++) {
    a[i].id = i            // Used for indentification below
    a[i][i*2%n] = '0'      // Keys in nodes are id refs to other nodes
    a[i][(i*2+1)%n] = '1'  // Values in nodes are the required chars to get to next node (the key)
  }
  
  const removeGroups = re => re.includes('(') ? removeGroups(re.replace(/\([^(]*?\)/g,'')) : re  // Removes anything inside `()`; exposes chars at root level only
  const ors = re => /\|/.test(removeGroups(re)) ? '('+re+')' : re  // Wraps in `()` if `|` at root level
  
  for (let i=a.length-1; i; i--) {  // Start with last node, work forward
  
    let self = a[i]
    let loop = self[i] ? (self[i].length>1 ? '('+self[i]+')' : self[i]) + '*' : ''  // Used to form new links below
    let tos = Object.keys(self).filter(k=>k!='id'&&k!=i).map(j=>a[j])  // Find links from self to other nodes
    let froms = a.filter(from => from != self && from[i])  // Find nodes with links to self
    
    froms.forEach(from => {
      tos.forEach(to => {
        let oldLink = a[from.id][to.id]    // Already known
        let newLink = ors(a[from.id][i]) + loop + ors(a[i][to.id])  // Link `from`->`self`; My loop; Link `self`->`to`
        
        a[from.id][to.id] = (oldLink ? oldLink+'|'+newLink : newLink)  // Merge links if old exists
        
      })
      delete a[from.id][i]  // Remove link to node that is about to be removed
    })
    a.splice(-1,1)  // Remove last node 
  }  
  return '^('+a[0][0]+')+$'  // Wrap appropriately
}
___________________________________________________________
const regexDivisibleBy = n => {
  if (n == 1) return '^(0|1)+$'; 
  const {states, arches} = initStatesAndArches(n);
  states.forEach((s, i) => {
    if (i == 0) return;
    reduceState(states, arches, s);
  });
  
  const R = arches[0][0];
  return `^(?:${R})+$`;
}

const initStatesAndArches = n => {
  const states = [];
  for (let i = 0; i < n; i++) {
    states.push({
      index: i,
      preList: [],
      postList: []
    });
  }
  
  const arches = Array(n).fill(0).map(() => Array(n));

  for (let i = 0; i < n; i++) {
    addArch(states, arches, i, i * 2 % n, '0');
    addArch(states, arches, i, (i * 2 + 1) % n, '1');
  }
  
  return {states, arches};
}

const addArch = (states, arches, from, to, str) => {
  if (from != to) {
    states[from].postList.push(to);
    states[to].preList.push(from);
  }
  arches[from][to] = str;
}

const deleteArch = (st, pre, index) => {
  const list = pre ? st.preList : st.postList;
  const i = list.indexOf(index);
  if (i < 0) return;
  list.splice(i, 1);
}

const reduceState = (states, arches, st) => {
  st.preList.forEach((k) => {
    st.postList.forEach((m) => {
      const q = states[k]; 
      const p = states[m];
      const Rkm = arches[k][m];
      const Qk = arches[k][st.index];
      const Pm = arches[st.index][m];
      const S = arches[st.index][st.index];

      const S_ = S ? (S.length > 1 ? `(?:${S})*` : `${S}*`) : E; 
      const str = addExp(Rkm, concatExp(Qk, S_, Pm));
      deleteArch(q, false, p.index);
      deleteArch(p, true, q.index);
      addArch(states, arches, q.index, p.index, str);

      deleteArch(q, false, st.index);
      deleteArch(p, true, st.index);
    });
  });
}

const addExp = (...args) => {
  const notEnotEmpty = args.filter((x) => x && x != E);
  return cleverJoin(notEnotEmpty, '|');
}

const concatExp = (...args) => {
  const notE = args.filter((x) => x != E);
  const hasEmptySet = args.some((x) => !x);
  return hasEmptySet ? '' : cleverJoin(notE, '');
}

const cleverJoin = (exps, sep) => {
  if (exps.length == 1) return exps[0];
  return exps.map((s) => s.indexOf('|') > 0 ? `(?:${s})` : s).join(sep);
}

const E = 'e'; // empty
___________________________________________________________
let START_STATE = 'START_STATE'
let END_STATE = 'END_STATE'

let DFAGenerator = (states, startState, acceptedStates) => {
    let dfa = {}
    dfa.states = states
    dfa.transitions = {}
    addTransition(dfa, START_STATE, startState, '')
    for (let acceptedState of acceptedStates) {
        addTransition(dfa, acceptedState, END_STATE, '')
    }
    return dfa
}

let addTransition = (dfa, from, to, trans) => {
    dfa.transitions[from + '=>' + to] = trans
}

let getTransition = (dfa, from, to) => dfa.transitions[from + '=>' + to]

let selectState = dfa => {
    let fromCount = {}
    let toCount = {}
    for (let key in dfa.transitions) {
        let splitKey = key.split('=>')
        let from = splitKey[0]
        let to = splitKey[1]
        if (from != to) {
            fromCount[from] = fromCount[from] ? fromCount[from] + 1 : 1
            toCount[to] = toCount[to] ? toCount[to] + 1 : 1
        }
    }
    return dfa.states.reduce((a, b) => {
        if (fromCount[a] * toCount[a] < fromCount[b] * toCount[b]) { return a; }
        return b;
    })
}

let reduceState = (dfa, state) => {
    let entering = {}
    let exiting = {}
    let loop = undefined
    for (let key in Object.assign({}, dfa.transitions)) {
        let trans = dfa.transitions[key]
        let splitKey = key.split('=>')
        let from = splitKey[0]
        let to = splitKey[1]
        if (from == to && from == state) {
            loop = trans
        }
        else if (to == state) {
            entering[from] = trans
        }
        else if (from == state) {
            exiting[to] = trans
        }
        if (from == state || to == state) {
            delete dfa.transitions[key]
        }
    }
    
    let loopTrans = typeof(loop) == 'undefined' ? '' : ('(' + loop + ')*')
    for (let enterState in entering) {
        let enterTrans = entering[enterState]
        for (let exitState in exiting) {
            let exitTrans = exiting[exitState]
            let trans = enterTrans + loopTrans + exitTrans
            let existingTrans = getTransition(dfa, enterState, exitState)
            if (existingTrans) {
                trans = '(' + existingTrans + '|' + trans + ')'
            }
            addTransition(dfa, enterState, exitState, trans)
        }
    }
    dfa.states = dfa.states.filter(a => a != state)
}

let reduceDFA = dfa => {
    while (dfa.states.length > 0) {
        let state = selectState(dfa)
        reduceState(dfa, state)
    }
    return getTransition(dfa, START_STATE, END_STATE)
}

function subRegexDivisibleBy(n) {
    if (n == 1) { return '0|1[01]*' }
    let states = [...Array(n+1).keys()].map(a => '' + a)
    let dfa = DFAGenerator(states, n, [0])
    for (let i = 0; i <= n; ++i) {
        addTransition(dfa, '' + i, '' + ((i * 2) % n), '0')
        addTransition(dfa, '' + i, '' + ((i * 2 + 1) % n), '1')
    }
    return reduceDFA(dfa)
}

function regexDivisibleBy(n) {
    let start = '^'
    let end = '$'
    while (n % 2 == 0) {
        end = '0' + end
        n /= 2
    }
    return start + subRegexDivisibleBy(n) + end
}
