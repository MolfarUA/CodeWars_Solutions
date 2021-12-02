from itertools import combinations
from collections import defaultdict
from datetime import date
import re


EXPIRE_DT          = date(1982,11,22)
NATION             = 'Arstotzka'.lower()
COUNTRIES          = set(map(str.lower, ('Arstotzka', 'Antegria', 'Impor', 'Kolechia', 'Obristan', 'Republia', 'United Federation')))
ACCESS_SUBSTITUTES = {'grant_of_asylum', 'diplomatic_authorization', 'access_permit'}
MISMATCHER         = {'NAME': 'name', 'NATION': 'nationality', 'ID#': 'ID number', 'DOB': 'date of birth'}
P_PAPERS           = re.compile( r'([^:]+): (.+)\n?' )
P_CONSTRAINTS      = re.compile( r'wanted by the state: (?P<wanted>.+)|'
                                 r'(?P<action>allow|deny) citizens of (?P<who>(?:[\w ]+|, )+)|'
                                 r'(?:citizens of )?(?P<who2>.+?)(?P<noMore> no longer)? require (?P<piece>[\w ]+)' )


class Inspector(object):
    
    def __init__(self):
        self.allowed   = {c: False for c in COUNTRIES}
        self.docs      = defaultdict(set)
        self.vacs      = defaultdict(set)
        self.wanted    = None
        self.papers    = None
        self.papersSet = None
        
    
    def receive_bulletin(self, b):
        self.wanted = None
        
        for m in P_CONSTRAINTS.finditer(b.lower()):
            
            if m["wanted"]:
                self.wanted = self.getWantedSet(m["wanted"])
                continue
                
            whos = (m['who'] or m['who2']).split(', ')
            if   whos == ['entrants']:   whos = COUNTRIES
            elif whos == ['foreigners']: whos = COUNTRIES - {NATION}
            
            if m["action"]:
                for country in whos:
                    self.allowed[country] = m["action"] == 'allow'
            else:
                toRemove = m['noMore']
                piece    = m['piece'].replace(' ','_')
                docType  = self.docs
                
                if piece.endswith('vaccination'):
                    piece   = piece.replace('_vaccination','')
                    docType = self.vacs
                elif piece=='id_card': piece = 'ID_card'
                
                for who in whos:
                    if toRemove: docType[who].discard(piece)
                    else:        docType[who].add(piece)
        
        
    def getWantedSet(self,s):   return set(s.replace(',','').split())
    
    def isWanted(self):         return any(self.getWantedSet(p.get('NAME','')) == self.wanted for _,p in self.papers.items())
    
    def isBanned(self,nation):  return not self.allowed.get(nation,0)
    
    def needWorkPass(self):     return ('work_pass' in self.docs['workers']
                                         and 'work' in self.papers.get('access_permit', {}).get('PURPOSE', set()))
    
    def getMismatchedPapers(self):
        for p1,p2 in combinations(self.papers, 2):
            p1,p2 = self.papers[p1], self.papers[p2]
            for k in set(p1) & set(p2) - {'EXP'}:
                if k in MISMATCHER and p1[k] != p2[k]: return MISMATCHER[k]
    
    def getMissingDocs(self,nation):
        required = set(self.docs.get(nation, {'passport'}))
        if self.vacs[nation]:   required.add('certificate_of_vaccination')
        if self.needWorkPass(): required.add('work_pass')
        return required - self.papersSet
    
    
    def inspect(self, papers):
        self.papers    = { k: {x:s.lower() for x,s in P_PAPERS.findall(p)}  for k,p in papers.items()}
        self.papersSet = set(self.papers)
        
        mismatched      = self.getMismatchedPapers()
        nation      = next((p['NATION'] for k,p in self.papers.items() if 'NATION' in p), '').lower()
        isForeign   = nation != NATION
        missingDocs = self.getMissingDocs(nation)
        expiredDocs = next( (k.replace("_", " ") for k,p in self.papers.items()
                             if 'EXP' in p and date(*map(int, p['EXP'].split('.'))) <= EXPIRE_DT), None)
        vaccines    = set(self.papers.get('certificate_of_vaccination', {}).get('VACCINES', '').replace(' ','_').split(',_'))
        misVaccines = self.vacs[nation] - vaccines
        
        isBadDiplo  = False
        if isForeign and 'access_permit' in missingDocs:
            substitute = ACCESS_SUBSTITUTES & self.papersSet
            if substitute: missingDocs.discard('access_permit')
            isBadDiplo = (substitute == {'diplomatic_authorization'} 
                          and NATION not in self.papers['diplomatic_authorization']['ACCESS'])
        
        if self.isWanted():       return  'Detainment: Entrant is a wanted criminal.'
        if mismatched:            return f'Detainment: {mismatched} mismatch.'
        if missingDocs:           return f'Entry denied: missing required {missingDocs.pop().replace("_", " ")}.'
        if isBadDiplo:            return  'Entry denied: invalid diplomatic authorization.'
        if self.isBanned(nation): return  'Entry denied: citizen of banned nation.'
        if expiredDocs:           return f'Entry denied: {expiredDocs} expired.'
        if misVaccines:           return  'Entry denied: missing required vaccination.'
        
        return "Cause no trouble." if isForeign else 'Glory to Arstotzka.'
