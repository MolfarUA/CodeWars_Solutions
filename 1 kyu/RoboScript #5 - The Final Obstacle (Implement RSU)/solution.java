import java.util.*;
import java.util.regex.*;
import java.util.stream.*;
import java.awt.Point;



public class RSUProgram {

    final static private int     INF  = Integer.MAX_VALUE-1;
    final static private Point[] DIRS = {new Point(0,1), new Point(1,0), new Point(0,-1), new Point(-1,0)};
    
    final static private String
        ID_PATT_BRA    = "[PpRFL)](?:0|[1-9]\\d*)|[RFLq()]",
        WHITE_COMMENTS = "\\s+|//.*?(?:\\n|$)|/\\*.*?\\*/";
    
    final static private Pattern
        TOKENIZER    = Pattern.compile(String.join("|", Arrays.asList(WHITE_COMMENTS, ID_PATT_BRA, ".")), Pattern.DOTALL),
        VALID_TOKEN  = Pattern.compile(ID_PATT_BRA),
        IS_CMT_WHITE = Pattern.compile(WHITE_COMMENTS, Pattern.DOTALL);
    
    private String source;
    
    //--------------------------------------------------------
    
    public RSUProgram(String src) { source = src; }
    
    public String execute() {
        return _executeRaw(compileCode(getTokens())); 
    }

    public List<String> convertToRaw(List<String> tokens) { 
        return compileCode(tokens).stream().flatMap(Cmd::expand).collect(Collectors.toList());
    }

    public String executeRaw(List<String> cmds) {
        return _executeRaw( cmds.stream().map( s -> new Cmd(s.charAt(0),1) ).collect(Collectors.toList()) ); 
    }
    
    public List<String> getTokens() {
        List<String> tokens = new ArrayList<>();
        Matcher m = TOKENIZER.matcher(source);
        while (m.find()) {
            String tok = m.group();
            if (IS_CMT_WHITE.matcher(tok).matches())  continue;
            if (VALID_TOKEN.matcher(tok).matches()) tokens.add(tok);
            else throw new RuntimeException("Invalid token found: \""+tok+"\"");
        }
        return tokens;
    }

    //--------------------------------------------------------
    
    private List<Cmd> compileCode(List<String> tokens) {
        Scope scope = new Scope();
        return applyPatterns(parseCode(tokens.iterator(), scope, false), scope, 0);
    }

    private Stack<Cmd> parseCode(Iterator<String> tokIter, Scope scope, boolean inPattern) {
        
        Stack<Stack<Cmd>> cmds = new Stack<>();
        cmds.add(new Stack<Cmd>());
        
        while (tokIter.hasNext()) {
            String  tok      = tokIter.next();
            char    cmd      = tok.charAt(0);
            int     r        = tok.length()>1 ? Integer.parseInt(tok.substring(1)) : 1;
            boolean isRepeat = !cmds.isEmpty() && !cmds.peek().isEmpty() && cmds.peek().peek().c==cmd && cmd!='P';
            
            // System.out.println(tok);
            
            if ((cmd=='p' || cmd=='q') && cmds.size()>1)
                throw new RuntimeException("Pattern definition inside loops isn't allowed.");
            
            if (cmd=='p') {
                String name = tok.toUpperCase();
                if (scope.containsKey(name))
                    throw new RuntimeException("Invalid pattern definition: duplicated name \""+tok+"\"");
                
                Scope freshScope = new Scope(scope);
                scope.put(name, freshScope);
                freshScope.cmds = parseCode(tokIter, freshScope, true);
                
            } else if (cmd=='q') {
                if (!inPattern) throw new RuntimeException("Unopened pattern error");
                inPattern = false;
                break;
                
            } else if (cmd=='(') { cmds.push(new Stack<Cmd>());
            
            } else if (cmd==')') { Stack<Cmd> tail = cmds.pop();
                                   for (int i=0 ; i<r ; i++) cmds.peek().addAll(tail);
            
            } else if (isRepeat) { Cmd tail = cmds.peek().pop();
                                   cmds.peek().push(new Cmd(cmd, r+tail.n)); 
            
            } else {               cmds.peek().push(cmd=='P' ? new Cmd(tok, 1) : new Cmd(cmd,r));
            }
        }
        
        if (inPattern)     throw new RuntimeException("Unclosed pattern definition");
        if (cmds.size()>1) throw new RuntimeException("Unclosed brackets");
        
        return cmds.pop();
    }
    
