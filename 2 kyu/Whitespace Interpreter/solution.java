import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.Reader;
import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Map.Entry;
import java.util.NoSuchElementException;
import java.util.function.Consumer;
import java.util.stream.IntStream;

public class WhitespaceInterpreter {
  
  @FunctionalInterface
  public static interface ThrowingConsumer<T> extends Consumer<T> {

    @Override
    default void accept(final T elem) {
      try {
        acceptThrows(elem);
      } catch (final Exception e) {
        throw new RuntimeException(e);
      }
    }

    void acceptThrows(T elem) throws Exception;
  } 
  
  public static class ExceptionalBufferedReader extends BufferedReader {

    public ExceptionalBufferedReader(Reader in) {
      super(in);
    }

    @Override
    public int read() throws IOException {
      int read = super.read();
      if (read < 0) throw new RuntimeException("End of input stream");
      return read;
    }
    
    @Override
    public String readLine() throws IOException {
      String read = super.readLine();
      if (read == null) throw new RuntimeException("End of input stream");
      return read;
    }
    
  }

  private static LinkedList<Integer> stack = new LinkedList<>();
  private static Map<String,String> heap = newHeap();
  private static BufferedReader input;
  private static OutputStream outputStream;
  private static String output = "";
  private static String code;
  private static String ret;
  private static boolean exit;
  
  private static Map<String, String> newHeap() {
    return new HashMap<String, String>() {

      @Override
      public String get(Object key) {
        String get = super.get(key); 
        if (get == null) {
          throw new NoSuchElementException(key.toString());
        }
        return get;
      }
    };
  }
  
  private final static Map<String, ThrowingConsumer<?>> INSTRUCTIONS = new HashMap<>();
  
  static {
    /* Stack Manipuldation */
    INSTRUCTIONS.put("ss", (Integer n) -> stack.push(n)); //push
    INSTRUCTIONS.put("sts", (Integer n) -> stack.push(stack.get(n))); //duplicate N
    INSTRUCTIONS.put("stn", (Integer n) -> IntStream.range(0, n < 0 ? stack.size() - 1 : Math.min(n, stack.size() - 1) ).forEach(i -> stack.remove(1))); //discard N
    INSTRUCTIONS.put("sns", o -> stack.push(stack.get(0))); //duplicate top
    INSTRUCTIONS.put("snt", o -> stack.push(stack.remove(1))); //swap
    INSTRUCTIONS.put("snn", o -> stack.pop()); //discard top
    
    /* Arithmetic */
    INSTRUCTIONS.put("tsss", o -> stack.push(stack.remove(1) + stack.pop()));
    INSTRUCTIONS.put("tsst", o -> stack.push(stack.remove(1) - stack.pop()));
    INSTRUCTIONS.put("tssn", o -> stack.push(stack.remove(1) * stack.pop()));
    INSTRUCTIONS.put("tsts", o -> stack.push(Math.floorDiv(stack.remove(1),stack.pop())));
    INSTRUCTIONS.put("tstt", o -> stack.push(Math.floorMod(stack.remove(1),stack.pop())));
    
    /* Heap Access */
    INSTRUCTIONS.put("tts", o -> heap.put(stack.remove(1).toString(), stack.pop().toString()));
    INSTRUCTIONS.put("ttt", o -> stack.push(Integer.parseInt(heap.get(stack.pop().toString()))));
    
    /* Input/Output */
    INSTRUCTIONS.put("tnss", o -> {int ch = stack.pop().intValue(); output += (char) ch; outputStream.write(ch);}); //output character
    INSTRUCTIONS.put("tnst", o -> {String num = stack.pop().toString(); output += num; outputStream.write(num.getBytes());}); //output number
    INSTRUCTIONS.put("tnts", o -> heap.put(stack.pop().toString(), Integer.toString(input.read()))); //read character
    INSTRUCTIONS.put("tntt", o -> heap.put(stack.pop().toString(), input.readLine())); //read number
    
    /* Flow Control */
    INSTRUCTIONS.put("nss", (String l) -> {}); //mark location
    INSTRUCTIONS.put("nst", (String l) -> {ret = code; code = heap.get(l);}); //call subroutine
    INSTRUCTIONS.put("nsn", (String l) -> code = heap.get(l)); //jump
    INSTRUCTIONS.put("nts", (String l) -> {if (stack.pop() == 0) code = heap.get(l);}); //jump if zero
    INSTRUCTIONS.put("ntt", (String l) -> {if (stack.pop() < 0) code = heap.get(l);}); //jump if less than zero
    INSTRUCTIONS.put("ntn", o -> {if (ret == null) throw new IllegalStateException("Not in subroutine"); code = ret;}); //exit subroutine
    INSTRUCTIONS.put("nnn", o -> exit = true); //exit
  }
    
  private static Integer parseNumber() {
    if (code.indexOf('n') == 0) throw new IllegalStateException("Illegal number");
    Integer num = Integer.parseInt("0" + code.substring(1,code.indexOf('n')).replace('s', '0').replace('t', '1'), 2);
    char sign = code.charAt(0);
    code = code.substring(code.indexOf('n') + 1);
    return sign == 't' ? -num : num;
  }
  
  private static String parseLabel() {
    String label = code.substring(0, code.indexOf('n') + 1);
    code = code.substring(code.indexOf('n') + 1);
    return label;
  }
  
  private static Object getArgument(String instruction) {
    Object arg = null;
    if (instruction.matches("ss|st.")) {
      arg = parseNumber();
    } else if (instruction.matches("ns.|nt[st]")) {
      arg = parseLabel();
    }
    return arg;
  }
  
