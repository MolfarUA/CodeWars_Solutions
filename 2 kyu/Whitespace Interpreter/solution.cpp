#include <map>
#include <math.h>

// To help with debugging
std::string unbleach(std::string s)
{
  std::transform(s.begin(), s.end(), s.begin(), [] (char c) { return (c == ' ') ? 's' : ((c == '\n') ? 'n' : 't'); });
  return s;
}


int parse_number(const std::string &code, int &ci) {
  bool negative;
  switch (code[ci]) {
    case '\t':
      negative = true;
      break;
    case ' ':
      negative = false;
      break;
    case '\n':
      return 0;
  }
  ci++;
  int number = 0, k = 0;
  while (code[ci] != '\n') {
    number = number * 2 + (code[ci] == '\t' ? 1 : 0);
    k++; ci++;
  }
  return number * ((negative)? -1 : 1);
}

std::string parse_label(const std::string &code, int &ci) {
  std::string s = "";
  while (code[ci] != '\n') {
    s += code[ci++];
  } 
  s += code[ci];
  return s;
}

int goto_label(std::vector<std::string> instructions, std::string label) {
  std::vector<int> labels; int in = 0;
  for (std::string instr : instructions) {
    if (instr[0] == '\n' && instr[1] == ' ' && instr[2] == ' ') {
      bool found = true;
      for (int i = 0; i < label.size(); i++) {
        if (i < instr.size()-3) {
          if (instr[i+3] != label[i])
            found = false;
        }
      }
      if (found)
        labels.push_back(in);
    }
    in++;
  }
  
  if (labels.size() == 1)
    return labels.back();
  else
    return -1; // not found
}

