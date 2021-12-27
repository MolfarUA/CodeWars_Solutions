import java.util.*;
import java.util.stream.*;
import java.util.regex.*;



public class ParseHer {
                                 //  Number      :   1       2      3...
    final static private String[]    RADICALS    = {"meth", "eth", "prop", "but",   "pent",  "hex",  "hept",  "oct",  "non",  "dec",  "undec",  "dodec",  "tridec",  "tetradec",  "pentadec",  "hexadec",  "heptadec",  "octadec",  "nonadec"},
                                     MULTIPLIERS = {        "di",  "tri",  "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca", "undeca", "dodeca", "trideca", "tetradeca", "pentadeca", "hexadeca", "heptadeca", "octadeca", "nonadeca"};

    
    // Grammar related enumerator:
    private static enum Gram { 
                ROOT,                // Start of a new chain, or function or subfunction, ... = a big part that can be multiplied as a whole
                BLOCK,               // Intermediate modifiers (like alkenes, akynes,...) that can have multipliers/positions. Distinction needed with ROOT to handle correctly the elisions.
                MULT,                // Multiplier...
                NONE };              // No special behavior here (meaning: cannot not be affected by a multiplier otherwise than through a full "ROOT" part
    
    final static private Pattern     P_STR_CF      = Pattern.compile("([a-zA-Z]+)(-?\\d+)"),        // used to define the Chemfunc instances
                                     REV_TOKENIZER;
    
    
    final static private String      REV_POS_S = "-\\d+(?:,\\d+)*(?:-|$|(?=[ \\[]))";

    
    // TO_SANITIZE: names where the tokenizer will have to be carful, to correctly match the 2-tridecyl from 1,1,1-TRIcedycl:
    final static private Set<String> TO_SANITIZE = Arrays.asList("tridec", "tetradec", "pentadec", "hexadec", "heptadec", "octadec", "nonadec")
                                                         .stream()
                                                         .collect(Collectors.toSet());
    
    
    /* SG: store all the singletons ChemFunc instances that will be used as bases for the parsing.
     *          key   = part of the name of the molecule
     *          value = related ChemFunc/Multiplier singleton instance */
    final static private Map<String,ChemFunc> SG = new HashMap<String,ChemFunc>();
    
    
    final static private ChemFunc H, C, N, O, insat, OOinsat,
                                  VOID = new ChemFunc();                   // Default name part/Multiplier
    static {
        
        /*  Utilities  */
        H     = new ChemFunc("H1");
        C     = new ChemFunc("C1");
        N     = new ChemFunc("N1,H1");
        O     = new ChemFunc("O1");
        insat = new ChemFunc("H-2");
        OOinsat = O.add(O).add(insat);
        
        
        /*-------------------------------
         *     SINGLETONS DEFINITION
         * meaning: calls with grammar
         *         and names information
         *-------------------------------*/
        
        
        List<Gram> gramLst = Arrays.asList(Gram.NONE);
        
        new ChemFunc(insat,                         gramLst,    Arrays.asList("cyclo"));
        new ChemFunc("",                            gramLst,    Arrays.asList("an"));
        
        gramLst = Arrays.asList(Gram.BLOCK);
        
        new ChemFunc(insat,                         gramLst,    Arrays.asList("en"));
        new ChemFunc(insat.mul(2),                  gramLst,    Arrays.asList("yn"));
        
        new ChemFunc("F1,H-1",                      gramLst,    Arrays.asList("fluoro"));
        new ChemFunc("Cl1,H-1",                     gramLst,    Arrays.asList("chloro"));
        new ChemFunc("Br1,H-1",                     gramLst,    Arrays.asList("bromo"));
        new ChemFunc("I1,H-1",                      gramLst,    Arrays.asList("iodo"));
        new ChemFunc(C.add(O).add(insat),           gramLst,    Arrays.asList("formyl"));
        
        gramLst = Arrays.asList(Gram.ROOT);
        
        new ChemFunc("",                            gramLst,    Arrays.asList("e"));
        new ChemFunc("",                            gramLst,    Arrays.asList("yl"));
        new ChemFunc(O.add(insat),                  gramLst,    Arrays.asList("al"));
        new ChemFunc(OOinsat,                       gramLst,    Arrays.asList("oic acid"));
        new ChemFunc(OOinsat,                       gramLst,    Arrays.asList("oate"));
        new ChemFunc(OOinsat,                       gramLst,    Arrays.asList("oyloxy"));
        new ChemFunc(OOinsat.add(C),                gramLst,    Arrays.asList("oxycarbonyl"));
        
        gramLst = Arrays.asList(Gram.ROOT, Gram.BLOCK);

        new ChemFunc(O,                             gramLst,    Arrays.asList("ol",               "hydroxy"));
        new ChemFunc(insat.add(O),                  gramLst,    Arrays.asList("one",              "oxo"));
        new ChemFunc(insat.add(N),                  gramLst,    Arrays.asList("imine",            "imino"));
        new ChemFunc(C.mul(6).add(insat.mul(4)),    gramLst,    Arrays.asList("benzene",          "phenyl"));
        new ChemFunc("S1",                          gramLst,    Arrays.asList("thiol",            "mercapto"));
        new ChemFunc(OOinsat.add(C),                gramLst,    Arrays.asList("carboxylic acid",  "carboxy"));
        
        
        gramLst = Arrays.asList(Gram.ROOT, Gram.ROOT);
        
        new ChemFunc(N,                             gramLst,    Arrays.asList("amine",            "amino"));
        new ChemFunc(insat.add(N).add(O),           gramLst,    Arrays.asList("amide",            "amido"));
        new ChemFunc("As1,H1",                      gramLst,    Arrays.asList("arsine",           "arsino"));
        new ChemFunc("P1,H1",                       gramLst,    Arrays.asList("phosphine",        "phosphino"));
        new ChemFunc(O,                             gramLst,    Arrays.asList("ether",            "oxy"));
        
        
        List<Gram> gramNone = Arrays.asList(Gram.NONE);
        
        IntStream.range(0, RADICALS.length   ).forEach( i -> new ChemFunc("C"+(i+1), gramNone, Arrays.asList(RADICALS[i])) );
        IntStream.range(0, MULTIPLIERS.length).forEach( i -> new Multiplier(i+2, MULTIPLIERS[i]) );
        
        REV_TOKENIZER = initialize_ReversedTokenizer();
    }
    
    
    private String   name;                                  // Name of the molecule
    private String[] parts;                                 // {auxiliary chain of esters (if exist), main part of the name}
    