    private List<Cmd> applyPatterns(List<Cmd> cmds, Scope scope, int depth) {
        if (depth>25) throw new RuntimeException("Infinite loop suspected");
        
        List<Cmd> lst = new ArrayList<>();
        for (Cmd cmd: cmds) {
            if (cmd.c=='P') {
                Scope nextScope = scope.reach(cmd.call);
                lst.addAll( applyPatterns(nextScope.cmds, nextScope, depth+1) );
            } else lst.add(cmd);
        }
        return lst;
    }

    private String _executeRaw(List<Cmd> cmds) {
        Point      pos   = new Point(0,0);
        int        iDir  = 0;
        Set<Point> seens = new HashSet<>(Arrays.asList(new Point(0,0)));
        for (Cmd cmd: cmds) {
            if (cmd.c=='F') {
                Point move = DIRS[iDir];
                IntStream.range(1,cmd.n+1)
                         .mapToObj( n -> new Point(pos.x+n*move.x, pos.y+n*move.y) )
                         .forEach(seens::add);
                pos.x = pos.x + cmd.n*move.x;
                pos.y = pos.y + cmd.n*move.y;
                
            } else {
                iDir = (iDir + DIRS.length + cmd.n % DIRS.length * (cmd.c=='L' ? -1:1)) % DIRS.length;
            }
        }
        return formatOutput(seens);
    }
    
    private String formatOutput(Set<Point> seens) {
        
        int miX = INF, maX = -INF, miY = INF, maY = -INF;
        for (Point p: seens) {
            if (p.x < miX) miX = p.x;
            if (p.y < miY) miY = p.y;
            if (p.x > maX) maX = p.x;
            if (p.y > maY) maY = p.y;
        }
        final int minX = miX, minY = miY, maxX = maX, maxY = maY;
        return IntStream.range(minX,maxX+1)
                        .mapToObj( x -> IntStream.range(minY, maxY+1)
                                                 .mapToObj( y -> seens.contains(new Point(x,y)) ? "*" : " " )
                                                 .collect(Collectors.joining()) )
                        .collect(Collectors.joining("\r\n"));
    }

    //--------------------------
    
    private static class Cmd {
        protected char c;
        protected int  n;
        protected String call=null;
        
        protected Cmd(char cmd, int i)      { c=cmd; n=i; }
        protected Cmd(String cmd, int i)    { c='P'; n=i; call=cmd; }
        @Override public String  toString() { return String.format("Cmd(%s,%d)", c,n); }
        protected Stream<String> expand()   { return IntStream.range(0,n).mapToObj( i -> ""+c ); }
    }
    
    @SuppressWarnings("serial")
    private static class Scope extends HashMap<String,Scope> {
        private Scope     parent = null;
        private List<Cmd> cmds   = new ArrayList<Cmd>();
        
        private Scope() { super(); }
        private Scope(Scope p) { super(); parent = p; }
        
        private Scope reach(String name) {
            boolean hasIt = containsKey(name);
            if (!hasIt && parent==null) throw new RuntimeException("Unknown pattern: "+name);
            return hasIt ? get(name) : parent.reach(name);
        }
        @Override public String toString() {
            return String.format("Scope(parent=%s, Children=%s)", parent, keySet());
        }
    }
}
_________________________________________________________
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

/**
 * Solution for 'RoboScript #5 - The Final Obstacle (Implement RSU)'.
 *
 * @author Johnny Lim
 */
public class RSUProgram {

  private static final char PATH = '*';

  private static final Pattern groupPattern = Pattern.compile("\\(([^()]*)\\)(\\d+)?");

  private static final Pattern pattern = Pattern.compile("([FLR])(\\d+)?");

  private final String src;