  private static boolean runInstruction(Entry<String, ThrowingConsumer<?>> entry) {
    code = code.substring(entry.getKey().length());
    try {
      // As Consumer isn't strictly typed, I can't just call accept(arg), but I can invoke method through reflection
      entry.getValue().getClass().getMethod("accept", Object.class).invoke(entry.getValue(), getArgument(entry.getKey()));
    } catch (NoSuchMethodException | SecurityException | IllegalAccessException ex) {
      throw new IllegalStateException("Lambda hasn't been invoked", ex);
    } catch (InvocationTargetException ex) {
      throw new IllegalArgumentException(ex.getTargetException().toString());
    }
    return true;
  }
  
  // transforms space characters to ['s','t','n'] chars;
  public static String unbleach(String code) {
    return code != null ? code.replaceAll("\\S", "").replace(' ', 's').replace('\t', 't').replace('\n', 'n') : null;
  }
  
  public static String execute(String code_str, InputStream input_stream) {
    return execute(code_str, input_stream, null);
  }
  
  private static void outputFlush() {
    try {
        outputStream.flush();
    } catch (IOException ex) {
      throw new RuntimeException(ex);
    }
  }
  
  // solution
  public static String execute(String code_str, InputStream input_stream, OutputStream output_stream) {
    output = "";
    stack = new LinkedList<>();
    heap = new HashMap<>();
    ret = null;
    exit = false;
    outputStream = output_stream == null ? new ByteArrayOutputStream() : output_stream;
    outputFlush();
    code = unbleach(code_str);
    if (input_stream != null) {
      input = new ExceptionalBufferedReader(new InputStreamReader(input_stream));
    }
    // dry run to find all labels
    while (code.length() > 0) {
      if (!INSTRUCTIONS.entrySet().stream().anyMatch(e -> {
        if (code.startsWith(e.getKey())) {
            code = code.substring(e.getKey().length());
            Object arg = getArgument(e.getKey());
            if (e.getKey().equals("nss")) {
              if (heap.containsKey((String) arg)) {
                heap.put((String) arg, null); //multiple lable, will get NPE in case of calling this
              } else {
                heap.put((String) arg, code);
              }
            }
            return true;
        }
        return false;
      })) break;
    }
    code = unbleach(code_str);
    // real run
    while (!exit && code.length() > 0) {
      if (!INSTRUCTIONS.entrySet().stream().anyMatch(e -> code.startsWith(e.getKey()) && runInstruction(e))) 
        throw new IllegalArgumentException("Unknown instruction");
    }
    if (!exit) throw new IllegalStateException("Unexpected exit");
    outputFlush();
    return output;
  }
}

___________________________________________________
import java.io.*;
import java.util.*;

public class WhitespaceInterpreter {
    public static boolean emulateInterpreter = true; // whether to execute an erroneous program
    private BufferedReader inputReader;
    private PrintWriter outputWriter;
    private StringBuilder outputBuilder;
    private Map<Integer, Integer> heap;
    private Stack<Integer> dataStack;
    private Stack<Integer> callStack;
    private int[] labelTable;
    private int ip; // instruction pointer

    private enum Symbol {
        SPACE(' '), TAB('\t'), LINEFEED('\n');

        private char c;

        Symbol(char c) {
            this.c = c;
        }
    }

    @SuppressWarnings("serial")
    public static class CompilationError extends Exception {
        private CompilationError(String msg) {
            super(msg);
        }
    }

    // These fields are used only during parsing phase
    private String code;
    private int length;
    private int ci; // code char index
    private int cs; // command start index (for error messages)

    private Symbol findNext(boolean mustExist) throws CompilationError {
        while (++ci < length) {
            char c = code.charAt(ci);
            for (Symbol s : Symbol.values())
                if (c == s.c)
                    return s;
        }
        if (mustExist)
            throw new CompilationError("Unexpected end of code");
        else
            return null;
    }

    private Symbol next() throws CompilationError {
        return findNext(true);
    }

    private void error(String errMsg) throws CompilationError {
        throw new CompilationError(errMsg + " command at " + cs);
    }

    int readNumber() throws CompilationError {
        int sign = 1;
        switch (next()) {
            case SPACE:
                break;
            case TAB:
                sign = -1;
                break;
            case LINEFEED:
                error("Wrong numerical argument for the");
        }
        int n = 0;
        Symbol s;
        while ((s = next()) != Symbol.LINEFEED) {
            n <<= 1;
            if (s == Symbol.TAB)
                n++;
        }
        return sign * n;
    }

    String readLabel() throws CompilationError {
        StringBuilder sb = new StringBuilder();
        Symbol s;
        while ((s = next()) != Symbol.LINEFEED)
            sb.append(s.c);
        return sb.toString();
    }

