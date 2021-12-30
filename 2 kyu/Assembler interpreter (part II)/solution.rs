use std::collections::HashMap;
use regex::Regex;

pub struct AssemblerInterpreter {
    registers: HashMap<String, i64>,
    labels: HashMap<String, usize>,
    stack: Vec<usize>,
    output: Vec<String>,
    ip: usize,
    ended: bool,
    compare_state: i64,
}

enum Operand { Ident(String), Val(i64), Text(String) }
type Command = (String, Vec<Operand>);
use Operand::*;

impl AssemblerInterpreter {
    pub fn interpret(input: &str) -> Option<String> {
        let mut this = AssemblerInterpreter {
            registers: HashMap::new(),
            labels: HashMap::new(),
            stack: Vec::new(),
            output: Vec::new(),
            ip: 0usize,
            ended: false,
            compare_state: 0,
        };
        let commands: Vec<Command> = this.preprocess_input(input).iter()
            .map(|line| { this.parse_command(line) }).collect();

        this.execute(&commands);
        if this.ended { Some(this.output.join("")) } else { None }
    }

    fn execute(&mut self, commands: &[Command]) {
        self.ip = 0;
        self.ended = false;
        while !self.ended && self.ip < commands.len() {
            self.execute_command(&commands[self.ip]);
            self.ip += 1;
        }
    }

    fn execute_command(&mut self, command: &Command) {
        match (command.0.as_str(), command.1.as_slice()) {
            ("mov", [left, right]) => self.binary_op(left, right, |_, y| y),
            ("inc", [arg]) => self.unary_op(arg, |x| x + 1),
            ("dec", [arg]) => self.unary_op(arg, |x| x - 1),
            ("add", [left, right]) => self.binary_op(left, right, |x, y| x + y),
            ("sub", [left, right]) => self.binary_op(left, right, |x, y| x - y),
            ("mul", [left, right]) => self.binary_op(left, right, |x, y| x * y),
            ("div", [left, right]) => self.binary_op(left, right, |x, y| x / y),
            ("cmp", [left, right]) => self.compare_state = self.get_value(left) - self.get_value(right),
            ("jmp", [arg]) => self.jump(arg, true),
            ("je", [arg]) => self.jump(arg, self.compare_state == 0),
            ("jne", [arg]) => self.jump(arg, self.compare_state != 0),
            ("jg", [arg]) => self.jump(arg, self.compare_state > 0),
            ("jge", [arg]) => self.jump(arg, self.compare_state >= 0),
            ("jl", [arg]) => self.jump(arg, self.compare_state < 0),
            ("jle", [arg]) => self.jump(arg, self.compare_state <= 0),
            ("call", [arg]) => {
                self.stack.push(self.ip+1);
                self.jump(arg, true);
            },
            ("ret", []) => self.ip = self.stack.pop().unwrap() - 1usize,
            ("end", []) => self.ended = true,
            ("msg", args) => self.message(args),
            _ => panic!()
        }
    }

    fn message(&mut self, args: &[Operand]) {
        for arg in args {
            let msg = match arg {
                Val(val) => val.to_string(),
                Ident(ident) => self.registers.get(ident).unwrap_or(&0).to_string(),
                Text(text) => text.clone()
            };
            self.output.push(msg);
        }
    }

    fn jump(&mut self, arg: &Operand, cond: bool) {
        if cond {
            if let Ident(label) = arg { self.ip = self.labels[label] - 1usize; }
        }
    }

    fn unary_op(&mut self, arg: &Operand, f: impl Fn(i64) -> i64) {
        if let Ident(ident) = arg {
            let reg = self.registers.get_mut(ident).unwrap();
            *reg = f(*reg);
        }
    }

    fn binary_op(&mut self, left: &Operand, right: &Operand, f: impl Fn(i64, i64) -> i64) {
        if let Ident(left) = left {
            let left_val = *self.registers.get(left).unwrap_or(&0);
            let right = self.get_value(right);
            self.registers.insert(left.to_string(), f(left_val, right));
        }
    }