    public ParseHer(String name) {
        this.name = name;
        parts = name.split("(?<=yl) ");
    }
    
    @Override public String toString() { return name; }

    
    /*  TOKENIZER METHODS: generating the reversed tokenizer */
    
    private static int cmpReg(String s1, String s2) {                           // Longest first, then lexicographic
        return s1.length() != s2.length() ? s2.length() - s1.length()
                                          : s1.compareTo(s2);
    }
    
    private static String revSanitizer(String s) {
        StringBuilder sb = new StringBuilder(s).reverse();
        if      (s.equals("dodec"))       sb.append("(?!ima|oi)");              // Needed to avoid matching conflicts between "iododecane" and "io-dodecane" (same with amido)
        else if (TO_SANITIZE.contains(s)) sb.append("(?!-\\d+,)");              // Avoid matching -1,2,3-tridec, -1,1,2,3-tetradec,... as tridecane, tetradecane, ...
        return sb.toString();
    }
    
    private static Pattern initialize_ReversedTokenizer() {
        String toks_RootBlock = SG.keySet().stream().filter( sk -> SG.get(sk).isRootBlock() ).sorted(ParseHer::cmpReg).map(ParseHer::revSanitizer).collect(Collectors.joining("|")),
               toks_Mult      = SG.keySet().stream().filter( sk -> SG.get(sk).isMult()      ).sorted(ParseHer::cmpReg).map(ParseHer::revSanitizer).collect(Collectors.joining("|")),
               toks_others    = SG.keySet().stream().filter( sk -> SG.get(sk).isDefault()   ).sorted(ParseHer::cmpReg).map(ParseHer::revSanitizer).collect(Collectors.joining("|")),
               
               pattern        = String.join("|", Arrays.asList("\\[|\\]| ",
                                                               toks_others, 
                                                               String.format("(%s)?(%s)?(%s)?", toks_RootBlock, toks_Mult, REV_POS_S), 
                                                               "."));           //  garbage matching: to see any matching problem in the tokenizer (won't skip any character in the name)
        return Pattern.compile(pattern);
    }    
    
    
    
    /*   PARSING METHODS   */
    
    public  ChemFunc parse()                       { return expandHydrogens( actualParser(genTokens()) ); }
    
