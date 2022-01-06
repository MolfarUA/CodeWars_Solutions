#![allow(illegal_floating_point_literal_pattern)]

use self::Exp::{BinaryOp, SingleOp, Value, Variable};
use std::boxed::Box;
use std::fmt::{Display, Error, Formatter};
use std::ops::{Add, Div, Mul, Sub};

#[derive(Debug, PartialEq, Clone)]
enum Exp<'a> {
    SingleOp(&'a str, Box<Exp<'a>>),
    BinaryOp(&'a str, Box<Exp<'a>>, Box<Exp<'a>>),
    Value(f64),
    Variable,
}

fn parser(s: &str) -> Exp {
    if s.starts_with('(') {
        let (operator, rest) = s[1..].split_at(s.find(' ').unwrap() - 1);
        let rest = &rest[1..];
        match operator {
            "*" | "+" | "-" | "/" | "^" => {
                let (arg1, rest) = if rest.starts_with('(') {
                    let mut count = 0;
                    let idx = rest
                        .chars()
                        .position(|c| {
                            match c {
                                '(' => count += 1,
                                ')' => count -= 1,
                                _ => {}
                            };
                            c == ')' && count == 0
                        })
                        .unwrap();
                    rest.split_at(idx + 1)
                } else {
                    let idx = match rest.find(' ') {
                        Some(idx) => idx,
                        None => rest.len() - 1,
                    };
                    rest.split_at(idx)
                };
                let rest = &rest[1..rest.len() - 1];
                BinaryOp(operator, Box::new(parser(arg1)), Box::new(parser(rest)))
            }
            "sin" | "cos" | "tan" | "exp" | "ln" => {
                // single op
                SingleOp(operator, Box::new(parser(&rest[..rest.len() - 1])))
            }
            _ => panic!("not a valid operator"),
        }
    } else if s == "x" {
        Variable
    } else {
        Value(s.parse().unwrap())
    }
}

impl<'a> Exp<'a> {
    fn diff_exp(&self) -> Exp {
        match self {
            Variable => Value(1f64),
            Value(_) => Value(0f64),
            SingleOp(op, arg) => {
                let res = arg.diff_exp();
                let arg = *arg.clone();
                match *op {
                    "sin" => res * arg.cos(),
                    "cos" => res * Value(-1f64) * arg.sin(),
                    "tan" => res * (Value(1f64) + (arg.tan().pow(Value(2f64)))),
                    "ln" => res * (Value(1f64) / arg.clone()),
                    "exp" => res * self.clone(),
                    _ => Value(0f64),
                }
            }
            BinaryOp(op, arg1, arg2) => {
                let res1 = arg1.diff_exp();
                let res2 = arg2.diff_exp();
                let arg1 = *arg1.clone();
                let arg2 = *arg2.clone();
                let res = match *op {
                    "+" => res1 + res2,
                    "-" => res1 - res2,
                    "*" => {println!("{}*{} + {}*{}", res1, arg2, arg1,res2);res1 * arg2 + arg1 * res2},
                    "/" => (res1 * arg2.clone() - res2 * arg1) / (arg2.clone() * arg2.clone()),
                    "^" => {
                        if arg1.has_variable() {
                            // x ^ a
                            arg2.clone() * (arg1.pow(arg2 - Value(1f64))) * res1
                        } else {
                            // a ^ x
                            res2 * arg2.ln() * self.clone()
                        }
                    }
                    _ => Value(0f64),
                };
                println!("{} => {}",self, res);
                res
            }
        }
    }

    fn simplify(&self) -> Self {
        match self {
            BinaryOp(op, arg1, arg2) => {
                let arg1 = (*arg1.clone()).simplify();
                let arg2 = (*arg2.clone()).simplify();
                match *op {
                    "+" => arg1 + arg2,
                    "-" => arg1 - arg2,
                    "*" => arg1 * arg2,
                    "/" => arg1 /arg2,
                    "^" => arg1.pow(arg2),
                    _ => Value(0f64)
                }
            }
            SingleOp(op, arg) => {
                let arg = (*arg.clone()).simplify();
                match *op {
                    "exp" => arg.exp(),
                    "sin" => arg.sin(),
                    "cos" => arg.cos(),
                    "tan" => arg.tan(),
                    "ln" => arg.ln(),
                    _ => Value(0f64),
                }
            }
            v => v.clone()
        }
    }

    fn has_variable(&self) -> bool {
        match self {
            SingleOp(_, arg) => arg.has_variable(),
            BinaryOp(_, arg1, arg2) => arg1.has_variable() || arg2.has_variable(),
            Value(_) => false,
            Variable => true,
        }
    }