    fn get_value(&self, op: &Operand) -> i64 {
        *match op {
            Val(val) => val,
            Ident(ident) => self.registers.get(ident).unwrap_or(&0),
            _ => panic!()
        }
    }

    fn parse_command(&self, command: &str) -> Command {
        let command_regex: Regex = Regex::new(r"\w+|\d+|'.*?'").unwrap();
        let matches: Vec<&str> = command_regex.find_iter(command)
            .map(|mat| mat.as_str()).collect();

        (matches[0].to_string(), matches[1..].iter().map(|m| self.parse_operand(m)).collect())
    }

    fn parse_operand(&self, op: &str) -> Operand {
        if op.starts_with("'") && op.ends_with("'") { Text(op[1..op.len()-1].to_string()) }
        else if op.chars().all(|c| c.is_digit(10) ) { Val(op.parse().unwrap()) }
        else { Ident(op.to_string()) }
    }

    fn preprocess_input(&mut self, input: &str) -> Vec<String> {
        let lines = input.split("\n")
            .map(|line| { line.split(";").next().unwrap().trim().to_string() })
            .filter(|line| !line.is_empty());

        let mut res = vec![];
        let label_re = Regex::new(r"^\w[\w\d]*:$").unwrap();
        for line in lines.into_iter() {
            if label_re.is_match(&line) {
                self.labels.insert(line[0..line.len()-1].to_string(), res.len());
            } else {
                res.push(line);
            }
        }
        res
    }
}
      
____________________________________________________
use regex::{Regex, Match};
use std::collections::HashMap;
use std::cmp::Ordering;

type Registers<'r> = HashMap<&'r str, i64>;
type LabelCalls<'r> = HashMap<usize, &'r str>;
type LabelPositions<'r> = HashMap<&'r str, usize>;

fn trim_line(s: &str) -> Option<&str> {
    let res = s.find(";").map(|pos| &s[..pos]).unwrap_or(s).trim();

    if res.is_empty() {
        None
    } else {
        Some(res)
    }
}

fn match_to_str<'s>(m: Match<'s>) -> &'s str { m.as_str() }

#[derive(Clone, Debug)]
enum Value<'r> {
    Const(i64),
    Reg(&'r str),
    Str(&'r str),
}

impl<'r> Value<'r> {
    fn reg(&self) -> &'r str {
        if let Value::Reg(r) = self { r } else { "" }
    }

    fn get<'b>(&self, registers: &'b Registers) -> i64 {
        match self {
            Self::Const(r) => *r,
            Self::Reg(r) => registers.get(r).map(|v| *v).unwrap_or_default(),
            _ => 0,
        }
    }

    fn append_str<'b, 'c>(&self, registers: &'b Registers, output: &'c mut String) {
        match self {
            Self::Const(r) => { *output += r.to_string().as_str(); }
            Self::Str(r) => { *output += *r; }
            Self::Reg(r) => { *output += registers.get(*r).map(|v| *v).unwrap_or_default().to_string().as_str(); }
        }
    }
}

