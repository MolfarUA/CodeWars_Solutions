5265b0885fda8eac5900093b



#[derive(Debug,Clone)]
enum Ast {
    BinOp(String, Box<Ast>, Box<Ast>),
    UnOp(String, i32),
}

impl Ast {
    fn new_bin(op: &str, a: &Ast, b: &Ast) -> Ast {
        Ast::BinOp(op.to_string(), Box::new(a.clone()), Box::new(b.clone()))
    }

    fn is_imm(&self) -> bool {
        match self {
            Ast::UnOp(tag, _) => tag == "imm",
            _ => false,
        }
    }

    fn is_arg(&self) -> bool {
        match self {
            Ast::UnOp(tag, _) => tag == "arg",
            _ => false,
        }
    }

    fn is_unop(&self) -> bool {
        self.is_imm() || self.is_arg()
    }

    fn imm(&self) -> i32 {
        match self {
            Ast::UnOp(_, val) => *val,
            _ => unreachable!(),
        }
    }
}

struct Compiler {
}

impl Compiler {
    fn new() -> Compiler {
        Compiler { }
    }

    /// Tokenize program (a string) into a sequence of tokens (a
    /// vector of strings).
    fn tokenize<'a>(&self, program : &'a str) -> Vec<String> {
        let mut tokens : Vec<String> = vec![];
        
        let mut iter = program.chars().peekable();
        loop {
            match iter.peek() {
                Some(&c) => match c {
                    'a'...'z'|'A'...'Z' => {
                        let mut tmp = String::new();
                        while iter.peek().is_some() && iter.peek().unwrap().is_alphabetic() {
                            tmp.push(iter.next().unwrap());
                        }
                        tokens.push(tmp);
                    },
                    '0'...'9' => {
                        let mut tmp = String::new();
                        while iter.peek().is_some() && iter.peek().unwrap().is_numeric() {
                            tmp.push(iter.next().unwrap());
                        }
                        tokens.push(tmp);
                    },
                    ' ' => { iter.next(); },
                    _ => {
                        tokens.push(iter.next().unwrap().to_string());
                    },
                },
                None => break
            }
        }
        
        tokens
    }

    fn compile(&mut self, program : &str) -> Vec<String> {
        let ast = self.pass1(program);
        let ast = self.pass2(&ast);
        self.pass3(&ast)
    }

    /// Pass 1: Translate tokens into AST.
    ///
    /// The parsing algorithm used here is a simple precedence-based
    /// bottom-up parser. It runs in linear time.
    fn pass1(&mut self, program : &str) -> Ast {
        let tokens = self.tokenize(program);
        let mut iter = tokens.iter();
        let mut args = vec![];
        let mut op_stack: Vec<char> = Vec::new();
        let mut ast_stack: Vec<Ast> = Vec::new();

        fn reduce(op: char, ast_stack: &mut Vec<Ast>) {
            let b = ast_stack.pop().unwrap();
            let a = ast_stack.pop().unwrap();
            ast_stack.push(Ast::BinOp(format!("{}", op), Box::new(a), Box::new(b)));
        }

        loop {
            match iter.next() {
                Some(token) => match token.as_ref() {
                    "[" => {
                        // Parse [ variable* ].
                        loop {
                            let arg = iter.next().expect("arg");
                            if arg == "]" {
                                break;
                            } else {
                                args.push(arg);
                            }
                        }
                    }
                    "(" => {
                        op_stack.push('(');
                    }
                    "+" | "-" => {
                        while let Some(op) = op_stack.pop() {
                            if op != '(' {
                                reduce(op, &mut ast_stack);
                            } else {
                                op_stack.push('(');
                                break;
                            }
                        }
                        op_stack.push(token.chars().nth(0).unwrap());
                    }
                    "*" | "/" => {
                        while let Some(op) = op_stack.pop() {
                            if op == '*' || op == '/' {
                                reduce(op, &mut ast_stack);
                            } else {
                                op_stack.push(op);
                                break;
                            }
                        }
                        op_stack.push(token.chars().nth(0).unwrap());
                    }
                    ")" => {
                        while let Some(op) = op_stack.pop() {
                            if op == '(' {
                                break;
                            } else {
                                reduce(op, &mut ast_stack);
                            }
                        }
                    }
                    value => {
                        let ast;
                        if value.chars().nth(0).expect("what").is_numeric() {
                            ast = Ast::UnOp("imm".to_string(), value.parse::<i32>().unwrap());
                        } else {
                            ast = Ast::UnOp("arg".to_string(), args.iter().position(|&x| x==value).unwrap() as i32);
                        }
                        ast_stack.push(ast);
                    }
                }
                None => {
                    break;
                }
            }
        }
        while let Some(op) = op_stack.pop() {
            reduce(op, &mut ast_stack);
        }
        ast_stack.pop().unwrap()
    }

    /// Pass 2: Constant folding.
    ///
    /// * Comm: 1+x = x+1
    /// * Assoc: (...+1)+1 = (...)+(1+1)
    /// * Assoc: (x+1)+x = (x+x)+1
    ///
    /// Note: / and * are tricky. 3*x/4 != 3/4*x = 0
    /// Note: Direction matters.
    fn pass2(&mut self, ast : &Ast) -> Ast {

        #[inline(always)]
        fn plus_like(op: &str) -> bool {
            if op == "+" || op == "-" { true } else { false }
        }

        /// Evaluate (a OP b).
        #[inline(always)]
        fn eval(op: &str, a: i32, b: i32) -> i32 {
            match op {
                "+" => a + b,
                "-" => a - b,
                "*" => a * b,
                "/" => a / b,
                _ => unreachable!(),
            }
        }

        /// Try fold constants.
        #[inline(always)]
        fn opt_fold(ast: &Ast) -> Option<Ast> {
            match ast {
                Ast::BinOp(op,a,b) if a.is_imm() && b.is_imm() => {
                    Some(Ast::UnOp("imm".to_string(), eval(op, a.imm(), b.imm())))
                }
                _ => None
            }
        }

        /// Try apply comm.
        #[inline(always)]
        fn opt_comm(ast: &Ast) -> Option<Ast> {
            match ast {
                Ast::BinOp(op,a,b) if b.is_arg() && a.is_imm() && (op=="+" || op=="*") => {
                    Some(Ast::BinOp(op.clone(), b.clone(), a.clone()))
                }
                Ast::BinOp(op,a,b) if b.is_arg() && a.is_imm() && (op=="-") => {
                    // a-b = (-b)+a
                    Some(Ast::new_bin("+", &Ast::new_bin("*", &b, &Ast::UnOp("imm".to_string(), -1)), &*a))
                }
                _ => None
            }
        }

        /// Try apply assoc. (?+1)+1 = ?+(1+1)
        #[inline(always)]
        fn opt_assoc(ast: &Ast) -> Option<Ast> {
            match ast {
                Ast::BinOp(op1, a1, b1) => {
                    match &**a1  {
                        Ast::BinOp(op2,a2,b2) if b1.is_imm() && b2.is_imm() &&
                            ((plus_like(op1) && plus_like(op2)) || (op1=="*" && op2=="*"))
                        => {
                            Some(Ast::BinOp(op2.clone(), a2.clone(), Box::new(Ast::BinOp(op1.clone(), b2.clone(), b1.clone()))))
                        }
                        _ => None,
                    }
                }
                _ => None
            }
        }

        /// Try apply assoc + comm to put x down. (1+x)+x = (x+x)+1.
        #[inline(always)]
        fn opt_assoc_comm(ast: &Ast) -> Option<Ast> {
            match ast {
                Ast::BinOp(op1, a1, b1) => {
                    match &**a1 {
                        Ast::BinOp(op2, a2, b2) if b1.is_arg() && b2.is_imm() &&
                            ((plus_like(op1) && plus_like(op2)) || (op1 == "*" && op2 == "*"))
                        => {
                            Some(Ast::BinOp(op2.clone(), Box::new(Ast::new_bin(op1, a2, b1)), b2.clone()))
                        }
                        _ => None,
                    }
                }
                _ => None
            }
        }

        /// Move x to the left side.
        #[inline(always)]
        fn opt_move(ast: &Ast) -> Option<Ast> {
            opt_assoc(ast).or(opt_assoc_comm(ast))
        }

        /// 0+x=0
        /// 1*x=1
        /// 0*x=0
        /// (-a)+b=b-a
        #[inline(always)]
        fn opt_algebraic(ast: &Ast) -> Option<Ast> {
            match ast {
                Ast::BinOp(op, a, b) if op == "+" && a.is_imm() && a.imm() == 0 => Some(*b.clone()),
                Ast::BinOp(op, a, b) if op == "+" && b.is_imm() && b.imm() == 0 => Some(*a.clone()),
                Ast::BinOp(op, a, b) if op == "*" && a.is_imm() && a.imm() == 1 => Some(*b.clone()),
                Ast::BinOp(op, a, b) if op == "*" && b.is_imm() && b.imm() == 1 => Some(*a.clone()),
                Ast::BinOp(op, a, _) if op == "*" && a.is_imm() && a.imm() == 0 => Some(*a.clone()),
                Ast::BinOp(op, _, b) if op == "*" && b.is_imm() && b.imm() == 0 => Some(*b.clone()),
                // This shouldn't be put here, because it undoes a-b=(-b)+a in `opt_comm'.
                //
                // Ast::BinOp(op1, a1, b1) if op1 == "+" => {
                //     // a2*(-1) + b1 = b1 - a2
                //     match &**a1 {
                //         Ast::BinOp(op2, a2, b2) if op2 == "*" && b2.is_imm() && b2.imm() == -1 => {
                //             Some(Ast::new_bin("-", &b1, &a2))
                //         }
                //         _ => None,
                //     }
                // }
                _ => None,
            }
        }

        /// Top-level optimizer.
        fn optimize(ast: &Ast) -> Ast {
            match ast {
                Ast::UnOp(_,_) => ast.clone(),
                Ast::BinOp(op,a,b) => {
                    let a = optimize(&*a);
                    let b = optimize(&*b);
                    let this = Ast::new_bin(op,&a,&b);
                    let this = opt_algebraic(&this).unwrap_or(this);
                    let this = opt_comm(&this).unwrap_or(this);
                    let this = match opt_move(&this) {
                        Some(ast) => match ast {
                            Ast::UnOp(_,_) => unreachable!(),
                            Ast::BinOp(op,a,b) => {
                                Ast::new_bin(&op, &*a, &opt_fold(&*b).unwrap_or(*b))
                            }
                        }
                        None => this
                    };
                    let this = opt_fold(&this).unwrap_or(this);
                    opt_algebraic(&this).unwrap_or(this)
                }
            }
        }

        fn normalize(ast: &Ast) -> Ast {
            let ast = match ast {
                Ast::UnOp(_,_) => return ast.clone(),
                Ast::BinOp(op,a,b) => {
                    Ast::new_bin(op, &normalize(a), &normalize(b))
                }
            };
            match &ast {
                Ast::BinOp(op,a,b) if a.is_arg() && b.is_imm() => {
                    Ast::new_bin(op,b,a)
                }
                Ast::BinOp(op1, a1, b1) if op1 == "+" => {
                    // a2*(-1) + b1 = b1 - a2
                    match &**a1 {
                        Ast::BinOp(op2, a2, b2) if op2 == "*" && b2.is_imm() && b2.imm() == -1 => {
                            Ast::new_bin("-", &b1, &a2)
                        }
                        _ => ast.clone()
                    }
                }
                _ => ast.clone()
            }
        }

        normalize(&optimize(ast))
    }

    /// Pass 3: Code generation.
    ///
    /// The stack is used, if and only if the second computation uses more than one register.
    /// UnOp meets this condition.
    ///
    /// This is a rather straightforward translation, and certainly
    /// more optimizations can be employed.
    ///
    /// It can't optimize, e.g., a+a+a (=3a), a*a*a*a (ar 0, sw, ar 0, mu, mu, mu), etc.
    fn pass3(&mut self, ast : &Ast) -> Vec<String> {
        fn opgen(op: &str) -> String {
            match op {
                "+" => "AD".to_string(),
                "-" => "SU".to_string(),
                "*" => "MU".to_string(),
                "/" => "DI".to_string(),
                _ => unreachable!(),
            }
        }
        let mut insts = vec![];
        match ast {
            Ast::UnOp(op, i) if op == "arg" => {
                insts.push(format!("AR {}", i));
            }
            Ast::UnOp(op, x) if op == "imm" => {
                insts.push(format!("IM {}", x));
            }
            Ast::BinOp(op, a, b) if a.is_unop() => {
                let proga = self.pass3(&*a);
                let progb = self.pass3(&*b);
                insts.extend(progb);          // R0 <- B.
                insts.push("SW".to_string()); // R1 <- B.
                insts.extend(proga);          // R0 <- A.
                insts.push(opgen(&op));
            }
            Ast::BinOp(op, a, b) if b.is_unop() => {
                let proga = self.pass3(&*a);
                let progb = self.pass3(&*b);
                insts.extend(proga);          // R0 <- A.
                insts.push("SW".to_string()); // R1 <- A.
                insts.extend(progb);          // R0 <- B.
                insts.push("SW".to_string()); // R0, R1 <- A, B
                insts.push(opgen(&op));
            }
            Ast::BinOp(op, a, b) => {
                let proga = self.pass3(&*a);
                let progb = self.pass3(&*b);
                insts.extend(proga);          // R0 <- A.
                insts.push("PU".to_string()); // PUSH[R0].
                insts.extend(progb);          // R0 <- B.
                insts.push("SW".to_string()); // R1 <- B.
                insts.push("PO".to_string()); // R0 <- A.
                insts.push(opgen(&op));
            }
            _ => unreachable!(),
        }
        insts
    }
}
      
