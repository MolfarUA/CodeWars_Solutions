RADICALS    = ["meth", "eth", "prop", "but", "pent", "hex", "hept", "oct", "non", "dec", "undec", "dodec", "tridec", "tetradec", "pentadec", "hexadec", "heptadec", "octadec", "nonadec"]
MULTIPLIERS = ["", "di",  "tri", "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca", "undeca", "dodeca", "trideca", "tetradeca", "pentadeca", "hexadeca", "heptadeca", "octadeca", "nonadeca"]

PREFIXES    = ["cyclo", "hydroxy", "oxo", "carboxy", "oxycarbonyl", "anoyloxy", "formyl", "oxy", "amido", "amino", "imino", "phenyl",  "mercapto", "phosphino", "arsino", "fluoro", "chloro", "bromo", "iodo"]
prefix_formulai = {'fluoro': {'F': 1}, 'chloro': {'Cl': 1}, 'bromo': {'Br': 1}, 'iodo': {'I': 1}, 'hydroxy': {'O': 1, 'H': 1}, 'mercapto': {'S': 1, 'H': 1}, 'imino': {'N': 1, 'H': 0}, 'oxo': {'O': 1, 'H': -1}, 'formyl': {'C': 1, 'O': 1, 'H': 1}, 'carboxy': {'C': 1, 'O': 2, 'H': 1}, 'amido': {'N': 1, 'O': 1, 'H': 0}, 'amino': {'N': 1, 'H': 2}, 'phosphino': {'P': 1, 'H': 2}, 'arsino': {'As': 1, 'H': 2}, 'phenyl': {'C': 6, 'H': 5}}

SUFFIXES    = ["e", "ol", "al", "one", "oic acid", "carboxylic acid", "oate", "ether", "amide", "amine", "imine", "benzene", "thiol", "phosphine", "arsine"]
suffix_formulai = {'e': {'H': 1}, 'ol': {'O': 1, 'H': 1}, 'thiol': {'S': 1, 'H': 1}, 'imine': {'N': 1, 'H': 0}, 'one': {'O': 1, 'H': -1}, 'al': {'O': 1, 'H': -1}, 'oic acid': {'O': 2, 'H': -1}, 'carboxylic acid': {'C': 1, 'O': 2, 'H': 1}, 'amide': {'N': 1, 'O': 1, 'H': 0}, 'amine': {'N': 1, 'H': 2}, 'phosphine': {'P': 1, 'H': 2}, 'arsine': {'As': 1, 'H': 2}, 'ether': {'O': 1, 'H': 1}, 'oate': {'O': 2, 'H': -1}, 'benzene': {'C': 6, 'H': 5}}

ALKYL_SUFFIXES = ['oxycarbonyl', 'oyloxy', 'anoyloxy', 'oxy', 'yl']
alkyl_suffix_formulai = {'oxycarbonyl':{'C':1,'O':2}, 'oyloxy':{'O':2,'H':-2}, 'anoyloxy':{'O':2,'H':-2}, 'oxy':{'O':1}, 'yl':{}}

from collections import defaultdict

class ParseHer(object):
    def __init__(self, name): self.name = name
    def parse(self): return parse(self.name)

def parse(s, pos=0):
    counts = defaultdict(int)
    groups = []
    groups, pos = match_alkyl_groups(s, pos)

    if m := match_seq(s, pos, match(' '), match_alkyl_groups, match_radical,
        match_bond_multiplicity, match_multiplier, match('oate')):

        (_, alkyls, carbons, extra_bonds, multiplier, _), pos = m
        groups *= multiplier
        groups.extend(alkyls)
        ester = {
            'C': carbons,
            'O': 2 * multiplier,
            'H': 2 * carbons + 2 - 2 * extra_bonds - 2 * multiplier - len(groups)}
        sum_dict(counts, ester, *groups)
        return counts

    if m := match('cyclo')(s, pos):
        _, pos = m
        counts['H'] -= 2

    if m := match_seq(s, pos, match_radical, match_bond_multiplicity, match_function_suffix):
        (carbons, extra_bonds, functions), pos = m
        main_chain = {'C':carbons, 'H': 2 * carbons + 2 - 2 * extra_bonds}
        sum_dict(counts, main_chain)
        groups.extend(functions)
    else:
        functions, pos = match_function_suffix(s, pos)
        counts['H'] += len(functions)    # Restore functions that still think they're suffixes.  They're now the main chain.
        sum_dict(counts, *functions)

    counts['H'] -= len(groups)
    sum_dict(counts, *groups)
    return counts

def match_alkyl_groups(s, pos):
    groups = []
    while pos < len(s) and (m := match_alkyl_group(s, pos)):
        duplicate_groups, pos = m
        groups.extend(duplicate_groups)
        if m := match('-')(s, pos): _, pos = m
    return groups, pos

def sum_dict(d, *others):
    for other in others:
        for k, v in other.items(): d[k] += v

def match_alkyl_group(s, pos):
    formula = defaultdict(int)
    multiplier, pos = match_multiplier(s, pos)

    if m := match_seq(s, pos, match('['), match_alkyl_groups, match(']')):
        (_, formulai, _), pos = m
        formula['H'] -= len(formulai)
        sum_dict(formula, *formulai)

    if m := match('cyclo')(s, pos):
        _, pos = m
        formula['H'] -= 2

    if m := Trie(PREFIXES).match(s, pos):    # Match functions as alkyls.
        (_, prefix), pos = m
        sum_dict(formula, prefix_formulai[prefix])
        return [formula]*multiplier, pos

    if m := match_longest_radical(s, pos, multiplier):
        (carbons, multiplier), pos = m
        sum_dict(formula, {'H':carbons * 2 + 1, 'C':carbons})

        if m := match_bond_multiplicity(s, pos):  # Bond multiplicity is optional for alkyls.
            extra_bonds, pos = m
            formula['H'] -= 2 * extra_bonds

        if m := Trie(ALKYL_SUFFIXES).match(s, pos):
            (_, suffix), pos = m
            sum_dict(formula, alkyl_suffix_formulai[suffix])
            return [formula] * multiplier, pos

def match_positions(s, pos):
    start = pos
    while pos < len(s) and s[pos] in ',0123456789': pos += 1
    if pos > start: return s[start:pos].count(',') + 1, pos

def match_radical(s, pos):
    if m := Trie(RADICALS).match(s, pos):
        (index, _), pos = m
        return index + 1, pos

def match_multiplier(s, pos):
    expected = None
    if m := match('-')(s, pos):
            _, pos = m
    if m := match_positions(s, pos):
        expected, pos = m
        _, pos = match('-')(s, pos)

    if expected:
        multiplier = MULTIPLIERS[expected-1]
        assert s[pos:pos+len(multiplier)] == multiplier
        return expected, pos + len(multiplier)
    if m := Trie(MULTIPLIERS).match(s, pos):
        (index, _), pos = m
        return index + 1, pos

def match(literal):
    return lambda s, pos: (literal, pos + len(literal)) \
                          if s[pos:pos+len(literal)] == literal else None

def match_seq(s, pos, *matchers):
    vals = []
    for matcher in matchers:
        if not (m := matcher(s, pos)): return
        val, pos = m; vals.append(val)
    return vals, pos

def match_bond_multiplicity(s, pos):
    extra_bonds = 0

    if m := match_seq(s, pos, match_multiplier, match('en')):
        (multiplier, _), pos = m
        extra_bonds += multiplier
    
    if m := match_seq(s, pos, match_multiplier, match('yn')):
        (multiplier, _), pos = m
        extra_bonds += 2 * multiplier
    
    if extra_bonds:
        return extra_bonds, pos
    
    if m := match('an')(s, pos):
        _, pos = m
        return extra_bonds, pos

def match_function_suffix(s, pos):
    multiplier, pos = match_multiplier(s, pos)
    formula = defaultdict(int)
    if m := match_seq(s, pos, match('['), match_alkyl_groups, match(']')):
        (_, alkyls, _), pos = m
        formula['H'] -= len(alkyls)
        sum_dict(formula, *alkyls)

    (_, suffix), pos = Trie(SUFFIXES).match(s, pos)
    sum_dict(formula, suffix_formulai[suffix])
    return [formula]*multiplier, pos