    private String   reverse(String s)             { return "" + new StringBuilder(s).reverse();        }
    private Matcher  genTokens()                   { return genTokens(parts.length-1);                  }
    private Matcher  genTokens(int idx)            { return REV_TOKENIZER.matcher(reverse(parts[idx])); }
    private ChemFunc expandHydrogens(ChemFunc  cf) { return cf.add( H.mul( 2*cf.get("C")+2 ) );         }    // Finalize the raw formula, adding the "lacking" hydrogens
    
    
    private ChemFunc actualParser(Matcher m) {
        
        Stack<ChemFunc> stk = new Stack<ChemFunc>() {{ add(VOID); }};
        
        while (m.find()) {
            
            String tok = m.group(1) != null ? m.group(1) : m.group(),           // Get the matched information
                   t   = m.group(1) != null ? m.group(1) : "",
                   mul = m.group(2) != null ? m.group(2) : "";
                   
            ChemFunc part = SG.getOrDefault(reverse(tok), VOID),
                     mult = SG.getOrDefault(reverse(mul), VOID );
            
            
            if (tok.equals("etao"))                     part = part.add(actualParser(genTokens(0))); 
            
            if      (part.isRoot())                     stk.add( part.mul(mult) );
            else if (part.isBlock())                    stk.add( stk.pop().add( part.mul(mult) ));
            else if ("]".equals(tok))                   stk.add( stk.pop().add( actualParser(m) ));
            else if ("[".equals(tok))                   break;
            else if (!mul.isEmpty() && t.isEmpty())     stk.add( stk.pop().mul( mult ));
            else                                        stk.add( stk.pop().add( part.mul(mult) ));
        }
        
        return stk.stream().reduce(ChemFunc::add).get();
    }
    
    
    
    
    /* *******************************
     *     HELPER CLASS : ChemFunc
     * *******************************/
     
    
    static class ChemFunc extends HashMap<String,Integer> {
        
        protected Gram   gram = Gram.NONE;
        protected String name = "";
        protected int    mult = 1;
        
        /*     REGULAR CONSTRUCTORS     */
        
        protected ChemFunc()                         { super();                           }
        protected ChemFunc(Map<String,Integer> that) { super(that);                       }
        protected ChemFunc(String chemStr)           { super(parseChemStrToMap(chemStr)); }

        
        /*    SINGLETONS CONSTRUCTORS   */
        
        protected ChemFunc(String chemStr, List<Gram> grams, List<String> names) {
            super(parseChemStrToMap(chemStr));
            makeSingletons(grams, names);  
        }
        protected ChemFunc(Map<String,Integer> that, List<Gram> grams, List<String> names) {
            super(that);
            makeSingletons(grams, names);
        }
        

        /*    MATHS METHODS   */
        
        protected ChemFunc mul(ChemFunc cf)      { return this.mul(cf.mult); }
        protected ChemFunc mul(int n)            { return new ChemFunc( this.keySet().stream().collect(Collectors.toMap( k -> k, k -> this.get(k) * n )) ); }
        
        protected ChemFunc add(ChemFunc other)   { return new ChemFunc( Stream.concat( this.keySet().stream(), other.keySet().stream() )
                                                                              .distinct()
                                                                              .collect(Collectors.toMap( k -> k, k -> this.get(k) + other.get(k) )) ); }
        
        /*     UTILITIES      */
        
        protected boolean isDefault()            { return gram == Gram.NONE;  }
        protected boolean isBlock()              { return gram == Gram.BLOCK; }
        protected boolean isMult()               { return gram == Gram.MULT;  }
        protected boolean isRoot()               { return gram == Gram.ROOT;  }
        protected boolean isRootBlock()          { return gram == Gram.ROOT || gram == Gram.BLOCK; }
        
        
        @Override public Integer get(Object key) { return this.getOrDefault(key, 0); }
        @Override public String  toString()      { return String.format("ChemFunc(%s, %s, %s)", super.toString(), name, gram); }
        
        
        protected void makeSingletons(List<Gram> grams, List<String> names) {
            
            for (int i=0; i<grams.size() ; i++) {
                ChemFunc zeta = this.isMult() ? new Multiplier(this) : new ChemFunc(this);
                zeta.gram = grams.get(i);
                zeta.name = names.get(i);
                SG.put(zeta.name , zeta);
            }    
        }
        
        private static Map<String,Integer> parseChemStrToMap(String exp) {
            
            Map<String,Integer> res = new HashMap<String,Integer>();
            Matcher m = ParseHer.P_STR_CF.matcher(exp);
            while (m.find()) res.put(m.group(1), Integer.parseInt(m.group(2)));
            return res;
        }
    }
    
    

    /* *******************************
     *    HELPER CLASS : Multiplier
     * *******************************/
    
    
    static class Multiplier extends ChemFunc {
        
        protected Multiplier(ChemFunc that) { super(that); mult = that.mult; }
        
        protected Multiplier(int mult, String name) {
            super();
            this.mult = mult;
            gram = Gram.MULT;
            makeSingletons(Arrays.asList(gram), Arrays.asList(name));
        }
        
        @Override public String toString() { return String.format("Mutliplier(%d, %s)", mult, name); }
    }
}
__________________________________________________________________________________
import java.util.*;
import java.util.regex.*;