__________________________________________________________________________________
use std::collections::HashMap;

#[derive(Debug)]
enum Ast {
    UnOp(String, i32),
    BinOp(String, Box<Ast>, Box<Ast>),
}

struct Compiler {
    // your code
}

impl Compiler {
    fn new() -> Compiler {
        Compiler {}
    }

    fn tokenize(&self, program: &str) -> Vec<String> {
        let mut tokens: Vec<String> = vec![];
        let mut iter = program.chars().peekable();
        while let Some(&c) = iter.peek() {
            match c {
                'a'..='z' | 'A'..='Z' => {
                    let mut tmp = String::new();
                    while iter.peek().is_some() && iter.peek().unwrap().is_alphabetic() {
                        tmp.push(iter.next().unwrap());
                    }
                    tokens.push(tmp);
                }
                '0'..='9' => {
                    let mut tmp = String::new();
                    while iter.peek().is_some() && iter.peek().unwrap().is_numeric() {
                        tmp.push(iter.next().unwrap());
                    }
                    tokens.push(tmp);
                }
                ' ' => { iter.next(); }
                _ => {
                    tokens.push(iter.next().unwrap().to_string());
                }
            }
        }
        tokens
    }

    fn compile(&mut self, program: &str) -> Vec<String> {
        let ast = self.pass1(program);
        let ast = self.pass2(&ast);
        let ret = self.pass3(&ast);
        ret
    }