// Solution
std::string whitespace(const std::string &c, const std::string &inp = std::string())
{
    std::map<int, int > heap;
    std::vector<int> stack;
    std::string output;
    std::string code;
    bool properExit = false;
    bool corruptCommand = false;
    std::vector<int> subret;
    
    std::vector<std::string> instructions;
    
    // remove comments
    for (int i = 0; i < c.size(); i++) {
      if (c[i] == ' ' || c[i] == '\t' || c[i] == '\n')
        code.push_back(c[i]);
    }
    // instructionize
    int ci = 0, prevci = 0, ip = 0;
    while (ci < code.size()) {
      prevci = ci;
      // IMP
      switch (code[ci++]) {
        case ' ': /* stack manipulation */ { 
          switch (code[ci++]) {
            case ' ': { // push n onto the stack
              while (code[ci++] != '\n'); ci--;
              instructions.push_back(code.substr(prevci,ci+1-prevci));
              break;
            }
            case '\t': {
              switch (code[ci++]) {
                case ' ': { // duplicate the nth value from the top of the stack
                  while (code[ci++] != '\n'); ci--;
                  instructions.push_back(code.substr(prevci,ci+1-prevci));
                  break;
                }
                case '\n': { // discard the top n values below the top of the stack from the stack.
                  while (code[ci++] != '\n'); ci--;
                  instructions.push_back(code.substr(prevci,ci+1-prevci));
                  break;
                }
                default:
                  throw "Invalid command!";
                  corruptCommand = true;
              }
              break;
            }
            case '\n': {
              switch (code[ci]) {
                case ' ': { // duplicate the top value on the stack.
                  instructions.push_back(code.substr(prevci,ci-prevci+1));
                  break;
                }
                case '\t': { // swap the top two value on the stack.
                  instructions.push_back(code.substr(prevci,ci-prevci+1));
                  break;
                }
                case '\n': { // discard the top value on the stack.
                  instructions.push_back(code.substr(prevci,ci-prevci+1));
                  break;
                }
                default:
                  throw "Invalid command!";
                  corruptCommand = true;
              }
              break;
            }
            default:
              throw "Invalid command!";
              corruptCommand = true;
          }
          break;
        }
        case '\t': {
          switch (code[ci++]) {
            case ' ': /* arithmetic */ {
              switch (code[ci++]) {
                case ' ': {
                  switch (code[ci]) {
                    case ' ': { // pop a and b, then push b+a
                      instructions.push_back(code.substr(prevci,ci-prevci+1));
                      break;
                    }
                    case '\t': { // pop a and b, then push b-a
                      instructions.push_back(code.substr(prevci,ci-prevci+1));
                      break;
                    }
                    case '\n': { // pop a and b, then push b*a
                      instructions.push_back(code.substr(prevci,ci-prevci+1));
                      break;
                    }
                    default:
                      throw "Invalid command!";
                      corruptCommand = true;
                  }
                  break;
                }
                case '\t': {
                  switch (code[ci]) { 
                    case ' ': { // pop a and b, then push b/a. if a is zero, throw error
                      instructions.push_back(code.substr(prevci,ci-prevci+1));
                      break;
                    }
                    case '\t': { // pop and and b, then push b%a. if a is zero, throw error
                      instructions.push_back(code.substr(prevci,ci-prevci+1));
                      break;
                    }
                    default:
                      throw "Invalid command!";
                      corruptCommand = true;
                  }
                  break;
                }
                default:
                  throw "Invalid command!";
                  corruptCommand = true;
              }
              break;
            }
            case '\t': /* heap access */ {
              switch (code[ci]) {
                case ' ': { // pop a and b, then store a at heap address b.
                  instructions.push_back(code.substr(prevci,ci-prevci+1));
                  break;
                }
                case '\t': { // pop a and then push the value at heap address a onto the stack
                  instructions.push_back(code.substr(prevci,ci-prevci+1));
                  break;    
                }
                default:
                  throw "Invalid command!";
                  corruptCommand = true;
              }
              break;
            }
            case '\n': /* input/output */ {
              switch (code[ci++]) {
                case ' ': {
                  switch (code[ci]) {
                    case ' ': { // pop a value off the stack and output it as a character
                      instructions.push_back(code.substr(prevci,ci-prevci+1));
                      break;
                    }
                    case '\t': { // pop a value off the stack and output it as a number
                      instructions.push_back(code.substr(prevci,ci-prevci+1));
                      break;
                    }
                    default:
                      throw "Invalid command!";
                      corruptCommand = true;
                  }
                  break;
                }
                case '\t': {
                  switch (code[ci]) {
                    case ' ': { // read a character from input, a, pop a value off the stack, b, then store the ASCII value of a at heap address b.
                      instructions.push_back(code.substr(prevci,ci-prevci+1));
                      break;
                    }
                    case '\t': { // read a number from input, a, pop a value off the stack, b, then store a at heap address b.
                      instructions.push_back(code.substr(prevci,ci-prevci+1));
                      break;
                    }
                    default:
                      throw "Invalid command!";
                      corruptCommand = true;
                  }
                  break;
                }
                default:
                  throw "Invalid command!";
                  corruptCommand = true;
              }
              break;
            }
            default:
              throw "Invalid command!";
              corruptCommand = true;
          }
          break;
        }
        case '\n': /* flow control */ {
          switch (code[ci++]) {
            case ' ': {
              switch (code[ci]) {
                case ' ': { // mark a location in the program with label n
                  while (code[ci++] != '\n'); ci--;
                  instructions.push_back(code.substr(prevci,ci+1-prevci));
                  break;
                }
                case '\t': { // call a subroutine with the location specified by label n
                  while (code[ci++] != '\n'); ci--;
                  instructions.push_back(code.substr(prevci,ci+1-prevci));
                  break;
                }
                case '\n': { // jump unconditionally to the position specified by label n
                  ci++;
                  while (code[ci++] != '\n'); ci--;
                  instructions.push_back(code.substr(prevci,ci+1-prevci));
                  break;
                }
                default:
                  throw "Invalid command!";
                  corruptCommand = true;
              }
              break;
            }
            case '\t': {
              switch (code[ci]) {
                case ' ': { // pop a value off the stack and jump to the label specified by n if value is zero
                  while (code[ci++] != '\n'); ci--;
                  instructions.push_back(code.substr(prevci,ci+1-prevci));
                  break;
                }
                case '\t': { // pop a value off the stack and jump to the label specified by n if value less than zero
                  while (code[ci++] != '\n'); ci--;
                  instructions.push_back(code.substr(prevci,ci+1-prevci));
                  break;
                }
                case '\n': { // exit a subroutine and return control to the location from which the subroutine was called.
                  instructions.push_back(code.substr(prevci,ci-prevci+1));
                  break;
                }
                default:
                  throw "Invalid command!";
                  corruptCommand = true;
              }
              break;
            }
            case '\n': {
              if (code[ci] == '\n') {
                instructions.push_back(code.substr(prevci,ci-prevci+1));
              } else {
                throw "Invalid command!";
                corruptCommand = true;
              }
              break;
            }
            default:
              throw "Invalid command!";
              corruptCommand = true;
          }
          break;
          }
        default:
          throw "Invalid command!";
          corruptCommand = true;
      }
            
      ci++;
    }
    
    int in = 0;
    while (in < instructions.size() && !properExit && !corruptCommand) {
      ci = 0;
    
      std::string instr = instructions[in];
      
      // IMP
      switch (instr[ci++]) {
        case ' ': /* stack manipulation */ { 
          switch (instr[ci++]) {
            case ' ': { // push n onto the stack
                stack.push_back(parse_number(instr, ci));
              break;
            }
            case '\t': {
              switch (instr[ci]) {
                case ' ': { // duplicate the nth value from the top of the stack
                  if (instr[ci+1] == '\n')
                    throw "Invalid number with only terminal value!";
                  int num = parse_number(instr, ++ci);
                  if (num < stack.size())
                    stack.push_back(stack[stack.size() - 1 - num]);
                  else
                    throw "Stack index out of bounds!";
                  break;
                }
                case '\n': { // discard the top n values below the top of the stack from the stack.
                  int top = 0;
                  if (stack.size() > 0) {
                    top = stack.back(); stack.pop_back();
                  } else {
                    throw "Can't obtain value from empty stack!";
                  }
                  
                  int n = parse_number(instr, ++ci);
                  if (n >= 0 && n < stack.size()) {
                    for (int i = 0; i < n; i++) {
                      if (stack.size() > 0) {
                        stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                    }
                  } else {
                    while (stack.size() > 0) {
                      stack.pop_back();
                    }
                  }
                  stack.push_back(top);
                  break;
                }
              }
              break;
            }
            case '\n': {
              switch (instr[ci]) {
                case ' ': { // duplicate the top value on the stack.
                  if (stack.size() > 0)
                    stack.push_back(stack.back());
                  else
                    throw "Can't obtain value from empty stack!";
                  break;
                }
                case '\t': { // swap the top two value on the stack.
                  int a = 0, b = 0;
                  if (stack.size() > 0) {
                    a = stack.back(); stack.pop_back();
                  } else {
                    throw "Can't obtain value from empty stack!";
                  }
                  if (stack.size() > 0) {
                    b = stack.back(); stack.pop_back();
                  } else {
                    throw "Can't obtain value from empty stack!";
                  }
                  stack.push_back(a); stack.push_back(b);
                  break;
                }
                case '\n': { // discard the top value on the stack.
                  if (stack.size() > 0) {
                    stack.pop_back();
                  } else {
                    throw "Can't obtain value from empty stack!";
                  }
                  break;
                }
              }
              break;
            }
          }
          break;
        }
        case '\t': {
          switch (instr[ci++]) {
            case ' ': /* arithmetic */ {
              switch (instr[ci++]) {
                case ' ': {
                  switch (instr[ci]) {
                    case ' ': { // pop a and b, then push b+a
                      int a = 0, b = 0;
                      if (stack.size() > 0) {
                        a = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      if (stack.size() > 0) {
                        b = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      stack.push_back(b+a);
                      break;
                    }
                    case '\t': { // pop a and b, then push b-a
                      int a = 0, b = 0;
                      if (stack.size() > 0) {
                        a = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      if (stack.size() > 0) {
                        b = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      stack.push_back(b-a);
                      break;
                    }
                    case '\n': { // pop a and b, then push b*a
                      int a = 0, b = 0;
                      if (stack.size() > 0) {
                        a = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      if (stack.size() > 0) {
                        b = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      stack.push_back(b*a);
                      break;
                    }
                  }
                  break;
                }
                case '\t': {
                  switch (instr[ci]) { 
                    case ' ': { // pop a and b, then push b/a. if a is zero, throw error
                      int a = 0, b = 0;
                      if (stack.size() > 0) {
                        a = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      if (stack.size() > 0) {
                        b = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      if (a == 0)
                        throw "Can't divide by zero!";
                      double num = floor((double) b / (double) a);
                      stack.push_back((int) num);
                      break;
                    }
                    case '\t': { // pop and and b, then push b%a. if a is zero, throw error
                      int a = 0, b = 0;
                      if (stack.size() > 0) {
                        a = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      if (stack.size() > 0) {
                        b = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      if (a == 0)
                        throw "Can't divide by zero!";
                      int num = b - floor((double)floor((double)b / a) * a);
                      if (num < 0 && a > 0 || num > 0 && a < 0)
                        num *= -1;
                      stack.push_back(num);
                      break;
                    }
                  }
                  break;
                }
              }
              break;
            }
            case '\t': /* heap access */ {
              switch (instr[ci]) {
                case ' ': { // pop a and b, then store a at heap address b.
                  int a = 0, b = 0;
                  if (stack.size() > 0) {
                    a = stack.back(); stack.pop_back();
                  } else {
                    throw "Can't obtain value from empty stack!";
                  }
                  if (stack.size() > 0) {
                    b = stack.back(); stack.pop_back();
                  } else {
                    throw "Can't obtain value from empty stack!";
                  }
                  heap[b] = a;
                  break;
                }
                case '\t': { // pop a and then push the value at heap address a onto the stack
                  int a = 0;
                  if (stack.size() > 0) {
                    a = stack.back(); stack.pop_back();
                  } else {
                    throw "Can't obtain value from empty stack!";
                  }
                  if (heap.count(a) > 0)
                    stack.push_back(heap[a]);
                  else
                    throw "Undefined heap address!";
                  break;    
                }
              }
              break;
            }
            case '\n': /* input/output */ {
              switch (instr[ci++]) {
                case ' ': {
                  switch (instr[ci]) {
                    case ' ': { // pop a value off the stack and output it as a character
                      char a = 0;
                      if (stack.size() > 0) {
                        a = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      output.push_back(a);
                      break;
                    }
                    case '\t': { // pop a value off the stack and output it as a number
                      int a = 0;
                      if (stack.size() > 0) {
                        a = stack.back(); stack.pop_back();
                      } else {
                        throw "Can't obtain value from empty stack!";
                      }
                      if (a < 0) {
                        output.push_back('-');
                        a *= -1;
                      }
                      for (char c : std::to_string(a))
                        output.push_back(c);
                      break;
                    }
                  }
                  break;
                }
                case '\t': {
                  switch (instr[ci]) {
                    case ' ': { // read a character from input, a, pop a value off the stack, b, then store the ASCII value of a at heap address b.
                      if (ip >= inp.size()) {
                        throw "Exceeded end of input!";
                      } else {
                        int a = inp[ip++];
                        if (stack.size() > 0) {
                          int b = stack.back(); stack.pop_back();
                          heap[b] = a;
                        } else { 
                          throw "Can't obtain value from empty stack!";
                        }
                      }
                      break;
                    }
                    case '\t': { // read a number from input, a, pop a value off the stack, b, then store a at heap address b.
                      int a = 0, b = 0;
                      if (ip >= inp.size()) {
                        throw "Exceeded end of input!";
                      } else {
                        while (inp[ip] != '\n' && ip < inp.size())
                          a = a*10 + inp[ip++] - '0';
                        ip++;
                        if (stack.size() > 0) {
                          b = stack.back(); stack.pop_back();
                        } else {
                          throw "Can't obtain value from empty stack!";
                        }
                        heap[b] = a;
                      }
                      break;
                    }
                  }
                  break;
                }
              }
              break;
            }
          }
          break;
        }
        case '\n': /* flow control */ {
          switch (instr[ci++]) {
            case ' ': {
              switch (instr[ci++]) {
                case ' ': { // mark a location in the program with label n
                  break;
                }
                case '\t': { // call a subroutine with the location specified by label n
                  std::string label = parse_label(instr, ci);
                  subret.push_back(in);
                  int loc = goto_label(instructions, label);
                  if (loc != -1) {
                    in = loc;
                  } else {
                    throw "Label does not exist!";
                  }
                  break;
                }
                case '\n': { // jump unconditionally to the position specified by label n
                  std::string label = parse_label(instr, ci);
                  int loc = goto_label(instructions, label);
                  if (loc != -1) {
                    in = loc;
                  } else {
                    throw "Label does not exist!";
                  }
                  break;
                }
              }
              break;
            }
            case '\t': {
              switch (instr[ci++]) {
                case ' ': { // pop a value off the stack and jump to the label specified by n if value is zero
                  int a = 0;
                  if (stack.size() > 0) {
                    a = stack.back(); stack.pop_back();
                    std::string label = parse_label(instr, ci);
                    if (a == 0) {
                      int loc = goto_label(instructions, label);
                      if (loc != -1) {
                        in = loc;
                      } else {
                        throw "Label does not exist!";
                      }
                    }
                  } else {
                    throw "Can't obtain value from empty stack!";
                  }
                  break;
                }
                case '\t': { // pop a value off the stack and jump to the label specified by n if value less than zero
                  int a = 0;
                  if (stack.size() > 0) {
                    a = stack.back(); stack.pop_back();
                    std::string label = parse_label(instr, ci);
                    if (a < 0) {
                      int loc = goto_label(instructions, label);
                      if (loc != -1) {
                        in = loc;
                      } else {
                        throw "Label does not exist!";
                      }
                    }
                  } else {
                    throw "Can't obtain value from empty stack!";
                  }
                  break;
                }
                case '\n': { // exit a subroutine and return control to the location from which the subroutine was called.
                  if (subret.size() > 0) {
                    in = subret.back(); subret.pop_back();
                  } else {
                    throw "Subroutine failed to return!";
                  }
                  break;
                }
              }
              break;
            }
            case '\n': {
              if (instr[ci] == '\n') { // exit the program
                ci = instr.size();
                properExit = true;
                break;
              }
              break;
            }
          }
          break;
        }
      }
            
      in++;
    }
    
    if (!properExit)
      throw "Unclean termination!";
    
    return output;
}

___________________________________________________
#include <iostream>
#include <vector>
#include <map>
#include <cmath>

//parser

enum instr_t{
    INSTR_EOF,
    //input and output
    INSTR_IO,
    INSTR_IO_IC,//input character into heap in stack position
    INSTR_IO_IN,//input number into heap in stack position
    INSTR_IO_OC,//output character from stack position in heap
    INSTR_IO_ON,//output number from stack position in heap
    //stack manipulation
    INSTR_STACK,
    INSTR_STACK_PSH,//read number from code and push into stack
    INSTR_STACK_DUPN,//duplicate stack value
    INSTR_STACK_POPN,//pop stack and discard
    INSTR_STACK_DUP,//duplicate stack value
    INSTR_STACK_SWP,//swap stack value
    INSTR_STACK_POP,//pop stack and discard
    //arithmetic
    INSTR_MATH,
    INSTR_MATH_ADD,
    INSTR_MATH_SUB,
    INSTR_MATH_MUL,
    INSTR_MATH_DIV,
    INSTR_MATH_MOD,
    //flow control
    INSTR_FC,
    INSTR_FC_LBL,//label
    INSTR_FC_CSR,//call subroutine
    INSTR_FC_JMP,//jump
    INSTR_FC_JZ,//jump if stack top is zero
    INSTR_FC_JN,//jump if stack top is negative
    INSTR_FC_RET,//return from subroutine
    INSTR_FC_END,//end execution
    //heap access
    INSTR_MEM,
    INSTR_MEM_STORE,//store in heap at stack value
    INSTR_MEM_LOAD,//get value from heap at stack value
    INSTR_INVALID,
};

struct Parser{
    const std::string &data;
    uint32_t i;
    uint32_t unsolved_labels;
    std::map<std::string,uint32_t> labels;
    std::map<std::string,std::vector<uint32_t>> jumps;
    std::vector<uint32_t> code;

    Parser(const std::string &s):data(s),i(0),unsolved_labels(0){
    }

    char next(){
        if(i>=data.size())return 0;
        while(data[i]!=' '&&data[i]!='\t'&&data[i]!='\n'){
            i++;
            if(i>=data.size())return 0;
        }
        return data[i++];
    }

    void add_instr(instr_t i){
        code.push_back(i);
    }

    void add_stack(instr_t i,int32_t val){
        code.push_back(i);
        code.push_back(*reinterpret_cast<uint32_t*>(&val));//store the integer's bytes
    }

    void add_jump(instr_t i,std::string label){
        code.push_back(i);
        if(labels.find(label)!=labels.end()){
            code.push_back(labels[label]);
        }else{
            uint32_t pos=get_top();
            code.push_back(0);//temporary destination
            if(jumps.find(label)!=jumps.end()){
                jumps[label].push_back(pos);
            }else{
                unsolved_labels++;
                jumps[label]=std::vector<uint32_t>({pos});
            }
        }
    }

    void add_label(std::string label){
        if(labels.find(label)!=labels.end())throw std::runtime_error("label redefinition");
        uint32_t pos=get_top();
        labels[label]=pos;
        if(jumps.find(label)!=jumps.end()){
            unsolved_labels--;
            for(uint32_t i:jumps[label]){
                code[i]=pos;//rewrite temporary destinations with actual destination
            }
        }
    }

    uint32_t get_top(){
        return code.size();
    }
};

enum imp_t{
    IMP_EOF,
    IMP_IO,
    IMP_STACK,
    IMP_MATH,
    IMP_FC,
    IMP_MEM,
};

imp_t read_imp(Parser &p){
    switch(p.next()){
    case 0: return IMP_EOF;
    case ' ': return IMP_STACK;
    case '\t':
        switch(p.next()){
        case ' ': return IMP_MATH;
        case '\t': return IMP_MEM;
        case '\n': return IMP_IO;
        }
    case '\n': return IMP_FC;
    }
    throw std::runtime_error("unreachable");
}

instr_t read_instr(Parser &p){
    switch(read_imp(p)){
    case IMP_EOF:return INSTR_EOF;//propagate EOF
    case IMP_IO:
        switch(p.next()){
        case '\t':
            switch(p.next()){
            case ' ': return INSTR_IO_IC;
            case '\t': return INSTR_IO_IN;
            default:
                throw std::runtime_error("unknown IO input instruction");
            }
        case ' ':
            switch(p.next()){
            case ' ': return INSTR_IO_OC;
            case '\t': return INSTR_IO_ON;
            default:
                throw std::runtime_error("unknown IO output instruction");
            }
        default:
            throw std::runtime_error("unknown IO instruction");
        }
    case IMP_STACK:
        switch(p.next()){
        case ' ': return INSTR_STACK_PSH;
        case '\t'://seems to be a nonstandard extension?
            switch(p.next()){
            case ' ': return INSTR_STACK_DUPN;
            case '\n': return INSTR_STACK_POPN;
            }
        case '\n':
            switch(p.next()){
            case ' ': return INSTR_STACK_DUP;
            case '\t': return INSTR_STACK_SWP;
            case '\n': return INSTR_STACK_POP;
            }
        default:
            throw std::runtime_error("unknown STACK instruction");
        }
    case IMP_MATH:
        switch(p.next()){
        case ' ':
            switch(p.next()){
            case ' ': return INSTR_MATH_ADD;
            case '\t': return INSTR_MATH_SUB;
            case '\n': return INSTR_MATH_MUL;
            }
        case '\t':
            switch(p.next()){
            case ' ': return INSTR_MATH_DIV;
            case '\t': return INSTR_MATH_MOD;
            default:
                break;
            }
        default:
            throw std::runtime_error("unknown MATH instruction");
        }
    case IMP_FC:
        switch(p.next()){
        case ' ':
            switch(p.next()){
            case ' ': return INSTR_FC_LBL;
            case '\t': return INSTR_FC_CSR;
            case '\n': return INSTR_FC_JMP;
            }
        case '\t':
            switch(p.next()){
            case ' ': return INSTR_FC_JZ;
            case '\t': return INSTR_FC_JN;
            case '\n': return INSTR_FC_RET;
            }
        case '\n':
            if(p.next()=='\n') return INSTR_FC_END;
            throw std::runtime_error("unknown FC instruction");
        }
    case IMP_MEM:
        switch(p.next()){
        case ' ': return INSTR_MEM_STORE;
        case '\t': return INSTR_MEM_LOAD;
        default:
            throw std::runtime_error("unknown MEM instruction");
        }
    }
    throw std::runtime_error("unknown instruction");
}

std::string read_label(Parser &p){
    std::string s;
    while(true){
        switch(p.next()){
        case ' ':
            s+='0';
            break;
        case '\t':
            s+='1';
            break;
        case '\n':
            return s;
        }
    }
}

uint32_t read_number(Parser &p,uint8_t maxbits){//doesn't read the sign
    std::string s;
    while(true){
        if(s.size()>maxbits)throw std::runtime_error("number too large");
        switch(p.next()){
        case ' ':
            s+='0';
            break;
        case '\t':
            s+='1';
            break;
        case '\n':
            return s==""?0:std::stoul(s,nullptr,2);
        }
    }
}

bool save_instruction(Parser &p,instr_t i){
    if(i==INSTR_EOF)return true;//end of file, stop parsing
    switch(i){
    case INSTR_STACK_PSH:
    case INSTR_STACK_DUPN:
    case INSTR_STACK_POPN:
        {
            bool negative;
            switch(p.next()){
            case ' ':
                negative=false;
                break;
            case '\t':
                negative=true;
                break;
            case '\n':
                throw std::runtime_error("malformed number");
            }
            int32_t n=static_cast<int32_t>(read_number(p,31));
            p.add_stack(i,negative?-n:n);
            return false;
        }
    case INSTR_FC_LBL:
    case INSTR_FC_CSR:
    case INSTR_FC_JMP:
    case INSTR_FC_JZ:
    case INSTR_FC_JN:
        {
            std::string lbl=read_label(p);
            if(i==INSTR_FC_LBL){
                p.add_label(lbl);
            }else{
                p.add_jump(i,lbl);
            }
            return false;
        }
    default:
        p.add_instr(i);
        return false;
    }
}

std::vector<uint32_t> parse(const std::string &data){
    Parser p(data);
    while(!save_instruction(p,read_instr(p)));
    if(p.code.size()==0)throw std::runtime_error("no code");
    if(p.unsolved_labels>0)throw std::runtime_error("jump to undefined label");
    return std::move(p.code);
}

//vm

struct output_handler{
    virtual void put_c(char)=0;
    virtual void put_i(int)=0;
};

struct input_provider{
    virtual char next_c()=0;
    virtual int next_i()=0;
};

/*constexpr*/ double knuth_mod(double a,double b){
    return a - b * floor(a/b);//why is floor not constexpr for clang?
}

struct VM{
    VM(std::vector<uint32_t> && d,input_provider &in,output_handler &out):data(d),input(in),output(out),pc(0){
    }
    std::vector<uint32_t> data;
    input_provider &input;
    output_handler &output;
    uint32_t pc;
    std::vector<int32_t> stack;
    std::vector<uint32_t> call_stack;
    std::map<int32_t,int32_t> heap;
    int32_t pop(){
        if(stack.size()==0) throw std::runtime_error("stack undeflow");
        int32_t i=stack.back();
        stack.pop_back();
        return i;
    }
    bool step(){
        instr_t i=next();
        switch(i){
        case INSTR_IO_IC:{
                int32_t addr=pop();
                heap[addr]=input.next_c();
            }
            break;
        case INSTR_IO_IN:{
                int32_t addr=pop();
                heap[addr]=input.next_i();
            }
            break;
        case INSTR_IO_OC:
            output.put_c(pop());
            break;
        case INSTR_IO_ON:
            output.put_i(pop());
            break;
        case INSTR_STACK_PSH:{
                stack.push_back(*reinterpret_cast<int32_t*>(&data[pc++]));
            }
            break;
        case INSTR_STACK_DUPN:{
                if(stack.size()==0) throw std::runtime_error("stack undeflow");
                int32_t d=*reinterpret_cast<int32_t*>(&data[pc++]);
                if(d<0||static_cast<uint32_t>(d)>=stack.size()){
                    throw std::runtime_error("invalid stack offset "+std::to_string(d));
                }
                stack.push_back(stack[(stack.size()-1)-d]);
            }
            break;
        case INSTR_STACK_POPN:{
                if(stack.size()==0) throw std::runtime_error("stack undeflow");
                int32_t save=stack.back();
                int32_t d=*reinterpret_cast<int32_t*>(&data[pc++]);
                if(d<0||static_cast<uint32_t>(d+1)>=stack.size()){
                    stack.clear();
                    stack.push_back(save);
                }else{
                    stack.resize(stack.size()-(d+1));
                    stack.push_back(save);
                }
            }
            break;
        case INSTR_STACK_DUP:
            if(stack.size()==0) throw std::runtime_error("stack undeflow");
            stack.push_back(stack.back());
            break;
        case INSTR_STACK_SWP:{
                if(stack.size()<2) throw std::runtime_error("stack undeflow");
                int32_t a=pop();
                int32_t b=pop();
                stack.push_back(a);
                stack.push_back(b);
            }
            break;
        case INSTR_STACK_POP:
            if(stack.size()==0) throw std::runtime_error("stack undeflow");
            stack.pop_back();
            break;
        case INSTR_MATH_ADD:
        case INSTR_MATH_SUB:
        case INSTR_MATH_MUL:
        case INSTR_MATH_DIV:
        case INSTR_MATH_MOD:{
                int32_t rhs=pop();
                int32_t lhs=pop();
                switch(i){
                case INSTR_MATH_ADD:
                    stack.push_back(lhs+rhs);
                    break;
                case INSTR_MATH_SUB:
                    stack.push_back(lhs-rhs);
                    break;
                case INSTR_MATH_MUL:
                    stack.push_back(lhs*rhs);
                    break;
                case INSTR_MATH_DIV:
                    if(rhs==0)throw std::runtime_error("trying to divide by zero");
                    //stack.push_back(lhs/rhs);
                    stack.push_back(floor(static_cast<double>(lhs)/static_cast<double>(rhs)));//shitty hack because of shitty requirements
                    break;
                case INSTR_MATH_MOD:
                    if(rhs==0)throw std::runtime_error("trying to divide by zero");
                    stack.push_back(knuth_mod(lhs,rhs));
                    break;
                default:
                    throw std::runtime_error("unreachable");
                }
            }
            break;
        case INSTR_FC_CSR:
            call_stack.push_back(pc+1);
            pc=data[pc];
            break;
        case INSTR_FC_JMP:
            pc=data[pc];
            break;
        case INSTR_FC_JZ:
            if(pop()==0){
                pc=data[pc];
            }else{
                pc++;
            }
            break;
        case INSTR_FC_JN:
            if(pop()<0){
                pc=data[pc];
            }else{
                pc++;
            }
            break;
        case INSTR_FC_RET:{
                if(call_stack.size()==0) throw std::runtime_error("call stack undeflow");
                pc=call_stack.back();
                call_stack.pop_back();
            }
            break;
        case INSTR_FC_END:
            return true;
        //heap access
        case INSTR_MEM_STORE:{
                int32_t val=pop();
                int32_t addr=pop();
                heap[addr]=val;
            }
            break;
        case INSTR_MEM_LOAD:{
                int32_t addr=pop();
                stack.push_back(heap.at(addr));
            }
            break;
        default:
            throw std::runtime_error("trying to execute invalid instruction");
        }
        return false;
    }
    instr_t next(){
        if(pc>=data.size())throw std::runtime_error("unexpected end of program");
        uint32_t i=data[pc++];
        if(i>=INSTR_INVALID)throw std::runtime_error("trying to execute invalid instruction");
        return(instr_t)i;
    }
};

struct str_input_provider : public input_provider {
    const std::string &data;
    uint32_t i;

    str_input_provider(const std::string &s):data(s),i(0){
    }

    virtual char next_c() override{
        if(i>=data.size())throw std::runtime_error("EOF");
        return data[i++];
    }

    virtual int next_i() override{
        std::string temp;
        char c;
        while((c=next_c())!='\n'){//while is not eof or newline
            if(c==0)throw std::runtime_error("EOF");
            temp+=c;
        }
        if(temp.size()>2&&temp[0]=='0'&&temp[1]=='x'){//hexadecimal
            return stoi(temp.substr(2),nullptr,16);
        }else{
            return stoi(temp);
        }
    }
};

struct str_output_handler : public output_handler {
    std::string buf;
    virtual void put_c(char c) override {
        buf+=c;
    }
    virtual void put_i(int i) override {
        buf+=std::to_string(i);
    }
};

// To help with debugging
std::string unbleach(std::string s) {
  std::transform(s.begin(), s.end(), s.begin(), [] (char c) { return (c == ' ') ? 's' : ((c == '\n') ? 'n' : 't'); });
  return s;
}

std::string whitespace(const std::string &data, const std::string &inp = std::string()) {
    std::cerr<<"["<<inp<<"]"<<unbleach(data);
    str_input_provider in(inp);
    str_output_handler out;
    VM vm(parse(data),in,out);
    try{
      while(!vm.step());
    }catch(std::exception &e){
        std::cerr<<"!EXCEPT:"<<e.what()<<"\n";
        throw;
    }
    std::cerr<<"="<<out.buf<<"\n";
    return out.buf;
}

___________________________________________________
#include <stack>
#include <sstream>
#include <map>

// To help with debugging
std::string unbleach(std::string s) {
  std::transform(s.begin(), s.end(), s.begin(), [] (char c) { return (c == ' ') ? 's' : ((c == '\n') ? 'n' : 't'); });
  return s;
}

constexpr char SP = ' ';
constexpr char TB = '\t';
constexpr char LF = '\n';


#define defptr(T) typedef std::shared_ptr<T> ptr_t

struct FlowNode;
struct MachineState {
    std::map<int, int> heap;
    std::stack<int> stack;
    std::stack<std::shared_ptr<FlowNode>> callstack;
    std::ostringstream out;
    std::istringstream in;
    std::shared_ptr<FlowNode> begin;
    std::shared_ptr<FlowNode> current;
    std::map<std::string, std::shared_ptr<FlowNode>> labels;
    
    void run();
};

struct FlowNode {
    defptr(FlowNode);
    ptr_t next = nullptr;
    virtual ~FlowNode() = default;
    virtual void run(MachineState& state){};
};

void MachineState::run() {
    while(true){
        current->run(*this);
        if(current == nullptr) return;
        if(current->next == nullptr) throw std::runtime_error("Didn't terminate");
        current = current->next;
    }
}

struct Start : public FlowNode{};

struct Push : public FlowNode{
    Push(int n) : n { n } {}
    const int n;
    void run(MachineState& state) {
        state.stack.push(n);
    }
};
struct DuplicateNth : public FlowNode{
    DuplicateNth(int n) : n { n } {}
    const int n;
    void run(MachineState& state) {
        std::runtime_error err { "Can't copy element " + std::to_string(n) + " from stack" };
        if(n < 0 || n == state.stack.size()) throw err;

        std::stack<int> tmp;
        for(int i = 0; i < n; i++) {
            if(state.stack.empty()) throw err;
            tmp.push(state.stack.top());
            state.stack.pop();
        }

        int val = state.stack.top();
        while(!tmp.empty()) {
            state.stack.push(tmp.top());
            tmp.pop();
        }
        
        state.stack.push(val);
    }
};
struct DiscardN : public FlowNode{
    DiscardN(int n) : n { n } {}
    const int n;
    void run(MachineState& state) {
        if(state.stack.empty()) return;
        
        int top = state.stack.top();
        state.stack.pop();
        
        if(n < 0)
            while (!state.stack.empty())
                state.stack.pop();
        else
            for(int i = 0; !state.stack.empty() && i < n; ++i)
                state.stack.pop();
        
        state.stack.push(top);
    }
};
struct DuplicateTop : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.empty())
            throw std::runtime_error("Can't duplicate top of empty stack");
        state.stack.push(state.stack.top());
    }
};
struct SwapTop : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.size() < 2)
            throw std::runtime_error("Can't swap less than 2 values");
        int a = state.stack.top(); state.stack.pop();
        int b = state.stack.top(); state.stack.pop();
        state.stack.push(a);
        state.stack.push(b);
    }
};
struct DiscardTop : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.size() < 2)
            throw std::runtime_error("Can't discard top of empty stack");
        state.stack.pop();
    }
};

struct Add : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.size() < 2)
            throw std::runtime_error("Not enough elements in the stack");
        int a = state.stack.top(); state.stack.pop();
        int& b = state.stack.top();
        b += a;
    }
};
struct Sub : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.size() < 2)
            throw std::runtime_error("Not enough elements in the stack");
        int a = state.stack.top(); state.stack.pop();
        int& b = state.stack.top();
        b -= a;
    }
};
struct Mul : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.size() < 2)
            throw std::runtime_error("Not enough elements in the stack");
        int a = state.stack.top(); state.stack.pop();
        int& b = state.stack.top();
        b *= a;
    }
};
#include <cmath>
struct Div : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.size() < 2)
            throw std::runtime_error("Not enough elements in the stack");
        
        int a = state.stack.top(); state.stack.pop();
        if(a == 0)
            throw std::runtime_error("Division by 0");

        int& b = state.stack.top();
        b = std::floor(static_cast<double>(b) / a);
    }
};
struct Mod : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.size() < 2)
            throw std::runtime_error("Not enough elements in the stack");
        
        int a = state.stack.top(); state.stack.pop();
        if(a == 0)
            throw std::runtime_error("Division by 0");

        int& b = state.stack.top();
        b %= a;
        if((b < 0 && a > 0) ||
           (b > 0 && a < 0)) b += a;

    }
};