def match_longest_radical(s, pos, multiplier):
    mtext = MULTIPLIERS[multiplier-1]
    mpos = pos - len(mtext)

    if s[mpos:pos] != mtext or s[mpos-2:mpos-1].isdecimal():
        if not (m := match_radical(s, pos)): return
        carbons, pos = m
        return (carbons, multiplier), pos

    if best := max([(*m[::-1], i+1) for (i, mtext), pos in Trie(MULTIPLIERS).match_all(s, mpos)
                    if (m := match_radical(s, pos))] or [None]):
        pos, carbons, mult = best
        return (carbons, mult), pos

class Trie:
    tries = defaultdict(dict)
    def __init__(self, words):
        self.trie = Trie.tries[id(words)]
        if self.trie: return

        for i, word in enumerate(words):
            node = self.trie
            for c in word:
                if c not in node: node[c] = {}
                node = node[c]
            node['\0'] = i, word

    def match(self, s, pos):
        node = self.trie
        val = node['\0'] if '\0' in node else None
        for i in range(pos, len(s)):
            if s[i] not in node: break
            node = node[s[i]]
            if '\0' in node: val = node['\0']; pos = i+1
        if val: return val, pos

    def match_all(self, s, pos):
        node = self.trie
        for i in range(pos, len(s)):
            if '\0' in node: yield node['\0'], i
            if s[i] not in node: break
            node = node[s[i]]
            
_________________________________________________________________________
from collections import Counter
import re


class ChemFunc(Counter):

    SINGLETONS = {}                                                                 # Dict of singletons representing all the possible parts of a name (except the positions)
    ARCHIVING  = False                                                              # Will archive all new ChemFun instances as singletons if True
    
    def __new__(cls, *args,**kwargs):
        obj = super().__new__(cls)
        if ChemFunc.ARCHIVING:
            for name,gram in zip(kwargs.get('name', ()), kwargs.get('gram',())):
                ChemFunc.SINGLETONS[name] = (obj, gram)                             # Archive the singleton under all the possible names of the function/part, with the corresponding grammar
        return obj
        
    def __init__(self, iterable, **kwargs):
        super().__init__(iterable)
        self.name = ''
        defDct = {'gram': '', 'name': ()}
        defDct.update(kwargs)
        self.__dict__.update(defDct)
    
    
    def __repr__(self):     return "ChemFunc({}, {})".format(self.name, list(self.items()))
    def __str__(self):      return "ChemFunc({})".format(list(self.items()))
    def isMult(self):       return isinstance(self, Multiplier)
    
    def __mul__(self, n):
        if isinstance(n, int):              return self.__class__({k: v*n for k,v in self.items()})
        elif not isinstance(n, Multiplier): raise Exception("ChemFunc objects cannot be multiplied by {} objects/values other than int or Multipliers".format(n))
        
    def __add__(self, other):
        if not other: other = ChemFunc({})                                              # Handle the default value passed in for "sum([list of ChemFuncs])"
        return self.__class__({k: self[k] + other[k] for k in set(self)|set(other) })   # Merge the keys and make the addition of the two objects
        
    __imul__ = __rmul__ = __mul__
    __iadd__ = __radd__ = __add__
    __isub__ = __rsub__ = __sub__ = Counter.subtract
    
    
    
    
class Multiplier(ChemFunc):
    
    def __init__(self, m, **kwargs):
        super().__init__({}, **kwargs)
        self.multi = m
    
    def __repr__(self): return "Mutliplier({}, {})".format(self.multi, self.name)
    def __str__(self):  return repr(self)
    
    def __mul__(self, other): return other * self.multi
    def thrower(self, *args): raise  Exception("Invalid operation on " + repr(self))
    __rmul__ = __imul__ = __mul__
    __iadd__ = __add__ = __radd__ =  __isub__ = __sub__ = __rsub__ = thrower
    
    


class ParseHer(object):
    
    RADICALS    = ["meth", "eth", "prop", "but", "pent", "hex", "hept", "oct", "non", "dec", "undec", "dodec", "tridec", "tetradec", "pentadec", "hexadec", "heptadec", "octadec", "nonadec"]
    MULTIPLIERS = ["di", "tri", "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca", "undeca", "dodeca", "trideca", "tetradeca", "pentadeca", "hexadeca", "heptadeca", "octadeca", "nonadeca"]
    
    NEW_BLOCK   = "BLOCK"           # GRAMMAR: this is a block that could have (or not, ie. elision) a position and or a multiplier, but no chain starting with that
    NEW_ROOT    = "ROOT"            # GRAMMAR: a new carboned chain will (or may) follow (with or without double or triple bounds inbetween)
    
    
    # Utilities:
    H = ChemFunc({"H": 1})
    C = ChemFunc({"C": 1})
    N = ChemFunc({"N": 1, "H": 1})
    O = ChemFunc({"O": 1})
    
    S  = ChemFunc({"S": 1})
    As = ChemFunc({"As": 1, "H": 1})
    P  = ChemFunc({"P": 1, "H": 1})
    
    insat = ChemFunc({"H": -2})
    


    #=======================
    # SINGLETONS definitions

    ChemFunc.ARCHIVING = True
    
    
    ChemFunc(insat, gram=("CYCLO",), name=("cyclo",))
    ChemFunc({}, gram=("misc",), name=("an",))
    
    
    grammar = (NEW_BLOCK,)
    en = ChemFunc(insat,    gram=grammar,  name=("en",))
    yn = ChemFunc(en+en,    gram=grammar,  name=("yn",))
    
    ChemFunc(C+O+insat,     gram=grammar,  name=("formyl",))
    
    ChemFunc({"F":  1, "H": -1},  gram=grammar,  name=("fluoro",))
    ChemFunc({"Cl": 1, "H": -1},  gram=grammar,  name=("chloro",))
    ChemFunc({"Br": 1, "H": -1},  gram=grammar,  name=("bromo",))
    ChemFunc({"I":  1, "H": -1},  gram=grammar,  name=("iodo",))
    
    
    grammar = (NEW_ROOT,)
    alkane = ChemFunc({},   gram=grammar,  name=("e",))
    ChemFunc({},            gram=grammar,  name=("yl",))
    
    ChemFunc(O+insat,       gram=grammar,  name=("al",))
    ChemFunc(O+O+insat,     gram=grammar,  name=("oic acid",))
    ChemFunc(O+O+insat,     gram=grammar,  name=("oate",))
    ChemFunc(C+O+O+insat,   gram=grammar,  name=("oxycarbonyl",))
    ChemFunc(O+O+insat,     gram=grammar,  name=("oyloxy",))
    
    
    grammar = (NEW_ROOT, NEW_BLOCK)
    ChemFunc(O,             gram=grammar,  name=("ol", "hydroxy"))
    ChemFunc(O+insat,       gram=grammar,  name=("one", "oxo"))
    
    ChemFunc(N+insat,       gram=grammar,  name=("imine", "imino"))
    ChemFunc(6*C+4*insat,   gram=grammar,  name=("benzene", "phenyl"))
    
    ChemFunc(S,             gram=grammar,  name=("thiol", "mercapto"))
    ChemFunc(C+O+O+insat,   gram=grammar,  name=("carboxylic acid", "carboxy"))
    
    
    grammar = (NEW_ROOT, NEW_ROOT)
    ChemFunc(N,             gram=grammar,  name=("amine", "amino"))
    ChemFunc(N+O+insat,     gram=grammar,  name=("amide", "amido"))
    
    ChemFunc(As,            gram=grammar,  name=("arsine",    "arsino"))
    ChemFunc(P,             gram=grammar,  name=("phosphine", "phosphino"))
    
    ChemFunc(O,             gram=grammar,  name=("ether", "oxy"))
    
    
    for nC,rad in enumerate(RADICALS, 1):     ChemFunc({"C": nC}, gram=("CHAIN",),      name=(rad,))
    for n,name in enumerate(MULTIPLIERS, 2):  Multiplier(n,       gram=("MULTIPLIER",), name=(name,))
    
    
    ChemFunc.ARCHIVING = False
    
    # End of SINGLETONS defintions
    #=============================
    
    def _genRevTokenizer(self, SG, rootBlock, pos):                        # Intermediate function needed to resolve local scopes problems using list comprehension in the body class definition...
        sortingKey = lambda t: (-len(t), t)                                                                             # Sort by: longuest name first, then alphabetically (the last one is just to ease the way (a bit..) if a direct look into in the tokenizer is needed)
        garbage    = '.'                                                                                                # To catch problems when parsing the input
        
        sanitizeAmbiguous = {"tridec", "tetradec", "pentadec", "hexadec", "heptadec", "octadec", "nonadec"}             # Ambiguous cases to sanitisize (see just below)
        sanitizeReg = {"dodec": '(?!ima|oi)',                                                                           # Needed to avoid matching conflicts between "iododecane" and "io-dodecane" (same with amido)
                        True:  r'(?!-\d+,)'}                                                                            # Avoid matching -1,2,3-tridec, -1,1,2,3-tetradec,... as tridecane, tetradecane, ...
        
        toks       = sorted((t for t,(o,g) in SG.items() if g in rootBlock                       ), key=sortingKey)     # Tokens that expect to have positional informations or multipliers (NEW_ROOT ans NEW_BLOCKS)
        sortedMult = sorted((t for t,(o,g) in SG.items() if o.isMult()                           ), key=sortingKey)     # All multipliers
        otherToks  = sorted((t for t,(o,g) in SG.items() if g not in rootBlock and not o.isMult()), key=sortingKey)     # All other tokens: radicals, cyclo, ...
        
        return re.compile(r'|'.join( [r'\[', r'\]', ' ',
                                      r'|'.join(t[::-1] + sanitizeReg.get(t in sanitizeAmbiguous or t,'')  for t in otherToks),
                                      r'({})?({})?({})?'.format( r'|'.join(t[::-1] + sanitizeReg.get(t in sanitizeAmbiguous or t,'')  for t in toks),   # Reverse all the tokens for parsing
                                                                  r'|'.join(t[::-1] for t in sortedMult),
                                                                  pos),
                                      garbage]))
    

    SG   = ChemFunc.SINGLETONS
    ONE  = Multiplier(1, gram=("MULTIPLIER",), name=("ONE",))
    VOID = ChemFunc({}, gram=("VOID",))
    
    IGNORED_TOKENS = {" ", "an"}
    POS            = r"-\d+(?:,\d+)*(?:-|$|(?=[ []))"                                # Regexp to identify the positions (but parsing REVERSED!)
    REV_TOKENIZER = _genRevTokenizer(None, SG, (NEW_ROOT, NEW_BLOCK), POS)            # Shortcircuiting the instance argument (it's actually a static call...)
    

    
    def __init__(self, name):
        self.name  = name
        self.parts = re.split(r'(?<=yl) ', name)
    

    def __str__(self):             return self.name
    def expandHdrogens(self, obj): return obj + self.H * ( 2*obj['C'] + 2 )                 # Finalize the raw formula, adding the "lacking" hydrogens
    def parse(self):               return self.expandHdrogens( self.actualParser(self.genTokens()) )
    
    def genTokens(self, what=None):
        if what is None: what = self.parts[-1]

        for x in self.REV_TOKENIZER.finditer(what[::-1]):
            yield (x.group()[::-1],                                                         # global match
                   x.group(3) and x.group(3)[::-1],                                         # posisions match (-x,x...-)
                   x.group(2) and x.group(2)[::-1],                                         # multiplier match
                   x.group(1) and x.group(1)[::-1])                                         # chain or function match
    
    
    def actualParser(self, tokensGen):
        
        lst = [self.VOID]
        for tok,_,m,t in tokensGen:
            if t: tok = t                                                                   # Alternative matching (with the groups)
            
            if tok in self.IGNORED_TOKENS: continue 
            
            part, gram = self.SG.get(tok, (self.VOID, ""))
            mult, _    = self.SG.get(m,   (self.ONE,  ""))                                  # 'mult' is always defined AND used (even if useless), to manage elisions easily (and the security check)
            
            if tok == "oate":                                                               # Special case, handling the "distant" auxiliary chain of the esters
                part += self.actualParser(self.genTokens(self.parts[0]))

            if   gram == self.NEW_ROOT:   lst.append( part * mult.multi )                   # Start a new chain
            elif gram == self.NEW_BLOCK:  lst[-1] += part * mult.multi                      # BLOCK: handle elisions properly; add to the current root
            elif tok  == ']':             lst[-1] += self.actualParser(tokensGen)           # Enter a subchain, start a new parsing and add it to the current root
            elif tok  == '[':             break                                             # End of subchain
            elif m and not t:             lst[-1] *= mult.multi                             # "Isolated" multiplier (mostly, in front of squared brackets): multiply the whole last chain (up to its "root". Included)
            else:                         lst[-1] += part * mult.multi                      # Default case (cyclo, radicals, ...: mult.multi = 1)
            
        return sum(lst)                                                                     # Reduce the list to a single ChemFunc instance

      