    fn pow(self, rhs: Self) -> Self {
        match (self, rhs) {
            (Value(a), Value(b)) => Value(a + b),
            (Value(1f64), _) => Value(1f64),
            (_, Value(0f64)) => Value(1f64),
            (e, Value(1f64)) => e,
            (e1, e2) => BinaryOp("^", Box::new(e1), Box::new(e2)),
        }
    }

    fn sin(&self) -> Self {
        SingleOp("sin", Box::new(self.clone()))
    }

    fn cos(&self) -> Self {
        SingleOp("cos", Box::new(self.clone()))
    }
    fn tan(&self) -> Self {
        SingleOp("tan", Box::new(self.clone()))
    }
    fn ln(&self) -> Self {
        SingleOp("ln", Box::new(self.clone()))
    }
    fn exp(&self) -> Self {
        SingleOp("exp", Box::new(self.clone()))
    }
}

impl<'a> Display for Exp<'a> {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result<(), Error> {
        match self {
            Variable => write!(f, "x"),
            Value(v) => write!(f, "{}", v),
            SingleOp(op, arg) => write!(f, "({} {})", op, arg),
            BinaryOp(op, arg1, arg2) => write!(f, "({} {} {})", op, arg1, arg2),
        }
    }
}

impl<'a> Add for Exp<'a> {
    type Output = Self;

    fn add(self, rhs: Self) -> Self {
        match (self, rhs) {
            (Value(a), Value(b)) => Value(a + b),
            (Value(0f64), e) | (e, Value(0f64)) => e,
            (e1, e2) => BinaryOp("+", Box::new(e1), Box::new(e2)),
        }
    }
}

impl<'a> Sub for Exp<'a> {
    type Output = Self;

    fn sub(self, rhs: Self) -> Self {
        match (self, rhs) {
            (Value(a), Value(b)) => Value(a - b),
            (e, Value(0f64)) => e,
            (e1, e2) => BinaryOp("-", Box::new(e1), Box::new(e2)),
        }
    }
}

impl<'a> Mul for Exp<'a> {
    type Output = Self;

    fn mul(self, rhs: Self) -> Self::Output {
        if self.has_variable() && self == rhs {
            return self.pow(Value(2f64));
        }
        match (self, rhs) {
            (Value(a), Value(b)) => Value(a * b),
            (Value(0f64), _) | (_, Value(0f64)) => Value(0f64),
            (Value(1f64), e) | (e, Value(1f64)) => e,
            (e1, e2) => BinaryOp("*", Box::new(e1), Box::new(e2)),
        }
    }
}

impl<'a> Div for Exp<'a> {
    type Output = Self;

    fn div(self, rhs: Self) -> Self::Output {
        match (self, rhs) {
            (Value(a), Value(b)) => Value(a / b),
            (e1, e2) => BinaryOp("/", Box::new(e1), Box::new(e2)),
        }
    }
}

fn diff(expr: &str) -> String {
    let ans = parser(expr).simplify().diff_exp().to_string();
    println!("{} => {}", expr, ans);
    ans
}
______________________________________________
use std::fmt;
use std::rc::Rc;
use Expression::*;
use Token::*;

fn diff(expr: &str) -> String {
    format!("{}", simplify(diff_raw(Rc::new(Expression::parse(expr)))))
}

// Return an unsimplified derivative 
fn diff_raw<'a>(expression: Rc<Expression<'a>>) -> Rc<Expression<'a>> {
    let d = |e: &Rc<Expression<'a>>| diff_raw(e.clone()); //maybe simplify?
    let c = |e: &Rc<Expression<'a>>| e.clone();
    let op = |s, f: Rc<Expression<'a>>, g: Rc<Expression<'a>>|
                Rc::new(Operator(s, f, g));
    let func = |s, f: Rc<Expression<'a>>|
                Rc::new(Function(s, f));
    let chain = |f_prime: Rc<Expression<'a>>, g: Rc<Expression<'a>>|
                op("*", f_prime, d(&g));
    let constant = |n| Rc::new(Constant(n));
    match &*expression {
        Identity => constant(1.0),
        Constant(_) => constant(0.0),
        Operator("+", f, g) => op("+", d(f), d(g)), 
        Operator("-", f, g) => op("-", d(f), d(g)),
        Operator("*", f, g) =>
            op("+", op("*", d(f), c(g)), op("*", c(f), d(g))),
        Operator("/", f, g) =>
            op( "/", 
                op("-", op("*", d(f), c(g)), op("*", c(f), d(g))),
                op("^", c(g), constant(2.0))
            ),
        Operator("^", f, g) => {
            match &&**f {
                // if p(x) = a^x: p(q(x))' = a^q(x) * ln a * q'(x)  
                Constant(_) => 
                    op("*", 
                       op("*", op("^", c(f), c(g)), func("ln", c(f))),
                       d(g)
                ),
                // p(x) = x^a: p(q(x))' = a * q(x)^(a - 1) * q'(x)
                _ => match &&**g {
                    Constant(n) => 
                        op("*", 
                           op("*", c(g), op("^", c(f), constant(n - 1.0))),
                           d(f)
                    ),
                    _ => panic!("f(x) = x ^ x or something similar"),
                }
            }
        },
        Function("sin", f) => chain(func("cos", c(f)), c(f)),
        Function("cos", f) =>
            chain(op("*", constant(-1.0), func("sin", c(f))), c(f)), 
        Function("tan", f) => {
            let tan2x = op("^", func("tan", c(f)), constant(2.0));
            chain(op("+", constant(1.0), tan2x), c(f)) 
        },
        Function("exp", f) => chain(func("exp", c(f)), c(f)),
        Function("ln", f) => chain(op("/", constant(1.0), c(f)), c(f)),
        unknown => panic!("Unrecognised expression: {}", unknown)
        }
    }