struct HeapPut : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.size() < 2)
            throw std::runtime_error("Not enough elements in the stack");
        int a = state.stack.top(); state.stack.pop();
        int b = state.stack.top(); state.stack.pop();
        state.heap[b] = a;
    }
};
struct HeapPull : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.empty())
            throw std::runtime_error("Not enough elements in the stack");
        int a = state.stack.top(); state.stack.pop();
        state.stack.push(state.heap.at(a));
    }
};

struct PutChar : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.empty())
            throw std::runtime_error("Not enough elements in the stack");
        state.out << static_cast<char>(state.stack.top());
        state.stack.pop();
    }
};
struct PutInt : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.empty())
            throw std::runtime_error("Not enough elements in the stack");
        state.out << state.stack.top();
        state.stack.pop();
    }
};
struct ReadChar : public FlowNode{
    void run(MachineState& state) {
        if(state.in.eof())
            throw std::runtime_error("Input is over");
        if(state.stack.empty())
            throw std::runtime_error("Not enough elements in the stack");
        char c;
        if(!(state.in >> c))
            throw std::runtime_error("Input is over");
        state.heap[state.stack.top()] = c;
        state.stack.pop();
    }
};
struct ReadInt : public FlowNode{
    void run(MachineState& state) {
        if(state.stack.empty())
            throw std::runtime_error("Not enough elements in the stack");
        int n;
        if(!(state.in >> n))
            throw std::runtime_error("Input is over");
        state.heap[state.stack.top()] = n;
        state.stack.pop();
    }
};