###########################
import re
from collections import defaultdict
import datetime

class Inspector:
    def __init__(self):
        self.allowed = set()
        self.wanted = ''
        self.vaccinations = defaultdict(list)
        self.require = defaultdict(list)
        self.exp = datetime.date(1982, 11, 22)
        self.m = {'ID#': 'ID number', 'NATION': 'nationality', 'DOB': 'date of birth', 'NAME': 'name'}

    def receive_bulletin(self, s):
        for i in s.splitlines():
            if re.search(r'^(Allow|Deny) citizens of .+$', i):
                msg = re.findall(r'^(Allow|Deny) citizens of (.+)$', i)[0]
                if msg[0] == 'Allow' : self.allowed.update(msg[1].split(', '))
                else : self.allowed -= set(msg[1].split(', '))
            
            elif re.search(r'^.+ require .+? vaccination$', i):
                msg = re.findall(r'^(.+?) (?:no longer )?require (.+?) vaccination$', i)[0]
                if 'Foreigners' in i or 'Entrants' in i:
                    if 'no longer' not in i :
                        self.vaccinations[msg[0]].append(msg[1])
                    else:
                        for k, l in self.vaccinations.items():
                            if k == msg[0] and msg[1] in l : self.vaccinations[k].remove(msg[1])
                
                elif 'Citizens' in i:
                    citizens = re.findall(r'Citizens of (.+)', msg[0])[0].split(', ')
                    if 'no longer' not in i:
                        for j in citizens:
                            self.vaccinations[j].append(msg[1])
                    else:
                        for k, l in self.vaccinations.items():
                            if k in citizens and msg[1] in l : self.vaccinations[k].remove(msg[1])

            elif re.search(r'^.+ require .+$', i):
                msg = re.findall(r'(.+) require (.+)', i)[0]
                if 'Citizens' in i:
                    for k in re.findall(r'Citizens of (.+)', msg[0])[0].split(', ') : self.require[k].append(msg[1])
                else : self.require[msg[0]].append(msg[1])

            elif re.search(r'^Wanted by the State: .+$', i) : self.wanted = i.split(': ')[1]

    def inspect(self, data):
        documents = []
        d = defaultdict(list)
        for i, j in data.items():
            documents.append(i.replace('_', ' '))
            for k in j.splitlines():
                a, b = k.split(': ')
                d[a].append((i.replace('_', ' '), b) if a == 'EXP' else b)

        data = {} 
        for i, j in d.items():
            if i != 'EXP':
                if len(set(j)) != 1 : return f'Detainment: {self.m[i]} mismatch.'
                data[i] = j[0]
            else : data[i] = j

        if 'NAME' in data and (data['NAME'] == self.wanted or all(i in data['NAME'] for i in self.wanted.split())) : return 'Detainment: Entrant is a wanted criminal.'
        
        if 'NATION' in data and data['NATION'] not in self.allowed : return 'Entry denied: citizen of banned nation.'
        
        if 'EXP' in d:
            for i, j in enumerate(d['EXP']):
                if datetime.datetime.strptime(j[1], '%Y.%m.%d').date() < self.exp : return f'Entry denied: {j[0]} expired.'

        if 'Entrants' in self.require:
            for i in self.require['Entrants']:
                if i not in documents : return f'Entry denied: missing required {i}.'

        if 'NATION' in data and data['NATION'] != 'Arstotzka' and 'Foreigners' in self.require:
            for i in self.require['Foreigners']:
                if i not in documents:
                    if i == 'access permit':
                        if 'diplomatic authorization' not in documents and 'grant of asylum' not in documents : return f'Entry denied: missing required {i}.'
                        if 'diplomatic authorization' in documents and ('ACCESS' not in data or 'Arstotzka' not in data['ACCESS']) : return 'Entry denied: invalid diplomatic authorization.'
                    else : return f'Entry denied: missing required {i}.'

        if 'Workers' in self.require and ('PURPOSE' in data and data['PURPOSE'] == 'WORK' and 'work pass' not in documents) : return 'Entry denied: missing required work pass.'

        for i, k in self.require.items():
            for j in k:
                if i not in 'Foreigners Workers Entrants' and data['NATION'] == i and j not in documents : return f'Entry denied: missing required {j}.'

        for i, k in self.vaccinations.items():
            for j in k:
                if i == 'Foreigners' and data['NATION'] != 'Arstotzka' and ('certificate of vaccination' not in documents or j not in data['VACCINES']):return 'Entry denied: missing required vaccination.'
                elif i == 'Entrants' and ('certificate of vaccination' not in documents or j not in data['VACCINES']) : return 'Entry denied: missing required vaccination.'
                elif data['NATION'] == i and ('certificate of vaccination' not in documents or j not in data['VACCINES']) : return 'Entry denied: missing required vaccination.'

        return 'Glory to Arstotzka.' if data['NATION'] == 'Arstotzka' else 'Cause no trouble.'