  public RSUProgram(String src) {
    this.src = src;
  }

  public List<String> getTokens() {
    return getTokens(this.src);
  }

  private List<String> getTokens(String source) {
    List<String> tokens = new ArrayList<>();
    String token = "";
    boolean numberExpected = false;
    for (int i = 0; i < source.length(); i++) {
      char c = source.charAt(i);
      switch (c) {
      case 'F':
      case 'L':
      case 'R':
      case ')':
      case 'p':
      case 'P':
        if (!token.isEmpty()) {
          validateToken(token);
          tokens.add(token);
          token = "";
        }
        token += c;
        numberExpected = true;
        break;

      case '(':
      case 'q':
        if (!token.isEmpty()) {
          validateToken(token);
          tokens.add(token);
          token = "";
        }
        tokens.add(String.valueOf(c));
        numberExpected = false;
        break;

      case '/':
        char next = source.charAt(i + 1);
        switch (next) {
        case '*':
          i += 2;
          while (true) {
            if (source.charAt(i) == '*' && source.charAt(i + 1) == '/') {
              break;
            }
            i++;
          }
          i++;
          break;

        case '/':
          while (true) {
            if (i == this.src.length() || source.charAt(i) == '\n') {
              break;
            }
            i++;
          }
          break;

        default:
          throw new RuntimeException("Unexpected next character: " + next);
        }
        numberExpected = false;
        break;

      case ' ':
      case '\r':
      case '\n':
        numberExpected = false;
        break;

      default:
        if (Character.isDigit(c)) {
          if (numberExpected) {
            if (token.length() == 2 && token.charAt(1) == '0') {
              throw new RuntimeException("A number shouldn't have a leading zero.");
            }

            token += c;
          }
          else {
            throw new RuntimeException("A number is not expected.");
          }
        }
        else {
          throw new RuntimeException("The character is not expected: " + c);
        }
        break;
      }
    }
    if (!token.isEmpty()) {
      validateToken(token);
      tokens.add(token);
    }
    return tokens;
  }

  private void validateToken(String token) {
    if (token.equalsIgnoreCase("p")) {
      throw new RuntimeException("Pattern definition should have an ID.");
    }
  }

  public List<String> convertToRaw(List<String> tokens) {
    List<String> afterPatternProcessing = new ArrayList<>();

    Stack<String> stack = new Stack<>();
    Stack<PatternDefinition> patternStack = new Stack<>();
    int groupDepth = 0;
    Map<String, PatternDefinition> globalScope = new HashMap<>();
    for (String token : tokens) {
      if (token.startsWith("p")) {
        if (groupDepth != 0) {
          throw new RuntimeException("A pattern can't be defined within a group.");
        }

        stack.add(token);
        patternStack.add(new PatternDefinition(token.substring(1)));
      }
      else if (token.equals("q")) {
        PatternDefinition pattern = patternStack.pop();
        List<String> definition = new ArrayList<>();
        String patternId = pattern.getId();
        while (true) {
          String popped = stack.pop();
          if (popped.equals("p" + patternId)) {
            break;
          }
          definition.add(0, popped);
        }

        // FIXME: This needs to be straightened.
        String joined = String.join("", definition);
        definition = getTokens(expandGroup(joined));

        pattern.setDefinition(definition);

        if (patternStack.isEmpty()) {
          if (globalScope.containsKey(patternId)) {
            throw new RuntimeException(
                "The pattern has been defined already in the same scope: " + patternId);
          }

          globalScope.put(patternId, pattern);
        }
        else {
          PatternDefinition parent = patternStack.peek();
          if (parent.getChildById().containsKey(patternId)) {
            throw new RuntimeException(
                "The pattern has been defined already in the same scope: " + patternId);
          }

          parent.addChild(pattern);
          pattern.setParent(parent);
        }
      }
      else {
        if (token.equals("(")) {
          groupDepth++;
        }
        else if (token.startsWith(")")) {
          groupDepth--;
        }

        if (!patternStack.isEmpty()) {
          stack.add(token);
        }
        else {
          afterPatternProcessing.add(token);
        }
      }
    }
    if (!stack.isEmpty()) {
      throw new RuntimeException("Patterns are broken.");
    }

    // FIXME: This needs to be straightened.
    afterPatternProcessing = getTokens(expandGroup(String.join("", afterPatternProcessing)));

    String result = "";
    for (String token : afterPatternProcessing) {
      if (token.startsWith("P")) {
        String patternId = token.substring(1);
        PatternDefinition pattern = globalScope.get(patternId);
        result += String.join("", applyPattern(globalScope, pattern, 1));
      }
      else {
        result += token;
      }
    }

    String expanded = expand(result);
    if (expanded.isEmpty()) {
      return Collections.emptyList();
    }

    return Arrays.stream(expanded.split("", 0)).collect(Collectors.toList());
  }