// Simplify an expression
fn simplify<'a>(expression: Rc<Expression<'a>>) -> Rc<Expression<'a>> {
    match &*expression {
        Operator(s, f, g) => {
            match simplify_op(s, f.clone(), g.clone()) {
                Some(e) => simplify(e),
                _ => {
                    let f = simplify(f.clone());
                    let g = simplify(g.clone());
                    match simplify_op(s, f.clone(), g.clone()) {
                        Some(e) => simplify(e),
                        _ => Rc::new(Operator(s, f, g))
                    }
                }
            }
        },
        Function(s, f) => Rc::new(Function(s, simplify(f.clone()))),
        _ => expression,
    }
}

// Simplify an operator expression, returning None if no simplifications
// were performed. This allows us to stop recursively simplifying if None 
// is returned.
fn simplify_op<'a>(s: &'a str, f: Rc<Expression<'a>>, g: Rc<Expression<'a>>)
    -> Option<Rc<Expression<'a>>>
{
    let constant = |n| Rc::new(Constant(n));
    let op = |s, f, g| Rc::new(Operator(s, f, g));
    match (&*f, &*g) { 
        (Constant(m), Constant(n)) => {
            Some(constant(match s {
                "+" => m + n,
                "-" => m - n,
                "*" => m * n,
                "/" => m / n,
                "^" => m.powf(*n),
                _ => panic!("Unknown operator {}", s)
            }))
        }
        (Constant(m), _) => {
            match *m as i64 {
                0 => Some(match s {
                    "+" => simplify(g.clone()),
                    "-" => op("*", constant(-1.0), simplify(g.clone())),
                    "*" | "/" | "^" => constant(0.0),
                    _ => panic!("Unknown operator {}", s)
                }),
                1 => match s {
                    "*" => Some(simplify(g.clone())),
                    "^" => Some(constant(1.0)),
                    _ => None
                },
                _ => None
            }
        },
        (_, Constant(n)) => {
            match *n as i64 {
                0 => Some(match s {
                    "+" | "-" => simplify(f.clone()),
                    "*" => constant(0.0),
                    "/" => panic!("Division by zero"),
                    "^" => constant(1.0),
                    _ => panic!("Unknown operator {}", s)
                }),
                1 => match s {
                    "*" | "/" | "^" => Some(simplify(f.clone())),
                    _ => None
                },
                _ => match s {
                    "+" | "*" => Some(op(s, constant(*n), f.clone())),
                    _ => None
                }
            }
        },
        _ => None
    }
}

#[derive(Debug)]
enum Expression<'a> {
    Identity,       // i.e. the variable 'x'
    Constant(f64),  
    Function(&'a str, Rc<Expression<'a>>),
    Operator(&'a str, Rc<Expression<'a>>, Rc<Expression<'a>>),
}

impl<'a> Expression<'a> {
    fn parse(input: &'a str) -> Expression<'a> {
        Expression::from_token(Token::parse(input))
    }

    fn from_token(token: Token<'a>) -> Expression {
        match token {
            Bracket(v) => Expression::from_tokens(v),
            Word("x") => Identity,
            Word(s) => Constant(s.parse().expect("Expected a number"))
        }
    }

    fn from_tokens(tokens: Vec<Token<'a>>) -> Expression<'a> {
        let to_expr = |tok| Rc::new(Expression::from_token(tok));
        let mut tokens = tokens.into_iter();
        let expr = match (tokens.next(), tokens.next(), tokens.next()) {
            (Some(e), None, _) => Expression::from_token(e),
            (Some(Word(func)), Some(arg), None) => 
                Function(func, to_expr(arg)),
            (Some(Word(func)), Some(arg1), Some(arg2)) => 
                Operator(func, to_expr(arg1), to_expr(arg2)),
            _ => panic!("Empty expression")
        };
        if tokens.next().is_some() {
            panic!("Expression has three arguments");
        }
        expr
    }
}

impl<'a> fmt::Display for Expression<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let show = match self {
            Identity => "x".to_string(),
            Constant(n) => format!("{}", n),
            Function(func, arg) => format!("({} {})", func, arg),
            Operator(func, a1, a2) => format!("({} {} {})", func, a1, a2)
        };
        write!(f, "{}", show)
    }
}
       