class ParseHer {
    final static private String[] 
    RADICALS    = {"meth", "eth", "prop", "but", "pent", "hex", "hept",  
        "oct", "non", "dec", "undec", "dodec", "tridec", "tetradec",  
        "pentadec", "hexadec", "heptadec", "octadec", "nonadec"},
    MULTIPLIERS = {"di", "tri", "tetra", "penta", "hexa", "hepta", "octa", 
        "nona", "deca", "undeca", "dodeca", "trideca", "tetradeca", "pentadeca", 
        "hexadeca", "heptadeca", "octadeca", "nonadeca"},
    SUFFIXES    = {"ol", "al", "one", "oic acid", "carboxylic acid", "oate", "ether", 
        "amide", "amine", "imine", "benzene", "thiol", "phosphine", "arsine"},
    PREFIXES    = {"cyclo", "hydroxy", "oxo", "carboxy", "oxycarbonyl", 
        "oyloxy", "formyl", "oxy", "amido", "amino", "imino", "phenyl", 
        "mercapto", "phosphino", "arsino", "fluoro", "chloro", "bromo", "iodo"};
    
    final private String 
        rgxAlk = "ane|an|ene|en|yne|yn|yl",
        rgxRadical = String.join("|", RADICALS),
        rgxMultiplier = String.join("|", MULTIPLIERS),
        rgxRadicalAlk = "(" + rgxRadical + ")((" + 
            rgxMultiplier + ")?(" + rgxAlk + "))*",    
        rgxSuffix = String.join("|", SUFFIXES),
        rgxPrefix = String.join("|", PREFIXES);
        
    boolean altFlag = false;
    
    ArrayList<String> tokens;
    int tokenInd = 0;
        
    public ParseHer(String name) {
        String str = refineInput(name);
        String rgx = String.join("|", new String[]{rgxRadicalAlk,
            rgxMultiplier, rgxSuffix, rgxPrefix, "\\[", "\\]"});
        tokens = tokenize(rgx, str);
    }
    
    public Map<String,Integer> parse() {
        Map<String,Integer> result = getTerm();
        while (tokenInd < tokens.size() 
         && !tokens.get(tokenInd).equals("]")){
           Map<String,Integer> temp = getTerm();
           result = addToResult(result, temp);
        }
        return result; 
    }
     
    private String refineInput(String input) {
        if (input.endsWith("dioate")) input = "di" + input;
        input = input.replaceAll("iodo", "iodo ");
        String rgx = "[0-9]+|[a-z\\s]+|\\[|\\]";
        String rgx2 = "^(" + 
          String.join("|", Arrays.copyOfRange(RADICALS, 12, 19)) + ")";
        ArrayList<String> tokList = tokenize(rgx, input);
        ArrayList<String> newList = new ArrayList<>();
        int cntNum = 0;
        for (String token : tokList) {
            if (token.matches("[0-9]+")) cntNum++;
            else {
                Matcher m = Pattern.compile(rgx2).matcher(token);
                if (m.find()) {
                    String s = m.group();
                    int num = 1 + Arrays.asList(RADICALS).indexOf(s);
                    if (cntNum > 2 && cntNum == num-10) 
                        token = token.substring(0, s.length()-3) 
                        + " " + token.substring(s.length()-3);
                }
                cntNum = 0; newList.add(token);
            }
        }
        return String.join("", newList); 
    }
    
    private String getToken() {
        return tokenInd < tokens.size() ? tokens.get(tokenInd) : ""; 
    }
    
    private Map<String,Integer> getTerm() {
        int mul = getMultiplier();
        Map<String,Integer> result = getChunk();
        if (mul > 1) multiply(result, mul);
        return result; 
    }   
    
    private int getMultiplier() {
        String token = getToken();
        if (token.matches(rgxMultiplier)) {
            tokenInd++;
            return 2 + Arrays.asList(MULTIPLIERS).indexOf(token);
        } 
        else return 1; 
    }
        
    private Map<String,Integer> multiply(Map<String,Integer> map, int mul)
    {
        map.entrySet().forEach(x -> x.setValue(x.getValue()*mul));
        return map; 
    } 
    
    private Map<String,Integer> addToResult(Map<String,Integer> res, 
        Map<String,Integer> map)
    {
        map.entrySet().forEach(x -> res.put(x.getKey(), 
            x.getValue() + res.getOrDefault(x.getKey(), 0)));
        return res; 
    }  
    
    private Map<String,Integer> getChunk() {
        String token = getToken(); tokenInd++;
        if (token.matches(rgxRadicalAlk)) {
            Map<String,Integer> temp = parseRadicalAlk(token);
            if (getToken().matches("oxycarbonyl|oyloxy|oxy")) {
                Map<String,Integer> next = getChunk();
                temp = addToResult(temp, next);
            }
            return temp;
        }
        else if (token.matches(rgxPrefix)) {
            Map<String,Integer> temp = parsePrefix(token);
            if (token.matches("cyclo")) {
                Map<String,Integer> next = getChunk();
                temp = addToResult(temp, next);
            }
            return temp;
        }
        else if (token.matches(rgxSuffix)) return parseSuffix(token);
        else if (token.equals("[")) {
            boolean savedAltFlag = altFlag;
            Map<String,Integer> temp = parse(); tokenInd++;
            altFlag = savedAltFlag;
            Map<String,Integer> next = getChunk();
            temp = addToResult(temp, next);
            return temp;
        } 
        else return null;
    }   
        