  private static String expandGroup(String code) {
    String previous = code;
    while (code.contains("(") || code.contains(")")) {
      Matcher matcher = groupPattern.matcher(code);
      StringBuilder sb = new StringBuilder();
      while (matcher.find()) {
        String group = matcher.group(1);
        String repeatGroup = matcher.group(2);
        int repeat = (repeatGroup != null) ? Integer.parseInt(repeatGroup) : 1;
        matcher.appendReplacement(sb, group.repeat(repeat));
      }
      matcher.appendTail(sb);
      code = sb.toString();

      if (code.equals(previous)) {
        throw new RuntimeException("A group expression is broken.");
      }

      previous = code;
    }
    return code;
  }

  private static String expand(String code) {
    code = expandGroup(code);
    return expandRepeat(code);
  }

  private static String expandRepeat(String code) {
    Matcher matcher = pattern.matcher(code);
    StringBuilder sb = new StringBuilder();
    while (matcher.find()) {
      String command = matcher.group(1);
      String repeatGroup = matcher.group(2);
      int repeat = (repeatGroup != null) ? Integer.parseInt(repeatGroup) : 1;
      matcher.appendReplacement(sb, command.repeat(repeat));
    }
    matcher.appendTail(sb);
    return sb.toString();
  }

  private static List<String> applyPattern(Map<String, PatternDefinition> globalScope,
      PatternDefinition patternDefinition, int depth) {
    if (depth > 500) {
      throw new RuntimeException("Too much invocation.");
    }

    List<String> result = new ArrayList<>();
    for (String token : patternDefinition.getDefinition()) {
      if (token.startsWith("P")) {
        String patternId = token.substring(1);
        PatternDefinition found = findPattern(patternDefinition, patternId);
        if (found == null) {
          found = globalScope.get(patternId);
        }
        result.addAll(applyPattern(globalScope, found, depth + 1));
      }
      else {
        result.add(token);
      }
    }
    return result;
  }

  private static PatternDefinition findPattern(PatternDefinition patternDefinition, String id) {
    if (patternDefinition == null) {
      return null;
    }

    PatternDefinition child = patternDefinition.getChildById().get(id);
    if (child != null) {
      return child;
    }

    return findPattern(patternDefinition.getParent(), id);
  }

  public String executeRaw(List<String> cmds) {
    // FIXME: This needs to be straightened.
    String code = String.join("", cmds);

    List<StringBuilder> grid = new ArrayList<>();
    grid.add(new StringBuilder().append(PATH));

    int row = 0;
    int column = 0;

    Direction direction = Direction.RIGHT;

    Matcher matcher = pattern.matcher(code);
    while (matcher.find()) {
      char command = matcher.group(1).charAt(0);
      String repeatGroup = matcher.group(2);
      int repeat = (repeatGroup != null) ? Integer.parseInt(repeatGroup) : 1;
      for (int i = 0; i < repeat; i++) {
        switch (command) {
        case 'F':
          switch (direction) {
          case RIGHT:
            column++;
            if (column == grid.get(row).length()) {
              for (int j = 0; j < grid.size(); j++) {
                grid.get(j).append(' ');
              }
            }
            break;

          case DOWN:
            if (row == grid.size() - 1) {
              grid.add(new StringBuilder(" ".repeat(grid.get(0).length())));
            }
            row++;
            break;

          case LEFT:
            if (column == 0) {
              for (int j = 0; j < grid.size(); j++) {
                grid.get(j).insert(0, ' ');
              }
            }
            else {
              column--;
            }
            break;

          case UP:
            if (row == 0) {
              grid.add(0, new StringBuilder(" ".repeat(grid.get(0).length())));
            }
            else {
              row--;
            }
            break;

          default:
            throw new IllegalStateException("Unexpected direction: " + direction);
          }
          grid.get(row).setCharAt(column, PATH);
          break;

        case 'L':
          direction = direction.rotate90DegreeCounterclockwise();
          break;

        case 'R':
          direction = direction.rotate90DegreeClockwise();
          break;

        default:
          throw new IllegalArgumentException("Unexpected command: " + command);
        }
      }
    }
    return grid.stream().map(StringBuilder::toString).collect(Collectors.joining("\r\n"));
  }