#####################################
import re
from itertools import combinations

class Inspector:
    groups = ('citizens', 'Wanted', 'Entrants', 'Foreigners', 'Workers',
              'Arstotzka', 'Antegria', 'Impor', 'Kolechia', 
              'Obristan','Republia','United Federation',)
    req_patterns_funcs = (
            # patterns for bulltein lines
            # store in dict of sets 
            # 1st group is keys and 2nd group is values for set func methods
            (re.compile(r'^Allow (citizens) of (.+)$'), set.add, ),
            (re.compile(r'^Deny (citizens) of (.+)$'), set.remove, ),
            (re.compile(r'^(Wanted) by the State: (.+)$'), set.add, ),
            (re.compile(r'^(?:Citizens of )?([A-z, ]+) no longer require (.+)$'), set.remove, ),
            (re.compile(r'^(?:Citizens of )?([A-z, ]+) require (.+)$'), set.add, ),
        )
    
    key_names = {
            'ID#': 'ID number',
            'NAME': 'name',
            'DOB': 'date of birth',
            'NATION': 'nationality'
        }
    
    def __init__(self):
        self.reqs = {group: set() for group in self.groups}
        self.nation = 'Arstotzka'
        #self.reqs['citizens'].add('Arstotzka')
    
    def receive_bulletin(self, bulletin):
        self.reqs['Wanted'].clear()
        for line in bulletin.splitlines():
            for pattern, func in self.req_patterns_funcs:
                if match := pattern.match(line):
                    keys, values = (group.split(', ') for group in match.groups())
                    for key in keys:
                        for value in values:
                            func(self.reqs[key], value)
                    break
            else:
                raise NotImplementedError(line)               
        
    def inspect(self, text_docs):
        if not text_docs:
            return 'Entry denied: missing required {}.'.format(*self.reqs['Entrants'])
        
        # dict-fy docs
        docs = { doctype.replace('_',' ') : 
                   { key: value for key, value in  
                        (line.split(': ') for line in doc.splitlines()) }
               for doctype, doc in text_docs.items() }
        
        # find mismatch
        for doc1, doc2 in combinations(docs.values(), 2):
            for key in set(doc1.keys()) & set(doc2.keys()) - {'EXP'}:
                if doc1[key] != doc2[key]:
                    return f'Detainment: {self.key_names[key]} mismatch.'                
        
        name = next(name for doc in docs.values() if (name := doc.get('NAME')))
        name = ' '.join(reversed(name.split(', ')))
        if name in self.reqs['Wanted']:
            return 'Detainment: Entrant is a wanted criminal.'
        
        nation = self.nation if 'ID card' in docs.keys() else next(nation for doc in docs.values() if (nation := doc.get('NATION')))
        if nation not in self.reqs['citizens']:
            return 'Entry denied: citizen of banned nation.'
        
        # Check exp dates
        for doctype, doc in docs.items():
            if date := doc.get('EXP'):
                if tuple(map(int, date.split('.'))) < (1982, 11, 22):
                    return f'Entry denied: {doctype} expired.'
                
        # list req items
        reqs = self.reqs[nation] | self.reqs['Entrants']
        req_vaxes = set()
        if nation != self.nation:
            reqs |= self.reqs['Foreigners']
        if docs.get('access permit', {}).get('PURPOSE') == 'WORK':
            reqs |= self.reqs['Workers']
        
        for req in reqs - set(docs.keys()) :
            if req == 'access permit':
                if 'diplomatic authorization' in docs.keys():
                    if self.nation not in docs['diplomatic authorization']['ACCESS']:
                        return 'Entry denied: invalid diplomatic authorization.'
                    else:
                        continue
                elif 'grant of asylum' in docs.keys():
                    continue
            elif req.endswith(' vaccination'):
                vaxes = set( req[:len(req)-len(' vaccination')].split(', ') )
                req_vaxes |= vaxes
                continue 
            return f'Entry denied: missing required {req}.'
        
        if req_vaxes:
            if vaxes := set(docs.get('certificate of vaccination', dict()).get('VACCINES', '').split(', ')):
                if not vaxes >= req_vaxes:
                        return f'Entry denied: missing required vaccination.'
            else:
                return 'Entry denied: missing required certificate of vaccination.'
            
        return f'Glory to {self.nation}.' if nation == self.nation else 'Cause no trouble.'