    private Map<String,Integer> parseRadicalAlk(String str) {
        Map<String,Integer> map = new HashMap<>();
        String rgx = String.join("|", 
            new String[]{rgxRadical, rgxMultiplier, rgxAlk, "yl"});
        ArrayList<String> radTokens = tokenize(rgx, str);
        altFlag = true; int mul = 1, numC = 0, numH = 0;
        for (String token : radTokens) {
            if (token.matches(rgxRadical)) {
                numC += 1 + Arrays.asList(RADICALS).indexOf(token);
                numH += 2 * numC + 2;
            }
            else if (token.matches(rgxMultiplier)) 
                mul = 2 + Arrays.asList(MULTIPLIERS).indexOf(token);
            else if (token.matches("ene|en")) {numH -= 2 * mul; mul = 1;}
            else if (token.matches("yne|yn")) {numH -= 4 * mul; mul = 1;}
            else if (token.matches("yl")) {numH -= 2; altFlag = false;} 
        }
        map.put("C", numC); map.put("H", numH);
        return map;
    }
    
    private Map<String,Integer> parsePrefix(String str) {
        Map<String,Integer> map = new HashMap<>();
        switch (str) {
            case "cyclo": map.put("H", -2); break;
            case "hydroxy": map.put("O", 1); break;
            case "oxo": map.put("O", 1); map.put("H", -2); break;
            case "carboxy": map.put("C", 1); map.put("O", 2); break;
            case "oxycarbonyl": map.put("C", 1); map.put("O", 2); 
                                map.put("H", -2); break;
            case "oyloxy": map.put("O", 2); map.put("H", -4); break;
            case "formyl": map.put("C", 1); map.put("O", 1); break;
            case "oxy": map.put("O", 1); map.put("H", -2); break;
            case "amido": map.put("N", 1); map.put("O", 1);
                          map.put("H", -1); break;
            case "amino": map.put("N", 1); map.put("H", 1); break;
            case "imino": map.put("N", 1); map.put("H", -1); break;
            case "phenyl": map.put("C", 6); map.put("H", 4); break;
            case "mercapto": map.put("S", 1); break;
            case "phosphino": map.put("P", 1); map.put("H", 1); break;
            case "arsino": map.put("As", 1); map.put("H", 1);; break;
            case "fluoro": map.put("F", 1); map.put("H", -1); break;
            case "chloro": map.put("Cl", 1); map.put("H", -1); break;
            case "bromo": map.put("Br", 1); map.put("H", -1); break;
            case "iodo": map.put("I", 1); map.put("H", -1); break;
        }
        return map;
    }
      
    private Map<String,Integer> parseSuffix(String str) {
        Map<String,Integer> map = new HashMap<>();
        switch (str) {
            case "ol": map.put("O", 1); break;
            case "al": map.put("O", 1); map.put("H", -2); break;
            case "one": map.put("O", 1); map.put("H", -2); break;
            case "oic acid": map.put("O", 2); map.put("H", -2); break;
            case "carboxylic acid": map.put("C", 1); map.put("O", 2); break;
            case "oate": map.put("O", 2); map.put("H", -2); break;
            case "ether": map.put("O", 1); map.put("H", 2); break;
            case "amide": map.put("N", 1); map.put("O", 1);
                          map.put("H", altFlag ? -1 : 1); break;
            case "amine": map.put("N", 1); 
                          map.put("H", altFlag ? 1 : 3); break;
            case "imine": map.put("N", 1); 
                          map.put("H", altFlag ? -1 : -3); break;
            case "benzene": map.put("C", 6); map.put("H", 6); break;
            case "thiol": map.put("S", 1); break;
            case "phosphine": map.put("P", 1); 
                              map.put("H", altFlag ? 1 : 3); break;
            case "arsine": map.put("As", 1); 
                           map.put("H", altFlag ? 1 : 3); break;
        }
        return map;
    }
    