    @SuppressWarnings("incomplete-switch")
    private List<Runnable> compile(String code) {
        List<Runnable> program = new ArrayList<>(); // compiled code
        Map<String, Integer> labelDirectory = new HashMap<>(); // assigns indices to labels
        Map<Integer, Integer> labelIndexToCS = new HashMap<>(); // label occurrences in parsed text
        Map<Integer, Integer> labelIndexToIP = new HashMap<>(); // label addresses in the program
        this.code = code;
        length = code.length();
        ci = -1;
        try {
            while (true) {
                Symbol s0 = findNext(false);
                if (s0 == null)
                    break;
                cs = ci;
                Runnable command = null;
                switch (s0) {
                    case SPACE: // Stack Manipulation
                        int n;
                        switch (next()) {
                            case SPACE:
                                n = readNumber();
                                command = () -> dataStack.push(n);
                                break;
                            case TAB:
                                switch (next()) {
                                    case SPACE:
                                        n = readNumber();
                                        command = () -> dataStack.push(dataStack.elementAt(dataStack.size() - 1 - n));
                                        break;
                                    case LINEFEED:
                                        n = readNumber();
                                        command = () -> {
                                            Integer x = dataStack.pop();
                                            if (n >= 0 && n < dataStack.size())
                                                for (int i = 0; i < n; i++)
                                                    dataStack.pop();
                                            else
                                                dataStack.clear();
                                            dataStack.push(x);
                                        };
                                        break;
                                }
                                break;
                            case LINEFEED:
                                switch (next()) {
                                    case SPACE:
                                        command = () -> dataStack.push(dataStack.peek());
                                        break;
                                    case TAB:
                                        command = () -> {
                                            Integer x = dataStack.pop();
                                            Integer y = dataStack.pop();
                                            dataStack.push(x);
                                            dataStack.push(y);
                                        };
                                        break;
                                    case LINEFEED:
                                        command = () -> dataStack.pop();
                                        break;
                                }
                                break;
                        }
                        break;
                    case TAB:
                        switch (next()) {
                            case SPACE: // Arithmetic
                                switch (next()) {
                                    case SPACE:
                                        switch (next()) {
                                            case SPACE:
                                                command = () -> dataStack.push(dataStack.pop() + dataStack.pop());
                                                break;
                                            case TAB:
                                                command = () -> dataStack.push(-dataStack.pop() + dataStack.pop());
                                                break;
                                            case LINEFEED:
                                                command = () -> dataStack.push(dataStack.pop() * dataStack.pop());
                                                break;
                                        }
                                        break;
                                    case TAB:
                                        switch (next()) {
                                            case SPACE:
                                                command = () -> {
                                                    int a = dataStack.pop();
                                                    int b = dataStack.pop();
                                                    dataStack.push(Math.floorDiv(b, a));
                                                };
                                                break;
                                            case TAB:
                                                command = () -> {
                                                    int a = dataStack.pop();
                                                    int b = dataStack.pop();
                                                    dataStack.push(Math.floorMod(b, a));
                                                };
                                                break;
                                        }
                                        break;
                                }
                                break;
                            case TAB: // Heap Access
                                switch (next()) {
                                    case SPACE:
                                        command = () -> {
                                            int a = dataStack.pop();
                                            int b = dataStack.pop();
                                            heap.put(b, a);
                                        };
                                        break;
                                    case TAB:
                                        command = () -> {
                                            int a = dataStack.pop();
                                            Integer x = heap.get(a);
                                            if (x == null)
                                                throw new RuntimeException(
                                                        "Invalid heap address: " + a);
                                            dataStack.push(x);
                                        };
                                        break;
                                }
                                break;
                            case LINEFEED: // Input/Output
                                switch (next()) {
                                    case SPACE:
                                        switch (next()) {
                                            case SPACE:
                                                command = () -> {
                                                    char c = (char)(int)dataStack.pop();
                                                    if (outputWriter != null)
                                                        outputWriter.append(c);
                                                    outputBuilder.append(c);
                                                };
                                                break;
                                            case TAB:
                                                command = () -> {
                                                    int x = dataStack.pop();
                                                    if (outputWriter != null)
                                                        outputWriter.print(x);
                                                    outputBuilder.append(x);
                                                };
                                                break;
                                        }
                                        break;
                                    case TAB:
                                        switch (next()) {
                                            case SPACE:
                                                command = () -> {
                                                    int a;
                                                    try {
                                                        a = inputReader.read();
                                                    } catch (IOException e) {
                                                        a = -1;
                                                    }
                                                    if (a == -1)
                                                        throw new RuntimeException(
                                                                "End of input or I/O error");
                                                    heap.put(dataStack.pop(), a);
                                                };
                                                break;
                                            case TAB:
                                                command = () -> {
                                                    String s;
                                                    try {
                                                        s = inputReader.readLine();
                                                    } catch (IOException e) {
                                                        s = null;
                                                    }
                                                    if (s == null)
                                                        throw new RuntimeException(
                                                                "End of input or I/O error");
                                                    Integer a = Integer.decode(s);
                                                    heap.put(dataStack.pop(), a);
                                                };
                                                break;
                                        }
                                        break;
                                }
                                break;
                        }
                        break;
                    case LINEFEED: // Flow Control
                        Symbol s1 = next();
                        Symbol s2 = next();
                        Integer labelIndex;
                        if (s1 == Symbol.SPACE || s1 == Symbol.TAB && s2 != Symbol.LINEFEED) {
                            String label = readLabel();
                            labelIndex = labelDirectory.computeIfAbsent(label, lbl -> labelDirectory.size());
                            labelIndexToCS.putIfAbsent(labelIndex, cs);
                            // only the first occurrence of this label is being kept
                        } else
                            labelIndex = 0;
                        switch (s1) {
                            case SPACE:
                                switch (s2) {
                                    case SPACE:
                                        if (labelIndexToIP.putIfAbsent(labelIndex, program.size() - 1) != null)
                                            if (emulateInterpreter)
                                                labelIndexToIP.put(labelIndex, -2);
                                            else
                                                error("Duplicate label in the");
                                        continue;
                                    case TAB:
                                        command = () -> {
                                            callStack.push(ip);
                                            ip = labelTable[labelIndex];
                                        };
                                        break;
                                    case LINEFEED:
                                        command = () -> ip = labelTable[labelIndex];
                                        break;
                                }
                                break;
                            case TAB:
                                switch (s2) {
                                    case SPACE:
                                        command = () -> {
                                            if (dataStack.pop() == 0)
                                                ip = labelTable[labelIndex];
                                        };
                                        break;
                                    case TAB:
                                        command = () -> {
                                            if (dataStack.pop() < 0)
                                                ip = labelTable[labelIndex];
                                        };
                                        break;
                                    case LINEFEED:
                                        command = () -> ip = callStack.pop();
                                        break;
                                }
                                break;
                            case LINEFEED:
                                if (s2 == Symbol.LINEFEED) {
                                    program.add(null); // clean exit from program
                                    continue;
                                }
                        }
                        break;
                }
                if (command != null)
                    program.add(command);
                else
                    error("Unknown"); // unknown command
            }
        } catch (CompilationError e) {
            if (emulateInterpreter)
                program.add(() -> {
                    throw new RuntimeException(e);
                }); // defer an error
            else
                throw new IllegalArgumentException(e);
        }
        int labelCount = labelDirectory.size();
        labelTable = new int[labelCount];
        for (int i = 0; i < labelCount; i++) {
            Integer addr = labelIndexToIP.get(i);
            if (addr == null)
                if (emulateInterpreter)
                    addr = -2;
                else
                    throw new IllegalArgumentException(
                            "Undefined label is used in the command at " + labelIndexToCS.get(i));
            labelTable[i] = addr;
        }
        this.code = null;
        return program;
    }

