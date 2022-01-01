use std::collections::{HashMap, HashSet};
use std::iter::{Peekable, repeat};
use std::mem::swap;
use std::str::Chars;

struct Interpreter {
    variables: HashMap<String, f32>,
    functions: HashMap<String, (Vec<String>, Ast)>,
}

impl Interpreter {
    fn new() -> Interpreter {
        Interpreter { variables: HashMap::new(), functions: HashMap::new() }
    }

    fn input(&mut self, input: &str) -> Result<Option<f32>, String> {
        let funcs = self.functions.iter().map(|(k, v)| (k.clone(), v.0.len())).collect();
        let mut parser = Parser::new(Lexer::new(input), funcs);

        if parser.lexer.peek().is_none() {
            return Ok(None);
        }

        let func = parser.lexer.peek() == Some(&Fn);

        let ast = if func {
            parser.parse_func()?
        } else {
            parser.parse_expr()?
        };

        if parser.lexer.peek().is_some() {
            return Err(format!("expected Eof, got `{:?}`", parser.lexer.collect::<Vec<_>>()));
        }

        let ret = self.eval(ast);

        if func {
            ret.map(|_| None)
        } else {
            ret.map(|x| Some(x))
        }
    }

    fn eval(&mut self, expr: Ast) -> Result<f32, String> {
        match expr {
            Const(num) => Ok(num),
            Var(name) => self.variables.get(&name)
                .cloned().ok_or(format!("unknown variable `{}`", name)),
            Bin(lhs, op, rhs) => Ok(match op {
                '+' => self.eval(*lhs)? + self.eval(*rhs)?,
                '-' => self.eval(*lhs)? - self.eval(*rhs)?,
                '*' => self.eval(*lhs)? * self.eval(*rhs)?,
                '/' => self.eval(*lhs)? / self.eval(*rhs)?,
                '%' => self.eval(*lhs)? % self.eval(*rhs)?,
                _ => unreachable!(),
            }),
            Assign(name, expr) => {
                if self.functions.contains_key(&name) {
                    return Err(format!("existing function with name `{}`", name));
                }
                let value = self.eval(*expr)?;
                self.variables.insert(name, value);
                Ok(value)
            },
            Call(name, args) => {
                let (argn, body) = self.functions.get(&name)
                    .cloned().ok_or(format!("unknown function `{}`", name))?;
                let mut vars = HashMap::new();
                for (arg, expr) in argn.iter().cloned().zip(args) {
                    vars.insert(arg, self.eval(expr)?);
                }
                swap(&mut self.variables, &mut vars);
                let ret = self.eval(body);
                self.variables = vars;
                ret
            },
            Func(name, args, expr) => {
                if self.variables.contains_key(&name) {
                    return Err(format!("existing variable with name `{}`", name));
                }
                let len = args.len();
                if len > args.iter().collect::<HashSet<_>>().len() {
                    return Err(format!("duplicate arguments"));
                }
                self.functions.insert(name.clone(), (args, *expr));
                let ret = self.eval(Call(name.clone(), repeat(Const(0.0)).take(len).collect()));
                if ret.is_err() {
                    self.functions.remove(&name);
                }
                ret
            },
        }
    }
}

use Token::*;

#[derive(PartialEq, Eq, Clone, Debug)]
enum Token {
    Ident(String),
    Num(String),
    BinOp(char),
    OpenParen,
    CloseParen,
    FatArrow,
    Eq,
    Fn,
}

struct Lexer<'a> {
    input: Peekable<Chars<'a>>,
}

impl<'a> Lexer<'a> {
    fn new(input: &'a str) -> Lexer<'a> {
        Lexer { input: input.chars().peekable() }
    }

    fn take_while<P: FnMut(&char) -> bool>(&mut self, mut predicate: P) -> String {
        let mut ret = String::new();
        while let Some(c) = self.input.peek().cloned() {
            if !predicate(&c) {
                break;
            }
            self.input.next();
            ret.push(c);
        }
        ret
    }
}

impl<'a> Iterator for Lexer<'a> {
    type Item = Token;
    