    fn pass1(&mut self, program: &str) -> Ast {
        let tokens = self.tokenize(program);
        let mut iter = tokens.into_iter();

        let mut val_stack = Vec::new();
        let mut op_stack = Vec::new();
        let mut arg_map = HashMap::new();

        fn consume(val_stack: &mut Vec<Ast>, op: String) {
            let t2 = val_stack.pop().unwrap();
            let t1 = val_stack.pop().unwrap();
            val_stack.push(Ast::BinOp(
                op,
                Box::new(t1),
                Box::new(t2),
            ))
        }

        while let Some(s) = iter.next() {
            match s.as_str() {
                "[" => continue,
                "]" => break,
                _ => { arg_map.insert(s, arg_map.len() as i32); }
            }
        }
        while let Some(s) = iter.next() {
            match s.as_str() {
                "(" => op_stack.push(s),
                ")" => {
                    while let Some(op) = op_stack.pop() {
                        match op.as_str() {
                            "(" => break,
                            _ => consume(&mut val_stack, op),
                        }
                    }
                }
                "+" | "-" => {
                    while let Some(op) = op_stack.last() {
                        match op.as_str() {
                            "(" => break,
                            _ => consume(&mut val_stack, op_stack.pop().unwrap()),
                        }
                    }
                    op_stack.push(s);
                }
                "*" | "/" => {
                    while let Some(op) = op_stack.last() {
                        match op.as_str() {
                            "*" | "/" => consume(&mut val_stack, op_stack.pop().unwrap()),
                            _ => break,
                        }
                    }
                    op_stack.push(s);
                }
                token => {
                    val_stack.push(match arg_map.get(token) {
                        Some(&index) => Ast::UnOp("arg".to_string(), index),
                        None => Ast::UnOp("imm".to_string(), s.parse().unwrap()),
                    });
                }
            }
        }
        while let Some(op) = op_stack.pop() {
            consume(&mut val_stack, op);
        }
        val_stack.pop().unwrap()
    }