  public String execute() {
    return executeRaw(convertToRaw(getTokens()));
  }

  static class PatternDefinition {

    private final String id;

    private List<String> definition;

    private final Map<String, PatternDefinition> childById = new HashMap<>();

    private PatternDefinition parent;

    PatternDefinition(String id) {
      this.id = id;
    }

    String getId() {
      return id;
    }

    List<String> getDefinition() {
      return definition;
    }

    void setDefinition(List<String> definition) {
      this.definition = definition;
    }

    Map<String, PatternDefinition> getChildById() {
      return childById;
    }

    void addChild(PatternDefinition definition) {
      this.childById.put(definition.getId(), definition);
    }

    PatternDefinition getParent() {
      return parent;
    }

    void setParent(PatternDefinition parent) {
      this.parent = parent;
    }

    @Override
    public String toString() {
      return "PatternDefinition{" + "id='" + id + '\'' + ", definition=" + definition + ", childById=" + childById
          + ", parent=" + parent + '}';
    }

  }

  enum Direction {

    RIGHT, DOWN, LEFT, UP;

    Direction rotate90DegreeClockwise() {
      Direction[] values = values();
      return values[(ordinal() + 1) % values.length];
    }

    Direction rotate90DegreeCounterclockwise() {
      Direction[] values = values();
      return values[(values.length + ordinal() - 1) % values.length];
    }

  }

}
__________________________________________________________
import java.util.*;
import java.util.regex.*;
import java.util.stream.*;
import java.awt.Point;

public class RSUProgram {
  
  private static String  CMDREGEX = "\\(|[pP](0|[1-9]\\d*)|q|[LRF)](0|[1-9]\\d*)?";
  private static String  CMTREGEX = "/\\*(.|\\n)*?\\*/|//.*";
  private static Pattern TOKENIZE = Pattern.compile(CMDREGEX + "|\\S");

  private String src;
  public RSUProgram(String src) { this.src = src; }
  
  public List <String> getTokens() {
    List <String> tokens = new ArrayList <> ();    
    for (Matcher m = TOKENIZE.matcher(src.replaceAll(CMTREGEX, " ")); m.find();) {
      String token = m.group();
      if (!token.matches(CMDREGEX)) throw new RuntimeException();
      tokens.add(token);
    }
    return tokens;
  }
  
  private static class RoboPattern {
    private RoboPattern               previous;
    private List <String>             commands = new ArrayList <> ();
    private Map <String, RoboPattern> patterns = new HashMap <> ();
    
    private RoboPattern() {}
    private RoboPattern(RoboPattern previous) { this.previous = previous; }
    
    private static RoboPattern startParsingPatterns(Queue <String> tokens) {
      RoboPattern init = new RoboPattern().parsePatterns(tokens);
      if (!tokens.isEmpty()) throw new RuntimeException();
      return init;
    }
    