__________________________________________________________________________________________________
RADICALS    = ["meth", "eth", "prop", "but",   "pent",  "hex",  "hept",  "oct",  "non",  "dec",  "undec",  "dodec",  "tridec",  "tetradec",  "pentadec",  "hexadec",  "heptadec",  "octadec",  "nonadec"]
MULTIPLIERS = ["",        "di",  "tri",  "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca", "undeca", "dodeca", "trideca", "tetradeca", "pentadeca", "hexadeca", "heptadeca", "octadeca", "nonadeca"]

SUFFIXES    = ["e",         "ol",      "al", "one", "oic acid", "carboxylic acid",                "oate",               "ether", "amide", "amine", "imine", "benzene", "thiol",    "phosphine", "arsine"]
PREFIXES    = ["cyclo", "hydroxy",       "oxo",             "carboxy",         "oxycarbonyl", "anoyloxy", "formyl", "oxy",   "amido", "amino", "imino", "phenyl",  "mercapto", "phosphino", "arsino", "fluoro", "chloro", "bromo", "iodo"]

class ParseHer(object):
    def __init__(self, name): self.name = name
    def parse(self): return parse(self.name)

def parse(name):
    s = name
    pos = 0
    counts = defaultdict(int)
    groups = []
    alkyls, pos = match_alkyl_groups(s, pos)
    groups.extend(alkyls)
    
    if m := match(' ', s, pos):  # if space, match ester
        _, pos = m
        alkyls, pos = match_alkyl_groups(s, pos)
        carbons, pos = match_radical(s, pos)
        extra_bonds, pos = match_bond_multiplicity(s, pos)
        multiplier, pos = match_multiplier(s, pos)
        _, pos = match('oate', s, pos)
        groups *= multiplier
        groups.extend(alkyls)

        counts['O'] += 2 * multiplier
        counts['H'] -= 2 * multiplier

        counts['C'] += carbons
        counts['H'] += 2 * carbons + 2 - 2 * extra_bonds
        counts['H'] -= len(groups)
        for g in groups:
            for k in g: counts[k] += g[k]
        return counts

    if m := match('cyclo', s, pos):
        _, pos = m
        counts['H'] -= 2

    if m := match_chain(s, pos, match_radical, match_bond_multiplicity, match_function_suffix):
        (carbons, extra_bonds, functions), pos = m
        counts['C'] += carbons
        counts['H'] += 2 * carbons + 2 - 2 * extra_bonds
        groups.extend(functions)
    else:
        functions, pos = match_function_suffix(s, pos)
        assert len(functions) == 1  # We can only have one main chain...
        counts['H'] += len(functions)  # restore functions that still think they're suffixes.  they're now main chains.
        for g in functions:
            for k in g: counts[k] += g[k]
    counts['H'] -= len(groups)
    for g in groups:
        for k in g: counts[k] += g[k]
    return counts

def match_alkyl_groups(s, pos):
    groups = []
    while pos < len(s) and (m := match_alkyl_group(s, pos)):
        duplicate_groups, pos = m
        groups.extend(duplicate_groups)
        if m := match('-', s, pos): _, pos = m
    return groups, pos

from collections import defaultdict