    fn pass2(&mut self, ast: &Ast) -> Ast {
        match ast {
            Ast::UnOp(t, v) => Ast::UnOp(t.clone(), *v),
            Ast::BinOp(op, c1, c2) => {
                let (c1, c2) = (self.pass2(c1), self.pass2(c2));
                match (&c1, &c2) {
                    (Ast::UnOp(t1, v1), Ast::UnOp(t2, v2))
                    if t1.as_str() == "imm" && t2.as_str() == "imm" =>
                        Ast::UnOp("imm".to_string(), match op.as_str() {
                            "+" => v1 + v2,
                            "-" => v1 - v2,
                            "*" => v1 * v2,
                            "/" => v1 / v2,
                            _ => panic!(),
                        }),
                    _ => Ast::BinOp(op.clone(), Box::new(c1), Box::new(c2))
                }
            }
        }
    }

    fn pass3(&mut self, ast: &Ast) -> Vec<String> {
        match ast {
            Ast::UnOp(t, v) => match t.as_str() {
                "arg" => vec![format!("AR {}", v)],
                "imm" => vec![format!("IM {}", v)],
                _ => panic!(),
            },
            Ast::BinOp(op, l_child, r_child) => {
                let mut ret = self.pass3(l_child);
                ret.push("PU".to_string());
                ret.extend(self.pass3(r_child));
                ret.push("SW".to_string());
                ret.push("PO".to_string());
                ret.push(match op.as_str() {
                    "+" => "AD",
                    "-" => "SU",
                    "*" => "MU",
                    "/" => "DI",
                    _ => panic!(),
                }.to_string());
                ret
            }
        }
    }
}
      
____________________________________________________
use std::iter::Peekable;

#[derive(Debug, Eq)]
enum Ast {
    BinOp(String, Box<Ast>, Box<Ast>),
    UnOp(String, i32),
}

impl Ast {
    fn new_bin(op: String, lhs: Ast, rhs: Ast) -> Ast {
        Ast::BinOp(op, Box::new(lhs), Box::new(rhs))
    }

    fn new_arg(v: i32) -> Ast {
        Ast::UnOp("arg".to_string(), v)
    }

    fn new_imm(v: i32) -> Ast {
        Ast::UnOp("imm".to_string(), v)
    }

    fn mk_simple(op: String, lhs: Box<Ast>, rhs: Box<Ast>) -> Ast {
        Ast::new_bin(op, lhs.simplify(), rhs.simplify())
    }

    fn choose_from_val(op: String, lhs: Box<Ast>, rhs: Box<Ast>, val: i32) -> Ast {
        if lhs.is_val(val) {
            rhs.simplify()
        } else if rhs.is_val(val) {
            lhs.simplify()
        } else {
            Ast::mk_simple(op, lhs, rhs)
        }
    }

    fn is_val(&self, val: i32) -> bool {
        match self {
            Ast::UnOp(op, v) => op.eq("imm") && v.eq(&val),
            _ => false,
        }
    }

    /* if (x * 0) or (0 * x) or (0 / x) for self or children */
    fn zeroable(&self) -> bool {
        match self {
            Ast::UnOp(op, v) => op.eq("imm") && v.eq(&0),
            Ast::BinOp(op, l, r) => match op.as_str() {
                "*" => l.is_val(0) || r.is_val(0) || l.zeroable() || r.zeroable(),
                "/" => l.is_val(0) || l.zeroable(),
                _ => false,
            }
        }
    }

    fn produce_code(&self, res: &mut Vec<String>) {
        match self {
            Ast::UnOp(op, v) if op == "imm" => { res.push(format!("IM {}", v)); }
            Ast::UnOp(op, v) if op == "arg" => { res.push(format!("AR {}", v)); }
            Ast::BinOp(op, lhs, rhs) => {
                lhs.produce_code(res);
                res.push("PU".to_string());
                rhs.produce_code(res);
                res.push("SW".to_string());
                res.push("PO".to_string());
                match op.as_str() {
                    "+" => { res.push("AD".to_string()); }
                    "-" => { res.push("SU".to_string()); }
                    "*" => { res.push("MU".to_string()); }
                    "/" => { res.push("DI".to_string()); }
                    _ => {}
                }
            }
            _ => {}
        }
    }