#[derive(Clone, Debug)]
enum Instr<'r> {
    Mov(&'r str, Value<'r>),
    Inc(&'r str),
    Dec(&'r str),
    Add(&'r str, Value<'r>),
    Sub(&'r str, Value<'r>),
    Mul(&'r str, Value<'r>),
    Div(&'r str, Value<'r>),
    Cmp(Value<'r>, Value<'r>),
    Jmp(usize),
    Jne(usize),
    Je(usize),
    Jge(usize),
    Jg(usize),
    Jle(usize),
    Jl(usize),
    Call(usize),
    Msg(Vec<Value<'r>>),
    Ret,
    End,
}

struct Program<'r>(Vec<Instr<'r>>);

impl<'r> Program<'r> {
    fn new(_: &'r str) -> Program<'r> {
        Self(vec![])
    }

    fn size(&self) -> usize {
        self.0.len()
    }

    fn add(&mut self, instr: Instr<'r>) {
        self.0.push(instr);
    }

    fn build_op<'a>(&mut self, args: &'a Vec<Value<'r>>, cons: impl Fn(&'r str, Value<'r>) -> Instr<'r>) {
        if let Some(dest) = args.get(0) {
            if let Some(src) = args.get(1) {
                let reg = dest.reg();

                if !reg.is_empty() {
                    self.0.push(cons(reg, src.clone()));
                }
            }
        }
    }

    fn build_with_reg<'a>(&mut self, args: &'a Vec<Value<'r>>, cons: impl Fn(&'r str) -> Instr<'r>) {
        if let Some(dest) = args.get(0) {
            let reg = dest.reg();

            if !reg.is_empty() {
                self.0.push(cons(reg));
            }
        }
    }

    fn build_with_vals<'a>(&mut self, args: &'a Vec<Value<'r>>, cons: impl Fn(Value<'r>, Value<'r>) -> Instr<'r>) {
        if let Some(dest) = args.get(0) {
            if let Some(src) = args.get(1) {
                self.0.push(cons(dest.clone(), src.clone()));
            }
        }
    }

    fn build_jump<'l, 'a>(&mut self, labels: &'l mut LabelCalls<'r>, args: &'a Vec<Value<'r>>, v: Instr<'r>) {
        if let Some(val) = args.get(0) {
            let label = val.reg();

            if !label.is_empty() {
                labels.insert(self.0.len(), label);
                self.0.push(v);
            }
        }
    }

    fn link<'c, 'p>(&mut self, lbl_calls: &'c LabelCalls<'r>, labels: &'p LabelPositions<'r>) -> Vec<Instr<'r>> {
        for (pos, label) in lbl_calls {
            if let Some(v) = self.0.get_mut(*pos) {
                match v {
                    Instr::Jmp(_) => { *v = Instr::Jmp(*labels.get(label).unwrap()) }
                    Instr::Jne(_) => { *v = Instr::Jne(*labels.get(label).unwrap()) }
                    Instr::Je(_) => { *v = Instr::Je(*labels.get(label).unwrap()) }
                    Instr::Jge(_) => { *v = Instr::Jge(*labels.get(label).unwrap()) }
                    Instr::Jg(_) => { *v = Instr::Jg(*labels.get(label).unwrap()) }
                    Instr::Jle(_) => { *v = Instr::Jle(*labels.get(label).unwrap()) }
                    Instr::Jl(_) => { *v = Instr::Jl(*labels.get(label).unwrap()) }
                    Instr::Call(_) => { *v = Instr::Call(*labels.get(label).unwrap()) }
                    _ => {}
                }
            }
        }

        self.0.clone()
    }
}

pub struct AssemblerInterpreter {
}