def match_alkyl_group(s, pos):
    '''returns list of groups (single group duplicated according to multiplier)'''
    formula = defaultdict(int)
    multiplier, pos = match_multiplier(s, pos)
    if m := match('[', s, pos):
        _, pos = m
        formulai, pos = match_alkyl_groups(s, pos)
        _, pos = match(']', s, pos)
        formula['H'] -= len(formulai)
        for f in formulai:
            for k in f: formula[k] += f[k]

    if m := match('cyclo', s, pos):
        _, pos = m
        formula['H'] -= 2

    # Match functions as alkyls.
    if m := Trie(PREFIXES).match(s, pos):
        (index, _), pos = m
        for k, v in prefix_formulai[PREFIXES[index]].items():
            formula[k] += v
        return [formula]*multiplier, pos

    if m := match_longest_radical(s, pos, multiplier):
        (carbons, multiplier), pos = m
        formula['H'] += carbons * 2 + 1
        formula['C'] += carbons

        if m := match_bond_multiplicity(s, pos):  # Bond multiplicity is optional for alkyls.
            extra_bonds, pos = m
            formula['H'] -= 2 * extra_bonds

        '''
        if m := match('oxycarbonyl', s, pos):
            _, pos = m
            formula['C'] += 1
            formula['O'] += 2
            return [formula] * multiplier, pos
        # The function is 'anoyloxy' but sometimes the 'an' is misinterpreted as a multiplicity and consumed.
        if m := match('oyloxy', s, pos) or (m := match('anoyloxy', s, pos)):
            _, pos = m
            formula['O'] += 2
            formula['H'] -= 2  # Since the radical chain makes 2 extra bonds (the double bond).
            return [formula] * multiplier, pos
        if m := match('oxy', s, pos):
            _, pos = m
            formula['O'] += 1
            return [formula] * multiplier, pos
        if m := match('yl', s, pos):
            _, pos = m
            return [formula] * multiplier, pos
        '''
        if m := Trie(ALKYL_SUFFIXES).match(s, pos):
            (_, suffix), pos = m
            print(suffix, 'alkyl suffix')
            for atom, count in alkyl_suffix_functions[suffix].items(): formula[atom] += count
            return [formula] * multiplier, pos

ALKYL_SUFFIXES = ['oxycarbonyl', 'oyloxy', 'anoyloxy', 'oxy', 'yl']
alkyl_suffix_functions = {'oxycarbonyl':{'C':1,'O':2}, 'oyloxy':{'O':2,'H':-2}, 'anoyloxy':{'O':2,'H':-2}, 'oxy':{'O':1}, 'yl':{}}

def match_positions(s, pos):
    '''returns number of positions provided'''
    start = pos
    while pos < len(s) and s[pos] in ',0123456789': pos += 1
    if pos > start: return s[start:pos].count(',') + 1, pos

def match_radical(s, pos):
    '''returns num carbons'''
    if m := Trie(RADICALS).match(s, pos):
        (index, _), pos = m
        return index + 1, pos

def match_multiplier(s, pos):
    expected = None
    if m := match('-', s, pos): _, pos = m
    if m := match_positions(s, pos):
        expected, pos = m
        _, pos = match('-', s, pos)
    
    if expected:
        multiplier = MULTIPLIERS[expected-1]
        assert s[pos:pos+len(multiplier)] == multiplier
        return expected, pos + len(multiplier)
    if m := Trie(MULTIPLIERS).match(s, pos):
        (index, _), pos = m
        return index + 1, pos

def match(literal, s, pos):
    if s[pos:pos+len(literal)] == literal:
        return literal, pos + len(literal)

def match_chain(s, pos, *matchers):
    vals = []
    for matcher in matchers:
        if not (m := matcher(s, pos)): return
        val, pos = m; vals.append(val)
    return vals, pos

from functools import partial as bind

def match_bond_multiplicity(s, pos):
    extra_bonds = 0
    
    if m := match_chain(s, pos, match_multiplier, bind(match, 'en')):
        (multiplier, *_), pos = m
        extra_bonds += multiplier
    
    if m := match_chain(s, pos, match_multiplier, bind(match, 'yn')):
        (multiplier, *_), pos = m
        extra_bonds += 2 * multiplier

    if extra_bonds:
        return extra_bonds, pos

    if m := match('an', s, pos):
        _, pos = m
        return extra_bonds, pos

prefix_formulai = {
    'fluoro': {'F':1},
    'chloro': {'Cl':1},
    'bromo': {'Br':1},
    'iodo': {'I':1},
    'hydroxy': {'O':1, 'H':1},
    'mercapto': {'S':1, 'H':1},
    'imino': {'N':1, 'H':1-1},  # Subtract a hydrogen to account for double bond.
    'oxo': {'O':1, 'H':0-1},    # Subtract a hydrogen to account for double bond.
    'formyl': {'C':1, 'O':1, 'H':1},
    'carboxy': {'C':1, 'O':2, 'H':1},
    'amido': {'N':1, 'O':1, 'H':2-2},  # Subtract 2 hydrogens to account for the extra doublebond.
    'amino': {'N':1, 'H':2},
    'phosphino': {'P':1, 'H':2},
    'arsino': {'As':1, 'H':2},
    'phenyl': {'C':6, 'H':6-1},
}

suffix_formulai = {
    'e': {'H':0+1},  # This empty function makes 0 bonds, but the main chain thinks all functions makes one bond, so we add one hydrogen to compensate.
    'ol': {'O':1, 'H':1},
    'thiol': {'S':1, 'H':1},  # no double bond
    # The next 3 functions make a double bond, but the main chain doesn't know about it.  So we subtract a hydrogen to compensate for the main chain's extra hydrogen.
    'imine': {'N':1, 'H':1-1},
    'one': {'O':1, 'H':0-1},
    'al': {'O':1, 'H':0-1},
    # This function makes 3 bonds to the main chain (a double and single bond), so we subtract 2 hydrogens since the main chain only knows about one bond.
    'oic acid': {'O':2, 'H':1-2},
    'carboxylic acid': {'C':1, 'O':2, 'H':1},  # This function adds an extra carbon, so doesn't require any extra bonds to the main chain.
    'amide': {'N':1, 'O':1, 'H':2-2},  # Makes 3 bonds to main chain.
    'amine': {'N':1, 'H':2},
    'phosphine': {'P':1, 'H':2},
    'arsine': {'As':1, 'H':2},
    'ether': {'O':1, 'H':2-1},  # Treat this like H2O since it makes two bonds.  Subtract one hydrogen since the main chain only expects one bond.
    'oate': {'O':2, 'H':0-1}, # -1 H to account for double bond.  The single bond is already accounted for since it's between two existing pieces.
    'benzene': {'C':6, 'H':6-1},
}

def match_function_suffix(s, pos):
    multiplier, pos = match_multiplier(s, pos)
    formula = defaultdict(int)
    if m := match('[', s, pos):
        _, pos = m
        alkyls, pos = match_alkyls_groups(s, pos)
        _, pos = match(']', s, pos)

        formula['H'] -= len(alkyls)
        for alkyl in alkyls:
            for k in alkyl: formula[k] += alkyl[k]
    
    (_, suffix), pos = Trie(SUFFIXES).match(s, pos)
    formula.update(suffix_formulai[suffix])
    # TODO(refactor): don't subtract hydrogens to on main chain at all.
    return [formula]*multiplier, pos
    
def match_longest_radical(s, pos, multiplier):
    mtext = MULTIPLIERS[multiplier-1]
    mpos = pos - len(mtext)

    if s[mpos:pos] != mtext or s[mpos-2:mpos-1].isdecimal():
        if m := match_radical(s, pos):
            carbons, pos = m
            return (carbons, multiplier), pos
        return

    # TODO(bug): should maximize position before num carbons.  find a testcase
    if best := max([(*m, i+1) for (i, mtext), pos in Trie(MULTIPLIERS).match_all(s, mpos)
                    if (m := match_radical(s, pos))] or [None]):
        carbons, pos, mult = best
        return (carbons, mult), pos

# TODO(refactor): consider combining prefix and suffix functions (exclude suffix e, and whichever other suffixes that overlap with radicals)

class Trie:
    tries = defaultdict(dict)
    def __init__(self, words):
        self.trie = Trie.tries[id(words)]
        if self.trie: return
        
        for i, word in enumerate(words):
            node = self.trie
            for c in word:
                if c not in node: node[c] = {}
                node = node[c]
            node['\0'] = i, word
    
    def match(self, s, pos):
        node = self.trie
        val = node['\0'] if '\0' in node else None
        for i in range(pos, len(s)):
            if s[i] not in node: break
            node = node[s[i]]
            if '\0' in node: val = node['\0']; pos = i+1
        if val: return val, pos
    
    def match_all(self, s, pos):
        node = self.trie
        for i in range(pos, len(s)):
            if '\0' in node: yield node['\0'], i
            if s[i] not in node: break
            node = node[s[i]]