struct MarkLabel : public FlowNode{
    const std::string label;
    MarkLabel(const std::string& label) : label { label }{}
};
struct CallLabel : public FlowNode{
    const std::string label;
    CallLabel(const std::string& label) : label { label }{}
    
    void run(MachineState& state) {
        if(state.labels.find(label) == state.labels.end())
            throw std::runtime_error("Label " + unbleach(label) + " does not exists");
        state.callstack.push(state.current);
        state.current = state.labels[label];
    }
};
struct Jump : public FlowNode{
    const std::string label;
    Jump(const std::string& label) : label { label }{}
    
    void run(MachineState& state) {
        if(state.labels.find(label) == state.labels.end())
            throw std::runtime_error("Label " + unbleach(label) + " does not exists");
        state.current = state.labels[label];
    }
};
struct IfNot : public FlowNode{
    const std::string label;
    IfNot(const std::string& label) : label { label }{}
    
    void run(MachineState& state) {
        if(state.stack.empty())
            throw std::runtime_error("Not enough elements in the stack");
        if(state.labels.find(label) == state.labels.end())
            throw std::runtime_error("Label " + unbleach(label) + " does not exists");
        
        int n = state.stack.top(); state.stack.pop();
        if(n == 0) state.current = state.labels[label];
    }
};
struct IfLt : public FlowNode{
    const std::string label;
    IfLt(const std::string& label) : label { label }{}
    