    /* Simplify x * 0, 0 * x, 0 / x */
    fn simplify_level1(self) -> Ast {
        match self {
            a @ Ast::UnOp(_, _) => a,
            Ast::BinOp(op, lhs, rhs) => match op.as_str() {
                "+" => if lhs.zeroable() {
                    rhs.simplify()
                } else if rhs.zeroable() {
                    lhs.simplify()
                } else {
                    Ast::mk_simple(op, lhs, rhs)
                }
                "-" => if rhs.zeroable() { lhs.simplify() } else { Ast::mk_simple(op, lhs, rhs) }
                _ => Ast::mk_simple(op, lhs, rhs),
            }
        }
    }

    /* Simplify 0 - x */
    fn simplify_level2(self) -> Ast {
        match self {
            a @ Ast::UnOp(_, _) => a,
            Ast::BinOp(op, lhs, rhs) => match op.as_str() {
                "+" => {
                    if let Ast::BinOp(o, l, _) = lhs.as_ref() {
                        if o.eq("-") && l.is_val(0) {
                            if let Ast::BinOp(_, _, r) = *lhs {
                                return Ast::mk_simple("-".to_string(), rhs, r);
                            }
                        }
                    }

                    if let Ast::BinOp(o, l, _) = rhs.as_ref() {
                        if o.eq("-") && l.is_val(0) {
                            if let Ast::BinOp(_, _, r) = *rhs {
                                return Ast::mk_simple("-".to_string(), lhs, r);
                            }
                        }
                    }

                    Ast::mk_simple(op, lhs, rhs)
                }
                "-" => {
                    if let Ast::BinOp(o, l, _) = rhs.as_ref() {
                        if o.eq("-") && l.is_val(0) {
                            if let Ast::BinOp(_, _, r) = *rhs {
                                return Ast::mk_simple("+".to_string(), lhs, r);
                            }
                        }
                    }

                    Ast::mk_simple(op, lhs, rhs)
                },
                _ => Ast::mk_simple(op, lhs, rhs),
            }
        }
    }

    /* Simplify x + 0, 0 + x, x - 0, x * 1, 1 * x, x / 1 */
    fn simplify_level3(self) -> Ast {
        match self {
            a @ Ast::UnOp(_, _) => a,
            Ast::BinOp(op, lhs, rhs) => match op.as_str() {
                "+" => Ast::choose_from_val(op, lhs, rhs, 0),
                "*" => Ast::choose_from_val(op, lhs, rhs, 1),
                "/" => if (&rhs).is_val(1) { lhs.simplify() } else { Ast::mk_simple(op, lhs, rhs) }
                "-" => if (&rhs).is_val(0) { lhs.simplify() } else { Ast::mk_simple(op, lhs, rhs) }
                _ => Ast::mk_simple(op, lhs, rhs)
            }
        }
    }

    /* Simplify x + 0, 0 + x, x - 0, 0 - x, x * 1, 1 * x, x * 0, 0 * x, 0 / x, x / 1 */
    fn simplify(self) -> Ast {
        self.simplify_level1().simplify_level2().simplify_level3()
    }
}

impl Clone for Ast {
    fn clone(&self) -> Self {
        match self {
            Ast::BinOp(s, lhs, rhs) => Ast::BinOp(s.clone(), lhs.clone(), rhs.clone()),
            Ast::UnOp(s, v) => Ast::UnOp(s.clone(), *v),
        }
    }
}

impl PartialEq for Ast {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (Ast::UnOp(ls, lv), Ast::UnOp(rs, rv)) => (ls == rs) && (lv == rv),
            (Ast::BinOp(lop, llhs, lrhs), Ast::BinOp(rop, rlhs, rrhs)) => match (lop.as_str(), rop.as_str()) {
                ("+","+")|("*","*") => ((llhs == rlhs) && (lrhs == rrhs)) || ((llhs == rrhs) && (lrhs == rlhs)),
                ("-","-")|("/","/") => (llhs == rlhs) && (lrhs == rrhs),
                _ => false,
            }
            _ => false,
        }
    }
}

pub struct Compiler {
    // your code
}

impl Compiler {
    pub fn new() -> Compiler {
        Compiler { }
    }

    fn tokenize(&self, program : &str) -> Vec<String> {
        let mut tokens : Vec<String> = vec![];

        let mut iter = program.chars().peekable();
        loop {
            match iter.peek() {
                Some(&c) => match c {
                    'a'..='z'|'A'..='Z' => {
                        let mut tmp = String::new();
                        while iter.peek().is_some() && iter.peek().unwrap().is_alphabetic() {
                            tmp.push(iter.next().unwrap());
                        }
                        tokens.push(tmp);
                    },
                    '0'..='9' => {
                        let mut tmp = String::new();
                        while iter.peek().is_some() && iter.peek().unwrap().is_numeric() {
                            tmp.push(iter.next().unwrap());
                        }
                        tokens.push(tmp);
                    },
                    ' ' => { iter.next(); },
                    _ => {
                        tokens.push(iter.next().unwrap().to_string());
                    },
                },
                None => break
            }
        }

        tokens
    }

    pub fn compile(&mut self, program : &str) -> Vec<String> {
        let ast = self.pass1(program);
        let ast = self.pass2(&ast);
        self.pass3(&ast)
    }