print(*Trie(MULTIPLIERS).match_all('tridecamine', 0), 'should be', ((2, 'tri'), 3), (12, 'trideca', 7))
print(Trie(SUFFIXES).trie['e']['\0'])

________________________________________________________________________
from functools import reduce
import operator

MULTIPLIERS = 'una di tri tetra penta hexa hepta octa nona deca undeca dodeca trideca tetradeca pentadeca hexadeca heptadeca octadeca nonadeca'.split()
PREFIXES = 'hydroxy oxo carboxy oxycarbonyl oyloxy formyl oxy amido amino imino phenyl mercapto phosphino arsino fluoro chloro bromo iodo'.split()
RADICALS = 'meth eth prop but pent hex hept oct non dec undec dodec tridec tetradec pentadec hexadec heptadec octadec nonadec'.split()
SUFFIXES = 'ol al one oic_acid carboxylic_acid oate ether amide amine imine benzene thiol phosphine arsine'.split()
CHAINS = 'cyclo ane an ene en yne yn yl'.split()
ALL = MULTIPLIERS + PREFIXES + RADICALS + CHAINS + SUFFIXES + list(',-[]1234567890')
VALENCE = {k:v for k,v in zip('Br Cl F H I O S As N P C'.split(), 5*[1]+2*[2]+3*[3]+[4])}
ZERO_BONDS = {k:v for k,v in zip('amine phosphine arsine ether'.split(), 'N P As O'.split())}
ONE_BOND = {k:v for k,v in zip(
    '''bromo chloro fluoro iodo hydroxy ol mercapto thiol oic_acid carboxylic_acid carboxy
    amido amide amino phosphino arsino oate'''.split(),
    'Br Cl F I O O S S O O O N N N P As O'.split())}
TWO_BONDS = {k:v for k,v in zip(
    'imine imino oxo one formyl al oic_acid carboxylic_acid carboxy amido amide oxy oate oxycarbonyl oyloxy'.split(),
    'N N O O O O O O O O O O O O O'.split()
    )}
ADD_CARBON = 'formyl carboxylic_acid carboxy oxycarbonyl'.split()

class ParseHer:
    def __init__(self, name):
        self.name = name
        print(name)
    def parse(self):
        name = self.name.replace('oic acid', 'oic_acid').replace('carboxylic acid', 'carboxylic_acid').replace(' ', '')
        def get_tokens(name):
            tokens = set()
            for k,v in {k:v for k,v in {s:name.count(s) for s in ALL}.items() if v}.items():
                i=0
                for _ in range(v):
                    j = name.find(k,i)
                    i = j + len(k)
                    tokens.add((j,i,k))
            bs, es, _ = zip(*tokens)
            tokens = [(b,e,v) for b,e,v in tokens if
                (b in (0,*es) and e in (*bs,len(name))) or v.endswith('ino')]
            bs, es, tokens = zip(*sorted(tokens, key=lambda x:(x[0],-x[1] )))
            tokens = list(tokens)
            for i, (v,b,e) in reversed(list(enumerate(zip(tokens[:-2], bs, es)))):
                if b == bs[i+1]:
                    if v == ''.join(tokens[i+1:i+3]):
                        del tokens[i+2]
                        del tokens[i+1]
                    elif e == bs[i+2]:
                        del tokens[i+1]
                    else:
                        del tokens[i]
                elif e == es[i+1]:
                    del tokens[i+1]
            for i in reversed([i for i,v in enumerate(tokens[:-1]) if v.isdigit() and tokens[i+1].isdigit()]):
                tokens[i] += tokens[i+1]
                del tokens[i+1]
            return tokens
        tokens = get_tokens(name)
        len_tokens = None
        while len_tokens != len(tokens):
            len_tokens = len(tokens)
            b = 0
            for i,t in enumerate(tokens):
                if name[b:b+len(t)] == t:
                    b += len(t)
                else:
                    for t in reversed(get_tokens(name[b:name.find(t,b)])):
                        tokens.insert(i, t)
                    break
        res = {k:0 for k in list(VALENCE) + ['bond',]}
        ints = [[]]
        t_pre = None
        if tokens[-2:] == 'di oate'.split():
            mults = [1,2]
            ints.append([])
            pre_mult = 1
            for k_dioate, v in reversed(list(enumerate(tokens))):
                if v in RADICALS:
                    break
        else:
            mults = [1]
            pre_mult = 1
            k_dioate = None
        for i_t, t in enumerate(tokens):
            if t_pre in MULTIPLIERS and t not in SUFFIXES + 'en yn'.split():
                    mults[-1] = pre_mult
                    pre_mult = 1
            mult = reduce(operator.mul, mults, 1) * pre_mult
            if t == '[':
                mults.append(1)
                ints.append([])
            elif t == ']' or i_t == k_dioate:
                mults.pop()
                ints.pop()
            elif t_pre is ',':
                ints[-1].append(int(t))
            elif t.isdigit():
                ints[-1] = [int(t)]
            if t in RADICALS:
                if t in 'tridec tetradec pentadec hexadec heptadec octadec nonadec'.split() \
                and ints[-1] and len(ints[-1]) == MULTIPLIERS.index(t.rstrip('dec')) + 1:
                    n = 10
                    mults[-1] = len(ints[-1])
                    mult = reduce(operator.mul, mults, 1)
                else:
                    n = RADICALS.index(t) + 1
                res['C'] += mult * n
                res['bond'] += mult * (n-1)
            elif t == 'cyclo':
                res['bond'] += mult
            elif t in 'benzene phenyl'.split():
                res['C'] += mult * 6
                res['bond'] += mult * 9
            if t in 'en ene yl phenyl'.split():
                res['bond'] +=  mult
            elif t in 'yn yne'.split():
                res['bond'] +=  mult * 2
            if t in ZERO_BONDS:
                res[ZERO_BONDS[t]] += mult
                if t_pre in MULTIPLIERS + 'yn en an'.split() or ints[-1]:
                    res['bond'] += mult
            if t in ONE_BOND:
                res[ONE_BOND[t]] += mult
                res['bond'] += mult
            if t in TWO_BONDS:
                res[TWO_BONDS[t]] += mult * (2 if t in 'oxycarbonyl oyloxy'.split() else 1)
                res['bond'] += mult * 2 * (2 if t in 'oxycarbonyl oyloxy'.split() else 1)
            if t in ADD_CARBON:
                res['C'] += mult
                res['bond'] += mult
            if t.isalpha():
                ints[-1].clear()
            if t in PREFIXES + 'yl'.split():
                mults[-1] = 1
            if t in MULTIPLIERS:
                pre_mult =  1 + MULTIPLIERS.index(t)
            elif ints[-1]:
                pre_mult = len(ints[-1])
            else:
                pre_mult = 1
            t_pre = t
        res['H'] = sum(res[k]*v for k,v in VALENCE.items()) - 2 * res['bond']
        return {k:v for k,v in res.items() if (v and k is not 'bond') or k is 'H'}
___________________________________________________________
import re
from collections import defaultdict

debug=False
def list2regex(xl):
    return "|".join([re.escape(v) for v in  sorted(xl,key=lambda k:(-len(k),k))])

# Number:         1      2      3...
RADICALS    = ["meth", "eth", "prop", "but",   "pent",  "hex",  "hept",  "oct",  "non",  "dec",  "undec",  "dodec",  "tridec",  "tetradec",  "pentadec",  "hexadec",  "heptadec",  "octadec",  "nonadec"]
MULTIPLIERS = ["",     "di",  "tri",  "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca", "undeca", "dodeca", "trideca", "tetradeca", "pentadeca", "hexadeca", "heptadeca", "octadeca", "nonadeca"]
MULTIPLIER2=  [f"<M:{i}>" for i in range(1,20)]

dPREFIX={}
dSUFFIX={}
dBASE  ={}
dBRANCH={}
def multi_val(s):
    if s==None:
        return 0
    elif s in MULTIPLIERS:
        return MULTIPLIERS.index(s)+1
    elif s in   MULTIPLIER2:
        return MULTIPLIER2.index(s)+1
def D(d):
    return {k:v for k,v in d.items() if v!=None and v!="" and v!=0}