    private RoboPattern parsePatterns(Queue <String> tokens) {
      int bracket_count = 0;
      while (!tokens.isEmpty() && !tokens.peek().equals("q")) {
        String s = tokens.poll();
        if (!s.startsWith("p")) {
          switch (s.charAt(0)) {
              case '(': bracket_count++; break;
              case ')': bracket_count--; break;
          }
          commands.add(s);
          checkCommands();
          continue;
        }
        String n = s.substring(1);
        if (patterns.containsKey(n) || bracket_count != 0) throw new RuntimeException();
        patterns.put(n, new RoboPattern(this).parsePatterns(tokens));
        if (!"q".equals(tokens.poll())) throw new RuntimeException();
      }
      if (bracket_count != 0) throw new RuntimeException();
      return this;
    }
    
    private void checkCommands() {
      if (!commands.get(commands.size() - 1).equals(")0")) return;
      int bracket_count = 0;
      do {
        String s = commands.remove(commands.size() - 1);
        switch (s.charAt(0)) {
            case '(': bracket_count--; break;
            case ')': bracket_count++; break;
        }
        if (bracket_count == 0) return;
      } 
      while (!commands.isEmpty());
      throw new RuntimeException();
    }
    
    private RoboPattern lookForName(String name) {
      RoboPattern base = this;
      while (base != null) {
        if (base.patterns.containsKey(name)) return base.patterns.get(name);
        base = base.previous;
      }
      throw new RuntimeException();
    }
    
    private List <String> startParsingCommands(Set <RoboPattern> seen) {
      Queue <String> tokens = new LinkedList <> (commands);
      List <String>  result = parseCommands(tokens, seen);
      if (!tokens.isEmpty()) throw new RuntimeException();
      return result;
    }
    
    private static int countTimes(String s) {
      String n = s.substring(1);
      return n.isEmpty() ? 1 : Integer.parseInt(n);
    }
    
    private List <String> parseCommands(Queue <String> tokens, Set <RoboPattern> seen) {
      List <String> result = new ArrayList <> ();
      while (!tokens.isEmpty() && !tokens.peek().startsWith(")")) {
        String s = tokens.poll();
        if (s.startsWith("(")) {
          List <String> grp = parseCommands(tokens, seen);
          for (int i = countTimes(tokens.poll()); i > 0; i--) result.addAll(grp);
        } 
        else if (s.startsWith("P")) {
          RoboPattern pat = lookForName(s.substring(1));
          if (!seen.add(pat)) throw new RuntimeException();
          result.addAll(pat.startParsingCommands(seen));
          seen.remove(pat);
        }
        else {
          String cmd = s.substring(0, 1);
          for (int i = countTimes(s); i > 0; i--) result.add(cmd);
        }
      }
      return result;
    }
  }
  
  public List <String> convertToRaw(List <String> tokens) {
    return RoboPattern.startParsingPatterns(new LinkedList <String> (tokens))
                      .startParsingCommands(new HashSet <RoboPattern> ());
  }
  
  public String executeRaw(List <String> cmds) {
    Point       cur = new Point(0, 0), 
                dir = new Point(1, 0);
    Set <Point> pth = new HashSet <> () {{ add(new Point(0, 0)); }};
    
    for (String s : cmds) switch (s) {
        case "F": pth.add(cur = new Point(cur.x + dir.x, cur.y + dir.y)); break;
        case "L": dir = new Point(-dir.y,  dir.x);                        break;
        case "R": dir = new Point( dir.y, -dir.x);                        break;
    }
    
    int min_x = Integer.MAX_VALUE, max_x = Integer.MIN_VALUE, 
        min_y = Integer.MAX_VALUE, max_y = Integer.MIN_VALUE;
    for (Point p: pth) {
      if (p.x < min_x) min_x = p.x;
      if (p.y < min_y) min_y = p.y;
      if (p.x > max_x) max_x = p.x;
      if (p.y > max_y) max_y = p.y;
    }
    char[][] ans = new char[max_y - min_y + 1][max_x - min_x + 1];
    for (var r : ans) Arrays.fill(r, ' ');
    for (var p : pth) ans[max_y - p.y][p.x - min_x] = '*';
    return Arrays.stream(ans).map(r -> new String(r))
                             .collect(Collectors.joining("\r\n"));
  }
    
  public String execute() { return executeRaw(convertToRaw(getTokens())); }
}