    fn pass1(&mut self, program : &str) -> Ast {
        let close = "]".to_string();
        let tokens = self.tokenize(program);
        let mut iter = tokens.into_iter().peekable();
        let mut args = Vec::new();

        iter.next();
        while iter.peek().unwrap_or(&close) != "]" {
            args.push(iter.next().unwrap().clone());
        }

        iter.next();

        fn expr<I: Iterator<Item = String>>(it: &mut Peekable<I>, args: &Vec<String>) -> Ast {
            let default = "".to_string();
            let mut res = term(it, args);

            while "+-".contains(it.peek().unwrap_or(&default)) {
                let op = match it.next() {
                    None => { break; }
                    Some(v) => v
                };

                res = Ast::new_bin(op.clone(), res, term(it, args));
            }

            res
        }

        fn term<I: Iterator<Item = String>>(it: &mut Peekable<I>, args: &Vec<String>) -> Ast {
            let default = "".to_string();
            let mut res = factor(it, args);

            while "*/".contains(it.peek().unwrap_or(&default)) {
                let op = match it.next() {
                    None => { break; }
                    Some(v) => v
                };

                res = Ast::new_bin(op.clone(), res, factor(it, args));
            }

            res
        }

        fn factor<I: Iterator<Item = String>>(it: &mut Peekable<I>, args: &Vec<String>) -> Ast {
            let tok = it.next().unwrap();

            if tok == "(" {
                let res = expr(it, args);

                it.next();

                res
            } else {
                if tok.chars().next().unwrap().is_digit(10) {
                    Ast::new_imm(tok.parse().unwrap())
                } else {
                    Ast::new_arg(args.iter().position(|r| r == &tok).unwrap() as i32)
                }
            }
        }

        expr(&mut iter, &args)
    }

    fn pass2(&mut self, ast: &Ast) -> Ast {
        Term::from_ast(ast).to_ast().simplify()
    }

    fn pass3(&mut self, ast : &Ast) -> Vec<String> {
        let mut res = Vec::new();

        ast.produce_code(&mut res);
        res
    }
}

enum Term { Arg(i32), Val(i32, i32), Line(Box<Line>) }
impl Term {
    fn is_val(&self) -> bool {
        match self {
            Term::Val(_, _) => true,
            _ => false,
        }
    }

    fn from_ast(ast: &Ast) -> Term {
        if let Ast::UnOp(op, v) = ast {
            if op == "arg" { Term::Arg(*v) } else { Term::Val(*v, 1) }
        } else {
            Term::Line(Box::new(Line::from_ast(ast)))
        }
    }

    fn to_ast(&self) -> Ast {
        match self {
            &Term::Arg(v) => Ast::new_arg(v),
            &Term::Val(num, den) => if den == 1 {
                Ast::new_imm(num)
            } else {
                Ast::new_bin("/".to_string(), Ast::new_imm(num), Ast::new_imm(den))
            },
            Term::Line(l) => l.to_ast(),
        }
    }

    fn reduce(self) -> Term {
        match self {
            Term::Val(mut num, mut den) if den != 1 => {
                if den < 0 { num = -num; den = -den; }

                let gcd = gcd(num, den);

                if gcd == 1 {
                    Term::Val(num, den)
                } else {
                    Term::Val(num / gcd, den / gcd)
                }
            }
            r @ _ => r,
        }
    }

    fn apply_op(&self, op: &Operation, term: &Term) -> Option<Term> {
        match self {
            Term::Val(lnum, lden) => match term {
                Term::Val(rnum, rden) => match op {
                    Operation::Add => Some(Term::Val((lnum * rden) + (rnum * lden), lden * rden).reduce()),
                    Operation::Sub => Some(Term::Val((lnum * rden) - (rnum * lden), lden * rden).reduce()),
                    Operation::Mul => Some(Term::Val(lnum * rnum, lden * rden).reduce()),
                    Operation::Div => Some(Term::Val(lnum * rden, lden * rnum).reduce()),
                },
                _ => None,
            }
            _ => None,
        }
    }

    fn apply_part(&self, part: &Part) -> Option<Term> {
        self.apply_op(&part.op, &part.term)
    }
}

#[derive(Clone, Copy)]
enum Operation { Add, Sub, Mul, Div }
impl Operation {
    fn from(op: &String) -> Operation {
        match op.as_str() {
            "-" => Operation::Sub,
            "*" => Operation::Mul,
            "/" => Operation::Div,
            _ => Operation::Add,
        }
    }

    fn is_same(&self, op: &Operation) -> bool {
        match self {
            Operation::Add|Operation::Sub => match op {  Operation::Add|Operation::Sub => true, _ => false },
            Operation::Mul|Operation::Div => match op {  Operation::Mul|Operation::Div => true, _ => false },
        }
    }
}

struct Part {
    op: Operation,
    term: Term,
}

impl Part {
    fn new(op: Operation, term: Term) -> Part { Part { op, term } }
    fn is_val(&self) -> bool { self.term.is_val() }
    fn to_ast(&self, lhs: Ast) -> Ast {
        let rhs = self.term.to_ast();

        match self.op {
            Operation::Add => Ast::new_bin("+".to_string(), lhs, rhs),
            Operation::Sub => Ast::new_bin("-".to_string(), lhs, rhs),
            Operation::Mul => Ast::new_bin("*".to_string(), lhs, rhs),
            Operation::Div => Ast::new_bin("/".to_string(), lhs, rhs),
        }
    }