impl AssemblerInterpreter {
    fn parse<'r>(input: &'r str) -> Vec<Instr<'r>> {
        let instr_patt = Regex::new(r"^(\w+)(?:(:)|\s+((?:\w+|'[^']*')(?:\s*,\s*(?:\w+|-\d+|'[^']*'))*))?$").unwrap();
        let arg_patt = Regex::new(r"^(?:(\w+|-\d+)|'([^']*)')(?:\s*,\s*(.+))?$").unwrap();
        let mut label_positions = LabelPositions::new();
        let mut label_calls = LabelCalls::new();
        let mut prog = Program::new(input);

        for line in input.lines().filter_map(trim_line) {
            if let Some(m) = instr_patt.captures(line) {
                let instr = m.get(1).map(match_to_str).unwrap_or("");

                if m.get(2).is_some() {
                    label_positions.insert(instr, prog.size());
                } else {
                    let args = if let Some(args) = m.get(3) {
                        let mut args = args.as_str();
                        let mut res = vec![];

                        while let Some(c) = arg_patt.captures(args) {
                            args = c.get(3).map(match_to_str).unwrap_or("");
                            match (c.get(1).map(match_to_str), c.get(2).map(match_to_str)) {
                                (Some(v), _) => if let Ok(cst) = v.parse::<i64>() {
                                    res.push(Value::Const(cst));
                                } else {
                                    res.push(Value::Reg(v));
                                }
                                (_, Some(v)) => { res.push(Value::Str(v)); }
                                (_, _) => {}
                            }
                        }

                        res
                    } else {
                        vec![]
                    };

                    match instr {
                        "ret" => { prog.add(Instr::Ret); }
                        "end" => { prog.add(Instr::End); }
                        "mov" => { prog.build_op(&args, |r, v| Instr::Mov(r, v)); }
                        "inc" => { prog.build_with_reg(&args, |r| Instr::Inc(r)); }
                        "dec" => { prog.build_with_reg(&args, |r| Instr::Dec(r)); }
                        "add" => { prog.build_op(&args, |r, v| Instr::Add(r, v)); }
                        "sub" => { prog.build_op(&args, |r, v| Instr::Sub(r, v)); }
                        "mul" => { prog.build_op(&args, |r, v| Instr::Mul(r, v)); }
                        "div" => { prog.build_op(&args, |r, v| Instr::Div(r, v)); }
                        "cmp" => { prog.build_with_vals(&args, |v1, v2| Instr::Cmp(v1, v2)); }
                        "jmp" => { prog.build_jump(&mut label_calls, &args, Instr::Jmp(0)); }
                        "jne" => { prog.build_jump(&mut label_calls, &args, Instr::Jne(0)); }
                        "je" => { prog.build_jump(&mut label_calls, &args, Instr::Je(0)); }
                        "jge" => { prog.build_jump(&mut label_calls, &args, Instr::Jge(0)); }
                        "jg" => { prog.build_jump(&mut label_calls, &args, Instr::Jg(0)); }
                        "jle" => { prog.build_jump(&mut label_calls, &args, Instr::Jle(0)); }
                        "jl" => { prog.build_jump(&mut label_calls, &args, Instr::Jl(0)); }
                        "call" => { prog.build_jump(&mut label_calls, &args, Instr::Call(0)); }
                        "msg" => { prog.add(Instr::Msg(args)); }
                        _ => {}
                    }
                }
            }
        }

        prog.link(&label_calls, &label_positions)
    }

    pub fn interpret(input: &str) -> Option<String> {
        let prog = Self::parse(input);
        let mut registers = Registers::new();
        let mut result: Option<String> = None;
        let mut output = String::new();
        let mut stack = vec![];
        let mut pos = 0;
        let mut cmp = Ordering::Equal;

        while let Some(instr) = prog.get(pos) {
            pos += 1;
            match instr {
                Instr::Mov(r, v) => { registers.insert(r, v.get(&registers)); }
                Instr::Inc(r) => { *registers.entry(r).or_insert(0) += 1; }
                Instr::Dec(r) => { *registers.entry(r).or_insert(0) -= 1; }
                Instr::Add(r, v) => { *registers.entry(r).or_insert(0) += v.get(&registers); }
                Instr::Sub(r, v) => { *registers.entry(r).or_insert(0) -= v.get(&registers); }
                Instr::Mul(r, v) => { *registers.entry(r).or_insert(0) *= v.get(&registers); }
                Instr::Div(r, v) => { *registers.entry(r).or_insert(0) /= v.get(&registers); }
                Instr::Cmp(v1, v2) => { cmp = v1.get(&registers).cmp(&v2.get(&registers)); }
                Instr::Jmp(a) => { pos = *a; }
                Instr::Jne(a) => match cmp {
                    Ordering::Equal => {}
                    _ => { pos= *a; }
                }
                Instr::Je(a) => match cmp {
                    Ordering::Equal => { pos= *a; }
                    _ => {}
                }
                Instr::Jge(a) => match cmp {
                    Ordering::Equal|Ordering::Greater => { pos= *a; }
                    _ => {}
                }
                Instr::Jg(a) => match cmp {
                    Ordering::Greater => { pos= *a; }
                    _ => {}
                }
                Instr::Jle(a) => match cmp {
                    Ordering::Equal|Ordering::Less => { pos= *a; }
                    _ => {}
                }
                Instr::Jl(a) => match cmp {
                    Ordering::Less => { pos= *a; }
                    _ => {}
                }
                Instr::Ret => if let Some(a) = stack.pop() { pos = a; }
                Instr::Call(a) => {
                    stack.push(pos);
                    pos = *a;
                }
                Instr::Msg(args) => {
                    output.clear();
                    for arg in args {
                        arg.append_str(&registers, &mut output);
                    }
                }
                Instr::End => {
                    result = Some(output.clone());
                    pos += prog.len();
                }
            }
        }

        result
    }
}
      