#####################################
class Inspector:
    req={}
    def receive_bulletin(self,bulletin):
        self.req["wanted"]=[]
        for rl in bulletin.splitlines():
            if  rl.find("Allow citizens of")!=-1:
                allow=self.req.get("allow",[])
                allow+=[x.strip() for x in rl[rl.find("of")+2:].split(",")]
                self.req["allow"]=allow
                deny=self.req.get("deny",[])
                self.req["deny"]=[x for x in deny if x not in allow]
            elif  rl.find("Deny citizens of")!=-1:
                deny=self.req.get("deny",[])
                deny+=[x.strip() for x in rl[rl.find("of")+2:].split(",")]
                self.req["deny"]=deny
                allow=self.req.get("allow",[])
                self.req["allow"]=[x for x in allow if x not in deny]
            elif rl.find("no longer")!=-1:
                rl2=rl
                if rl.find("Citizens")!=-1: rl2=rl[rl.find(" of")+3:]
                cl=[x.strip() for x in rl2[0:rl2.find("no longer require")].split(",")]
                rlist=[x.strip() for x in rl2[rl2.find("no longer require")+18:].split(",")]
                for c in cl:
                    cr=self.req.get(c,[])
                    for r in rlist:
                        while r in cr:
                            cr.remove(r)
                    self.req[c]=cr
            elif rl.find("require")!=-1:
                rl2=rl
                if rl.find("Citizens")!=-1: rl2=rl[rl.find(" of")+3:]
                cl=[x.strip() for x in rl2[0:rl2.find(" require"):].split(",")]
                rlist=[x.strip() for x in rl2[rl2.find("require")+7:].split(",")]
                for c in cl:
                    cr=self.req.get(c,[])+rlist
                    self.req[c]=cr
            elif rl.find("Wanted")!=-1:
                self.req["wanted"]=rl[rl.find(":")+1:].strip()

    def inspect(self,person):
        mt={"NATION":" nationality ","ID#":" ID number ","NAME": " name ","DOB":" date of birth "}
        pd={}
        mismatch=False
        expired=False
        for k,vlines in [ (ku.replace("_"," ").strip(), vu.splitlines()) for ku,vu in person.items()]:
            pd[k]=""
            for vl in vlines:
                ve=vl.split(":"); ve[1]=ve[1].strip()
                if ve[0]=="EXP":
                    if ve[1]<="1982.11.22":
                        expired=True
                        expEle=k
                else:
                    if ve[0]=="NAME":
                        ve[1]=ve[1].split(",")
                        ve[1]=ve[1][1].strip()+" "+ve[1][0]
                        if ve[1] in self.req["wanted"]:
                            return 'Detainment: Entrant is a wanted criminal.'
                    if ve[0] in pd and ve[1]!=pd[ve[0]]:
                        mismatch= True
                        misEle = ve[0]
                    else:
                        if ve[0]=="VACCINES":
                            for vac in ve[1].split(","):
                                pd[vac.strip()+" vaccination"]=""
                        else:
                            pd[ve[0]]=ve[1]
        if mismatch:
            return 'Detainment:' + mt[misEle]+    'mismatch.'
        if expired:
            return 'Entry denied: '+ expEle + ' expired.'
        
        rl=self.req.get("Entrants",[]).copy()
        if pd.get("NATION","")!="Arstotzka": rl+=self.req.get("Foreigners",[]).copy()
        rl+=self.req.get(pd.get("NATION",""),[]).copy()
        if pd.get("PURPOSE")=="WORK": rl+=self.req.get("Workers",[])
        rej=[]
        for r in rl:
            if r not in pd:
                if r=="access permit":
                    if "grant of asylum" in pd : continue
                    if "diplomatic authorization" in pd:
                        if pd.get("ACCESS","").find("Arstotzka")==-1:
                            rej=['Entry denied: invalid diplomatic authorization.']+rej
                        continue
                    rej=['Entry denied: missing required access permit.']+rej
                elif r.find("vaccination")>=0:
                    if "certificate of vaccination" in pd:
                        rej+= ['Entry denied: missing required vaccination.']
                    else:
                        rej+=['Entry denied: missing required certificate of vaccination.']
                elif r=="passport":
                        return 'Entry denied: missing required passport.'
                else:
                    rej+= ['Entry denied: missing required '+r+"."]
        if len(rej)>0:
            return rej[0]
        if pd.get("NATION","") in self.req.get("deny",[]) or pd.get("NATION","") not in self.req["allow"]:
            return 'Entry denied: citizen of banned nation.'
        if pd["NATION"] == "Arstotzka":
            return 'Glory to Arstotzka.'
        else:
            return 'Cause no trouble.'