    fn next(&mut self) -> Option<Token> {
        self.take_while(|c| c.is_whitespace());
        if let Some(c) = self.input.peek().cloned() {
            match c {
                c if c.is_alphabetic() => {
                    let ident = self.take_while(|c| c.is_alphanumeric() || c == &'_');
                    if ident == "fn" {
                        return Some(Fn);
                    }
                    return Some(Ident(ident));
                },
                c if c.is_digit(10) => return Some(Num(self.take_while(|c| c.is_digit(10) || c == &'.'))),
                '+' | '-' | '*' | '/' | '%' => { self.input.next(); return Some(BinOp(c)); },
                '(' => { self.input.next(); return Some(OpenParen); },
                ')' => { self.input.next(); return Some(CloseParen); },
                '=' => {
                    self.input.next();
                    if let Some(&'>') = self.input.peek() {
                        self.input.next();
                        return Some(FatArrow);
                    }
                    return Some(Eq);
                },
                _ => (),
            }
        }
        None
    }
}

use Ast::*;

#[derive(Clone, Debug)]
enum Ast {
    Const(f32),
    Var(String),
    Bin(Box<Ast>, char, Box<Ast>),
    Assign(String, Box<Ast>),
    Call(String, Vec<Ast>),
    Func(String, Vec<String>, Box<Ast>),
}

struct Parser<'a> {
    lexer: Peekable<Lexer<'a>>,
    funcs: HashMap<String, usize>,
}

impl<'a> Parser<'a> {
    fn new(lexer: Lexer<'a>, funcs: HashMap<String, usize>) -> Parser<'a> {
        Parser { lexer: lexer.peekable(), funcs: funcs }
    }

    fn prec(&mut self) -> i32 {
        match self.lexer.peek() {
            Some(&BinOp(ref op)) => {
                match op.clone() {
                    '*' | '/' | '%' => 3,
                    '+' | '-' => 2,
                    _ => 1,       
                }
            },
            _ => 0,
        }
    }

    fn parse_expr(&mut self) -> Result<Ast, String> {
        let lhs = self.parse_factor()?;
        self.parse_expr_rhs(lhs, 0)
    }

    fn parse_expr_rhs(&mut self, lhs: Ast, lhs_prec: i32) -> Result<Ast, String> {
        let prec = self.prec();
        if prec <= lhs_prec {
            return Ok(lhs);
        }
        let op = match self.lexer.next() {
            Some(BinOp(op)) => op,
            e => return Err(format!("expected BinOp, got `{:?}`", e)),
        };
        let rhs = self.parse_factor()?;
        let next_prec = self.prec();
        if prec < next_prec {
            return Ok(Bin(Box::new(lhs), op, Box::new(self.parse_expr_rhs(rhs, prec)?)));
        }
        self.parse_expr_rhs(Bin(Box::new(lhs), op, Box::new(rhs)), 0)
    }

    fn parse_factor(&mut self) -> Result<Ast, String> {
        match self.lexer.next() {
            Some(Num(num)) => Ok(Const(num.parse().unwrap())),
            Some(OpenParen) => {
                let expr = self.parse_expr()?;
                match self.lexer.next() {
                    Some(CloseParen) => (),
                    e => return Err(format!("expected CloseParen, got `{:?}`", e)),
                }
                Ok(expr)
            },
            Some(Ident(ident)) => {
                if let Some(&Eq) = self.lexer.peek() {
                    self.lexer.next();
                    let expr = self.parse_expr()?;
                    return Ok(Assign(ident, Box::new(expr)));
                }
                if let Some(argc) = self.funcs.get(&ident).cloned() {
                    let mut args = Vec::new();
                    for _ in 0..argc {
                        args.push(self.parse_expr()?)
                    }
                    return Ok(Call(ident, args));
                }
                Ok(Var(ident))
            }
            e => Err(format!("expected Factor, got `{:?}`", e)),
        }
    }

    fn parse_func(&mut self) -> Result<Ast, String> {
        match self.lexer.next() {
            Some(Fn) => (),
            e => return Err(format!("expected Fn, got `{:?}`", e)),
        }
        let name = match self.lexer.next() {
            Some(Ident(name)) => name,
            e => return Err(format!("expected Ident, got `{:?}`", e)),
        };
        let mut args = Vec::new();
        while let Some(Ident(arg)) = self.lexer.peek().cloned() {
            self.lexer.next();
            args.push(arg);
        }
        match self.lexer.next() {
            Some(FatArrow) => (),
            e => return Err(format!("expected FatArrow, got `{:?}`", e)),
        }
        Ok(Func(name, args, Box::new(self.parse_expr()?)))
    }
}
      
___________________________________________________________________________
extern crate regex;

use regex::Regex;

struct Interpreter {m: Memory}

struct Memory {f: Vec<Function>, v: Vec<Variable>}

#[derive(Debug)]
struct Function {name: String, input: String, output: String}

#[derive(Debug)]
struct Variable{name: String, value: String}

fn str_replace(input: &String, start: usize, end: usize, replacement: String) -> String{
    format!("{}{}{}", &input[..start], &replacement, &input[end..])
}

impl Interpreter {
    fn new() -> Interpreter {
        Interpreter{m: Memory{f: Vec::new(), v: Vec::new()}}
    }