____________________________________________________
use std::collections::HashMap;

#[derive(Debug, Clone)]
enum Token {
    Lit(i64),    // an i64 literal
    Reg(String), // a named register
}
impl<S: AsRef<str>> From<S> for Token {
    fn from(s: S) -> Self {
        // if unable to parse as i64, assume register
        match s.as_ref().parse::<i64>() {
            Ok(n) => Self::Lit(n),
            Err(_) => Self::Reg(s.as_ref().into()),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct Label(String);

#[derive(Debug, Clone)]
enum Instruction {
    Mov(Token, Token),
    Inc(Token),
    Dec(Token),
    Add(Token, Token),
    Sub(Token, Token),
    Mul(Token, Token),
    Div(Token, Token),
    Lbl(Label),
    Jmp(Label),
    Cmp(Token, Token),
    Jne(Label),
    Je(Label),
    Jge(Label),
    Jg(Label),
    Jle(Label),
    Jl(Label),
    Call(Label),
    Ret,
    Msg(String),
    End,
}

#[derive(Debug)]
pub struct AssemblerInterpreter {
    ins: Vec<Instruction>,      // Instructions
    pc: usize,                  // Program counter
    sp: Vec<usize>,             // Stack pointer
    cmp: i64,                   // Compare result
    out: String,                // Output
    regs: HashMap<String, i64>, // GP registers
}
impl Default for AssemblerInterpreter {
    fn default() -> Self {
        Self {
            ins: vec![],
            pc: 0,
            sp: vec![],
            cmp: 0,
            out: "".into(),
            regs: HashMap::new(),
        }
    }
}
impl AssemblerInterpreter {
    /// instantiates and parses a string into a list of instructions
    fn parse(input: &str) -> Self {
        let ins = input
            .lines()
            .map(|l| l.trim()) // remove surrounding indentations
            .filter(|l| !l.is_empty() && l.chars().next().unwrap() != ';') // remove comments
            .map(|l| {
                let ins = l
                    .split_ascii_whitespace()
                    .next()
                    .expect("Instruction parsing fatal error: empty line not filtered");
                // handle label
                if let Some(':') = ins.chars().last() {
                    let lbl = ins[..ins.len() - 1].into();
                    return Instruction::Lbl(Label(lbl));
                }
                // handle `msg`
                if ins == "msg" {
                    let arg = l[3..] // remove instruction name
                        .split(';') // strip comment
                        .next()
                        .unwrap() // split always returns at least 1 element, which suits us well here
                        .trim()
                        .into();
                    return Instruction::Msg(arg);
                }
                // handle other instructions
                let args: Vec<_> = l
                    .split_ascii_whitespace()
                    .skip(1) // remove instruction name
                    .collect::<String>()
                    .split(';') // strip comment
                    .next()
                    .unwrap() // split always returns at least 1 element
                    .split(',')
                    .filter(|arg| !arg.is_empty()) // split always returns at least 1 element, even if it's ""
                    .map(|arg| arg.trim().to_string())
                    .collect();
                match ins {
                    "mov" => {
                        assert!(args.len() == 2, "`mov` expects 2 args, found {}", args.len());
                        Instruction::Mov((&args[0]).into(), (&args[1]).into())
                    }
                    "inc" => {
                        assert!(args.len() == 1, "`inc` expects 1 arg, found {}", args.len());
                        Instruction::Inc((&args[0]).into())
                    }
                    "dec" => {
                        assert!(args.len() == 1, "`dec` expects 1 arg, found {}", args.len());
                        Instruction::Dec((&args[0]).into())
                    }
                    "add" => {
                        assert!(args.len() == 2, "`add` expects 2 args, found {}", args.len());
                        Instruction::Add((&args[0]).into(), (&args[1]).into())
                    }
                    "sub" => {
                        assert!(args.len() == 2, "`sub` expects 2 args, found {}", args.len());
                        Instruction::Sub((&args[0]).into(), (&args[1]).into())
                    }
                    "mul" => {
                        assert!(args.len() == 2, "`mul` expects 2 args, found {}", args.len());
                        Instruction::Mul((&args[0]).into(), (&args[1]).into())
                    }
                    "div" => {
                        assert!(args.len() == 2, "`div` expects 2 args, found {}", args.len());
                        Instruction::Div((&args[0]).into(), (&args[1]).into())
                    }
                    "jmp" => {
                        assert!(args.len() == 1, "`jmp` expects 1 arg, found {}", args.len());
                        Instruction::Jmp(Label(args[0].to_owned()))
                    }
                    "cmp" => {
                        assert!(args.len() == 2, "`cmp` expects 2 args, found {}", args.len());
                        Instruction::Cmp((&args[0]).into(), (&args[1]).into())
                    }
                    "jne" => {
                        assert!(args.len() == 1, "`jne` expects 1 arg, found {}", args.len());
                        Instruction::Jne(Label(args[0].to_owned()))
                    }
                    "je" => {
                        assert!(args.len() == 1, "`je` expects 1 arg, found {}", args.len());
                        Instruction::Je(Label(args[0].to_owned()))
                    }
                    "jge" => {
                        assert!(args.len() == 1, "`jge` expects 1 arg, found {}", args.len());
                        Instruction::Jge(Label(args[0].to_owned()))
                    }
                    "jg" => {
                        assert!(args.len() == 1, "`jg` expects 1 arg, found {}", args.len());
                        Instruction::Jg(Label(args[0].to_owned()))
                    }
                    "jle" => {
                        assert!(args.len() == 1, "`jle` expects 1 arg, found {}", args.len());
                        Instruction::Jle(Label(args[0].to_owned()))
                    }
                    "jl" => {
                        assert!(args.len() == 1, "`jl` expects 1 arg, found {}", args.len());
                        Instruction::Jl(Label(args[0].to_owned()))
                    }
                    "call" => {
                        assert!(args.len() == 1, "`call` expects 1 arg, found {}", args.len());
                        Instruction::Call(Label(args[0].to_owned()))
                    }
                    "ret" => {
                        assert!(args.len() == 0, "`ret` expects 0 args, found {}", args.len());
                        Instruction::Ret
                    }
                    "end" => {
                        assert!(args.len() == 0, "`end` expects 0 args, found {}", args.len());
                        Instruction::End
                    }
                    _ => panic!("Unknown instruction: {}", ins),
                }
            })
            .collect();
        Self { ins, ..Self::default() }
    }
    /// instantiate and run
    pub fn interpret(input: &str) -> Option<String> {
        Self::parse(input).run_to_completion()
    }
    /// get value of a Token, either from literal or register
    fn get_val(&self, src: &Token) -> i64 {
        match src {
            Token::Lit(i) => *i,
            Token::Reg(n) => *self.regs.get(n).expect(&format!("Requested register not set: {}", n)),
        }
    }
    /// stores a new value into a register
    fn set_reg(&mut self, tgt: &Token, src: &Token) {
        match tgt {
            Token::Lit(i) => panic!("Cannot set literal: {}", *i),
            Token::Reg(n) => self.regs.insert(n.to_owned(), self.get_val(src)),
        };
    }
    /// find the address of a label in the list of instructions
    fn find_lbl(&self, lbl: &Label) -> usize {
        self.ins
            .iter()
            .position(|ins| if let Instruction::Lbl(l) = ins { l == lbl } else { false })
            .expect(&format!("Undefined label: {:?}", lbl))
    }
    /// run until program terminates via either `end` or EOF
    fn run_to_completion(&mut self) -> Option<String> {
        use Instruction::*;
        loop {
            let ci_opt = self.ins.get(self.pc).cloned();
            match ci_opt {
                // exit conditions
                None => break None,                           // terminates via EOF
                Some(End) => break Some(self.out.to_owned()), // terminates via `end`
                _ => (),                                      // continue
            };
            let ci = ci_opt.unwrap(); // current instruction

            // misc instructions
            match &ci {
                Lbl(_) => {
                    // do nothing
                    self.pc += 1;
                    continue;
                }
                Cmp(a, b) => {
                    self.cmp = self.get_val(a) - self.get_val(b); // set cmp reg
                    self.pc += 1;
                    continue;
                }
                Call(lbl) => {
                    self.sp.push(self.pc); // add return pointer to stack
                    self.pc = self.find_lbl(lbl); // set program counter to label
                    continue;
                }
                Ret => {
                    self.pc = self.sp.pop().expect("Nowhere to return: Stack Pointer is empty") + 1; // return to next instruction
                    continue;
                }
                Msg(args) => {
                    let mut str_tokens = vec!["".to_string()];
                    let mut escaped = false;
                    // cannot use a simple split on ',' because ',' might be within quotes
                    for ch in args.chars() {
                        if ch == '\'' {
                            // toggle escape mode
                            escaped = !escaped;
                        }
                        if ch == ',' && !escaped {
                            // add new token
                            str_tokens.push("".into());
                        } else {
                            // append to last token
                            str_tokens.last_mut().unwrap().push(ch);
                        }
                    }
                    self.out = str_tokens
                        .iter()
                        .map(|seg| seg.trim())
                        .map(|seg| {
                            if seg.starts_with('\'') && seg.ends_with('\'') {
                                // string literal
                                seg[1..seg.len() - 1].into()
                            } else {
                                // register
                                self.get_val(&Token::Reg(seg.into())).to_string()
                            }
                        })
                        .collect();
                    self.pc += 1;
                    continue;
                }
                _ => (),
            };

            // set instructions
            if matches!(
                &ci,
                Mov(_, _) | Inc(_) | Dec(_) | Add(_, _) | Sub(_, _) | Mul(_, _) | Div(_, _)
            ) {
                let (reg, new_val) = match &ci {
                    Mov(tgt, src) => (tgt, self.get_val(src)),
                    Inc(tgt) => (tgt, self.get_val(tgt) + 1),
                    Dec(tgt) => (tgt, self.get_val(tgt) - 1),
                    Add(tgt, src) => (tgt, self.get_val(tgt) + self.get_val(src)),
                    Sub(tgt, src) => (tgt, self.get_val(tgt) - self.get_val(src)),
                    Mul(tgt, src) => (tgt, self.get_val(tgt) * self.get_val(src)),
                    Div(tgt, src) => (tgt, self.get_val(tgt) / self.get_val(src)),
                    _ => unreachable!(),
                }; // compute new value
                self.set_reg(reg, &Token::Lit(new_val)); // write
                self.pc += 1;
                continue;
            };

            // jump instructions
            if matches!(&ci, Jmp(_) | Jne(_) | Je(_) | Jge(_) | Jg(_) | Jle(_) | Jl(_)) {
                let (do_jmp, lbl) = match &ci {
                    Jmp(lbl) => (true, lbl),
                    Jne(lbl) => (self.cmp != 0, lbl),
                    Je(lbl) => (self.cmp == 0, lbl),
                    Jge(lbl) => (self.cmp >= 0, lbl),
                    Jg(lbl) => (self.cmp > 0, lbl),
                    Jle(lbl) => (self.cmp <= 0, lbl),
                    Jl(lbl) => (self.cmp < 0, lbl),
                    _ => unreachable!(),
                }; // check jump condition
                if do_jmp {
                    self.pc = self.find_lbl(lbl) + 1; // jump to just after label
                } else {
                    self.pc += 1;
                }
                continue;
            }

            unreachable!("Unhandled instruction: {:?}", &ci);
        }
    }
}