    private ArrayList<String> tokenize(String regex, String input) {
        ArrayList<String> tokList = new ArrayList<>();
        Pattern pattern = Pattern.compile("(" + regex+ ")$");
        String token = "", str = input;
        while (token != null) {
            Matcher m = pattern.matcher(str);
            token = m.find() ? m.group() : null;
            if (token != null) {
                tokList.add(token);
                str = str.substring(0, str.lastIndexOf(token)).trim();
            }
        }
        if (str.equals("")) Collections.reverse(tokList);
        else {
            tokList.clear();
            Matcher m = Pattern.compile(regex).matcher(input);
            while (m.find()) tokList.add(m.group());
        }
        return tokList;
    }
}
____________________________________________________________________________
import java.util.*;
import java.util.stream.*;
import java.util.regex.*;



public class ParseHer {
                                 //  Number      :   1       2      3...
    final static private String[]    RADICALS    = {"meth", "eth", "prop", "but",   "pent",  "hex",  "hept",  "oct",  "non",  "dec",  "undec",  "dodec",  "tridec",  "tetradec",  "pentadec",  "hexadec",  "heptadec",  "octadec",  "nonadec"},
                                     MULTIPLIERS = {        "di",  "tri",  "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca", "undeca", "dodeca", "trideca", "tetradeca", "pentadeca", "hexadeca", "heptadeca", "octadeca", "nonadeca"};

    
    // Grammar related enumerator:
    private static enum Gram { 
                ROOT,                // Start of a new chain, or function or subfunction, ... = a big part that can be multiplied as a whole
                BLOCK,               // Intermediate modifiers (like alkenes, akynes,...) that can have multipliers/positions. Distinction needed with ROOT to handle correctly the elisions.
                MULT,                // Multiplier...
                NONE };              // No special behavior here (meaning: cannot not be affected by a multiplier otherwise than through a full "ROOT" part
    
    final static private Pattern     P_STR_CF      = Pattern.compile("([a-zA-Z]+)(-?\\d+)"),        // used to define the Chemfunc instances
                                     REV_TOKENIZER;
    
    
    final static private String      REV_POS_S = "-\\d+(?:,\\d+)*(?:-|$|(?=[ \\[]))";

    
    // TO_SANITIZE: names where the tokenizer will have to be carful, to correctly match the 2-tridecyl from 1,1,1-TRIcedycl:
    final static private Set<String> TO_SANITIZE = Arrays.asList("tridec", "tetradec", "pentadec", "hexadec", "heptadec", "octadec", "nonadec")
                                                         .stream()
                                                         .collect(Collectors.toSet());
    
    
    /* SG: store all the singletons ChemFunc instances that will be used as bases for the parsing.
     *          key   = part of the name of the molecule
     *          value = related ChemFunc/Multiplier singleton instance */
    final static private Map<String,ChemFunc> SG = new HashMap<String,ChemFunc>();
    
    
    final static private ChemFunc H, C, N, O, insat, OOinsat,
                                  VOID = new ChemFunc();                   // Default name part/Multiplier
    static {
        
        /*  Utilities  */
        H     = new ChemFunc("H1");
        C     = new ChemFunc("C1");
        N     = new ChemFunc("N1,H1");
        O     = new ChemFunc("O1");
        insat = new ChemFunc("H-2");
        OOinsat = O.add(O).add(insat);
        
        
        /*-------------------------------
         *     SINGLETONS DEFINITION
         * meaning: calls with grammar
         *         and names information
         *-------------------------------*/
        
        
        List<Gram> gramLst = Arrays.asList(Gram.NONE);
        
        new ChemFunc(insat,                         gramLst,    Arrays.asList("cyclo"));
        new ChemFunc("",                            gramLst,    Arrays.asList("an"));
        
        gramLst = Arrays.asList(Gram.BLOCK);
        
        new ChemFunc(insat,                         gramLst,    Arrays.asList("en"));
        new ChemFunc(insat.mul(2),                  gramLst,    Arrays.asList("yn"));
        
        new ChemFunc("F1,H-1",                      gramLst,    Arrays.asList("fluoro"));
        new ChemFunc("Cl1,H-1",                     gramLst,    Arrays.asList("chloro"));
        new ChemFunc("Br1,H-1",                     gramLst,    Arrays.asList("bromo"));
        new ChemFunc("I1,H-1",                      gramLst,    Arrays.asList("iodo"));
        new ChemFunc(C.add(O).add(insat),           gramLst,    Arrays.asList("formyl"));
        
        gramLst = Arrays.asList(Gram.ROOT);
        
        new ChemFunc("",                            gramLst,    Arrays.asList("e"));
        new ChemFunc("",                            gramLst,    Arrays.asList("yl"));
        new ChemFunc(O.add(insat),                  gramLst,    Arrays.asList("al"));
        new ChemFunc(OOinsat,                       gramLst,    Arrays.asList("oic acid"));
        new ChemFunc(OOinsat,                       gramLst,    Arrays.asList("oate"));
        new ChemFunc(OOinsat,                       gramLst,    Arrays.asList("oyloxy"));
        new ChemFunc(OOinsat.add(C),                gramLst,    Arrays.asList("oxycarbonyl"));
        
        gramLst = Arrays.asList(Gram.ROOT, Gram.BLOCK);

        new ChemFunc(O,                             gramLst,    Arrays.asList("ol",               "hydroxy"));
        new ChemFunc(insat.add(O),                  gramLst,    Arrays.asList("one",              "oxo"));
        new ChemFunc(insat.add(N),                  gramLst,    Arrays.asList("imine",            "imino"));
        new ChemFunc(C.mul(6).add(insat.mul(4)),    gramLst,    Arrays.asList("benzene",          "phenyl"));
        new ChemFunc("S1",                          gramLst,    Arrays.asList("thiol",            "mercapto"));
        new ChemFunc(OOinsat.add(C),                gramLst,    Arrays.asList("carboxylic acid",  "carboxy"));
        
        
        gramLst = Arrays.asList(Gram.ROOT, Gram.ROOT);
        
        new ChemFunc(N,                             gramLst,    Arrays.asList("amine",            "amino"));
        new ChemFunc(insat.add(N).add(O),           gramLst,    Arrays.asList("amide",            "amido"));
        new ChemFunc("As1,H1",                      gramLst,    Arrays.asList("arsine",           "arsino"));
        new ChemFunc("P1,H1",                       gramLst,    Arrays.asList("phosphine",        "phosphino"));
        new ChemFunc(O,                             gramLst,    Arrays.asList("ether",            "oxy"));
        
        
        List<Gram> gramNone = Arrays.asList(Gram.NONE);
        
        IntStream.range(0, RADICALS.length   ).forEach( i -> new ChemFunc("C"+(i+1), gramNone, Arrays.asList(RADICALS[i])) );
        IntStream.range(0, MULTIPLIERS.length).forEach( i -> new Multiplier(i+2, MULTIPLIERS[i]) );
        
        REV_TOKENIZER = initialize_ReversedTokenizer();
    }
    
    
    private String   name;                                  // Name of the molecule
    private String[] parts;                                 // {auxiliary chain of esters (if exist), main part of the name}
    
