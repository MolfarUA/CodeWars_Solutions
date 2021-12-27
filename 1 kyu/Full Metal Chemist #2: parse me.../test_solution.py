
def doFixedTests():
    FIXED_TESTS = [
# (draw,
#  name,                                       raw formula as a dict            Test.describe, Test.it (name of the molecule if empty)
# )
("""
CH4
""",
 "methane",                                     {"C": 1,  "H": 4 },              "Simple chains / impact of the number of C", "",
),

("""
CH3-CH3
""",
 "ethane",                                      {"C": 2,  "H": 6 },              "", "",
),



("""
CH3-CH2-CH2-CH3
""",
 "butane",                                      {"C": 4,  "H": 10},              "", "",
),



("""
CH3-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH3
""",
 "decane",                                      {"C": 10, "H": 22},              "", "",
),







("""
CH3-CH2-CH2-CH2-CH2-CH2-CH2-CH3
""",
 "octane",                                      {"C":  8, "H": 18},              "Simple ramifications", "REFERENCE: C8H18 (octane)",
),


("""
        CH2-CH3
        |
CH3-CH2-CH-CH2-CH2-CH3
""",
 "3-ethylhexane",                               {"C":  8, "H": 18},              "", "One ramification",
),


("""
   CH3  CH2-CH3
    |   |
CH3-CH-CH-CH2-CH3
""",
 "3-ethyl-2-methylpentane",                     {"C":  8, "H": 18},              "", "Two ramifications",
),


("""
        CH2-CH3
        |
CH3-CH2-C-CH2-CH3
        |
        CH3
""",
 "3-ethyl-3-methylpentane",                     {"C":  8, "H": 18},              "", "Two ramifications on the same C",
),

("""
        CH3
        |
CH3-CH2-C-CH2-CH2-CH3
        |
        CH3
""",
 "3,3-dimethylhexane",                          {"C":  8, "H": 18},              "", "Handle multipliers",
),

("""
 CH3   CH3
   \\   /
CH3-C-C-CH3
   /   \\
 CH3   CH3 
""",
 "2,2,3,3-tetramethylbutane",                   {"C":  8, "H": 18},              "", "Handle multipliers",
),






("""
 CH2-CH2-CH2-CH2
 |           |
 CH2-CH2-CH2-CH2
""",
 "cyclooctane",                                 {"C":  8, "H": 16},              "Effect of cycles and multiple bounds", "REFERENCE: C8H16 (cyclooctane)",
),
         
          
("""
 CH2-CH2-CH-CH2-CH3
 |       |
 CH2-CH2-CH2  
""",
 "1-ethylcyclohexane",                          {"C":  8, "H": 16},              "", "One cycle of size 6 and one ramification",
),

  
("""
 CH2-CH-CH2-CH3
 |   |
 CH2-C-CH3
     |
     CH3 
""",
 "1-ethyl-2,2-dimethylcyclobutane",             {"C":  8, "H": 16},              "", "One cycle of size 4 and several ramifications",
),



("""
CH2=CH-CH2-CH2-CH2-CH2-CH2-CH3
""",
 "oct-1-ene",                                   {"C":  8, "H": 16},              "", "One double bound: at an extremity",
),


            
("""
CH3-CH2-CH=CH-CH2-CH2-CH2-CH3 
""",
 "oct-3-ene",                                   {"C":  8, "H": 16},              "", "One double bound: anywhere in the chain",
),



("""
CH2=CH-CH2-CH2-CH2-CH2-CH2-CH3
""",
 "octene",                                      {"C":  8, "H": 16},              "", "One double bound: elision of the position '-1-'",
),







("""
CH3-CH=CH-CH2-CH=CH-CH2-CH3
""",
 "oct-2,5-diene",                               {"C":  8, "H": 14},              "Effect of mutliple bounds and cycles, part 2", "Double bounds",
),



("""
CH{=}C-CH2-CH2-CH2-CH2-CH2-CH3      "{=}" used as triple bound (should be 3 lines)
""",
 "oct-1-yne",                                   {"C":  8, "H": 14},              "", "Triple bound: at an extremity",
),



("""
CH3-C{=}C-CH2-CH2-CH2-CH2-CH3
""",
 "oct-2-yne",                                   {"C":  8, "H": 14},              "", "Triple bound: in the chain",
),



("""
CH{=}C-CH2-CH2-CH2-CH2-CH2-CH3
""",
 "octyne",                                      {"C":  8, "H": 14},              "", "Triple bound: elision of the position",
),


("""
 CH2-CH2-CH-CH2-CH3
 |       |
 CH=CH-CH2   
""",
 "3-ethylcyclohexene",                          {"C":  8, "H": 14},              "", "Mix of cycles and multiple bounds",
),






("""
CH3-CH2-CH2-CH2-CH3
""",
 "pentane",                                    {"C": 5, "H": 12},                "Simple functions: oxygen", "REFERENCE: C5H12 (pentane)",
),



("""
CH3-CH2-CH2-CH2-CH2-OH
""",
 "pentanol",                                   {"C": 5, "H": 12, "O": 1},        "", "",
),

("""
    OH
    |
CH3-CH-CH2-CH2-CH3
""",
 "pentan-2-ol",                                {"C": 5, "H": 12, "O": 1},        "", "",
),

("""
    OH     OH
    |      |
CH3-CH-CH2-CH-CH3
""",
 "pentan-2,4-diol",                            {"C": 5, "H": 12, "O": 2},        "", "",
),


("""
CH3-CH2-CH2-CH2-CH=O
""",
 "pentanal",                                   {"C": 5, "H": 10, "O": 1},        "", "",
),

("""
    O
    ||
CH3-C-CH2-CH2-CH3
""",
 "pentan-2-one",                               {"C": 5, "H": 10, "O": 1},        "", "",
),


("""
O=CH-CH2-CH2-CH2-CH=O
""",
 "pentandial",                                 {"C": 5, "H": 8, "O": 2},         "", "",
),

("""
    O     O
    ||    ||
CH3-C-CH2-C-CH3
""",
 "pentan-2,4-dione",                           {"C": 5, "H": 8, "O": 2},         "", "",
),








("""
CH3-CH2-CH2-CH2-CH3
""",
 "pentane",                                    {"C": 5, "H": 12},                "Simple functions: halogens", "REFERENCE: C5H12 (pentane)",
),


("""
CH3-CH2-CH2-CH2-CH2-F
""",
 "1-fluoropentane",                            {"C": 5, "H": 11, "F": 1},        "", "",
),


("""
    Cl
    |
CH3-CH-CH2-CH2-CH3
""",
 "2-chloropentane",                            {"C": 5, "H": 11, "Cl": 1},       "", "",
),


("""
    Cl
    |
CH3-CH-CH2-CH2-CH2-Br
""",
 "1-bromo-4-chloropentane",                    {"C": 5, "H": 10, "Cl": 1, "Br": 1},  "", "",
),








("""
CH3-CH2-CH2-CH2-CH2-CH3
""",
 "hexane",                                     {"C": 6, "H": 14},                "Simple functions: nitrogen", "REFERENCE: C6H14 (hexane)",
),



("""
CH3-CH2-CH2-CH2-CH2-CH2-NH2
""",
 "hexylamine",                                 {"C": 6, "H": 15, "N": 1},        "", "",
),



("""
CH3-CH2-CH2-CH2-NH-CH2-CH3
""",
 "butylethylamine",                            {"C": 6, "H": 15, "N": 1},        "", "",
),


("""
            CH3
            |
CH3-CH2-CH2-N-CH2-CH3
""",
 "ethylmethylpropylamine",                     {"C": 6, "H": 15, "N": 1},        "", "",
),



("""
N(CH2-CH3)3
""",
 "triethylamine",                              {"C": 6, "H": 15, "N": 1},        "", "",
),



("""
NH2-CH2-CH2-CH2-CH2-CH2-CH2-NH2
""",
 "hexan-1,6-diamine",                          {"C": 6, "H": 16, "N": 2},        "", "Alternative nomenclature: hexan-1,6-diamine",
),



("""
                    O
                    ||
CH3-CH2-CH2-CH2-CH2-C-NH2
""",
 "hexanamide",                                 {"C": 6, "H": 13, "N": 1, "O": 1}, "", "WARNING: amiDe, not amiNe, here!",
),








("""
CH2-CH2-CH2-CH2-CH2-CH2-CH2-OH
|
CH2-CH2-CH2-CH2-CH2-CH2-CH2-OH
""",
 "tetradecan-1,14-diol",                       {"C":  14, "H": 30, "O": 2},      "Complex ramifications", "REFERENCE: C14H30O2 (tetradecandiol)",
),



("""
CH3-CH2-CH2      CH2-CH2-CH2-OH
          \\     /
           CH-CH
          /     \\
CH3-CH2-CH2      CH2-CH2-CH2-OH
""",
 "4-[1-propyl]butylheptan-1,7-diol",             {"C":  14, "H": 30, "O": 2},    "", "",
),



("""
      CH3      CH2-CH2-OH
        \\     /
    CH3  CH-CH
    |   /     \\
CH3-C-CH2      CH2-CH2-CH2-OH
    |
    CH2-CH3
""",
 "3-[1,3,3-trimethyl]pentylhexan-1,6-diol",       {"C":  14, "H": 30, "O": 2},   "", "",
),



("""
       CH3        CH3
       |          |
   CH3-C-CH3  CH3-C-CH3
       |          |
HO-CH2-CH-CH2-CH2-CH-CH2-OH
""",
 "2,5-di[dimethyl]ethylhexan-1,6-diol",         {"C":  14, "H": 30, "O": 2},     "", "Subchain with elision: 2,5-di[dimethyl]ethylhexan-1,6-diol",
),







   
("""
CH2-CH2-C=O
|       |
CH2-CH2-CH2
""",
 "cyclohexanone",                               {"C": 6,  "H": 10,  "O": 1},     "Parse correctly some edge cases", "Warm up... (hexanone)",
),

             
("""
H2C--C(C9H19)2
  |  |
O=C  C(C9H19)2
  |  |
 HC--C(C9H19)2
  |
  OH
""",
 "3,3,4,4,5,5-hexanonyl-2-hydroxycyclohexanone",  {"C": 60, "H": 118, "O": 2},     "", "Split correctly 'hexanonyl'",
),

             
("""
            O
            ||
CH3-(CH2)16-C-CH3
""",
 "nonadecanone",                                {"C": 19, "H": 38,  "O": 1},     "", "Split correctly nonadecanone",
),

             
("""
    O
    ||
CH3-C-(CR2)9-CHR-(CH2)5-CH2-CH3    with R = ...-CH2-(CH2)17-CH3
""",
 "3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12-nonadecanonadecylnonadecanone", {"C": 380, "H": 760, "O": 1},  "", "Find your way in 'nonadeca|nonadecyl|nonadecan|one'... ;s (with elision)",
),







             
("""
O=CH-O-CH3
""",
 "methyl methanoate",                           {"C": 2,  "H": 4,   "O": 2},     "Let's begin the hard stuff!!...", "",
),

             
("""
        O
        ||
CH3-CH2-C-OH
""",
 "propanoic acid",                              {"C": 3, "H": 6,  "O": 2},     "", "",
),

             
("""
    O                 O  H2C-CH2
    ||                ||  |  |
CH3-C-CH2-CH2-CH2-CH2-C-O-CH-CH2
""",
 "cyclobutyl 6-oxoheptanoate",                  {"C": 11, "H": 18,  "O": 3},     "", "",
),

             
("""
    O             O  H2C-CH2
    ||            ||  |  |
CH3-C-C{=}C-C{=}C-C-O-CH-CH2
""",
 "cyclobutyl 6-oxohept-2,4-diynoate",           {"C": 11, "H": 10,  "O": 3},     "", "",
),

             
("""
   O   CH3-CH-CH3
  ||       |
HO-C-CH=CH-C=CH-CH2-OH
""",
 "4-[1-methyl]ethyl-6-hydroxyhex-2,4-dienoic acid", {"C": 9, "H": 14,  "O": 3},     "", "",
),

             
("""
CH=CH-CH=CH
|        |
CH-C{=}C-CH-CH3
|
OH
""",
 "4-methylcyclooct-5,7-dien-2-ynol",         {"C": 9,  "H": 10,   "O": 1},     "", "",
),
             
("""
    OH
    |
CH2-CH-CH2-CH2\\
|              C=O
CH2-CH2-CH2-CH/
            |
            O-CH3
""",
 "7-hydroxy-2-methoxycyclononanone",            {"C": 10, "H": 18,  "O": 3},     "", "",
),

             
("""
               CH3
               |
           CH3-C-CH3
               |
           CH2-CH-CH3
           |      
HO-CH2-CH2-C-CH2-CH2-CH2-OH
           |   
           CH2-CH-CH3
               |
           CH3-C-CH3
               |
               CH3   

""",
 "3,3-di[3,3,2-trimethyl]butylhexan-1,6-diol",  {"C": 20, "H": 42,  "O": 2},     "", "",
),
             
             
("""
HOOC-CH-CH2-CH-COOH
     |      |
  HO-CH     CH-OH
     |      |
 CH2=CH     CH=CH2
""",
 "2,4-di[1-hydroxy]prop-2-enylpentandioic acid" ,                   {"C": 11, "H": 16,  "O": 6},  "", "",
),
             
             
("""
     CH=O
     |
O=CH-CH-CH-CH-CH2-CH2-OH
       /   \\
   HO-CH2   CH-CH3
            |
            CH3
""",
 "2-[2-[1-methyl]ethyl-4-hydroxy-1-[1-hydroxy]methyl]butylpropandial", {"C": 11, "H": 20,  "O": 4},  "", "",
),


("""
I-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH3
""",
 "iododecane",                                 {"C": 10, "H": 21, "I": 1},      "", "No mistake between iododecane and dodecane",
),


("""
Br            C10H21             C10H21     C10H21
|             |                  |          |
CH=CH-CH2-CH2-CH-CH2-CH2-CH2-CH2-CH-CH2-CH2-C=CH2
""",
 "bromo-5,10,13-tridecyltetradec-1,13-diene",  {"C": 44, "H": 85, "Br": 1},      "", "Do not parse non ambiguous tri-decyls as tridecyl...",
),


("""
Br            C13H27
|             |
CH=CH-CH2-CH2-CH-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH=CH2
""",
 "bromo-5-tridecyltetradec-1,13-diene",        {"C": 27, "H": 51, "Br": 1},      "", "...but match correctly a tridecyl",
),


("""
                             R R R R
                             | | | |
O=CH-CH2-CH2-CH2-CH2-CH2-CH2-C-C-C-C-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH=O
                             | | | |
                             R R R R

With ...R = ...-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH3
""",
 "8,8,9,9,10,10,11,11-octadecylnonadecandial",  {"C": 99, "H": 196, "O": 2},      "", "The same happens with other radicals!",
),


("""
                             R  R  R  R
                             |  |  |  |
O=CH-CH2-CH2-CH2-CH2-CH2-CH2-CH-CH-CH-CH-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH=O

With ...R = ...-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH3
""",
 "8,9,10,11-tetradecylnonadecandial",           {"C": 59, "H": 116, "O": 2},      "", "The same happens with other radicals!",
),


("""
             R
             |
R-CH-CH2-CH2-C-R
  |          |
R-CH-CH2-CH2-CH2

                       X  X  X  X            Cl
                       |  |  |  |            |
with ...-R  =  ...-CH2-CH-CH-CH-CH-C{=}C-CH2-CH-CH2-CH2-C{=}CH    ( "{=}" being a triple bound )

and  ...-X  =  ...-CH=CH-C{=}C-CH3
                      
""",
 "3,4,7,7-tetra[9-chloro-2,3,4,5-tetrapenten-3-ynyl]tridec-6,12-diynylcyclooctane",
 {'Cl': 4, 'C': 140, 'H': 148},                                         "", "Handle complex cases with elision",
),
 

("""
HOOC-CH2-CH-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-COOH
         |
         CH2-CH-CH2-CH2-COOH
             |
           O=C-O-CH3
""",
 "3-[4-carboxy-2-methoxycarbonyl]butyldodecandioic acid",      {"C": 19, "H": 32, "O": 8},   "", "",
),

             
("""
HOOC-CH2-CH-C-CH2-CH2-CH2-CH-CH2-CH2-CH2-COOH
        /  / \\            |
       R  R   R           R
       
where R = ...-CH2-CH-CH2-CH2-COOH
                  |
                O=C-O-CH3
""",
 "3,4,4,8-tetra[4-carboxy-2-methoxycarbonyl]butyldodecandioic acid", {"C": 40, "H": 62, "O": 20},  "", "",
),

             
("""
    CH2
    / \\
 H2C   CH2
   \\   /
   HC-C
   //  \\
   O    COOH
""",
 "2-oxocyclopentan-1-carboxylic acid",             {"C": 6, "H": 8, "O": 3},  "", "",
),


("""
       CH=O
      /
  HC-C
 //   \\\\
HC     C-I
 \\    /
  HC=C
      \\
       CH=O
""",
 "1,3-diformyl-2-iodobenzene",                      {"C": 8, "H": 5, "O": 2, "I": 1},  "", "",
),


("""
   SH SH SH SH   SH SH SH SH 
   |  |  |  |    |  |  |  |
HS-CH-CH-CH-CH-O-CH-CH-CH-CH-SH
""",
 "di[1,2,3,4,4-pentamercapto]butylether",           {"C": 8, "H": 18, "O": 1, "S": 10},  "", "",
),


("""
      F   SH  F
       \\  |  /
HS-CH2-CH-C-CH-CH2-SH
          |
          SH
""",
 "2,4-difluoropentan-1,3,3,5-tetrathiol",           {"C": 5, "H": 10, "F": 2, "S": 4},  "", "",
),


("""
      F   SH  F
       \\  |  /
HS-CH2-CH-C-CH-CH2-SH
          |
          SH
""",
 "2,4-difluoropentan-1,3,3,5-tetrathiol",           {"C": 5, "H": 10, "F": 2, "S": 4},  "", "",
),


("""
                              HC-CH
                             //   \\\\
R-As-R        where R-... = HC     C-...
   |                         \\    /
   R                          HC=CH
""",
 "triphenylarsine",                                 {"C": 18, "H": 15, "As": 1},  "", "",
),


("""
     O        O
    ||        ||
  HO-C        C-OH
     |        |
HO-C-CH-CH-CH-CH-C-OH
  ||    |  |     ||
   O  R2P  PR2   O

                         Cl
                        /
                    HC-C
                   //   \\\\
where ...-R = ...-C      C-CH3
                   \\    /
                    HC=C
                        \\
                         Cl
""",
 "3,4-di[di[3,5-dichloro-4-methyl]phenyl]phosphino-2,5-dicarboxyhexan-1,6-dioic acid",             {"C": 7*2*2+8, "H": 5*2*2+8, "Cl": 8, "O": 8, "P": 2},  "", "",
),


("""
PH3
""",
 "phosphine",               {"P": 1, "H": 3},  "", "You didn't expect this one, I'd bet...? Well it works the same way! (btw, they talk about it in \"Breaking Bad\"... ;) And if really it bothers you, you have my blessing to hardocde it :) )",
),


("""
            NH
            ||
CH3-CH2-CH2-C-CH-CH3
              |
              Br
""",
 "2-bromohexan-3-imine",    {"C": 6, "H": 12, "Br":1, "N":1},    "", "",
),


("""
   O                         O
  ||                         ||   
HO-C-CH2-C{=}C-C{=}C-C{=}C-O-C-CH2-C{=}CH
""",
 "8-but-3-ynoyloxyoct-3,5,7-triynoic acid",    {"C": 12, "H": 6, 'O': 4},    "", "",
),



 
 
 
 
 
 
 


("""
CH3-CH2-CH2-CH2-CH-C{=}C-CH2-CH2-CH2-CH-CH2-CH2-C{=}CH
                |                    |
                R                    R
with:
...-R  =  ...-C=CH-C{=}CH2-CH-C{=}C-C{=}C-CH2-CH2-CH3
              |            |
              Br           Br
""",
 "5,11-di[1,5-dibromo]dodecen-3,6,8-triynylpentadec-6,14-diyne",     {'Br': 4, 'C': 39, 'H': 40},    "CRAZY STUFF, HERE!", "",
),




("""
                  O O
                 || ||
CH3-CH2-CH2-CH2-O-C-C-O-CH2-CH2-CH2-CH3
""",
"butyl ethan-1,2-dioate",     {'C': 10, 'H': 18, 'O':4},    "", "Esters with multipliers can be vicious ones...",
),



("""
       OH
       |
H3C-CH-C=O
    |
    CH2-CH2-CH2-CH2-CH-CH-CH2-R
                    |  |
                    R  R
With R =     ...
              |
            O=C-O-CH2-CBr2-CH2-Br
""",
 "2-[5,6,7-tri[2,2,3-tribromo]propoxycarbonyl]heptylpropanoic acid",     {'C': 22,'H': 29,  'Br': 9, 'O': 8},    "", "",
),


("""
Main chain: cycle with 13 carbons,
            2 triple bounds at 7 and 9,
            4 times 'R' at positions 3,3,6 and 12

R:          cycle with 18 carbons,
            1 double bound on the first carbon
            2 triple bounds at 3 and 14
""",
 "3,3,6,12-tetracyclooctadecen-3,14-diynylcyclotridec-7,9-diyne",     {'C': 85, 'H': 114},    "", "",
),


("""
Main Chain: 11 carbons,
            3 triple bounds at 3,7,10
            4 times 'R' at 5,6,6,9

R:          5 carbons,
            1 double bound at position 1 (elision)
            1 triple bound at position 4
            2 Cl atoms at 2,5,
            3 Br at 1,3,3
""",
 "5,6,6,9-tetra[1,3,3-tribromo-2,5-dichloro]penten-4-ynylundec-3,7,10-triyne",
 {'Cl': 8, 'C': 31, 'H': 8, 'Br': 12},    "", "",
),


("""
Main Chain: 16 carbons,
            1 "-oic acid" at 1
            2 triple bounds at 3,14
            1 double bound at 11
            4 times 'R1' at 5,7,8,12
            2 times 'Cl' at 6,16
            4 times 'R2' at 2,6,7,10

R1:         13 carbons,
            2 triple bounds at 7,10
            
R2:         4 carbons,
            1 triple bound at 3
            1 double bound at 1 (elision)
            2 'Br' at 2,4
""",
 "2,6,7,10-tetra[2,4-dibromo]buten-3-ynyl-6,16-dichloro-5,7,8,12-tetratridec-7,10-diynylhexadec-11-en-3,14-diynoic acid",
 {'C': 84, 'H': 92, 'O': 2, 'Br': 8, 'Cl': 2},    "", "",
),


("""
Main Chain: 16 carbons,
            1 "-oic acid"
            2 triple bounds at 10,13
            4 times 'R1' at 2,4,5,12
            1 times 'R2' at 15

R1:         6 carbons,
            2 triple bounds at 3,5
            1 double bound at 1 (elision)
            1 'R1-2' at position 1 (elision)
            1 'R1-3' at position 2
            
            
R2:         ester (anoyloxy)
            3 carbons
            1 double bound at 1 (elision)
            3 amino (NH2, here) at 1,2,3

R1-2:       ester (oxycarbonyl)
            2 carbons
            1 double bound at 1 (elision)
            2 amino at 1,2
            
R1-3:       arsino with 1 H and 1 subchain, 'R-As'

R-As:       7 carbons
            1 double bound at 2
            4 'Cl' at 1,4,6,7
            3 'Br' at 4,5,5
            
""",
 "15-[1,2,2-triamino]propenanoyloxy-2,4,5,12-tetra[2-[[4,5,5-tribromo-1,4,6,7-tetrachloro]hept-2-enyl]arsino[1,2-diamino]ethenoxycarbonyl]hexen-3,5-diynylhexadec-10,13-diynoic acid",
 {'C': 83, 'H': 77, 'O': 12, 'N': 11, 'As': 4, 'Br': 12, 'Cl': 16},    "", "",
),


("""
Main Chain: 4 carbons,
            2 "-oic acid" (at both ends ; elisions)
            1 times 'R' at 2

R:          ester (oxycarbonyl)
            14 carbons,
            1 'Cl' at 10
            4 times [...]amino at 4,6,9,11 with:
                    1 [...] tetradecyl (14 carbons) at 11 with:
                            1 [...]phosphino at 1 (elision) with:
                                    1 [2-iodo]ethyl
                                    1 [6,16,18-triarsino]octadecyl
                    1 phenyl at 10

""",
 "2-[4,6,9,11-tetra[[10-phenyl-11-[[6,16,18-triarsino]octadecyl[2-iodo]ethyl]phosphino]tetradecyl]amino-10-chloro]tetradecoxycarbonylbutandioic acid",
 {'C': 179, 'Cl': 1, 'H': 337, 'O': 6, 'I': 4, 'N': 4, 'As': 12, 'P': 4},    "", "",
),


("""
       OH
       |
H3C-CH-C=O
    |
    CH2-CH2-CH2-CH2-CH-CH-CH2-R
                    |  |
                    R  R
With R =     ...
              |
            O=C-O-CH2-CBr2-CH2-Br
""",
 "2-[5,6,7-tri[2,2,3-tribromo]propoxycarbonyl]heptylpropanoic acid",     {'C': 22,'H': 29,  'Br': 9, 'O': 8},    "", "",
),
 
 


("""
O=C-CH2-CH2-CH3
  |
  O         I  NH
  |         |  ||
I-C-CH2-CH2-CH-C-CH2-CH2-CH2-CH2
  |                          /
  CH2                       CH2
   \\                       /
    CH2-CH2-CH2-C-CH2-CH2-CH2
                  ||
                  NH
""",
 "5,14-diimino-1,4-diiodobutanoyloxycyclooctadecane",     {'I': 2, 'N': 2, 'O': 2, 'H': 38, 'C': 22},    "", "",
),



("""
  OH           Ph    Ph Ph
  |            |      | |
O=C-CH2-CH2-CH-CH-CH2-C-CH-CH-CH-CH2-CH2-R
            |         |    |  |
            R         Ph   R  R

With -R = -O-C-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH3
             ||
             O
and -Ph = C6H5
""",
 "4,9,10,12-tetradecanoyloxy-5,7,7,8-tetraphenyldodecanoic acid",     {'H': 112, 'O': 10, 'C': 76},    "", "",
),

        
        
  
("""
Main chain: 19 carbons
Ramifications: 15x 13 carbons
(non official name)
""",
 "6,6,7,7,8,8,9,9,10,10,11,11,12,12,13-pentadecatridecylnonadecane",     {'H': 430, 'C': 214},    "", "",
),

]

    # to update the test suite to the new framework: reformatting the fixed tests data
    lstTests=[]
    for data in FIXED_TESTS:
        clean = data[:-2]+('',)+data[-1:]
        if data[-2]: lstTests.extend( (data,data,clean) )  # 1) break test.it loop / 2) create test.describe / 3) test.it again
        else:        lstTests.append(data)
    
    iterTests = iter(lstTests)        # share the linear data between the different loops
    next(iterTests)                   # consume the useless first data
    
    for _,_,_,desc,_ in iterTests:
        assert desc, "No test.describe(...) message!"
        
        @test.describe(desc)
        def _():
            for draw,molec,exp,desc,msg in iterTests:
                if desc: break
                    
                @test.it(msg or molec)
                def _():
                    print(draw)
                    print(molec, "=", sorted(exp.items()))
                    
                    actual = ParseHer(molec).parse()
                    test.assert_equals(actual, exp, molec)
    