######################################################
import re
import time


class Inspector:
    def __init__(self):

        self.requirements = {
            "Arstotzka": {"vaccinations": [], "documents": []},
            "Antegria": {"vaccinations": [], "documents": []},
            "Impor": {"vaccinations": [], "documents": []},
            "Kolechia": {"vaccinations": [], "documents": []},
            "Obristan": {"vaccinations": [], "documents": []},
            "Republia": {"vaccinations": [], "documents": []},
            "United Federation": {"vaccinations": [], "documents": []},
            "wrw": False
        }

        self.bulletin = {
            "allowed_nations": [],
            "criminal": "",
        }

        self.nations = [
            "Arstotzka",
            "Antegria",
            "Impor",
            "Kolechia",
            "Obristan",
            "Republia",
            "United Federation"
        ]

    def receive_bulletin(self, bulletin):
        for i in bulletin.split("\n"):
            temp = list(filter(None, re.split(r"(?:(Allow|Deny) citizens of (.*)|(?:(Foreigners|Workers|Entrants)|Citizens of (.*)) (?:((?<!no longer )require)|(no longer require)) (.*)|(Wanted) by the State: (.*))", i)))
            if "Allow" in temp[0]:
                self.bulletin["allowed_nations"] += [x for x in temp[1].split(", ") if x not in self.bulletin["allowed_nations"]]
            elif "Deny" in temp[0]:
                self.bulletin["allowed_nations"] = [x for x in self.bulletin["allowed_nations"] if x not in temp[1].split(", ")]
            elif "Wanted" in temp[0]:
                self.bulletin.update({"criminal": temp[1]})
            elif "require" in temp[1]:
                if temp[0] == "Foreigners": temp[0] = str([x for x in self.nations if x != "Arstotzka"]).strip("[]").replace("'", "")
                if temp[0] == "Entrants": temp[0] = str(self.nations).strip("[]").replace("'", "")
                if temp[0] == "Workers":
                    if temp[1] == "require": self.requirements["wrw"] = True
                    if temp[1] == "no longer require": self.requirements["wrw"] = False
                if temp[0] in self.nations or set(temp[0].split(", ")).issubset(set(self.nations)):
                    for j in temp[0].split(", "):
                        if "vaccination" in temp[2]:
                            if temp[1] == "require": self.requirements[j]["vaccinations"].append(temp[2].replace(" vaccination", ""))
                            if temp[1] == "no longer require": self.requirements[j]["vaccinations"].remove(temp[2].replace(" vaccination", ""))
                            if len(self.requirements[j]["vaccinations"]) > 0: self.requirements[j]["documents"].append("certificate_of_vaccination")
                            if len(self.requirements[j]["vaccinations"]) == 0: self.requirements[j]["documents"] = [x for x in self.requirements[j]["documents"] if x != "certificate_of_vaccination"]

                        else:
                            if temp[1] == "require": self.requirements[j]["documents"].append(temp[2].replace(" ", "_"))
                            if temp[1] == "no longer require": self.requirements[j]["documents"].remove(temp[2])

    def inspect(self, entrant):
        try:
            nation = re.search(r"NATION: (.*)\n", str(list(entrant.values())).strip("[]").replace("'", "").replace("\\n", "\n")).group(1)
            name = re.search(r"NAME: (.*)\n", str(list(entrant.values())).strip("[]").replace("'", "").replace("\\n", "\n")).group(1)
        except:
            return "Entry denied: missing required passport."

        def convert_to_dict():
            for i in entrant:
                entrant[i] = dict(map(lambda x: x.split(": "), entrant[i].split("\n")))

        def check_discrepancies():
            not_unique_keys = [
                "EXP"
            ]
            val = list(entrant.values())
            x = val[0]
            neq = []
            for i in val[1:]:
                for j in i:
                    if j in x and x[j] != i[j] and j not in not_unique_keys:
                        neq.append(j)
            neq = list(dict.fromkeys(neq))
            if len(neq) > 0: return "Detainment: " + neq[0].replace("ID#", "ID number").replace("NATION", "nationality").replace("NAME", "name").replace("DOB", "date of birth") + " mismatch."
            return True

        def check_documents():
            if set(self.requirements[nation].get("documents") + (["work_pass"] if self.requirements["wrw"] else [])).issubset(set(list(entrant.keys()))):
                return True
            missing = list(set(self.requirements[nation].get("documents")) - set(entrant.keys()))
            if "access_permit" in self.requirements[nation].get("documents") and ("access_permit" in entrant.keys() or "grant_of_asylum" in entrant.keys() or "diplomatic_authorization" in entrant.keys()):
                if "diplomatic_authorization" in entrant.keys():
                    if "Arstotzka" not in entrant["diplomatic_authorization"]["ACCESS"].split(", "):
                        return "Entry denied: invalid diplomatic authorization."
                elif "'PURPOSE': 'WORK'" in str(entrant.values()) and self.requirements["wrw"]:
                    if "work_pass" not in entrant.keys(): return "Entry denied: missing required work pass."
                missing = [x for x in missing if x != "access_permit"]
            if len(missing) > 0:
                return "Entry denied: missing required " + missing[0].replace("_", " ") + "."
            return True

        def check_expiration():
            for i in entrant:
                if "EXP" in entrant[i].keys():
                    if time.strptime(entrant[i]["EXP"], "%Y.%m.%d") <= time.strptime("1982.11.22", "%Y.%m.%d"):
                        return "Entry denied: " + str(i).replace("_", " ") + " expired."
            return True

        def check_vaccinations():
            if self.requirements[nation].get("vaccinations"):
                if not set(self.requirements[nation].get("vaccinations")).issubset(set(entrant["certificate_of_vaccination"]["VACCINES"].split(", "))):
                    return "Entry denied: missing required vaccination."
            return True

        def check_criminal():
            re_name = list(filter(None, re.split(r"([a-zA-Z]*), ([a-zA-Z]*)", name)))
            wanted = self.bulletin["criminal"].split(" ")
            if sorted(re_name) == sorted(wanted):
                return "Detainment: Entrant is a wanted criminal."
            return True

        def check_foreigner():
            if not nation == "Arstotzka":
                if nation not in self.bulletin.get("allowed_nations"):
                    return "Entry denied: citizen of banned nation."
                else:
                    return "Cause no trouble."
            else:
                return "Glory to Arstotzka."

        def run(func):
            x = func
            if x is not True:
                raise Exception(x)
            return

        try:
            convert_to_dict()
            run(check_criminal())
            run(check_discrepancies())
            run(check_documents())
            run(check_expiration())
            run(check_vaccinations())
            return run(check_foreigner())
        except Exception as e:
            return e.args[0]