    fn apply_op(&mut self, part: &Part) {
        match (self.op, part.op) {
            (Operation::Add, _)|(Operation::Mul, _) => {
                if let Some(term) = self.term.apply_op(&(&part).op, &part.term) {
                    self.term = term;
                }
            }
            (Operation::Sub, Operation::Add) => {
                if let Some(term) = part.term.apply_op(&Operation::Sub, &self.term) {
                    self.op = Operation::Add;
                    self.term = term;
                }
            }
            (Operation::Sub, _) => {
                if let Some(term) = self.term.apply_op(&Operation::Add, &part.term) {
                    self.term = term;
                }
            }
            (Operation::Div, Operation::Mul) => {
                if let Some(term) = part.term.apply_op(&Operation::Div, &self.term) {
                    self.op = Operation::Mul;
                    self.term = term;
                }
            }
            (Operation::Div, _) => {
                if let Some(term) = self.term.apply_op(&Operation::Mul, &part.term) {
                    self.term = term;
                }
            }
        }
    }
}

#[derive(Clone, Copy)]
enum LinePosition { None, Head, Tail(usize) }

struct Line { pos: LinePosition, head: Term, tail: Vec<Part> }
impl Line {
    fn new(head: Term) -> Line {
        Line {
            pos: if (&head).is_val() { LinePosition::Head } else { LinePosition::None },
            head,
            tail: Vec::new()
        }
    }

    fn from_ast(ast: &Ast) -> Line {
        if let Ast::BinOp(op, lhs, rhs) = ast {
            let part = Part::new(Operation::from(op), Term::from_ast(rhs));
            let head = Term::from_ast(lhs);

            if let Term::Line(v) = head { v.operate(part) } else { Line::new(head).operate(part) }
        } else {
            Line::new(Term::from_ast(ast))
        }
    }

    fn to_ast(&self) -> Ast {
        self.tail.iter().fold(self.head.to_ast(), |r, t| t.to_ast(r))
    }

    fn get_operation(&self) -> Option<&Operation> {
        self.tail.first().map(|p| &p.op)
    }

    fn fetch_val_part_pos(&mut self) -> LinePosition {
        match self.pos {
            v @ LinePosition::Head|v @ LinePosition::Tail(_) => v,
            LinePosition::None => match self.tail.iter().position(|p| p.is_val()) {
                None => LinePosition::None,
                Some(pos) => { self.pos = LinePosition::Tail(pos); self.pos }
            }
        }
    }

    fn add_operation_part(mut self, part: Part) -> Line {
        let parts = &mut (&mut self).tail;

        match parts.first() {
            None => {
                parts.push(part);

                self
            },
            Some(first) => {
                if first.op.is_same(&(&part).op) {
                    parts.push(part);

                    self
                } else {
                    Line { pos: LinePosition::None, head: Term::Line(Box::new(self)), tail: vec![part] }
                }
            }
        }
    }

    fn append(mut self, part: Part) -> Line {
        if (&part).is_val() {
            if let LinePosition::Head = self.pos {
                if let Some(res) = self.head.apply_part(&part) {
                    self.head = res;
                }

                self
            } else {
                if let Some(first) = self.tail.first() {
                    if first.op.is_same(&(&part).op) {
                        if let LinePosition::Tail(pos) = self.fetch_val_part_pos() {
                            self.tail.get_mut(pos).unwrap().apply_op(&part);
                        } else {
                            let parts = &mut self.tail;

                            self.pos = LinePosition::Tail(parts.len());
                            parts.push(part);
                        }

                        self
                    } else {
                        Line { pos: LinePosition::Tail(0), head: Term::Line(Box::new(self)), tail: vec![part] }
                    }
                } else {
                    self.pos = LinePosition::Tail(0);
                    self.tail.push(part);

                    self
                }
            }
        } else {
            self.add_operation_part(part)
        }
    }

    fn operate(self, part: Part) -> Line {
        if let Term::Line(line) = part.term {
            if let Some(op) = line.get_operation() {
                if op.is_same(&part.op) {
                    let res = self.append(Part::new(part.op, line.head));

                    line.tail.into_iter().fold(res, |r, p| r.append(p))
                } else {
                    self.append(Part::new(part.op, Term::Line(line)))
                }
            } else {
                self.append(Part::new(part.op, line.head))
            }
        } else {
            self.append(part)
        }
    }
}

fn gcd(mut x: i32, mut y: i32) -> i32 {
    while y != 0 {
        let t = x;
        x = y;
        y = t % y;
    }
    x
}
      
________________________________________
#[derive(Debug, Clone)]
enum Ast {
    BinOp(String, Box<Ast>, Box<Ast>),
    UnOp(String, i32),
}

struct Compiler {
    arguments: Vec<String>,
}
macro_rules! must_have {
    ($ch:expr, $i:ident, $blk:block) => {
        if $ch == $i.next().unwrap() {
            $blk
        } else {
            panic!();
        }
    };
}

impl Compiler {
    fn new() -> Compiler {
        Compiler {
            arguments: Vec::new(),
        }
    }