doFixedTests()



  
@test.describe("Random tests")
def _():
    
    from random import sample, randrange as rand
    from collections import Counter, defaultdict
    from operator import attrgetter
    import re
    
    
    class MyChemFunc(Counter):
    
        SINGLETONS = {}                                                                     # Dict of singletons representing all the possible parts of a name (except the positions)
        ARCHIVING  = False                                                                  # Will archive all new ChemFun instances as singletons if True
        
        def __new__(cls, *args,**kwargs):
            obj = super().__new__(cls)
            if MyChemFunc.ARCHIVING:
                for name in kwargs.get('name', ()):
                    MyChemFunc.SINGLETONS[name] = obj                                       # Archive the singleton under all the possible names of the function/part
            return obj
            
        def __init__(self, iterable={}, **kwargs):
            super().__init__(iterable)
            self.name = ''
            defDct = {'name': ()}
            defDct.update(kwargs)
            self.__dict__.update(defDct)
        
        
        def expandHydrogens(self):  return self + self.SINGLETONS['H'] * ( 2*self['C'] + 2 )
        def __repr__(self):        return "MyChemFunc({}, {})".format(self.name, list(self.items()))
        def __str__(self):         return "MyChemFunc({})".format(list(self.items()))
        
        def __mul__(self, n):
            if isinstance(n, int):
                return self.__class__({k: v*n for k,v in self.items()})
                
            elif not isinstance(n, Multiplier):
                raise Exception("MyChemFunc objects cannot be multiplied by {} objects/values other than int or Multipliers".format(n))
            
        def __add__(self, other):
            if not other: other = MyChemFunc({})                                              # Handle the default value passed in for "sum([list of MyChemFuncs])"
            return self.__class__({k: self[k] + other[k] for k in set(self)|set(other) })   # Merge the keys and make the addition of the two objects
            
        __imul__ = __rmul__ = __mul__
        __iadd__ = __radd__ = __add__
        __isub__ = __rsub__ = __sub__ = Counter.subtract
        
        
    
    
    DEBUG       = False
    
    
    MAX_DEPTH   = 4             # Maximal depth for the number of carboned chain ('lvl'). Do not apply on prefixes that REQUIRE carbon chains (sometimes ends up with depths of 10... :/ )
    VOID_CF     = MyChemFunc()
    
    RADICALS    = ["", "meth", "eth", "prop", "but",   "pent",  "hex",  "hept",  "oct",  "non",  "dec",  "undec",  "dodec",  "tridec",  "tetradec",  "pentadec",  "hexadec",  "heptadec",  "octadec",  "nonadec"]
    MULTIPLIERS = ["",  "",    "di",  "tri",  "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca", "undeca", "dodeca", "trideca", "tetradeca", "pentadeca", "hexadeca", "heptadeca", "octadeca", "nonadeca"]
    
    
    
    """
    ABOUT SUFFIXES:
            A  = posNeed = Position conditions:     (used only for the main chains and the mutliple bounds. Prefixes functions are not concerned with this)
                                1 = at an extremity
                                0 = no constraint   
                               -1 = at neither of the extremities
                               -2 = not at the end
            B  = valNeed  = valence needed on the carbon holding
            B2 = val4Pref = same as valNeed, but for the prefixes
            C  = subNeed  = [a,b): possible number of subchains to ADD for a PREFIX, as boundaries for randrange(a,b).
                            (values consistent with the use of the functions as prefixes, so need one more for "ether" 
                            and "amine" as primary function/"chain" = in "AlkylWay")
            D  = maxN     = max number of function per chain (-1 -> no limit except the available valences: will be 
                            converted to Integer.MAX_VALUE in the constructor)
        
        Suffixes with empty names are not used
        """
                #   SUFFIX            A        B      B2         C         D       PREFIX
    SUFFIXES = (("oic acid",        1,       3,     1,         (),       2,     "carboxy"    ),      # 0
                ("oate",            1,       3,     1,      (1,2),       2,     "oxycarbonyl"),      # 1
                ("oate",            1,       3,     1,      (1,2),       2,     "oyloxy"     ),      # 2
                ("amide",           1,       3,     1,         (),       2,     "amido"      ),      # 3
                ("al",              1,       3,     1,         (),       2,     "formyl"     ),      # 4
                ("one",            -1,       2,     2,         (),      -1,     "oxo"        ),      # 5
                ("ol",              0,       1,     1,         (),      -1,     "hydroxy"    ),      # 6
                ("thiol",           0,       1,     1,         (),      -1,     "mercapto"   ),      # 7
                ("amine",           0,       1,     1,      (0,3),      -1,     "amino"      ),      # 8
                ("imine",           1,       2,     2,         (),      -1,     "imino"      ),      # 9
                ("ether",          -1,       1,     1,      (1,2),      -1,     "oxy"        ),      # 10
                ("",                0,       1,     1,         (),      -1,     "phenyl"     ),      # 11
                ("phosphine",       0,       1,     1,      (0,3),      -1,     "phosphino"  ),      # 12
                ("arsine",          0,       1,     1,      (0,3),      -1,     "arsino"     ),      # 13
                ("",                0,       1,     1,         (),      -1,     "fluoro"     ),      # 14
                ("",                0,       1,     1,         (),      -1,     "chloro"     ),      # 15
                ("",                0,       1,     1,         (),      -1,     "bromo"      ),      # 16
                ("",                0,       1,     1,         (),      -1,     "iodo"       ),      # 17
               )
                
    
    AN_EN_YN_YL = (("e",            0,       0,     1,         (),       0,     "WRONG"      ),
                   ("en",          -2,       1,     1,         (),      -1,     "WRONG"      ),
                   ("yn",          -2,       2,     2,         (),      -1,     "WRONG"      ),
                   ("WRONG",       -1,       1,     1,         (),      -1,     "yl"         ),
                  )
    
    SUFF, POSNEED, VALNEED, VAL4PREF, SUBNEED, MAXN, PREF = range(len(SUFFIXES[0]))       # constants to call easily the data in SUFFIXES
    
    
    
    SPECIAL_PREF_POS_NEEDS  = {"oxo":2, "imino":2}                      # To add those ones, a special check of the available valences is needed
    
    REQUIRE_ALKYLWAY        = ("ether",)                                # Always in "alkylway"
    MIGHT_REQUIRE_ALKYLWAY  = ("amine", "phosphine", "arsine")          # In alkyl way or alkan way... (randomly)
    REQUIRE_AUX_WITHOUT_YL  = ("oxycarbonyl", "oyloxy", "oxy")          # The terminal "yl" at the end of the name of the subparts will be removed in those cases
    
    
    def thrower(): raise Exception("Not yet implemented")
    
    
    
    
    
    
    
    
    class Builder(object):
        
        # Utilities:
        C     = MyChemFunc({"C": 1})
        N     = MyChemFunc({"N": 1, "H": 1})
        O     = MyChemFunc({"O": 1})
        insat = MyChemFunc({"H": -2})
        
        S     = MyChemFunc({"S":  1})
        As    = MyChemFunc({"As": 1, "H": 1})
        P     = MyChemFunc({"P":  1, "H": 1})
    
    
        #=======================
        # SINGLETONS definitions
    
        MyChemFunc.ARCHIVING = True
        
        
        MyChemFunc({"F":  1, "H": -1},  name=("fluoro",))
        MyChemFunc({"Cl": 1, "H": -1},  name=("chloro",))
        MyChemFunc({"Br": 1, "H": -1},  name=("bromo",))
        MyChemFunc({"I":  1, "H": -1},  name=("iodo",))
        
        H = MyChemFunc({"H": 1},    name='H')                        # needed for the implementation of closeHydrogen in the MyChemFunc class (not done this way in the soluiton because of the parser/regexp built)
        
        MyChemFunc(insat,           name=("cyclo",))
        
        MyChemFunc(insat,           name=("ene", "en"))
        MyChemFunc(insat+insat,     name=("yne", "yn"))
        
        MyChemFunc({},              name=("ane", "an"))
        MyChemFunc({},              name=("yl",))
        
        MyChemFunc(O,               name=("ol",    "hydroxy"))
        MyChemFunc(O,               name=("ether", "oxy"))
        MyChemFunc(O+insat,         name=("al",))
        MyChemFunc(O+insat,         name=("one",   "oxo"))
        
        MyChemFunc(O+O+insat,       name=("oic acid",))
        MyChemFunc(O+O+insat,       name=("oate",))
        
        MyChemFunc(N,               name=("amine", "amino"))
        MyChemFunc(N+O+insat,       name=("amide", "amido"))
        
        MyChemFunc(C+O+insat,       name=("formyl",))
        MyChemFunc(N+insat,         name=("imino",   "imine"))
        MyChemFunc(6*C+4*insat,     name=("benzene", "phenyl"))
        
        MyChemFunc(S,               name=("thiol",           "mercapto"))
        MyChemFunc(C+O+O+insat,     name=("carboxylic acid", "carboxy"))
        MyChemFunc(C+O+O+insat,     name=("oxycarbonyl",))
        MyChemFunc(O+O+insat,       name=("oyloxy",))
        
        MyChemFunc(As,              name=("arsine",    "arsino"))
        MyChemFunc(P,               name=("phosphine", "phosphino"))
    
        
        for nC,rad in enumerate(RADICALS[1:], 1):    MyChemFunc({"C": nC}, name=(rad,))
        
        del C,N,O,insat,S,As,P,nC,rad                   # Clean up to ease the debugging
        
        MyChemFunc.ARCHIVING = False
        
        SG = MyChemFunc.SINGLETONS
        
        
        # End of SINGLETONS defintions
        #=============================
        
        
        
        def __init__(self, inLine=False):
            
            self.name           = ''                # Name of the current part
            self.mult           = 1                 # multiplier...
            self.lvl            = 1                 # Depth of the current chain:  lvl==1 means alkane (main chain), lvl>1  means alkyle
            self.funcPrior      = 0                 # Index of the top priority main function. Increase (in value, so decrease in priority) when going deeper in the structure
            self.pos            = []                # Positions for this part on the related parent carbon chain (elisions handled when generating the positions)
            self.parent         = VOID              # Upper level builder (necessary to update the positions and multipliers for the main functions)
            self.cf             = VOID_CF           # (could be removed because never used but ease the way for debugging)
    
            self.children       = []                # All children of this Builder instances...
            self.nChildren      = 0                 # Define the number of children that will be generated afterward
    
            self.isInLine       = inLine            # Forbid a name containning squared brackets
            self.hasCyclo       = False             # Tells if a cycle is present at an upper level
            self.hasEn          = False             # Tells if a double bound is present at an upper level
            self.hasYn          = False             # Tells if a triple bound is present at an upper level
        
    
        #def __hash__(self): return hash(self.__class__.__name__)
    
    
    
        """
        **************************
            BUILDING FUNCTIONS
        **************************
        """
    
        def buildNext(self):              thrower()
    
        def gotEn(self):    self.hasEn    = True
        def gotYn(self):    self.hasYn    = True
        def gotCyclo(self): self.hasCyclo = True
        
        def chooseFunc(self, prior=None): return rand(self.funcPrior if prior is None else prior, len(SUFFIXES))
        
    
        def buildCarbChildren(self):
            """ Used for functions needing carboned subchains only, and that won't need any positional informations,
                meaning: ehter, oxy, amine, amino, carbonyloxy, ...
                (info hold by the prefix that is itself holding the CarbChain instances that will be generated here...
                 if you follow me... ;/ )
            """
            lst, count = [], 0
            while count < self.nChildren:
                nChild = 1 + rand(self.nChildren-count)             # Peek a multiplier for "that" child
                child  = CarbChain(self, nChild).buildNext()        # Build it!
                count += nChild                                     # Update count of already built children
                lst.append(child)                                   # Archive
            
            return lst
    
    
    
        """
        ***************************
            GETTERS & OBSERVERS
        ***************************
        """
    
        def isAnoylOxy(self):   return self.name == 'oyloxy'
        def isAlkylWay(self):   return isinstance(self, AlkylWay)
        def isEster(self):      return isinstance(self, Ester)
    
        def getData(self):      return SUFFIXES[self.funcPrior]
        def getValNeed(self):   thrower()
        def getAuxName(self):   thrower()
    
        def getCF(self):        return (self.getCFfromSG() + self.getChildrenCF()) * self.mult
        def getCFfromSG(self):  self.cf = Builder.SG.get(self.name, VOID_CF) ; return self.cf
        
        def getChildrenCF(self, lst=None):
            if lst is None: lst=self.children
            return sum(x.getCF() for x in lst)
    
    
        def getName(self):  
            return self.getPosStr() + MULTIPLIERS[self.mult] + self.getChildrenNames() + self.name
        
        def getPosStr(self):
            possibleElision = len(set(self.pos)) == 1 and self.pos[0]==0
            return ','.join(str(p+1) for p in self.pos) * (not possibleElision or not rand(3))        # Elision 2 times over 3 if possible
        
        def getChildrenNames(self, lst=None):
            if lst is None: lst=self.children
            return ''.join(x.getName() for x in sorted(lst, key=attrgetter('name')))
        
    
        
        def genOccupiedValences(self, pos=None, v=None):
            if pos is None: pos = self.pos
            if v is None:   v   = self.getValNeed()
            for p in pos: yield p,v
    
    
        def constrainValencesInSub(self):            # By default, all subchains are linked by one single bound to the parent function
            yield 0,1
    
    
    
    
        """
        ***************************
              STATS FUNCTIONS
                (debugging)
        ***************************
        """
    
        def getMaxDepth(self):      return max([self.lvl] + [c.getMaxDepth() for c in self.children])
        def getMaxBranches(self):   return max([len(self.children)] + [c.getMaxBranches() for c in self.children])
    
    
        def __str__(self):  return """                  
    STATE:
    name:   {}
    mult:   {}
    pos:    {}
    lvl:    {}
    prior:  {}
    upper:  {}
    cf:     {}
    ----
    """.format(self.name, self.mult, self.pos, self.lvl, self.funcPrior, self.parent, self.cf)
        
    
    
    
    
    VOID = None             # Temporary declaration... :/ (Java is better, for static variables with a complete tree hierarchy... :// )
    
    class Void(Builder):
        def getCF(self):        return VOID_CF
        def getName(self):      return ""
        def buildNext(self):    return self
        def doNotNeedYl(self):  return False
        def __bool__(self):     return True
        def constrainValencesInSub(self): thrower()
    
    
    
    VOID = Void()
    
    
    
    
    class Root(Builder):
        def getCF(self):     return dict(super().getCF().expandHydrogens())
        def getName(self):   return self.insertDashes( super().getName() )
    
        def insertDashes(self, s): return re.sub(r'(?<=\d)(?=[a-z[])|(?<=[a-z])(?=\d)', '-', s)
    
        def buildNext(self):
            self.children = [ CarbChain(self).buildNext() ]
            return self
    
        def constrainValencesInSub(self):             # Root instance isn't a regular parent
            return
            yield 0                                   # needed so that the compiler identify the fonction as a generator
    
    
    
    
    
    
    
    class Transcient(Builder):
        """
        Relay class, to have a general constructor that updates "automatically" 
        the information of the child object according to the parent's ones.
        """
    
        TO_UPDATE = ('funcPrior', 'hasCyclo', 'hasEn', 'hasYn', 'lvl')
    
        def __init__(self, parent):
            super().__init__(parent.isInLine)
            self.parent = parent
            for att in Transcient.TO_UPDATE:                self.__dict__[att] = parent.__dict__[att]
            if (isinstance(parent, (CarbChain,PrefFunc) )): self.lvl += 1
            
        def buildNext(self):
            self.children = self.buildCarbChildren()
            return self
    
    
    
    
    
    class Tail(Transcient):
        
        def __init__(self, parent, fd, mult, isPref, pos):
            super().__init__(parent)
            self.config = fd
            self.name   = fd[PREF] if isPref else fd[SUFF]
            self.isPref = isPref
            self.mult   = mult
            self.pos    = pos
            self.nChildren = fd[SUBNEED] and rand(*fd[SUBNEED]) or 0
    
    
        def getData(self):      return self.config
        def getValNeed(self):   return self.config[VAL4PREF if self.isPref else VALNEED]
        def doNotNeedYl(self):  return False
        
        def getName(self):
            s = self.getChildrenNames()
            if s and not self.isAlkylWay() and not self.doNotNeedYl():
                s = "["+s+"]"
            return ''.join((self.getPosStr(), MULTIPLIERS[self.mult], s, self.name))
        
    
    
    class Alkane(Tail):
        def __init__(self, parent):                 super().__init__(parent, AN_EN_YN_YL[0], 1, False, [])
    
    class Alkyl(Tail): 
        def __init__(self, parent):                 super().__init__(parent, AN_EN_YN_YL[3], 1, True, [])
    
    class MainFunc(Tail):
        def __init__(self, parent, fd, mult, pos):  super().__init__(parent, fd, mult, False, pos)
    
    class PrefFunc(Tail): 
        def __init__(self, parent, fd, mult, pos):  super().__init__(parent, fd, mult, True, pos)
        def doNotNeedYl(self):                      return self.name in REQUIRE_AUX_WITHOUT_YL
        
        def constrainValencesInSub(self):
            if   self.name=="oylxy": yield 0,3
            else: yield from super().constrainValencesInSub()
    
    class Ester(MainFunc):
        def getName(self):    return self.getPosStr() + MULTIPLIERS[self.mult] + self.name
        def getAuxName(self): return self.getChildrenNames()
        
    
    class AlkylWay(Tail):
        def __init__(self, parent, fd):
            super().__init__(parent, fd, 1, False, [])
            self.nChildren += 1                                     # Need to add one child when representing a main function in "alkyl way" (see SUFFIXES description)
    
        def buildNext(self):
            super().buildNext()
            if (len(self.children) == 1
                    and self.children[0].mult == 3
                    and self.children[0].name == "dec"):            # Avoid the generation of ambiguous matches ("tri-decylamine" instead of "tridecylamine")
                self.children[0].mult = 2
                self.nChildren -= 1
            return self
    
            
    
    
    
    
    
    
    
    
    class Modifier(Transcient):
        GET_DATA_IDX = 100                          # Would throw an error (wanted)
    
        def __init__(self, parent, pos):
            super().__init__(parent)
            self.pos  = pos
            self.mult = len(pos)
    
        def buildNext(self): return self
        def getData(self):   return AN_EN_YN_YL[self.GET_DATA_IDX]
    
        def genOccupiedValences(self,pos=None,v=None):
            """ generator for multiple bond only """
            for p,v in super().genOccupiedValences(pos,v):
                yield p,v
                yield p+1,v
    
    
    
    class Alkene(Modifier):
        GET_DATA_IDX = 1
    
        def __init__(self, parent, pos):
            super().__init__(parent, pos)
            self.name = "en"
            parent.gotEn()
    
        def getValNeed(self): return 1
    
    
    class Alkyne(Modifier): 
        GET_DATA_IDX = 2
    
        def __init__(self, parent, pos):
            super().__init__(parent, pos)
            self.name = "yn"
            parent.gotYn()
            
        def getValNeed(self): return 2
    
    
    class Cyclo(Modifier):
        def __init__(self, parent):
            super().__init__(parent, [])
            self.name = "cyclo"
            self.mult = 1
            parent.gotCyclo()
    
        def genOccupiedValences(self,pos=None,v=None):
            assert pos is None and v is None, 'cannot call genOccupiedValences for a Cyclo instance with specified positions or needed valence as arguments'
            yield 0,1
            yield -1,1
    
    
    
    
    
    
    class CarbChain(Transcient):
    
        def __init__(self, parent, mult=None, pos=None):
            super().__init__(parent)
            if mult is not None: self.mult = mult
            if pos  is not None: self.pos  = pos
            self.cyclo  = VOID
            self.tail   = VOID
            self.AnEnYn = []
    
        
        """ 
        ***********************
            GENERAL METHODS
        ***********************
        """
        
        def getValNeed(self): return 1
    
        def getCF(self):
            return ( self.getCFfromSG()
                   + self.getChildrenCF()
                   + self.cyclo.getCF()
                   + self.getChildrenCF(self.AnEnYn)
                   + self.tail.getCF() 
                     ) * self.mult
    
    
        def getName(self):
            head        = self.tail.getAuxName()+" " if self.tail.isEster() else ""
            childrenStr = self.getChildrenNames()
            modifiers   = self.getChildrenNames(self.AnEnYn)
    
            if not (self.lvl==1 or not self.children or self.tail.doNotNeedYl()):
                childrenStr = "["+childrenStr+"]"
            
            if not self.AnEnYn and (self.lvl==1 and self.name or self.parent.isAnoylOxy()):
                modifiers = "an"
            
            return ''.join([head,
                            self.getPosStr(),
                            MULTIPLIERS[self.mult],
                            childrenStr,
                            self.cyclo.getName(),
                            self.name,
                            modifiers,
                            self.tail.getName()])
        
    
        def buildNext(self):
            self.buildChain()
            self.constraintValenceAccordingToParent()
            self.makeTail()
            if self.tail.isAlkylWay():
                 return self
            self.makeCyclo()
            self.makeAnEnYn()
            self.makeSubParts()
            return self
        
        
        """ 
        ************************
            SPECIFIC METHODS
        ************************
        """
        
        def updateValences(self, that):
            was = self.valences[:]                                # debugging purpose
            for p,v in that.genOccupiedValences():
                self.valences[p] -= v
                assert self.valences[p]>=0, f'was: {was}, became: {self.valences} (p,v={p},{v})\n\nself=\n"{self}\n\nthat=\n{that}"'
    
    
        def buildChain(self):
            self.nC           = rand(1 + (self.lvl==1), len(RADICALS))              # Frobid the building of "methane" (useless and too many possible problems with it)
            self.name         = RADICALS[self.nC]
            self.valences     = [2] * self.nC                                       # Make a chain of ...-CH2-...
            self.valences[0]  = 3                                                   # Free start
            self.valences[-1] = 3                                                   # Free end
            """
            self.valences[0] += self.lvl == 1                                       # Free start at level 1, otherwise the first carbon is linked to the upper level
            if self.parent.isAnoylOxy(): self.valences[0] = 0                       # If the holding parent is of "oyloxy" kind, the "=O" double bound on the first carbon makes it unable to do other bounds.
            """
        
        def constraintValenceAccordingToParent(self):
            for p,v in self.parent.constrainValencesInSub():
                self.valences[p]-=v
        
        def makeTail(self):
            
            if self.lvl==1:
                
                self.funcPrior = self.chooseFunc()                                  # Peek a suffix index
                fd             = self.getData()
                funcName       = fd[SUFF]
                funcPos        = self.genPos(100, fd, 5 if rand(4) else 20, False)  # Limit the max number of functions to 20 one time over four, otherwise 5 max.
                
                if funcName in MIGHT_REQUIRE_ALKYLWAY and rand(100) < 50 or funcName in REQUIRE_ALKYLWAY:
                    self.tail  = AlkylWay(self, fd).buildNext()
    
                    self.name  = ''                                                 # Clean up/empty the current CarbChain instance
                    self.pos   = []
                    self.mult  = 1
                    self.nC    = 0
                    self.nChildren = 0
                    self.valences  = []
    
                
                elif funcName == "oate":
                    self.tail  = Ester(self, fd, len(funcPos), funcPos).buildNext()
                
                elif not funcName or not funcPos:
                    self.funcPrior = len(SUFFIXES)-4                                # Allow only halogens
                    self.tail      = Alkane(self).buildNext()
    
                else:
                    self.tail = MainFunc(self, fd, len(funcPos), funcPos)
    
            
            elif self.parent.name not in REQUIRE_AUX_WITHOUT_YL:                    # If lvl > 1: automatically add the "yl" termination, unless the parent doesn't need it
                self.tail = Alkyl(self)
            
    
            if self.tail is not VOID: self.updateValences(self.tail)
            
    
        
        def makeCyclo(self):
            
            if (self.lvl!=1 and not (self.hasCyclo or self.hasEn or self.hasYn)     # Forbid new cycles in molecule that have neither alkenes, akynes nor cycles at an upper level
                 or self.nC < 3                                                     # Forbid cycles for too short chains
                 or self.valences[0] == 0 or self.valences[-1] == 0                 # Forbid cycles if extremities aren't free (carboxylic acid, for example)
                 or rand(100) > 50/self.lvl):                                       # Finally, skip cycles randomly, according the the depth/lvl of the chain
                return
            
            self.cyclo = Cyclo(self)
            self.updateValences(self.cyclo)
    
    
    
        def makeAnEnYn(self):
            
            if self.lvl!=1 and not (self.hasEn or self.hasYn): return               # Forbid new insaturations in molecule that have neither alkenes, akynes nor cycles at an upper level
    
            for i,klass in enumerate( (Alkene,Alkyne), 1):
                
                fd     = AN_EN_YN_YL[i]
                cndPos = [] if rand(100) > 50 else self.genPos(50, fd, 5)
    
                if not cndPos or i == 2 and self.lvl != 1 and not self.hasYn:       # Skip alkynes of not present in an upper part or empty array of positions
                    continue
    
                if i==1: cndPos = sorted(set(cndPos))                               # Forbid two double bound at the same position (mathematically possible but would actually be a triple bound
                
                vals,filteredPos = self.valences[:], []
                for p in cndPos:
                    if vals[p] >= fd[VALNEED] and vals[p+1] >= fd[VALNEED]:
                        filteredPos.append(p)
                        vals[p]-=1
                        vals[p+1]-=1
                
                if filteredPos:
                    multiBond = klass(self, filteredPos).buildNext()
                    self.AnEnYn.append(multiBond)
                    self.updateValences(multiBond)
    
    
        
        def makeSubParts(self):
            
            if (self.isInLine and self.lvl > 1                                      # Forbid more than 2 levels of carbon chains if is "in line"
                    or rand(100) < 10                                               # Skip subparts in 1 case out of ten
                    or self.lvl == MAX_DEPTH):                                      # Forbid too much depth in the tree
                return
            
    
            seens     = set()                                                       # Already encountered subparts (other than CarbChains)
            isChain   = False                                                       # Define if the subpart choosen will be replaced by a carbon chain or not
            iSub      = 0                                                           # Index of the subpart FuncData to be...
            available = sum(self.valences)                                          # Total number of available valences
            nRndSub   = rand(min(4,self.nC+1)) if not self.isInLine else \
                        rand( min(available//2, self.nC//2), available+1 )            # Number of subparts to (try to) add (much more if inline)
    
            for _ in range(nRndSub):
                
                while len(seens) < len(SUFFIXES):                                   # Global aborting condition (avoiding infinite loop, even if unlikely)
                    iSub    = self.chooseFunc(0)                                    # Peek a prefix/suffix
                    isChain = iSub <= self.funcPrior                                # If prefix has to high priority (meaning, too low value...), replace it with a chain
    
                    if iSub not in seens:                                           # Archive already used prefixes to avoid duplicates (don't care about the chains.... even if...)
                        if not isChain: seens.add(iSub)
                        break
                
                fd  = AN_EN_YN_YL[3] if isChain else SUFFIXES[iSub]
                pos = self.genPos(100, fd, rand(min(self.nC+1, 8)))
    
                if pos:
                    partToAdd = (CarbChain(self, len(pos), pos)
                                    if isChain else
                                 PrefFunc(self, fd, max(1,len(pos)), pos) ).buildNext()
    
                    self.updateValences(partToAdd)
                    self.children.append(partToAdd)
                    self.nChildren += 1
    
    
    
        def genPos(self, proba, fd, limit=1000, isPref=True):
            
            pos     = []
            name    = fd[SUFF] if isPref else fd[PREF]
            valNeed = fd[VAL4PREF] if isPref else fd[VALNEED]
            posNeed = SPECIAL_PREF_POS_NEEDS.get(name, fd[POSNEED])
            maxNF   = min(limit,
                          limit if fd[MAXN]==-1 else fd[MAXN],
                          sum(self.valences) // (2*valNeed),
                          len(MULTIPLIERS)-1 )
            
            if maxNF and rand(100) < proba:
                nF = rand(1,maxNF+1)
    
                if posNeed == 1:
                    pos = [p for p in (0, self.nC-1) if self.valences[p] >= valNeed][:nF]
                
                else:
                    rng = ( range(self.nC-1)   if posNeed == -2 else                # Not at the end...
                            range(1,self.nC-1) if posNeed == -1 else                # Not any extremity...
                            range(self.nC) )                                        # ... or anywhere
    
                    availablePos = [p for p in rng for _ in range(self.valences[p]//valNeed)]
                    pos          = sorted( sample(availablePos, min(len(availablePos),nF)) )
    
            return pos
    
    
    
    
    
    
    
    
    if True:
        N_TESTS, MAX_FAILED = 5500, 20
        WITH_STATS = False
    
        if WITH_STATS:
            c, cAlkylWay, cDepth, cBranch = Counter(), Counter(), defaultdict(list), defaultdict(list)
    
        @test.it("{} random tests...".format(N_TESTS))
        def _():
            
            nFailed = 0
            for n in range(1,1+N_TESTS):
                her  = Root(n%3==0).buildNext()
                exp  = her.getCF()
                name = her.getName()
        
                if WITH_STATS:
                    tailName = her.children[0].tail.name
        
                    c[tailName] += 1
                    cDepth[tailName].append(her.getMaxDepth())
                    cBranch[tailName].append(her.getMaxBranches())
        
                    if her.children[0].tail.funcPrior in (8,10,12,13):
                        cAlkylWay[(tailName, her.children[0].tail.isAlkylWay())] += 1
                
        
                act  = ParseHer(name).parse()
        
                if act != exp:
                    nFailed += 1
                    test.assert_equals(act, exp, name)
                if nFailed > MAX_FAILED: break
        
            test.expect(True)
            print("{}/{} random tests done{}.".format(n, N_TESTS, ' (tests aborted because too much failures)' * (n!=N_TESTS)))
            
        
        if WITH_STATS:
            print('\n'.join(map(str, sorted(c.items()))))
            print("-----")
            print('\n'.join(map(str, sorted(cAlkylWay.items()))))
            print("-----")
            print('\n'.join(map(str, sorted(cDepth.items()))))
            print("-----")
            print('\n'.join(map(str, sorted(cBranch.items()))))
        
        