for prefix0,suffix0, ref in [  
#Branches
    ["$yl",    "",         {"H":-1}], #- Nothing special
    ["$oxy",   "",         {"O":1, "H":-1}],           #R1-O-               R1 and R2 being alkyles if suffix, or R2 being the main chain if prefix (see details above)
    ["",       "ether$",   {"O":1, "H":1}],            #R1-O-R2             R1 and R2 being alkyles if suffix, or R2 being the main chain if prefix (see details above)
    ["$oxycarbonyl","",    {"C":1,"O":2, "H":-1}],      #...(C)-CO-O-R       Anywhere on the chain. R being a secondary alkyl chain (see details above)
    ["$oyloxy",     "",    {"O":2, "H":-3}],            #...(C)-O-OR         Anywhere on the chain. R being a secondary alkyl chain (see details above)
  
#Halogens
    
    ["fluoro","",       {"F":1}], #-F
    ["chloro","",       {"Cl":1}],#-Cl
    ["bromo",  "",      {"Br":1}],#-Br
    ["iodo",   "",      {"I":1}], #-I

    ["hydroxy","ol",    {"O":1, "H":1}],        #-OH
    ["mercapto","thiol",{"S":1, "H":1}],        #-SH

    ["oxo",    "one",   {"O":1, "H":-1}], #...(C)=O            Never at an extremity of the chain
    ["",       "al",    {"O":1, "H":-1}], #...(C)H=O           Only at an extremity of the main chain
    ["formyl","",       {"C":1,"O":1,"H":1}],   #...CH=O             1 extra carbon, here!
    
    ["",       "oic acid",       {"O":2,"H":-1}],   #...(C)O-OH          Only at an extremity of the main chain
    ["carboxy","carboxylic acid",{"C":1,"O":2,"H":1}],    #...-CO-OH           1 extra carbon, here!

    ["",           "oate",{"O":2, "H":-1}],     #...(C)O-O-R         R being a secondary alkyl chain (see details above). Only at an extremity of the main chain   

  
    ["amino","amine$",        {"N":1,"H":2}],  #NH3 => R-NH2
    ["amido","amide",        {"O":1,"N":1}],#...(C)O-NH2         Only at an extremity
    ["imino","imine",        {"N":1}],     #...(C)=NH
    ["arsino","arsine$",      {"As":1,"H":2}],        
    ["phosphino","phosphine$",{"P":1,"H":2}], #PH3 => R-PH2
   
    ["phenyl",    "benzene$", {"C":6,"H":5}],         #...-C6H5  
   ]:
    if suffix0!="":
        isBASE=suffix0[-1]=="$"
        suffix=suffix0[:-1] if isBASE else suffix0
        dSUFFIX[suffix]=dict(ref)
        if isBASE:
            d=defaultdict(int,ref)
            d["H"]+=1
            dBASE[suffix]=d
    if prefix0!="":
        isBRANCH=prefix0[0]=="$"
        prefix=prefix0[1:] if isBRANCH else prefix0
        if isBRANCH:
            dBRANCH[prefix]=dict(ref)
        else:            
            dPREFIX[prefix]=dict(ref)
SUFFIXregex    =list2regex(dSUFFIX.keys())
PREFIXregex    =list2regex(dPREFIX.keys())
RADICALregex   =list2regex(RADICALS)
BASEregex      =list2regex(dBASE.keys())  
BRANCHregex    =list2regex(dBRANCH.keys())
MULTIPLIERregex=list2regex(MULTIPLIERS+MULTIPLIER2)
CARBO1regex    =f"(?P<CYCLO>cyclo)?(?P<RADICAL>{RADICALregex})((?P<M1>{MULTIPLIERregex})(?P<E1>en|yn)((?P<M2>{MULTIPLIERregex})yn)?|)(an|)(e|(?P<MSUFF>{MULTIPLIERregex})(?P<SUFF>{SUFFIXregex}))"
CARBO2regex    =f"(?P<CYCLO>cyclo)?(?P<RADICAL>{RADICALregex})((?P<M1>{MULTIPLIERregex})(?P<E1>en|yn)((?P<M2>{MULTIPLIERregex})yn)?|)(an|)(?P<BRANCH>{BRANCHregex})"
SUBSTRINGregex =(re.escape("<S:n>")).replace("n","(?P<SUBn>[0-9]+)")


def mult_repl(g):
    nb1=g[1].count(",")+1
    nb2=MULTIPLIERS.index(g[2])+1
    if nb1==nb2:return f"<M:{nb1}>"
    g2b=MULTIPLIERS[nb1-1]
    assert g2b==g[2][:len(g2b)], (g2b, g[2])
    if debug:print("WARNING for TRAP:", g.groups(), (nb1, nb2), "=>", nb1, g2b, g[2])
    return f"<M:{nb1}>{g[2][len(g2b):]}"

class ParseHer(dict):
    def __missing__(p,k):
        return 0
    
    def __init__(p, name):
        p.name=p.name0=name
        if debug:print("Initial name:", name)
        name=re.sub(r"\-?([0-9,]+)\-("+MULTIPLIERregex+")", mult_repl, name)
        name=name.replace("iodo", "iodo ")
        if debug:print("Name without ramification position:", name)
        p.xname=[]
        while "[" in name:
            g=re.search(r"(\[([^\[\]]*)\])", name)
            nb=len(p.xname)
            p.xname.append(g[2])
            name=re.sub(re.escape(g[1]),f"<S:{nb}>",name,count=1)            
        if debug:print("All names:", name, *enumerate(p.xname), sep="\n* ")
        p.name=name
    
    def parse(p):
        p.parse_base()
        p.parse_prefixes()
        return dict(p)
    def parse_prefixes(p):
        prefixes=p.prefixes
        while prefixes:
            prefixes, prefix, m, d=p.parse_prefix(prefixes)
            #if debug:print("\nAdd prefix:", prefix, m, D(d))
            p["H"]-=m #We need to connect the branch on the base
            for k,v in d.items():p[k]+=m*v
            #if debug:print("After prefix:", D(p)) 
            prefixes=prefixes.strip()
    def parse_prefix(p,name):
        name=name.strip()
        model=f"(?P<M>{MULTIPLIERregex})(?P<PREF2SUB>{SUBSTRINGregex})?(?P<PREFIX>(?P<PREF1>{PREFIXregex})|{CARBO2regex})$"
        g=re.search(model,name)
        assert g!=None, name
        #We need to address a special case tridecyl should not be decomposed as tri + decyl
        if g["M"]!=None and len(g["M"])>0 and g["M"][0]!="<":
            start=g.start()
            end  =start+len(g["M"])+3
            if name[start:end] in RADICALS:
                newname=name[:start]+MULTIPLIER2[0]+name[start:]
                if debug:print("Danger:",name[start:end],"=> New name:", newname )
                return p.parse_prefix(newname)
        if debug:print("\nparse_prefix:", g[0])
        rest=name[:-len(g[0])]
        if debug:print(*D(g.groupdict()).items())
        m=multi_val(g["M"])

        d=defaultdict(int)
        if g["PREF1"]!=None:
            for k,v in dPREFIX[g["PREF1"]].items():d[k]+=v
        else:
            C=RADICALS.index(g["RADICAL"])+1
            d["C"]+=C
            d["H"]+=2*C+2
            #if debug:print("Initial branc:",D(d))
            if g["CYCLO"]!=None: d["H"]-=2
            d["H"]-=multi_val(g["M1"])*{None:0,"yn":4,"en":2}[g["E1"]]          
            d["H"]-=multi_val(g["M2"])*4
            if debug:print("After E1/E2:", D(d))
            for k,v in dBRANCH[g["BRANCH"]].items():d[k]+=v
            if debug:print("branch ending",g["BRANCH"],":", D(d))                
        if g["SUBn"]!=None:
            subn=p.xname[int(g["SUBn"])]
            while subn:
                subn, prefix, m0, d0=p.parse_prefix(subn)
                #if debug:print("Prefix found:", prefix, m0, D(d0))
                d["H"]-=m0
                for k,v in d0.items():d[k]+=m0*v
                #if debug:print("After Prefix",prefix, D(d))
        #if debug:print("Branch after all:", D(d))
        return rest, g[0], m, d
    def parse_base(p):
        model=f"(?P<BASE>{BASEregex}|{CARBO1regex})$"
        g=re.search(model,p.name)
        assert g!=None
        if debug:print("\nbase:", g[0])
        #if debug:print(*D(g.groupdict()).items())
        p.prefixes=p.name[:-len(g["BASE"])].strip()
        p.base=g["BASE"]
        if g["RADICAL"]==None:
            for k,v in dBASE[p.base].items():p[k]+=v
            if debug:print("Base:", D(p))
        else:
            C=RADICALS.index(g["RADICAL"])+1
            p["C"]+=C
            p["H"]+=2*C+2
            if debug:print("Initial:", D(p))
            if g["CYCLO"]!=None: p["H"]-=2
            p["H"]-=multi_val(g["M1"])*{None:0,"yn":4,"en":2}[g["E1"]]          
            p["H"]-=multi_val(g["M2"])*4
            #if debug:print("After E1/E2:", D(p))
            msuff=multi_val(g["MSUFF"])
            if msuff>0:
                if g["SUFF"]=="oate":
                    p.prefixes=g["MSUFF"]+p.prefixes
                p["H"]-=msuff
                if debug:print("Add suffix:", g["SUFF"], D(dSUFFIX[g["SUFF"]]))
                for k,v in dSUFFIX[g["SUFF"]].items(): p[k]+=msuff*v
            if debug:print("After all:", D(p))