    public ParseHer(String name) {
        this.name = name;
        parts = name.split("(?<=yl) ");
    }
    
    @Override public String toString() { return name; }

    
    /*  TOKENIZER METHODS: generating the reversed tokenizer */
    
    private static int cmpReg(String s1, String s2) {                           // Longest first, then lexicographic
        return s1.length() != s2.length() ? s2.length() - s1.length()
                                          : s1.compareTo(s2);
    }
    
    private static String revSanitizer(String s) {
        StringBuilder sb = new StringBuilder(s).reverse();
        if      (s.equals("dodec"))       sb.append("(?!ima|oi)");              // Needed to avoid matching conflicts between "iododecane" and "io-dodecane" (same with amido)
        else if (TO_SANITIZE.contains(s)) sb.append("(?!-\\d+,)");              // Avoid matching -1,2,3-tridec, -1,1,2,3-tetradec,... as tridecane, tetradecane, ...
        return sb.toString();
    }
    
    private static Pattern initialize_ReversedTokenizer() {
        String toks_RootBlock = SG.keySet().stream().filter( sk -> SG.get(sk).isRootBlock() ).sorted(ParseHer::cmpReg).map(ParseHer::revSanitizer).collect(Collectors.joining("|")),
               toks_Mult      = SG.keySet().stream().filter( sk -> SG.get(sk).isMult()      ).sorted(ParseHer::cmpReg).map(ParseHer::revSanitizer).collect(Collectors.joining("|")),
               toks_others    = SG.keySet().stream().filter( sk -> SG.get(sk).isDefault()   ).sorted(ParseHer::cmpReg).map(ParseHer::revSanitizer).collect(Collectors.joining("|")),
               
               pattern        = String.join("|", Arrays.asList("\\[|\\]| ",
                                                               toks_others, 
                                                               String.format("(%s)?(%s)?(%s)?", toks_RootBlock, toks_Mult, REV_POS_S), 
                                                               "."));           //  garbage matching: to see any matching problem in the tokenizer (won't skip any character in the name)
        return Pattern.compile(pattern);
    }    
    
    
    
    /*   PARSING METHODS   */
    
    public  ChemFunc parse()                       { return expandHydrogens( actualParser(genTokens()) ); }
    