    void run(MachineState& state) {
        if(state.stack.empty())
            throw std::runtime_error("Not enough elements in the stack");
        if(state.labels.find(label) == state.labels.end())
            throw std::runtime_error("Label " + unbleach(label) + " does not exists");
        
        int n = state.stack.top(); state.stack.pop();
        if(n < 0) state.current = state.labels[label];
    }
};
struct Exit : public FlowNode{
    void run(MachineState& state) {
        if(state.callstack.empty())
            throw std::runtime_error("Not in subroutine");
        state.current = state.callstack.top();
        state.callstack.pop();
    }
};
struct End : public FlowNode{
    void run(MachineState& state) {
        state.current = nullptr;
    }
};

struct Parser {
    typedef std::string::const_iterator it_t;
    typedef std::pair<FlowNode::ptr_t, it_t> res_t;
    
    static FlowNode::ptr_t parse(std::string code) {
        code.erase(std::remove_if(code.begin(), code.end(), [](char c){
            return c != SP && c != TB && c != LF;
        }), code.end());
        auto prog = tryProgram(code.cbegin(), code.cend());
        if(prog.second != code.cend())
            throw std::runtime_error("Unable to parse: " + unbleach(std::string(prog.second, code.cend())));
        return prog.first;
    }
    
#define NOTHING { nullptr, begin }
    static res_t tryProgram(it_t begin, it_t end) {
        FlowNode::ptr_t res = std::make_shared<Start>();
        
        auto res_it = res;
        it_t it = begin;
        while (it != end) {
            res_t tmp = [it, begin, end]() -> res_t {
                if(*it == SP) {
                    return tryStackManipulation(it + 1, end);
                }
                if(*it == LF) {
                    return tryFlowControl(it + 1, end);
                }
                if(std::distance(it, end) < 2) return NOTHING;
                if(*it == TB && *(it + 1) == SP) {
                    return tryArithmetic(it + 2, end);
                }
                if(*it == TB && *(it + 1) == TB) {
                    return tryHeapAccess(it + 2, end);
                }
                if(*it == TB && *(it + 1) == LF) {
                    return tryIO(it + 2, end);
                }
                return NOTHING;
            }();
            if(!tmp.first) return { res, it };
            
            it = tmp.second;
            res_it->next = tmp.first;
            res_it = res_it->next;
        }
        
        return { res, it };
    }
    