#[derive(Debug)]
enum Token<'a> {
    Word(&'a str),
    Bracket(Vec<Token<'a>>)
}

impl<'a> Token<'a> {
    fn parse(input: &'a str) -> Token<'a> {
        let input = {
            if input.starts_with('(') && input.ends_with(')') {
                &input[1..(input.len() - 1)]
            } else {
                input
            }
        };
        let mut split1 = input.splitn(2, '('); 
        let left = split1.next().unwrap();
        let right = split1.next();
        println!("Parsing; left = '{}'; right = '{:?}'", left, right);
        let mut token_vec: Vec<Token> =
            left.split_whitespace().map(|s| Word(s)).collect();
        match right {
            None => (),
            Some(s) => {
                let mut split2 = s.rsplitn(2, ')');
                let end = split2.next();    // note reverse order;
                let middle = split2.next(); // rsplit iterates backwards.
                token_vec.extend(middle.iter().map(|s| Token::parse(s)));
                token_vec.extend(
                    end.expect("Missing end parenthesis")
                        .split_whitespace()
                        .map(|s| Word(s))
                );
            }
        }
        Bracket(token_vec)
    }
}
______________________________________________
use std::collections::HashMap;

fn diff(expr: &str) -> String {
    Node::new(expr).derivative().simplify().expand()
}

enum Node {
    None,
    Var,
    Val(f64),
    Neg(Box<Node>),
    Add(Box<Node>, Box<Node>),
    Sub(Box<Node>, Box<Node>),
    Mul(Box<Node>, Box<Node>),
    Div(Box<Node>, Box<Node>),
    Pow(Box<Node>, Box<Node>),
    Cos(Box<Node>),
    Sin(Box<Node>),
    Tan(Box<Node>),
    Exp(Box<Node>),
    Log(Box<Node>),
}

impl Node {
    fn new(expr: &str) -> Node {
        let arities: HashMap<&str, usize> = vec![
            ("+", 2), ("-", 2), ("*", 2), ("/", 2), ("^", 2), ("cos", 1), ("sin", 1), ("tan", 1), ("exp", 1), ("ln", 1)
        ].into_iter().collect();

        enum Token { None, Int, Num, Ident }

        struct ParseContext {
            stack: Vec<Node>,
            ops: Vec<(String, usize)>,
            op: String,
            pos: usize,
            ident: String,
            num: u128,
            dec: i32,
            neg: bool,
            token: Token,
        }

        impl ParseContext {
            fn new() -> ParseContext {
                ParseContext {
                    stack: Vec::new(),
                    ops: Vec::new(),
                    op: String::new(),
                    pos: 0,
                    ident: String::new(),
                    num: 0,
                    dec: 0,
                    neg: false,
                    token: Token::None,
                }
            }

            fn make_result_node(&mut self) -> Node {
                self.stack.pop().unwrap_or(Node::None)
            }

            fn append_to_ident(&mut self, ch: char) {
                self.token = Token::Ident;
                self.ident.push(ch);
            }

            fn append_to_num(&mut self, ch: char) {
                if let Some(digit) = ch.to_digit(10) {
                    self.num = (self.num * 10) + (digit as u128);
                    if let Token::Num = self.token {
                        self.dec -= 1;
                    } else {
                        self.token = Token::Int;
                    }
                }
            }

            fn enable_decimal(&mut self) {
                self.token = Token::Num;
            }

            fn enable_neg(&mut self) {
                self.neg = true;
            }

            fn commit_node(&mut self, arities: &HashMap<&str, usize>) {
                match self.token {
                    Token::Num|Token::Int => {
                        let mut v = self.num as f64;

                        if self.neg { v = -v; }
                        if self.dec != 0 { v *= 10f64.powi(self.dec); }

                        self.stack.push(Node::Val(v));
                    }
                    Token::Ident => {
                        if self.ident == "x" {
                            self.stack.push(Node::Var);
                        } else {
                            if !self.op.is_empty() { self.ops.push((self.op.clone(), self.pos)); }
                            self.pos = self.stack.len();
                            self.op = self.ident.clone();
                        }
                    }
                    _ => {}
                }

                self.token = Token::None;
                self.ident.clear();
                self.num = 0;
                self.dec = 0;
                self.neg = false;

                while !self.op.is_empty() {
                    let arg_count = self.stack.len() - self.pos;

                    if arg_count < 1 { return }
                    if let Some(arity) = arities.get(self.op.as_str()) {
                        if arg_count.lt(arity) { return }

                        let mut args = self.stack.drain(self.pos..).map(Box::new).collect::<Vec<_>>();
                        let arg = args.remove(0);

                        match self.op.as_str() {
                            "+" => { self.stack.push(Node::Add(arg, args.remove(0))); }
                            "-" => { self.stack.push(Node::Sub(arg, args.remove(0))); }
                            "*" => { self.stack.push(Node::Mul(arg, args.remove(0))); }
                            "/" => { self.stack.push(Node::Div(arg, args.remove(0))); }
                            "^" => { self.stack.push(Node::Pow(arg, args.remove(0))); }
                            "cos" => { self.stack.push(Node::Cos(arg)); }
                            "sin" => { self.stack.push(Node::Sin(arg)); }
                            "tan" => { self.stack.push(Node::Tan(arg)); }
                            "exp" => { self.stack.push(Node::Exp(arg)); }
                            "ln" => { self.stack.push(Node::Log(arg)); }
                            _ => {}
                        }

                        if let Some((op, pos)) = self.ops.pop() {
                            self.op = op;
                            self.pos = pos;
                        } else {
                            self.op.clear();
                            self.pos = self.stack.len()
                        }
                    }
                }
            }
        }

        let mut ctx = ParseContext::new();
        let mut prev: char = 'Ø';

        for c in expr.chars() {
            match c {
                c @ '0'..='9' => { ctx.append_to_num(c); }
                c @ 'a'..='z' | c @ '+' | c @ '*' | c @ '/' | c @ '^' => {
                    ctx.append_to_ident(c);
                }
                '-' => if prev == ' ' { ctx.enable_neg(); } else { ctx.append_to_ident('-'); }
                '.' => { ctx.enable_decimal(); }
                '('|')'|' ' => { ctx.commit_node(&arities); }
                _ => {}
            }

            prev = c;
        }

        ctx.commit_node(&arities);
        ctx.make_result_node()
    }

    fn expand(&self) -> String {
        match self {
            Node::None => "0".to_string(),
            Node::Var => "x".to_string(),
            Node::Val(v) => format!("{}", v),
            Node::Neg(x) => format!("(* -1 {})", x.expand()),
            Node::Add(lhs, rhs) => format!("(+ {} {})", lhs.expand(), rhs.expand()),
            Node::Sub(lhs, rhs) => format!("(- {} {})", lhs.expand(), rhs.expand()),
            Node::Mul(lhs, rhs) => format!("(* {} {})", lhs.expand(), rhs.expand()),
            Node::Div(lhs, rhs) => format!("(/ {} {})", lhs.expand(), rhs.expand()),
            Node::Pow(lhs, rhs) => format!("(^ {} {})", lhs.expand(), rhs.expand()),
            Node::Cos(x) => format!("(cos {})", x.expand()),
            Node::Sin(x) => format!("(sin {})", x.expand()),
            Node::Tan(x) => format!("(tan {})", x.expand()),
            Node::Exp(x) => format!("(exp {})", x.expand()),
            Node::Log(x) => format!("(ln {})", x.expand()),
        }
    }

    fn derivative(&self) -> Box<Node> {
        Box::new(match self {
            Node::None => Node::None,
            Node::Var => Node::Val(1.),
            Node::Val(_) => Node::Val(0.),
            Node::Neg(x) => Node::Neg(x.derivative()),
            Node::Add(lhs, rhs) => Node::Add(lhs.derivative(), rhs.derivative()),
            Node::Sub(lhs, rhs) => Node::Sub(lhs.derivative(), rhs.derivative()),
            Node::Mul(lhs, rhs) => Node::Add(
                Box::new(Node::Mul(lhs.derivative(), rhs.clone())),
                Box::new(Node::Mul(lhs.clone(), rhs.derivative())),
            ),
            Node::Div(lhs, rhs) => Node::Div(
                Box::new(Node::Sub(
                    Box::new(Node::Mul(lhs.derivative(), rhs.clone())),
                    Box::new(Node::Mul(lhs.clone(), rhs.derivative())),
                )),
                Box::new(Node::Pow(rhs.clone(), Box::new(Node::Val(2.)))),
            ),
            Node::Pow(lhs, rhs) => Node::Mul(
                Box::new(Node::Mul(
                    rhs.clone(),
                    Box::new(Node::Pow(
                        lhs.clone(),
                        Box::new(Node::Sub(rhs.clone(), Box::new(Node::Val(1.)))),
                    )),
                )),
                lhs.derivative(),
            ),
            Node::Cos(x) => Node::Mul(
                Box::new(Node::Neg(x.derivative())),
                Box::new(Node::Sin(x.clone())),
            ),
            Node::Sin(x) => Node::Mul(
                x.derivative(),
                Box::new(Node::Cos(x.clone())),
            ),
            Node::Tan(x) => Node::Mul(
                x.derivative(),
                Box::new(Node::Add(
                    Box::new(Node::Val(1.)),
                    Box::new(Node::Pow(
                        Box::new(Node::Tan(x.clone())),
                        Box::new(Node::Val(2.))
                    )),
                )),
            ),
            Node::Exp(x) => Node::Mul(x.derivative(), Box::new(Node::Exp(x.clone()))),
            Node::Log(x) => Node::Div(x.derivative(), x.clone()),
        })
    }

    fn compute(self) -> Node {
        match self {
            Node::None => Node::None,
            Node::Var => Node::Var,
            Node::Val(v) => Node::Val(v),
            Node::Neg(x) => match x.compute() {
                Node::None => Node::None,
                Node::Val(v) => Node::Val(-v),
                v => Node::Neg(Box::new(v)),
            },
            Node::Add(lhs, rhs) => match (lhs.compute(), rhs.compute()) {
                (Node::None, _)|(_, Node::None) => Node::None,
                (Node::Val(v1), Node::Val(v2)) => Node::Val(v1 + v2),
                (Node::Val(v1), Node::Add(l, r)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Add(Box::new(Node::Val(v1+v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Add(Box::new(l), Box::new(Node::Val(v1+v2))),
                    (l, r) => Node::Add(
                        Box::new(Node::Val(v1)),
                        Box::new(Node::Add(Box::new(l), Box::new(r))),
                    ),
                }
                (Node::Add(l, r), Node::Val(v1)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Add(Box::new(Node::Val(v1+v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Add(Box::new(l), Box::new(Node::Val(v1+v2))),
                    (l, r) => Node::Add(
                        Box::new(Node::Add(Box::new(l), Box::new(r))),
                        Box::new(Node::Val(v1)),
                    ),
                }
                (Node::Val(v1), Node::Sub(l, r)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Sub(Box::new(Node::Val(v1+v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Add(Box::new(l), Box::new(Node::Val(v1-v2))),
                    (l, r) => Node::Add(
                        Box::new(Node::Val(v1)),
                        Box::new(Node::Sub(Box::new(l), Box::new(r))),
                    ),
                }
                (Node::Sub(l, r), Node::Val(v1)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Sub(Box::new(Node::Val(v1+v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Add(Box::new(l), Box::new(Node::Val(v1-v2))),
                    (l, r) => Node::Add(
                        Box::new(Node::Sub(Box::new(l), Box::new(r))),
                        Box::new(Node::Val(v1)),
                    ),
                }
                (lhs, rhs) => Node::Add(Box::new(lhs), Box::new(rhs)),
            }
            Node::Sub(lhs, rhs) => match (lhs.compute(), rhs.compute()) {
                (Node::None, _)|(_, Node::None) => Node::None,
                (Node::Val(v1), Node::Val(v2)) => Node::Val(v1 - v2),
                (Node::Val(v1), Node::Add(l, r)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Sub(Box::new(Node::Val(v1-v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Sub(Box::new(Node::Val(v1-v2)), Box::new(l)),
                    (l, r) => Node::Sub(
                        Box::new(Node::Val(v1)),
                        Box::new(Node::Add(Box::new(l), Box::new(r))),
                    ),
                }
                (Node::Add(l, r), Node::Val(v1)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Add(Box::new(Node::Val(v2-v1)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Add(Box::new(l), Box::new(Node::Val(v2-v1))),
                    (l, r) => Node::Sub(
                        Box::new(Node::Add(Box::new(l), Box::new(r))),
                        Box::new(Node::Val(v1)),
                    ),
                }
                (Node::Val(v1), Node::Sub(l, r)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Add(Box::new(Node::Val(v1-v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Sub(Box::new(Node::Val(v1+v2)), Box::new(l)),
                    (l, r) => Node::Sub(
                        Box::new(Node::Val(v1)),
                        Box::new(Node::Sub(Box::new(l), Box::new(r))),
                    ),
                }
                (Node::Sub(l, r), Node::Val(v1)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Sub(Box::new(Node::Val(v2-v1)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Sub(Box::new(l), Box::new(Node::Val(v1+v2))),
                    (l, r) => Node::Sub(
                        Box::new(Node::Sub(Box::new(l), Box::new(r))),
                        Box::new(Node::Val(v1)),
                    ),
                }
                (lhs, rhs) => Node::Sub(Box::new(lhs), Box::new(rhs)),
            }
            Node::Mul(lhs, rhs) => match (lhs.compute(), rhs.compute()) {
                (Node::None, _)|(_, Node::None) => Node::None,
                (Node::Val(v1), Node::Val(v2)) => Node::Val(v1 * v2),
                (Node::Val(v1), Node::Mul(l, r)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Mul(Box::new(Node::Val(v1*v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Mul(Box::new(l), Box::new(Node::Val(v1*v2))),
                    (l, r) => Node::Mul(
                        Box::new(Node::Val(v1)),
                        Box::new(Node::Mul(Box::new(l), Box::new(r))),
                    ),
                }
                (Node::Mul(l, r), Node::Val(v1)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Mul(Box::new(Node::Val(v1*v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Mul(Box::new(l), Box::new(Node::Val(v1*v2))),
                    (l, r) => Node::Mul(
                        Box::new(Node::Mul(Box::new(l), Box::new(r))),
                        Box::new(Node::Val(v1)),
                    ),
                }
                (Node::Val(v1), Node::Div(l, r)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Div(Box::new(Node::Val(v1*v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Mul(Box::new(l), Box::new(Node::Val(v1/v2))),
                    (l, r) => Node::Mul(
                        Box::new(Node::Val(v1)),
                        Box::new(Node::Div(Box::new(l), Box::new(r))),
                    ),
                }
                (Node::Div(l, r), Node::Val(v1)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Div(Box::new(Node::Val(v1*v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Mul(Box::new(l), Box::new(Node::Val(v1/v2))),
                    (l, r) => Node::Mul(
                        Box::new(Node::Div(Box::new(l), Box::new(r))),
                        Box::new(Node::Val(v1)),
                    ),
                }
                (lhs, rhs) => Node::Mul(Box::new(lhs), Box::new(rhs)),
            }
            Node::Div(lhs, rhs) => match (lhs.compute(), rhs.compute()) {
                (Node::None, _)|(_, Node::None) => Node::None,
                (Node::Val(v1), Node::Val(v2)) => Node::Val(v1 / v2),
                (Node::Val(v1), Node::Mul(l, r)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Div(Box::new(Node::Val(v1/v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Div(Box::new(Node::Val(v1/v2)), Box::new(l)),
                    (l, r) => Node::Div(
                        Box::new(Node::Val(v1)),
                        Box::new(Node::Mul(Box::new(l), Box::new(r))),
                    ),
                }
                (Node::Mul(l, r), Node::Val(v1)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Mul(Box::new(Node::Val(v2/v1)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Mul(Box::new(l), Box::new(Node::Val(v2/v1))),
                    (l, r) => Node::Div(
                        Box::new(Node::Mul(Box::new(l), Box::new(r))),
                        Box::new(Node::Val(v1)),
                    ),
                }
                (Node::Val(v1), Node::Div(l, r)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Mul(Box::new(Node::Val(v1/v2)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Div(Box::new(Node::Val(v1*v2)), Box::new(l)),
                    (l, r) => Node::Div(
                        Box::new(Node::Val(v1)),
                        Box::new(Node::Div(Box::new(l), Box::new(r))),
                    ),
                }
                (Node::Div(l, r), Node::Val(v1)) => match (*l, *r) {
                    (Node::Val(v2), r) => Node::Div(Box::new(Node::Val(v2/v1)), Box::new(r)),
                    (l, Node::Val(v2)) => Node::Mul(Box::new(l), Box::new(Node::Val(v1/v2))),
                    (l, r) => Node::Div(
                        Box::new(Node::Div(Box::new(l), Box::new(r))),
                        Box::new(Node::Val(v1)),
                    ),
                }
                (lhs, rhs) => Node::Div(Box::new(lhs), Box::new(rhs)),
            }
            Node::Pow(lhs, rhs) => match (lhs.compute(), rhs.compute()) {
                (Node::None, _)|(_, Node::None) => Node::None,
                (Node::Val(v1), Node::Val(v2)) => Node::Val(v1.powf(v2)),
                (Node::Val(v), _) if v == 0. => Node::Val(0.),
                (Node::Val(v), _) if v == 1. => Node::Val(1.),
                (lhs, Node::Val(v)) => match v {
                    v if v == 0. => Node::Val(1.),
                    v if v == 1. => lhs,
                    v if v == -1. => Node::Div(Box::new(Node::Val(1.)), Box::new(lhs)),
                    v => Node::Pow(Box::new(lhs), Box::new(Node::Val(v))),
                }
                (lhs, rhs) => Node::Pow(Box::new(lhs), Box::new(rhs)),
            }
            Node::Cos(x) => match x.compute() {
                Node::None => Node::None,
                Node::Val(v) => Node::Val(v.cos()),
                v => Node::Cos(Box::new(v)),
            }
            Node::Sin(x) => match x.compute() {
                Node::None => Node::None,
                Node::Val(v) => Node::Val(v.sin()),
                v => Node::Sin(Box::new(v)),
            }
            Node::Tan(x) => match x.compute() {
                Node::None => Node::None,
                Node::Val(v) => Node::Val(v.tan()),
                v => Node::Tan(Box::new(v)),
            }
            Node::Exp(x) => match x.compute() {
                Node::None => Node::None,
                Node::Val(v) => Node::Val(v.exp()),
                v => Node::Exp(Box::new(v)),
            }
            Node::Log(x) => match x.compute() {
                Node::None => Node::None,
                Node::Val(v) => Node::Val(v.ln()),
                v => Node::Log(Box::new(v)),
            }
        }
    }

    fn simplify(self) -> Node {
        (match self {
            Node::Neg(x) => match x.simplify() {
                Node::Neg(v) => *v,
                v => Node::Neg(Box::new(v)),
            }
            Node::Add(l, r) => match l.simplify() {
                Node::Val(v) if v == 0. => r.simplify(),
                Node::Neg(l) => match r.simplify() {
                    Node::Neg(r) => Node::Neg(Box::new(Node::Add(l, r))),
                    r => Node::Sub(Box::new(r), l),
                }
                l => match r.simplify() {
                    Node::Val(v) if v == 0. => l,
                    Node::Neg(r) => Node::Sub(Box::new(l), r),
                    r => Node::Add(Box::new(l), Box::new(r)),
                }
            }
            Node::Sub(l, r) => match l.simplify() {
                Node::Val(v) if v == 0. => Node::Neg(Box::new(r.simplify())),
                Node::Neg(l) => match r.simplify() {
                    Node::Neg(r) => Node::Add(l, r),
                    r => Node::Neg(Box::new(Node::Add(l, Box::new(r)))),
                }
                l => match r.simplify() {
                    Node::Val(v) if v == 0. => l,
                    Node::Neg(r) => Node::Add(Box::new(l), r),
                    r => Node::Sub(Box::new(l), Box::new(r)),
                }
            }
            Node::Mul(l, r) => match l.simplify() {
                Node::Val(n) if n == 0. => Node::Val(0.),
                Node::Val(n) if n == 1. => r.simplify(),
                Node::Neg(l) => match r.simplify() {
                    Node::Neg(r) => Node::Mul(l, r),
                    r => Node::Mul(Box::new(Node::Neg(l)), Box::new(r)),
                }
                l => match r.simplify() {
                    Node::Val(n) if n == 0. => Node::Val(0.),
                    Node::Val(n) if n == 1. => l,
                    r => Node::Mul(Box::new(l), Box::new(r)),
                }
            }
            Node::Div(l, r) => match l.simplify() {
                Node::Val(n) if n == 0. => Node::Val(0.),
                Node::Neg(l) => match r.simplify() {
                    Node::Neg(r) => Node::Div(l, r),
                    r => Node::Div(Box::new(Node::Neg(l)), Box::new(r)),
                }
                l => match r.simplify() {
                    Node::Val(n) if n == 1. => l,
                    r => Node::Div(Box::new(l), Box::new(r)),
                }
            }
            Node::Pow(l, r) => match l.simplify() {
                Node::Val(n) if n == 0. => Node::Val(0.),
                Node::Val(n) if n == 1. => Node::Val(1.),
                l => match r.simplify() {
                    Node::Val(n) if n == 0. => Node::Val(1.),
                    Node::Val(n) if n == 1. => l,
                    Node::Val(n) if n == -1. => Node::Div(Box::new(Node::Val(1.)), Box::new(l)),
                    r => Node::Pow(Box::new(l), Box::new(r)),
                }
            }
            Node::Cos(x) => Node::Cos(Box::new(x.simplify())),
            Node::Sin(x) => Node::Sin(Box::new(x.simplify())),
            Node::Tan(x) => Node::Tan(Box::new(x.simplify())),
            Node::Exp(x) => Node::Exp(Box::new(x.simplify())),
            Node::Log(x) => Node::Log(Box::new(x.simplify())),
            v => v,
        }).compute()
    }
}

impl Clone for Node {
    fn clone(&self) -> Self {
        match self {
            Node::None => Node::None,
            Node::Var => Node::Var,
            Node::Val(v) => Node::Val(*v),
            Node::Neg(v) => Node::Neg(v.clone()),
            Node::Add(l, r) => Node::Add(l.clone(), r.clone()),
            Node::Sub(l, r) => Node::Sub(l.clone(), r.clone()),
            Node::Mul(l, r) => Node::Mul(l.clone(), r.clone()),
            Node::Div(l, r) => Node::Div(l.clone(), r.clone()),
            Node::Pow(l, r) => Node::Pow(l.clone(), r.clone()),
            Node::Cos(x) => Node::Cos(x.clone()),
            Node::Sin(x) => Node::Sin(x.clone()),
            Node::Tan(x) => Node::Tan(x.clone()),
            Node::Exp(x) => Node::Exp(x.clone()),
            Node::Log(x) => Node::Log(x.clone()),
        }
    }
}