    fn tokenize<'a>(&self, program: &'a str) -> Vec<String> {
        let mut tokens: Vec<String> = vec![];

        let mut iter = program.chars().peekable();
        loop {
            match iter.peek() {
                Some(&c) => match c {
                    'a'...'z' | 'A'...'Z' => {
                        let mut tmp = String::new();
                        while iter.peek().is_some() && iter.peek().unwrap().is_alphabetic() {
                            tmp.push(iter.next().unwrap());
                        }
                        tokens.push(tmp);
                    }
                    '0'...'9' => {
                        let mut tmp = String::new();
                        while iter.peek().is_some() && iter.peek().unwrap().is_numeric() {
                            tmp.push(iter.next().unwrap());
                        }
                        tokens.push(tmp);
                    }
                    ' ' => {
                        iter.next();
                    }
                    _ => {
                        tokens.push(iter.next().unwrap().to_string());
                    }
                },
                None => break,
            }
        }

        tokens
    }

    fn compile(&mut self, program: &str) -> Vec<String> {
        let ast = self.pass1(program);
        let ast = self.pass2(&ast);
        self.pass3(&ast)
    }

    fn pass1(&mut self, program: &str) -> Ast {
        let tokens = self.tokenize(program);
        let mut iter = tokens.into_iter().peekable();

        self.function(&mut iter)
    }

    fn function<T>(&mut self, iter: &mut std::iter::Peekable<T>) -> Ast
    where
        T: Iterator<Item = String>,
    {
        must_have!("[", iter, {
            self.arg_lists(iter);
            must_have!("]", iter, { self.expression(iter) })
        })
    }

    fn arg_lists<T>(&mut self, iter: &mut std::iter::Peekable<T>)
    where
        T: Iterator<Item = String>,
    {
        while iter.peek().is_some() && iter.peek().unwrap() != "]" {
            self.arguments.push(iter.next().unwrap());
        }
    }

    fn expression<T>(&mut self, iter: &mut std::iter::Peekable<T>) -> Ast
    where
        T: Iterator<Item = String>,
    {
        let mut result = self.term(iter);
        while iter.peek().is_some() && (iter.peek().unwrap() == "+" || iter.peek().unwrap() == "-")
        {
            let op = iter.next().unwrap();
            result = Ast::BinOp(op, Box::new(result), Box::new(self.term(iter)));
        }
        result
    }
    fn term<T>(&mut self, iter: &mut std::iter::Peekable<T>) -> Ast
    where
        T: Iterator<Item = String>,
    {
        let mut result = self.factor(iter);
        while iter.peek().is_some() && (iter.peek().unwrap() == "*" || iter.peek().unwrap() == "/")
        {
            let op = iter.next().unwrap();
            result = Ast::BinOp(op, Box::new(result), Box::new(self.factor(iter)));
        }
        result
    }

    fn factor<T>(&mut self, iter: &mut std::iter::Peekable<T>) -> Ast
    where
        T: Iterator<Item = String>,
    {
        if Compiler::is_variable(iter.peek().unwrap()) {
            let var = iter.next().unwrap();
            Ast::UnOp(
                String::from("arg"),
                self.arguments
                    .iter()
                    .position(|s| s == &var)
                    .expect("No such argument") as i32,
            )
        } else if Compiler::is_number(iter.peek().unwrap()) {
            let imm = iter.next().unwrap();
            Ast::UnOp(
                String::from("imm"),
                imm.parse::<i32>().expect("Invalid number"),
            )
        } else {
            iter.next(); // "("
            let ast = self.expression(iter);
            iter.next(); // ")"
            ast
        }
    }

    fn is_variable(s: &String) -> bool {
        s.as_bytes()
            .iter()
            .map(|n| char::from(*n))
            .all(char::is_alphabetic)
    }
    fn is_number(s: &String) -> bool {
        s.as_bytes()
            .iter()
            .map(|n| char::from(*n))
            .all(char::is_numeric)
    }
    fn pass2(&self, ast: &Ast) -> Ast {
        match ast {
            &Ast::BinOp(ref op, ref lhs, ref rhs) => {
                let lhs = self.pass2(&lhs);
                let rhs = self.pass2(&rhs);
                if let Ast::UnOp(ref imm, lv) = lhs {
                    if imm == "imm" {
                        if let Ast::UnOp(ref imm, rv) = rhs {
                            if imm == "imm" {
                                return Ast::UnOp(
                                    String::from("imm"),
                                    match op.as_str() {
                                        "+" => lv + rv,
                                        "-" => lv - rv,
                                        "*" => lv * rv,
                                        "/" => lv / rv,
                                        _ => panic!("Unexpected operator"),
                                    },
                                );
                            }
                        }
                    }
                }
                Ast::BinOp(op.clone(), Box::new(lhs), Box::new(rhs))
            }
            &Ast::UnOp(_, _) => ast.clone(),
        }
    }

    fn pass3(&self, ast : &Ast) -> Vec<String> {
        let mut result = Vec::new();
        match ast {
            &Ast::UnOp(ref ty, val) => {
                let ty = ty.as_str();
                match ty {
                    "imm" => {
                        result.push(format!("IM {}", val));
                    },
                    "arg" => {
                        result.push(format!("AR {}", val));
                    }
                    _ => panic!("Unexpected ast type"),
                }
            },
            &Ast::BinOp(ref op, ref lhs, ref rhs) => {
                let op = op.as_str();
                result.append(&mut self.pass3(&*rhs));
                result.push(String::from("SW"));
                result.push(String::from("PU"));
                result.append(&mut self.pass3(&*lhs));
                result.push(String::from(match op {
                    "+" => "AD",
                    "-" => "SU",
                    "*" => "MU",
                    "/" => "DI",
                    _ => panic!("Unexpected ast operator"),
                }));
                result.push(String::from("SW"));
                result.push(String::from("PO"));
                result.push(String::from("SW"));
            }
        }
        result
      }
}