    static res_t tryStackManipulation(it_t begin, it_t end) {
        if(begin == end) return NOTHING;
        const it_t it = begin;
        
        if(*it == SP) {
            auto n = tryNumber(std::next(it), end);
            if(!n.first) return NOTHING;
            return { std::make_shared<Push>(*n.first), n.second };
        }
        if(std::distance(it, end) < 2) return NOTHING;
        
        if(*it == TB && *(it + 1) == SP) {
            auto n = tryNumber(it + 2, end);
            if(!n.first) return NOTHING;
            return { std::make_shared<DuplicateNth>(*n.first), n.second };
        }
        if(*it == TB && *(it + 1) == LF) {
            auto n = tryNumber(it + 2, end);
            if(!n.first) return NOTHING;
            return { std::make_shared<DiscardN>(*n.first), n.second };
        }
        if(*it == LF && *(it + 1) == SP) {
            return { std::make_shared<DuplicateTop>(), it + 2 };
        }
        if(*it == LF && *(it + 1) == TB) {
            return { std::make_shared<SwapTop>(), it + 2 };
        }
        if(*it == LF && *(it + 1) == LF) {
            return { std::make_shared<DiscardTop>(), it + 2 };
        }

        return NOTHING;
    }
    
    static res_t tryArithmetic(it_t begin, it_t end) {
        if(begin == end) return NOTHING;
        if(std::distance(begin, end) < 2) return NOTHING;
        const it_t it = begin;
        
        if(*it == SP && *(it + 1) == SP) {
            return { std::make_shared<Add>(), it + 2 };
        }
        if(*it == SP && *(it + 1) == TB) {
            return { std::make_shared<Sub>(), it + 2 };
        }
        if(*it == SP && *(it + 1) == LF) {
            return { std::make_shared<Mul>(), it + 2 };
        }
        if(*it == TB && *(it + 1) == SP) {
            return { std::make_shared<Div>(), it + 2 };
        }
        if(*it == TB && *(it + 1) == TB) {
            return { std::make_shared<Mod>(), it + 2 };
        }

        return NOTHING;
    }
    