    private String run(List<Runnable> program, InputStream input, OutputStream output) {
        try (BufferedReader reader = input == null ? null : new BufferedReader(new InputStreamReader(input));
                PrintWriter writer = output == null ? null : new PrintWriter(output)) {
            inputReader = reader;
            outputWriter = writer;
            outputBuilder = new StringBuilder();
            heap = new HashMap<>();
            dataStack = new Stack<>();
            callStack = new Stack<>();
            int sz = program.size();
            try {
                for (ip = 0; ip < sz; ip++) {
                    Runnable command = program.get(ip);
                    if (command != null)
                        command.run();
                    else
                        return outputBuilder.toString();
                }
                throw new RuntimeException("Unclean termination");
            } catch (ArrayIndexOutOfBoundsException e) {
                assert emulateInterpreter;
                throw new RuntimeException("Undefined label");
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static void flush(OutputStream toilet) {
        if (toilet != null)
            try {
                toilet.flush();
            } catch (IOException e) {
                e.printStackTrace();
            }
    }

    public static String execute(String code, InputStream input, OutputStream output) {
        flush(output);
        WhitespaceInterpreter wsi = new WhitespaceInterpreter();
        try {
            return wsi.run(wsi.compile(code), input, output);
        } finally {
            flush(output);
        }
    }

    public static String execute(String code, InputStream input) {
        return execute(code, input, null);
    }
}

___________________________________________________
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Stack;

public class WhitespaceInterpreter 
{

  // Overloads
  public static String execute(String code) throws Exception 
  {
  return execute(code,null,null);
  }
  
  public static String execute(String code, InputStream input) throws Exception
  {
  return execute(code,input,null);
  }
  
  public static String execute(String code, InputStream input, OutputStream outputStream) throws Exception 
  {
  
  BufferedReader INPUT ;
  if(input!=null)  INPUT = new BufferedReader(new InputStreamReader(input));  
   else INPUT = null;
  
  PrintWriter OUTPUT;
   if(outputStream!=null) 
   {
     OUTPUT = new PrintWriter(outputStream);
     OUTPUT.flush();
   }
   else OUTPUT = null;
        
  String _code=parseCode(code); 
    String output = "";
    Stack<Integer> stack = new Stack<>();
    Map<Integer,Integer> heap = new HashMap<>();
    List<String> instructions = parseInstructions(_code);
    Stack<Integer> callback = new Stack<Integer>();
    //Map functions
    Map<String,Integer> callmap;
    //Process
    String line = "";
    boolean end=false;
    int pointer = 0;
    while(end==false)
    {
      line = instructions.get(pointer);
      if(line.startsWith("push"))
      {
        String buff[] = line.split(" ");
        int number = Integer.parseInt(buff[1]);
        stack.push(number);
        //return
        
      }else
      if(line.startsWith("dup"))
      {
        String buff[] = line.split(" ");
        int number = Integer.parseInt(buff[1]);
        int stackPointer = stack.size()-number-1;
          number = stack.get(stackPointer);
          stack.push(number);
          //return
          
      }else
      if(line.startsWith("popn"))
      {
        String buff[] = line.split(" ");
        int number = Integer.parseInt(buff[1]);
        if(number<0 || number>=stack.size())  
          {
            //n<0 | n>l clear stack
            int topValue = stack.pop();
            stack.clear();
            stack.push(topValue);
          }else
          {
            int topValue = stack.pop();
            for(int b=0;b<number;b++) //Discarding values
            {
              stack.pop();
            }
            stack.push(topValue);
          }
        //return
      }else
      if(line.startsWith("call"))
      {
        String buff[] = line.split(" ");
        String label = buff[1];
        callmap = getLabels(instructions);
        if(callmap.containsKey(label)==true)
        {
          //execute call
          callback.push(pointer+1);
          pointer = callmap.get(label);
          continue;
        }else
        {
          System.out.println("ERROR: LABEL NOT FOUND!");
          throw new Exception();
        }
        //return
      
      }else
      if(line.startsWith("jump"))
      {
        String buff[] = line.split(" ");
        String label = buff[1];
        callmap = getLabels(instructions);  
        if(callmap.containsKey(label)==true)
        {
          //execute jump
          pointer = callmap.get(label);
          
          continue;
        }else
        {
          System.out.println("ERROR: LABEL NOT FOUND!");
          throw new Exception();
        }
      }else
      if(line.startsWith("jmpz"))
      {
        String buff[] = line.split(" ");
        String label = buff[1];
        int a = stack.pop();
        if(a==0)
        {
          callmap = getLabels(instructions);
          if(callmap.keySet().contains(label)==true)
          {
            //execute jump
            pointer = callmap.get(label);
            continue;
          }else
          {
            System.out.println("ERROR: LABEL NOT FOUND!");
            throw new Exception();
          }
        }
        //return
        
      }else
      if(line.startsWith("jmp"))
      {
        String buff[] = line.split(" ");
        String label = buff[1];
        int a = stack.pop();
        if(a<0)
        { 
          callmap = getLabels(instructions);
          if(callmap.containsKey(label)==true)
          {
            //execute jump
            pointer = callmap.get(label);
            continue;
          }else
          {
            System.out.println("ERROR: LABEL NOT FOUND!");
            throw new Exception();
          }
        }
        //return
        
      }else
      if(line.endsWith(":"))
      {
         //Skipping
      }
      else
      {
        //temp var
        int charValue;
        int a;
        int b;
        double c;
        double d;
        switch(line)
        {
          case "top": a = stack.pop();
                  stack.push(a);
                  stack.push(a);
                break;
                
          case "swp": int first = stack.pop();
                int second = stack.pop();
                stack.push(first);
                stack.push(second);
                break;
                
          case "pop": stack.pop();
                break;
                
          case "add": a = stack.pop();
                b = stack.pop();
                stack.push(a+b);
                break;
                
          case "sub": a = stack.pop();
                b = stack.pop();
                stack.push(b-a);
                break;
                
          case "mul": a = stack.pop();
                b = stack.pop();
                stack.push(b*a);
                break;
                
          case "div": c = stack.pop();
                if(c==0) 
                { 
                  System.out.println("ERROR Division by zero!");
                  throw new Exception();
                }else
                {
                  d = stack.pop();
                  int result = (int) Math.floor(d/c);
                  stack.push(result);
                }
                break;
                
          case "mod": a = stack.pop();
                if(a==0) 
                {
                  System.out.println("ERROR zero");
                  throw new Exception();
                  
                }else
                {
                  int factor = 1;
                  b = stack.pop();
                  int result = Math.floorMod(b, a);
                  stack.push(result*factor);
                }
                break;
                
           case "save": a = stack.pop();
                  b = stack.pop();
                  heap.put(b,a);
                  break;
                  
           case "load": a = stack.pop();
                  int value = heap.get(a);
                  stack.push(value);  
                  break;
                  
            case "out":  charValue = stack.pop();
                 char letter = (char) charValue;
                 output+=letter;
                 
                  if(OUTPUT!=null) 
                  {
                    String buff = ""+letter;
                    try { outputStream.write(buff.getBytes()); } 
                    catch (IOException e) {e.printStackTrace();}
                  }
                  
                break;
                
           case "outn": int number = stack.pop();
                output+=number;
                
                  if(OUTPUT!=null) 
                  {
                    String buff = ""+number;
                    try { outputStream.write(buff.getBytes()); } 
                    catch (IOException e) {e.printStackTrace();}
                  }
                
                break;
                
           case "rchr": int read = INPUT.read();
                          if(read<0) 
                          {
                            //throw new Exception();
                          }else
                          {
                            char chr = (char) read;
                            System.out.println("'"+chr);
                    b = stack.pop();
                    charValue = (int) chr;
                    heap.put(b,charValue);
                          }
                    break;
                     
           case "rnum": a = Integer.parseInt(INPUT.readLine());
                            b = stack.pop();
                heap.put(b,a);
                    break;
                    
            case "ret": if(callback.size()<1)
                  {
                    System.out.println("#ERROR: no subroutine callback");
                    throw new Exception();
                  }else
                  {
                    pointer = callback.pop();
                    continue;
                  }
                  //break;
                  
           case "stop": end = true;
                  break;
                  
             default: System.out.println("Terrible error no command found");
                   
        }
      
      }//endIfBranching
      
      //RETURN:
      pointer++;
      
    }//endWhile
    
  if(OUTPUT!=null) OUTPUT.flush();
  System.out.println("OUTPUT="+output);
    return output;
  }
  
  /***************
   * PROCEDURES
   * @throws Exception 
   ***************/

  public static Map<String,Integer> getLabels(List<String> instructionSet) throws Exception// throws Exception
  {
  Map<String,Integer> result = new HashMap<String,Integer>();  
  String label = "";
    for(int f=0;f<instructionSet.size();f++)
    {
      label = instructionSet.get(f);
      if(label.endsWith(":"))
      {
        label=label.substring(0,label.length()-1);
        if(result.containsKey(label)==true) 
          {
            System.out.println("Multiple labels!");
            throw new Exception();
          }
        result.put(label, f);
      }
    }
    return result;
  }

  public static String unbleach(String code) 
  {
    return code != null ? code.replace(' ', 's').replace('\t', 't').replace('\n', 'n') : null;
  }
    
  private static String parseCode(String s)
  {
    String result = "";
    char currentChar;
    for(int i=0;i<s.length();i++)
    {
      currentChar = s.charAt(i);
      if(currentChar==' ')
      {
        result+="s";
      }else
        if(currentChar=='\t')
        {
          result+="t";
        }else
          if(currentChar=='\n')
          {
            result+="n";
          }
    }
    return result;
  }
  
  private static String[] getNumber(String str)
  {
      int ptr=0;
      char chr=str.charAt(ptr);
    String[] num = new String[2];
    num[0]="";
    num[1]="";
    while(chr!='n')
    {
      num[0]+=chr;
      ptr++;
      chr=str.charAt(ptr);
    }
    num[0] += chr; //add n as well
    ptr++;
    num[1]=""+ptr;
    return num;
  }
  
  /*
   *  While solving this kata i got stuck at some point couldn't get my head around debugging raw whitespace code myself. An idea 
   *  for a simple Whitespace to human translator was born. I will implement it in a new Kata with that name :) (and lower Kyu) thus
   *  I think it's ok to involve this solution in here :). Thanks for great Kata!
   */
   
  private static List<String> parseInstructions(String s) throws IOException
  {
      List<String> instructionSet = new ArrayList<String>();
      boolean finished = false;
      int pointer = 0;
      String process = "";
      char currentChar;
      String[] number = new String[2];
      do
      {
      try{
        if(finished==true) break;
        pointer=0;
        number[0]="";
        number[1]="";
        process=s.substring(pointer,pointer+2);
        if(process.equals("ss")==true)
        {
          pointer+=2; //should point at sign
          //get Number
            s=s.substring(pointer,s.length());
            number = getNumber(s);
            pointer = Integer.parseInt(number[1]);
            s=s.substring(pointer,s.length());
          instructionSet.add("push "+parseNumber(number[0]));
          continue;
          
        }else
        {
          process=s.substring(pointer,pointer+3);
          switch(process)
          {
            /************Stack Manipulation********/
            case "sts" :
                  pointer+=3; //should be sign
                  s=s.substring(pointer,s.length());
                  number = getNumber(s);
                  pointer = Integer.parseInt(number[1]);
                  s=s.substring(pointer,s.length());
                  instructionSet.add("dup "+parseNumber(number[0]));
                  break;
                  
            case "stn" :
                  pointer+=3; //should be sign
                  s=s.substring(pointer,s.length());
                  number = getNumber(s);
                  pointer = Integer.parseInt(number[1]);
                  s=s.substring(pointer,s.length());
                  instructionSet.add("popn "+parseNumber(number[0]));
                  break;
                  
            case "sns" :
                  instructionSet.add("top");
                  pointer+=3; //should be at new instruction
                  s=s.substring(pointer,s.length());
                  break;
                  
            case "snt" :
                  instructionSet.add("swp");
                  pointer+=3; //should be at new instruction
                  s=s.substring(pointer,s.length());
                  break;
                  
            case "snn" :
                  instructionSet.add("pop");
                  pointer+=3; //should be at new instruction
                  s=s.substring(pointer,s.length());
                  break;
                  
            /************Maths*********************/
            case "tss" :
                  pointer=pointer+3;
                  currentChar=s.charAt(pointer);
                  if(currentChar=='s')
                  {
                  instructionSet.add("add");
                  }else
                  if(currentChar=='t')
                  {
                    instructionSet.add("sub");
                  }else
                  if(currentChar=='n')
                  {
                    instructionSet.add("mul");
                  }
                  else
                  {
                    System.out.println("ERROR: Unrecognized command! Math 1");
                    finished=true;
                  }
                  pointer++;
                  s=s.substring(pointer,s.length());
                  break;
                  
            case "tst" :
                  pointer=pointer+3;
                  currentChar=s.charAt(pointer);
                  if(currentChar=='s')
                  {
                    instructionSet.add("div");
                  }else
                  if(currentChar=='t')
                  {
                    instructionSet.add("mod");
                  }
                  else
                  {
                  System.out.println("ERROR: Unrecognized command! Math 2");
                    finished=true;
                  }
                  pointer++;
                  s=s.substring(pointer,s.length());
                  break;
                  
            /************Heap**********************/
            case "tts" :
                  instructionSet.add("save");
                  pointer+=3; //should be at new instruction
                  s=s.substring(pointer,s.length());
                  break;  
                  
            case "ttt" :
                  instructionSet.add("load");
                  pointer+=3; //should be at new instruction
                  s=s.substring(pointer,s.length());
                  break;
                  
            /************Input/Output***************/
            case "tns" :
                  pointer=pointer+3;
                  currentChar=s.charAt(pointer);
                  if(currentChar=='s')
                  {
                    instructionSet.add("out");
                  }else
                  if(currentChar=='t')
                  {
                    instructionSet.add("outn");
                  }
                  else
                  {
                    System.out.println("ERROR: Unrecognized command! IO 1");
                    finished=true;
                  }
                  pointer++;
                  s=s.substring(pointer,s.length());
                  break;
                  
            case "tnt" :
                  pointer=pointer+3;
                  currentChar=s.charAt(pointer);
                  if(currentChar=='s')
                  {
                  instructionSet.add("rchr");
                  }else
                  if(currentChar=='t')
                  {
                  instructionSet.add("rnum");
                  }
                  else
                  {
                    System.out.println("ERROR: Unrecognized command! IO 2");
                    finished=true;
                  }
                  pointer++;
                  s=s.substring(pointer,s.length());
                  break;
                  
            /************Flow Control***************/
            case "nss" :
                  pointer+=3; //should be start of label
                  //get Number
                  s=s.substring(pointer,s.length());
                  number = getNumber(s);  //LABEL
                  pointer = Integer.parseInt(number[1]);
                  s=s.substring(pointer,s.length());
                  instructionSet.add("_"+number[0]+":");
                  break;  
                  
            case "nst" :
                  pointer+=3; //should be start of label
                  //get Number
                  s=s.substring(pointer,s.length());
                  number = getNumber(s);  //LABEL
                  pointer = Integer.parseInt(number[1]);
                  s=s.substring(pointer,s.length());
                  instructionSet.add("call _"+number[0]);
                  break;  
                  
            case "nsn" :
                  pointer+=3; //should be start of label
                  //get Number
                  s=s.substring(pointer,s.length());
                  number = getNumber(s);  //LABEL
                  pointer = Integer.parseInt(number[1]);
                  s=s.substring(pointer,s.length());
                  instructionSet.add("jump _"+number[0]);
                  break;  
                  
            case "nts" :
                  pointer+=3; //should be start of label
                  //get Number
                  s=s.substring(pointer,s.length());
                  number = getNumber(s);  //LABEL
                  pointer = Integer.parseInt(number[1]);
                  s=s.substring(pointer,s.length());
                  instructionSet.add("jmpz _"+number[0]);
                  break;
                  
            case "ntt" :
                  pointer+=3; //should be start of label
                  //get Number
                  s=s.substring(pointer,s.length());
                  number = getNumber(s);  //LABEL
                  pointer = Integer.parseInt(number[1]);
                  s=s.substring(pointer,s.length());
                  instructionSet.add("jmp _"+number[0]);
                  break;  
                  
            case "ntn" :
                  pointer+=3;
                  instructionSet.add("ret");
                  s=s.substring(pointer,s.length());
                  break;  
                  
            case "nnn" :
                  if(pointer+4>s.length()-1)
                  {
                    finished=true;
                  }
                  pointer+=3;
                  instructionSet.add("stop");
                  //finished=true;
                  s=s.substring(pointer,s.length());
                  break;  
                  
            /***DEF******************************/
            default:
              System.out.println("ERROR: Unrecognized command! Flow control");
              finished=true;
          }//endSwitch
        }//endIfElse
      }catch(StringIndexOutOfBoundsException e)
      {
        finished=true;
      }
      
      }while(finished==false);
    
    return instructionSet;
  }

  private static int parseNumber(String s)
  {
    if(s.charAt(0)=='n')
    {
      System.out.println("INVALID NUMBER");
    }
    int factor = 1;
    if(s.charAt(0)=='t') factor = -1;
    String number = "";
    if(s.charAt(1)=='n') return 0;  //throws Exception Out of Bound
     for(int i=1;i<s.length()-1;i++)
     {
       if(s.charAt(i)=='s') number+="0";
        else number+="1"; 
     }
   return Integer.parseInt(number,2)*factor;
  }
}

        Best Practices0
        Clever1
    0
    Fork
    Link

user3218639

import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class WhitespaceInterpreter {

    private static final String EMPTY_STACK = "2";
    private static final String UNCLEAN_TERMINATION = "3";
    private static final String MULTIPLE_LABEL = "3";
    private static final String END_OF_INPUT = "12";
    private static final String SUB_NOT_RETURN = "12";

    private final List<Token> tokens = new ArrayList<>();
    private BufferedReader br;

    private int programCounter = 0;
    private Stack<Integer> stack = new Stack();
    private Stack<Integer> callStack = new Stack();
    private Map<Integer, Integer> heap = new HashMap<>();

    private Map<String, Argument> codes = new HashMap<>();

    public WhitespaceInterpreter(String code, InputStream input) {
        if (code == null || code.isEmpty()) throw new IllegalArgumentException();
        if (input != null) {
            this.br = new BufferedReader(new InputStreamReader(input));
        }

        initCodes();
        tokenize(code);
    }

    public String execute() {
        try {
            StringBuilder sb = new StringBuilder();

            while (programCounter < tokens.size()) {
                Token token = tokens.get(programCounter);
                programCounter++;

                if (token.code.equals("ss")) {
                    stack.push(number(token.argument));
                } else if (token.code.equals("sts")) {
                    int value = stack.get(stack.size() - 1 - number(token.argument));
                    stack.push(value);
                } else if (token.code.equals("stn")) {
                    int n = number(token.argument);
                    if (n < 0 || n >= stack.size()) {
                        int value = pop();
                        stack.clear();
                        stack.push(value);
                    } else {
                        int value = pop();
                        for (int i = 0; i < n; i++) pop();
                        stack.push(value);
                    }
                } else if (token.code.equals("sns")) {
                    stack.push(stack.peek());
                } else if (token.code.equals("snt")) {
                    int v0 = pop();
                    int v1 = pop();
                    stack.push(v0);
                    stack.push(v1);
                } else if (token.code.equals("snn")) {
                    pop();
                } else if (token.code.equals("tsss")) {
                    int a = pop();
                    int b = pop();
                    stack.push(b + a);
                } else if (token.code.equals("tsst")) {
                    int a = pop();
                    int b = pop();
                    stack.push(b - a);
                } else if (token.code.equals("tssn")) {
                    int a = pop();
                    int b = pop();
                    stack.push(b * a);
                } else if (token.code.equals("tsts")) {
                    int a = pop();
                    int b = pop();
                    if (a == 0) throw new IllegalArgumentException();
                    stack.push(Math.floorDiv(b, a));
                } else if (token.code.equals("tstt")) {
                    int a = pop();
                    int b = pop();
                    if (a == 0) throw new IllegalArgumentException();
                    stack.push(Math.floorMod(b, a));
                } else if (token.code.equals("tts")) {
                    int a = pop();
                    int b = pop();
                    heap.put(b, a);
                } else if (token.code.equals("ttt")) {
                    stack.push(get(pop()));
                } else if (token.code.equals("tnss")) {
                    sb.append((char) (int) pop());
                } else if (token.code.equals("tnst")) {
                    sb.append(pop());
                } else if (token.code.equals("tnts")) {
                    if (br == null) throw new IllegalArgumentException(END_OF_INPUT);
                    int in = br.read();
                    if (in == -1) throw new IllegalArgumentException(END_OF_INPUT);
                    heap.put(pop(), (int) (char) in);
                } else if (token.code.equals("tntt")) {
                    if (br == null) throw new IllegalArgumentException(END_OF_INPUT);
                    String in = br.readLine();
                    if (in == null) throw new IllegalArgumentException(END_OF_INPUT);
                    heap.put(pop(), Integer.parseInt(in));
                } else if (token.code.equals("nss")) {
                    // do nothings
                } else if (token.code.equals("nst")) {
                    callStack.push(programCounter);
                    jump(token.argument);
                } else if (token.code.equals("nsn")) {
                    jump(token.argument);
                } else if (token.code.equals("nts")) {
                    if (pop() == 0) jump(token.argument);
                } else if (token.code.equals("ntt")) {
                    if (pop() < 0) jump(token.argument);
                } else if (token.code.equals("ntn")) {
                    programCounter = callStack.pop();
                } else if (token.code.equals("nnn")) {
                    break;
                }
            }

            return sb.toString();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private int pop() {
        if (stack.isEmpty()) throw new IllegalArgumentException(EMPTY_STACK);
        return stack.pop();
    }

    private int get(int value) {
        if (!heap.containsKey(value)) throw new IllegalArgumentException();
        return heap.get(value);
    }

    private void jump(String label) {
        for (int i = 0; i < tokens.size(); i++) {
            Token token = tokens.get(i);
            if (token.code.equals("nss") && token.argument.equals(label)) {
                programCounter = i;
                return;
            }
        }

        throw new IllegalArgumentException("Unknown label: " + label);
    }

    private int number(String argument) {
        String bits = argument.substring(1).replace("n", "").replace("s", "0").replace("t", "1");
        if (bits.length() == 0) return 0;

        int number = Integer.parseInt(bits, 2);
        return argument.startsWith("s") ? number : -number;
    }

    private void initCodes() {
        codes.put("ss", Argument.NUMBER);
        codes.put("sts", Argument.NUMBER);
        codes.put("stn", Argument.NUMBER);
        codes.put("sns", Argument.NONE);
        codes.put("snt", Argument.NONE);
        codes.put("snn", Argument.NONE);

        codes.put("tsss", Argument.NONE);
        codes.put("tsst", Argument.NONE);
        codes.put("tssn", Argument.NONE);
        codes.put("tsts", Argument.NONE);
        codes.put("tstt", Argument.NONE);

        codes.put("tts", Argument.NONE);
        codes.put("ttt", Argument.NONE);

        codes.put("tnss", Argument.NONE);
        codes.put("tnst", Argument.NONE);
        codes.put("tnts", Argument.NONE);
        codes.put("tntt", Argument.NONE);

        codes.put("nss", Argument.LABEL);
        codes.put("nst", Argument.LABEL);
        codes.put("nsn", Argument.LABEL);
        codes.put("nts", Argument.LABEL);
        codes.put("ntt", Argument.LABEL);
        codes.put("ntn", Argument.NONE);
        codes.put("nnn", Argument.NONE);
    }

    private void tokenize(String code) {
        System.out.println(code);
        while (!code.isEmpty()) {
            String op = findOperation(code);
            code = code.replaceFirst(op, "");

            String argument = findArgument(code, op);
            code = code.replaceFirst(argument, "");

            tokens.add(new Token(op, argument));
        }

        System.out.println(tokens);

        validateMultipleLabels();
        if (countToken("nst") > 0 && countToken("ntn") == 0 && countToken("nnn") == 0)
            throw new IllegalArgumentException(SUB_NOT_RETURN);
        if (countToken("nnn") == 0) throw new IllegalArgumentException(UNCLEAN_TERMINATION);
    }

    private void validateMultipleLabels() {
        List<Token> tokens = findTokens("nss");
        Set<String> labels = new HashSet<>();
        for (Token t : tokens) {
            if (labels.contains(t.argument)) throw new IllegalArgumentException(MULTIPLE_LABEL);
            labels.add(t.argument);
        }
    }

    private String findOperation(String code) {
        for (String op : codes.keySet()) {
            if (code.startsWith(op)) return op;
        }

        throw new IllegalArgumentException("12");
    }

    private String findArgument(String code, String op) {
        Argument arg = codes.get(op);
        if (arg == Argument.NONE) return "";

        String pattern = arg == Argument.LABEL ? "^[ts]*n" : "^[ts]{1}[ts]*n";
        Matcher m = Pattern.compile(pattern).matcher(code);
        if (!m.find()) throw new IllegalArgumentException();

        return m.group();
    }

    private List<Token> findTokens(String op) {
        List<Token> found = new ArrayList<>();
        for (Token token : tokens) {
            if (token.code.equals(op)) found.add(token);
            if (token.code.equals("nnn")) break;
        }

        return found;
    }

    private int countToken(String op) {
        return findTokens(op).size();
    }

    public static String unbleach(String code) {
        return code != null ? code.replace(' ', 's').replace('\t', 't').replace('\n', 'n') : null;
    }

    public static String execute(String code, InputStream input) {
        return new WhitespaceInterpreter(unbleach(code.replaceAll("[^ \t\n]", "")), input).execute();
    }

    public static String execute(String code, InputStream input, OutputStream output) {
        try {
            String result = execute(code, input);
            if (output != null) {
                output.write(result.getBytes());
                output.flush();
            }
            return result;
        } catch (IllegalArgumentException e) {
            if (output != null) {
                try {
                    String message = e.getMessage();
                    if (message == null) message = "";
                    output.write(message.getBytes());
                    output.flush();
                } catch (IOException e1) {
                    e1.printStackTrace();
                }
            }

            throw e;
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }

    class Token {
        String code, argument;

        Token(String code, String argument) {
            this.code = code;
            this.argument = argument;
        }

        @Override
        public String toString() {
            String arg = codes.get(code) == Argument.NUMBER ? "" + number(argument) : argument;
            return "{" + code + ", " + arg + '}';
        }
    }

    enum Argument {
        LABEL, NUMBER, NONE
    }

    public static void main(String[] args) {
        try {
            WhitespaceInterpreter.execute("   \t\t\n   \t\t\n\t\n \t\t\n \t\n\n\n", null);
        } catch (Exception e) {
            e.printStackTrace();
        }

        String code = "blahhhhssstarggggghhhssssstntnssnnn";
        System.out.println(code.replaceAll("[^stn]", ""));
    }

}