    private String   reverse(String s)             { return "" + new StringBuilder(s).reverse();        }
    private Matcher  genTokens()                   { return genTokens(parts.length-1);                  }
    private Matcher  genTokens(int idx)            { return REV_TOKENIZER.matcher(reverse(parts[idx])); }
    private ChemFunc expandHydrogens(ChemFunc  cf) { return cf.add( H.mul( 2*cf.get("C")+2 ) );         }    // Finalize the raw formula, adding the "lacking" hydrogens
    
    
    private ChemFunc actualParser(Matcher m) {
        
        Stack<ChemFunc> stk = new Stack<ChemFunc>() {{ add(VOID); }};
        
        while (m.find()) {
            
            String tok = m.group(1) != null ? m.group(1) : m.group(),           // Get the matched information
                   t   = m.group(1) != null ? m.group(1) : "",
                   mul = m.group(2) != null ? m.group(2) : "";
                   
            ChemFunc part = SG.getOrDefault(reverse(tok), VOID),
                     mult = SG.getOrDefault(reverse(mul), VOID );
            
            
            if (tok.equals("etao"))                     part = part.add(actualParser(genTokens(0))); 
            
            if      (part.isRoot())                     stk.add( part.mul(mult) );
            else if (part.isBlock())                    stk.add( stk.pop().add( part.mul(mult) ));
            else if ("]".equals(tok))                   stk.add( stk.pop().add( actualParser(m) ));
            else if ("[".equals(tok))                   break;
            else if (!mul.isEmpty() && t.isEmpty())     stk.add( stk.pop().mul( mult ));
            else                                        stk.add( stk.pop().add( part.mul(mult) ));
        }
        
        return stk.stream().reduce(ChemFunc::add).get();
    }
    
    
    
    
    /* *****************************
     *     HELPER CLASS : ChemFunc
     * *******************************/
     
    
    static class ChemFunc extends HashMap<String,Integer> {
        
        protected Gram   gram = Gram.NONE;
        protected String name = "";
        protected int    mult = 1;
        
        /*     REGULAR CONSTRUCTORS     */
        
        protected ChemFunc()                         { super();                           }
        protected ChemFunc(Map<String,Integer> that) { super(that);                       }
        protected ChemFunc(String chemStr)           { super(parseChemStrToMap(chemStr)); }

        
        /*    SINGLETONS CONSTRUCTORS   */
        
        protected ChemFunc(String chemStr, List<Gram> grams, List<String> names) {
            super(parseChemStrToMap(chemStr));
            makeSingletons(grams, names);  
        }
        protected ChemFunc(Map<String,Integer> that, List<Gram> grams, List<String> names) {
            super(that);
            makeSingletons(grams, names);
        }
        

        /*    MATHS METHODS   */
        
        protected ChemFunc mul(ChemFunc cf)      { return this.mul(cf.mult); }
        protected ChemFunc mul(int n)            { return new ChemFunc( this.keySet().stream().collect(Collectors.toMap( k -> k, k -> this.get(k) * n )) ); }
        
        protected ChemFunc add(ChemFunc other)   { return new ChemFunc( Stream.concat( this.keySet().stream(), other.keySet().stream() )
                                                                              .distinct()
                                                                              .collect(Collectors.toMap( k -> k, k -> this.get(k) + other.get(k) )) ); }
        
        /*     UTILITIES      */
        
        protected boolean isDefault()            { return gram == Gram.NONE;  }
        protected boolean isBlock()              { return gram == Gram.BLOCK; }
        protected boolean isMult()               { return gram == Gram.MULT;  }
        protected boolean isRoot()               { return gram == Gram.ROOT;  }
        protected boolean isRootBlock()          { return gram == Gram.ROOT || gram == Gram.BLOCK; }
        
        
        @Override public Integer get(Object key) { return this.getOrDefault(key, 0); }
        @Override public String  toString()      { return String.format("ChemFunc(%s, %s, %s)", super.toString(), name, gram); }
        
        
        protected void makeSingletons(List<Gram> grams, List<String> names) {
            
            for (int i=0; i<grams.size() ; i++) {
                ChemFunc zeta = this.isMult() ? new Multiplier(this) : new ChemFunc(this);
                zeta.gram = grams.get(i);
                zeta.name = names.get(i);
                SG.put(zeta.name , zeta);
            }    
        }
        
        private static Map<String,Integer> parseChemStrToMap(String exp) {
            
            Map<String,Integer> res = new HashMap<String,Integer>();
            Matcher m = ParseHer.P_STR_CF.matcher(exp);
            while (m.find()) res.put(m.group(1), Integer.parseInt(m.group(2)));
            return res;
        }
    }
    
    

    /* *****************************
     *    HELPER CLASS : Multiplier
     * *******************************/
    
    
    static class Multiplier extends ChemFunc {
        
        protected Multiplier(ChemFunc that) { super(that); mult = that.mult; }
        
        protected Multiplier(int mult, String name) {
            super();
            this.mult = mult;
            gram = Gram.MULT;
            makeSingletons(Arrays.asList(gram), Arrays.asList(name));
        }
        
        @Override public String toString() { return String.format("Mutliplier(%d, %s)", mult, name); }
    }
}