    static res_t tryHeapAccess(it_t begin, it_t end) {
        if(begin == end) return NOTHING;
        const it_t it = begin;
        
        if(*it == SP)
            return { std::make_shared<HeapPut>(), it + 1 };
        if(*it == TB)
            return { std::make_shared<HeapPull>(), it + 1 };

        return NOTHING;
    }
    
    static res_t tryFlowControl(it_t begin, it_t end) {
        if(begin == end) return NOTHING;
        if(std::distance(begin, end) < 2) return NOTHING;
        const it_t it = begin;
        
        if(*it == SP && *(it + 1) == SP) {
            auto label = tryLabel(it + 2, end);
            if(!label.first) return NOTHING;
            return { std::make_shared<MarkLabel>(*label.first), label.second };
        }
        if(*it == SP && *(it + 1) == TB) {
            auto label = tryLabel(it + 2, end);
            if(!label.first) return NOTHING;
            return { std::make_shared<CallLabel>(*label.first), label.second };
        }
        if(*it == SP && *(it + 1) == LF) {
            auto label = tryLabel(it + 2, end);
            if(!label.first) return NOTHING;
            return { std::make_shared<Jump>(*label.first), label.second };
        }
        if(*it == TB && *(it + 1) == SP) {
            auto label = tryLabel(it + 2, end);
            if(!label.first) return NOTHING;
            return { std::make_shared<IfNot>(*label.first), label.second };
        }
        if(*it == TB && *(it + 1) == TB) {
            auto label = tryLabel(it + 2, end);
            if(!label.first) return NOTHING;
            return { std::make_shared<IfLt>(*label.first), label.second };
        }
        if(*it == TB && *(it + 1) == LF) {
            return { std::make_shared<Exit>(), it + 2 };
        }
        if(*it == LF && *(it + 1) == LF) {
            return { std::make_shared<End>(), it + 2 };
        }

        return NOTHING;
    }
    