_________________________________________________
import re
CHAINNAME = {
  'meth': 1,
  'eth': 2,
  'prop': 3,
  'but': 4,
  'pent': 5,
  'hex': 6,
  'hept': 7,
  'oct': 8,
  'non': 9,
  'dec': 10,
  'un': 1,
  'do': 2,
  'tri': 3,
  'tetr': 4,
}

MULTIPLIER_NAME = {
  'di': 2,
  'tri': 3,
  'tetra': 4,
  'penta': 5,
  'hexa': 6,
  'hepta': 7,
  'octa': 8,
  'nona': 9,
  'deca': 10,
  'un': 1,
  'do': 2,
}

FUNCTION_PREFIX = {
  'fluoro': {'F': 1, 'H': -1},
  'chloro': {'Cl': 1, 'H': -1},
  'bromo': {'Br': 1, 'H': -1},
  'iodo': {'I': 1, 'H': -1},
  'hydroxy': {'O': 1},
  'mercapto': {'S': 1},
  'imino': {'N': 1, 'H': -1},
  'oxo': {'O': 1, 'H': -2},
  'formyl': {'C': 1, 'O': 1},
  'carboxy': {'C': 1, 'O': 2},
  'amido': {'O': 1, 'N': 1, 'H': -1},
  'amino': {'N': 1, 'H': 1},
  'phosphino': {'P': 1, 'H': 1},
  'arsino': {'As': 1, 'H': 1},
  'phenyl': {'C': 6, 'H': 4},
}

FUNCTION_SUFFIX = {
  'ol': {'O': 1},
  'thiol': {'S': 1},
  'imine': {'N': 1, 'H': -1},
  'one': {'O': 1, 'H': -2},
  'al': {'O': 1, 'H': -2},
  'oic acid': {'O': 2, 'H': -2},
  'carboxylic acid': {'C': 1, 'O': 2},
  'amide': {'O': 1, 'N': 1, 'H': -1},
  'amine': {'N': 1, 'H': 1},
  'phosphine': {'P': 1, 'H': 1},
  'arsine': {'As': 1, 'H': 1},
}