    fn input(&mut self, input: &str) -> Result<Option<f32>, String> {
        println!("{:?}", input);
        let mut inp = String::from(input);
        let re = Regex::new(r"(?P<s>\()(?P<e>[a-zA-Z0-9]+(\.[0-9]+)?)").unwrap();
        inp = re.replace_all(&inp, "$s $e").to_string();
        let re = Regex::new(r"(?P<s>[a-zA-Z0-9]+(\.[0-9]+)?)(?P<e>\))").unwrap();
        inp = re.replace_all(&inp, "$s $e").to_string();
        let list = vec![
            r"fn\s(?P<name>[a-zA-z]+)\s(?P<input>([a-zA-z]+\s?)*)\s?=>\s(?P<output>.+)",
            r"(?P<num1>[0-9]+(\.[0-9]+)?)\s*(?P<operator>[\*/%])\s*(?P<num2>[0-9]+(\.[0-9]+)?)",
            r"(?P<num1>[0-9]+(\.[0-9]+)?)\s*(?P<operator>[\+-])\s*(?P<num2>[0-9]+(\.[0-9]+)?)",
            r"\s(?P<name>[a-zA-z]+)(?P<input>(\s[0-9]+(\.[0-9]+)?)+)",
            r"(?P<name>[a-zA-z]+)(?P<input>(\s[0-9]+(\.[0-9]+)?)+)",
            r"\s(?P<name>[a-zA-z]+)\s*=\s*(?P<val>[0-9]+(\.[0-9]+)?)",
            r"(?P<name>[a-zA-z]+)\s*=\s*(?P<val>[0-9]+(\.[0-9]+)?)",
            r"=\s(?P<name>[a-zA-z]+)",
            r"(?P<name>[a-zA-z]+)",
            ];
        let mut finder: bool = true; 
        while finder {
            let r = Regex::new(r"\(\s*(?P<e>[0-9]+(\.[0-9]+)?)\s*\)").unwrap();
            inp = r.replace_all(&inp, "$e").to_string();
            for (i, reg) in list.iter().enumerate(){
                let re = Regex::new(reg).unwrap();
                let pos = re.find(&inp);
                if pos == None && i == list.len() - 1 {finder = false; continue;} else if pos == None {continue;}
                let cap = re.captures(&inp).unwrap();
                inp = str_replace(&inp, pos.unwrap().start(), pos.unwrap().end(), match i {
                    1 => { let num1 = &cap["num1"].parse::<f32>().unwrap();
                        let num2 = &cap["num2"].parse::<f32>().unwrap();
                        match &cap["operator"] {
                        "*" => num1 * num2,
                        "/" => num1 / num2,
                        "%" => num1 % num2,
                        _ => 0_f32,
                    }.to_string()},
                    2 => { let num1 = &cap["num1"].parse::<f32>().unwrap();
                        let num2 = &cap["num2"].parse::<f32>().unwrap();
                        match &cap["operator"] {
                        "+" => num1 + num2,
                        "-" => num1 - num2,
                        _ => 0_f32,
                    }.to_string()},
                    5|6 => { let name = &cap["name"];
                        let val = &cap["val"].to_string(); 
                        if (&self.m.f).into_iter().any(|x| x.name == name) {return Err("error 5|6".to_string());}
                        self.m.v.retain(|x| &x.name != name);
                        self.m.v.push(Variable{name: name.to_string(), value: val.clone().to_string()});    
                        val.to_string()
                    },
                    7|8 => { let name = &cap["name"];
                        let mut val = String::new(); 
                        self.m.v.retain(|x| (if &x.name == name {val = x.value.clone();}, true).1);
                        self.m.f.retain(|x| (if &x.name == name && x.input.len() == 0 {val = x.output.clone();}, true).1);
                        if val.is_empty() {return Err("error 7|8".to_string());} else {
                            if i == 8 {val} else {format!("= {}", val)}}
                    },
                    0 => { let name = &cap["name"];
                        let _i = &cap["input"]; 
                        let _o = &cap["output"]; 
                        if (&self.m.v).into_iter().any(|x| x.name == name) {return Err("error 0".to_string());}
                        let mut vec_i = _i.clone().split_whitespace().collect::<Vec<&str>>();
                        let sl = vec_i.len();
                        let vec_o = _o.clone().split_whitespace().collect::<Vec<&str>>();
                        vec_i.sort(); vec_i.dedup();
                        if sl != vec_i.len() {return Err("error 0".to_string());}
                        let vec_diff = vec_o.into_iter().filter(|x| !vec_i.contains(x)).collect::<Vec<&str>>();
                        if Regex::new(r"[a-zA-Z]+").unwrap().find(&vec_diff.join(" ")) != None 
                        {return Err("error 0".to_string());} 
                        self.m.f.retain(|x| &x.name != name);
                        self.m.f.push(Function{name: name.to_string(), input: _i.to_string(), output: _o.to_string()}); 
                        String::new()
                    },
                    3|4 => { let name = &cap["name"];
                        let _i = &cap["input"]; 
                        let vec_i = _i.split_whitespace().collect::<Vec<&str>>();
                        let mut f_i = String::new(); 
                        let mut f_o = String::new(); 
                        self.m.f.retain(|x| (if &x.name == name {f_i = x.input.clone(); f_o = x.output.clone()},true).1);
                        if f_i.is_empty() {return Err("error 3|4".to_string());}
                        let vec_f_i = f_i.split_whitespace().collect::<Vec<&str>>();
                        let vec_f_o = f_o.split_whitespace().collect::<Vec<&str>>();
                        if vec_i.len() != vec_f_i.len() {return Err("error 3|4".to_string());}
                        format!(" {}", vec_f_o.into_iter().map(|x| match vec_f_i.contains(&x){
                            true => vec_i[vec_f_i.binary_search(&x).unwrap()],
                            false => x,
                        }).collect::<Vec<&str>>().join(" "))
                    },
                    _ => String::new()
                });
                println!("{:?}", inp);
                break;
            }
        }
        if inp.chars().nth(0) == Some(' ') {inp = inp[1..].to_string();}
        match inp.parse::<f32>() {
            Ok(res) => Ok(Some(res)),
            _ => {
                let r = Regex::new(r"\s").unwrap();
                inp = r.replace_all(&inp, "").to_string();
                match inp.len(){
                0 => Ok(None),
                _ => Err("input error".to_string()),
                }
            }
        }
    }
}