    static res_t tryIO(it_t begin, it_t end) {
        if(begin == end) return NOTHING;
        if(std::distance(begin, end) < 2) return NOTHING;
        const it_t it = begin;
        
        if(*it == SP && *(it + 1) == SP)
            return { std::make_shared<PutChar>(), it + 2 };
        if(*it == SP && *(it + 1) == TB)
            return { std::make_shared<PutInt>(), it + 2 };
        if(*it == TB && *(it + 1) == SP)
            return { std::make_shared<ReadChar>(), it + 2 };
        if(*it == TB && *(it + 1) == TB)
            return { std::make_shared<ReadInt>(), it + 2 };

        return NOTHING;
    }
    
    static std::pair<std::shared_ptr<std::string>, it_t> tryLabel(it_t begin, it_t end) {
        if(begin == end) return NOTHING;
        it_t it = begin;
        auto res = std::make_shared<std::string>();
        while (*it != LF)
            res->push_back(*it++);
        return { res, it + 1 };
    }
    
    static std::pair<std::shared_ptr<int>, it_t> tryNumber(it_t begin, it_t end) {
        if(begin == end) return NOTHING;
        it_t it = begin;
        
        int sign;
        if(*it == TB) sign = -1;
        else if(*it == SP) sign = 1;
        else return NOTHING;
        
        it = std::next(it);
        if(it == end) return NOTHING;
        
        auto res = std::make_shared<int>(0);
        if(*it == LF) return { res, std::next(it) };
        
        while(it != end && *it != LF) {
            *res <<= 1;
            *res |= *it++ == TB;
        }
        *res *= sign;
        
        return { res, std::next(it) };
    }
    
#undef NOTHING
};

MachineState prepare_state(const std::string& code, const std::string& inp) {
    MachineState res;
    
    res.begin = Parser::parse(code);
    res.current = res.begin;
    res.in.str(inp);
    
    for(auto it = res.begin; it != nullptr; it = it->next) {
        auto mark = std::dynamic_pointer_cast<MarkLabel>(it);
        if(!mark) continue;
        const auto& label = mark->label;
        if(res.labels.find(label) != res.labels.end())
            throw std::runtime_error("Dublicate label " + unbleach(label));
        res.labels[label] = it;
    }
    
    return res;
}

// Solution
std::string whitespace(const std::string &code, const std::string &inp = std::string()) {
    auto state = prepare_state(code, inp);
    state.run();
    return state.out.str();
}