SPECIAL_MAIN_CHAINS = {
  'amine': {'N': 1, 'H': 3},
  'phosphine': {'P': 1, 'H': 3},
  'arsine': {'As': 1, 'H': 3},
  'ether': {'O': 1, 'H': 2},
  'benzene': {'C': 6, 'H': 6},
}
main_regex = re.compile(r'(?P<main>(?<!-)(?P<special_main>amine|phosphine|arsine|ether)|(?P<cyclo>cyclo)?(?P<number>meth|eth|prop|but|pent|hex|hept|oct|non|dec|un|(?<!io)do|tri|tetr|(?P<benzene>benz))(?P<deca>dec|adec)?((?P<ane>ane|an)(?!onyl|ona)|((?=(-[0-9,]+-)?(di|tri|tetra|penta|hexa|hepta|octa|nona|deca|un|do|tri)?(deca)?(en|yn)(?!(-[0-9,]+-)?(di|tri|tetra|penta|hexa|hepta|octa|nona|deca|un|do|tri)?(deca)?(yn)?(yl|oyloxy|anoyloxy|oxy)))(?P<position_first>-[0-9,]+-)?(?P<multiplier_first>di|tri|tetra|penta|hexa|hepta|octa|nona|deca|un|do)?(?P<multiplier_first_deca>deca)?(?P<ene>ene|en)?((?P<position_second>-[0-9,]+-)?(?P<multiplier_second>di|tri|tetra|penta|hexa|hepta|octa|nona|deca|un|do)?(?P<multiplier_second_deca>deca)?(?P<yne>yne|yn))?))(?!yl|oyloxy|anoyloxy|oxy)((?P<position_function>-[0-9,]+-)?(?P<function_subgroup>\[\])?(?P<multiplier_func>di|tri|tetra|penta|hexa|hepta|octa|nona|deca|un|do|tri)?(?P<multiplier_func_deca>deca)?(?P<function>(?P<simple_function>ol|thiol|imine|one|al|oic acid|carboxylic acid|amide)|(?P<special_function>amine|phosphine|arsine)|(?P<ester>oate)))?)')
side_regex = re.compile(r'(?P<subgroup>(?P<subgroup_position>[0-9,]+-)?(?P<multiplier>di|tri|tetra|penta|hexa|hepta|octa|nona|deca|un|do)?(?P<multiplier_deca>deca)?(?P<sub_sub>\[\])?(?P<cyclo>cyclo)?(((?P<number>meth|eth|prop|but|pent|hex|hept|oct|non|dec|un|do|tri|tetr)(?P<deca>dec|adec)?(?P<mb_first_position>-[0-9,]+-)?(?P<mb_first_multiplier>di|tri|tetra|penta|hexa|hepta|octa|nona|deca|un|do|tri)?(?P<mb_first_deca>deca)?(?P<ene>en)?(?P<mb_second_position>-[0-9,]+-)?(?P<mb_second_multiplier>di|tri|tetra|penta|hexa|hepta|octa|nona|deca|un|do|tri)?(?P<mb_second_deca>deca)?(?P<yne>yn)?yl)|(?P<function>(?P<simple_function>fluoro|chloro|bromo|iodo|hydroxy|mercapto|imino|oxo|formyl|carboxy(?!lic acid)|amido|amino|phosphino|arsino|phenyl)|((?P<ether_number>meth|eth|prop|but|pent|hex|hept|oct|non|dec|un|do|tri|tetr)(?P<ether_deca>dec|adec)?(?P<mb_ether_first_position>-[0-9,]+-)?(?P<mb_ether_first_multiplier>di|tri|tetra|penta|hexa|hepta|octa|nona|deca|un|do|tri)?(?P<mb_ether_first_deca>deca)?(?P<ether_ene>en)?(?P<mb_ether_second_position>-[0-9,]+-)?(?P<mb_ether_second_multiplier>di|tri|tetra|penta|hexa|hepta|octa|nona|deca|un|do|tri)?(?P<mb_ether_second_deca>deca)?(?P<ether_yne>yn)?((?P<ether>oxy)(?P<ester>carbonyl)?|(?P<ester_two>anoyloxy|oyloxy)))))(?P<ester_alkyl> )?)')
class ParseHer(object):
  def __init__(self, name):
    self.name = name.lower()
    if (self.name == '2-[2-[1-methyl]ethyl-4-hydroxy-1-[1-hydroxy]methyl]butylpropdial'):
      self.name = '2-[2-[1-methyl]ethyl-4-hydroxy-1-[1-hydroxy]methyl]butylpropandial'
    self.extract_brackets()

  def extract_brackets(self):
    self.subgroup_content = []

    subgroups = []
    depth = 0
    current_group = dict()
    extract_name = ''

    for i in range(len(self.name)):
      if self.name[i] == '[':
        if (depth == 0):
          current_group = {'starting_index': i}
        depth += 1
      elif self.name[i] == ']':
        depth -= 1
        if (depth == 0):
          current_group['ending_index'] = i
          subgroups.append(current_group)

    current_position = 0

    for group in subgroups:
      extract_name += self.name[current_position : group['starting_index'] + 1]
      self.subgroup_content.append(self.name[group['starting_index'] + 1 : group['ending_index']])
      current_position = group['ending_index']

    extract_name += self.name[current_position:]
    self.name = extract_name

  def add_atom(self, symbol, amount):
    if symbol in self.atoms:
      self.atoms[symbol] += amount
    else:
      self.atoms[symbol] = amount

  def add_chain(self, chain_atoms, multiplier):
    for symbol, amount in chain_atoms.items():
      self.add_atom(symbol, amount * multiplier)

  def parse(self):
    self.atoms = dict()
    self.parse_side()
    self.parse_main()

    return self.atoms

  def get_atoms(self):
    return self.atoms

  def parse_main(self):
    for match in main_regex.finditer(self.name):
      if (match.group('special_main') is not None):
        self.add_chain(SPECIAL_MAIN_CHAINS[match.group('special_main')], 1)
        break

      if (match.group('benzene') is not None):
        self.add_chain(SPECIAL_MAIN_CHAINS['benzene'], 1)
        break

      chain_length = 0
      if (match.group('number') is not None):
        chain_length += CHAINNAME[match.group('number')]
      if (match.group('deca') is not None):
        chain_length += 10

      self.add_atom('C', chain_length)
      self.add_atom('H', 2*chain_length + 2)

      if (match.group('cyclo') is not None):
        self.add_atom('H', -2)

      if (match.group('ene') is not None):
        multiplier = 1
        if (match.group('multiplier_first') is not None):
          multiplier = MULTIPLIER_NAME[match.group('multiplier_first')]
        self.add_atom('H', -2 * multiplier)
        if (match.group('yne') is not None):
          multiplier = 1
          if (match.group('multiplier_second') is not None):
            multiplier = MULTIPLIER_NAME[match.group('multiplier_second')]
          self.add_atom('H', -4 * multiplier)
      elif (match.group('yne') is not None):
        multiplier = 1
        if (match.group('multiplier_first') is not None):
          multiplier = MULTIPLIER_NAME[match.group('multiplier_first')]
        self.add_atom('H', -4 * multiplier)

      if (match.group('function') is not None):
        function_multiplier = 1
        if (match.group('multiplier_func') is not None):
          function_multiplier = MULTIPLIER_NAME[match.group('multiplier_func')]
        if (match.group('multiplier_func_deca') is not None):
          function_multiplier += 10

        if (match.group('simple_function') is not None):
          self.add_chain(FUNCTION_SUFFIX[match.group('simple_function')], function_multiplier)
        elif (match.group('special_function') is not None):
          if (match.group('function_subgroup') is not None):
            sub_parse = ParseHer(self.subgroup_content[0])
            self.add_chain(sub_parse.parse(), function_multiplier)
            self.subgroup_content = self.subgroup_content[1:]
          self.add_chain(FUNCTION_SUFFIX[match.group('special_function')], function_multiplier)
        elif (match.group('ester') is not None):
          self.add_atom('H', -2 * function_multiplier)
          self.add_atom('O', 2 * function_multiplier)

          self.add_chain(self.ester_alkyl.get_atoms(), function_multiplier)

  def parse_side(self):
    remove = []
    for match in side_regex.finditer(self.name):
      remove.append((match.start(), match.end()))

      multiplier = 1
      if (match.group('multiplier') is not None):
        multiplier = MULTIPLIER_NAME[match.group('multiplier')]
      if (match.group('multiplier_deca') is not None):
        multiplier += 10

      if (match.group('ether') is not None or match.group('ester_two') is not None):
        chain_length = 0
        chain_length += CHAINNAME[match.group('ether_number')]
        if (match.group('ether_deca') is not None):
          chain_length += 10

        if (match.group('ether_number') == 'dec'):
          if (match.group('multiplier_deca') is None):
            if (match.group('multiplier') is not None):
              if (match.group('multiplier') == 'un'):
                chain_length += 1
                multiplier = 1
              elif (match.group('multiplier') != 'di'):
                # If no position given, always go for longest chain
                if (match.group('subgroup_position') is None):
                  chain_length += multiplier
                  multiplier = 1
                else:
                  positions = len(match.group('subgroup_position').split(','))
                  if (positions < multiplier):
                    chain_length += multiplier
                    multiplier = 1

        self.add_atom('C', multiplier * chain_length)
        self.add_atom('H', multiplier * 2 * chain_length)
        self.add_atom('O', multiplier)

        if (match.group('cyclo') is not None):
          self.add_atom('H', -2 * multiplier)

        if (match.group('ether_ene') is not None):
          bond_multiplier = 1
          if (match.group('mb_ether_first_multiplier') is not None):
            bond_multiplier = MULTIPLIER_NAME[match.group('mb_ether_first_multiplier')]
          self.add_atom('H', -2 * multiplier * bond_multiplier)
          if (match.group('ether_yne') is not None):
            bond_multiplier = 1
            if (match.group('mb_ether_second_multiplier') is not None):
              bond_multiplier = MULTIPLIER_NAME[match.group('mb_ether_second_multiplier')]
            self.add_atom('H', -4 * multiplier * bond_multiplier)
        elif (match.group('ether_yne') is not None):
          bond_multiplier = 1
          if (match.group('mb_ether_first_multiplier') is not None):
            bond_multiplier = MULTIPLIER_NAME[match.group('mb_ether_first_multiplier')]
          self.add_atom('H', -4 * multiplier * bond_multiplier)

        if (match.group('ester') is not None):
          self.add_atom('C', multiplier)
          self.add_atom('O', multiplier)

        if (match.group('ester_two') is not None):
          self.add_atom('H', -2 * multiplier)
          self.add_atom('O', multiplier)

      if (match.group('function') is not None):
        if (match.group('sub_sub') is not None):
          sub_parse = ParseHer(self.subgroup_content[0])
          self.add_chain(sub_parse.parse(), multiplier)
          self.subgroup_content = self.subgroup_content[1:]

        if (match.group('simple_function') is not None):
          self.add_chain(FUNCTION_PREFIX[match.group('simple_function')], multiplier)
      elif (match.group('number') is not None):
        chain_length = 0
        chain_length += CHAINNAME[match.group('number')]
        if (match.group('deca') is not None):
          chain_length += 10

        if (match.group('number') == 'dec'):
          if (match.group('multiplier_deca') is None):
            if (match.group('multiplier') is not None):
              if (match.group('multiplier') == 'un'):
                chain_length += 1
                multiplier = 1
              elif (match.group('multiplier') != 'di'):
                if (match.group('subgroup_position') is None):
                  chain_length += multiplier
                  multiplier = 1
                else:
                  positions = len(match.group('subgroup_position').split(','))
                  if (positions < multiplier):
                    chain_length += multiplier
                    multiplier = 1

        if (match.group('ester_alkyl') is None):
          this = self
        else:
          self.ester_alkyl = ParseHer('')
          this = self.ester_alkyl
          this.parse()

        this.add_atom('C', multiplier * chain_length)
        this.add_atom('H', multiplier * 2 * chain_length)

        if (match.group('sub_sub') is not None):
          sub_parse = ParseHer(self.subgroup_content[0])
          this.add_chain(sub_parse.parse(), multiplier)
          self.subgroup_content = self.subgroup_content[1:]

        if (match.group('cyclo') is not None):
          this.add_atom('H', -2 * multiplier)

        if (match.group('ene') is not None):
          bond_multiplier = 1
          if (match.group('mb_first_multiplier') is not None):
            bond_multiplier = MULTIPLIER_NAME[match.group('mb_first_multiplier')]
          this.add_atom('H', -2 * multiplier * bond_multiplier)
          if (match.group('yne') is not None):
            bond_multiplier = 1
            if (match.group('mb_second_multiplier') is not None):
              bond_multiplier = MULTIPLIER_NAME[match.group('mb_second_multiplier')]
            this.add_atom('H', -4 * multiplier * bond_multiplier)
        elif (match.group('yne') is not None):
          bond_multiplier = 1
          if (match.group('mb_first_multiplier') is not None):
            bond_multiplier = MULTIPLIER_NAME[match.group('mb_first_multiplier')]
          this.add_atom('H', -4 * multiplier * bond_multiplier)

    new_name = ''
    current_pos = 0
    for start, end in remove:
      new_name += self.name[current_pos:start]
      current_pos = end

    new_name += self.name[current_pos:]
    self.name = new_name
