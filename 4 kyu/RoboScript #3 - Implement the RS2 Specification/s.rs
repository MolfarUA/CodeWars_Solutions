58738d518ec3b4bf95000192


use std::collections::HashSet;
use itertools::Itertools;

// Just expand the code into single instructions without parens or repeats
fn preprocess(code: &str) -> String {
    let mut output = String::new();
    let mut iter = code.chars().peekable();
    let mut prev = String::new();
    while let Some(c) = iter.next() {
        match c {
            'F' | 'R' | 'L' => {
                output.push(c);
                prev = c.to_string();
            }
            '(' => {
                let mut open = 1;
                let inner_str = iter.by_ref().take_while(|&c| {
                    match c {
                        '(' => { open += 1; true },
                        ')' => { open -= 1; true },
                        _ => true
                    }
                } && open > 0).collect::<String>();
                let inner = preprocess(&inner_str);
                output.push_str(&inner);
                prev = inner;
            }

            '0'..='9' => {
                let mut number = c.to_string();
                while let Some(d) = iter.next_if(|x| x.is_digit(10)) {
                    number.push(d);
                }
                match number.parse::<usize>() {
                    Ok(0) => output.replace_range(output.len()-prev.len().., ""),
                    Ok(n) => output.push_str(&prev.repeat(n-1)),
                    Err(_) => ()
                }
            }
            _ => (),
        }
    }
    output
}



// Now we can use our code from last time, but even simpler!
pub fn execute(code: &str) -> String {
    let processed_code = preprocess(code);
    let mut dir = (0, 1);
    let mut pos = (0i32, 0i32);
    let mut path = HashSet::new();
    path.insert(pos);
    let (mut min_x, mut max_x) = (0, 0);
    for cmd in processed_code.chars() {
        match cmd {
            'R' => dir = (dir.1, -dir.0),
            'L' => dir = (-dir.1, dir.0),
            'F' => {
                pos = (pos.0 + dir.0, pos.1 + dir.1);
                min_x = min_x.min(pos.1);
                max_x = max_x.max(pos.1);
                path.insert(pos);
            }
            _ => (),
        }
    }
    let mut lines = vec![];
    let width = (max_x - min_x + 1) as usize;
    for (_, coords) in &path.iter().sorted().group_by(|&e| e.0) {
        let mut row = vec![" "; width];
        for i in coords.map(|c| (c.1 - min_x) as usize) {
            row[i] = "*";
        }
        lines.push(row.join(""));
    }
    lines.join("\r\n")
}
__________________________
use regex::Regex;
use std::{mem, iter::Peekable};

enum Rotation { None, Left, Right }

#[derive(Copy, Clone, Eq, PartialEq)]
enum Direction { Up = 0, Right, Down, Left }

impl Direction {
    fn from_num(count: isize) -> Direction {
        let count = if count < 0 {
            4 - (-count % 4)
        } else {
            count % 4
        };

        match count {
            1 => Direction::Right,
            2 => Direction::Down,
            3 => Direction::Left,
            _ => Direction::Up,
        }
    }

    fn to_num(self) -> isize {
        self as isize
    }

    fn next(&self, pos: &mut (isize, isize), count: isize) {
        match self {
            Direction::Up => { let (_, y) = pos; *y -= count; }
            Direction::Right => { let (x, _) = pos; *x += count; }
            Direction::Down => { let (_, y) = pos; *y += count; }
            Direction::Left => { let (x, _) = pos; *x -= count; }
        }
    }

    #[allow(unused_must_use)]
    fn change(&mut self, rot: Rotation, count: isize) {
        let v = self.to_num();

        match rot {
            Rotation::Left => { mem::replace(self, Self::from_num(v - count)); }
            Rotation::Right => { mem::replace(self, Self::from_num(v + count)); }
            _ => {}
        }
    }
}

struct TheGridForTron {
    grid: Vec<String>,
    size: isize,
    org: (isize, isize),
    pos: (isize, isize),
    dir: Direction,
}

impl TheGridForTron {
    fn new() -> Self {
        Self { grid: vec!["*".to_string()], size: 1, org: (0, 0), pos: (0, 0), dir: Direction::Right }
    }

    fn grow(&mut self) {
        let diff = self.org.0 - self.pos.0;

        // Grow to left
        if diff > 0 {
            self.org.0 = self.pos.0;
            self.size += diff;

            let s = " ".repeat(diff as usize);

            for line in self.grid.iter_mut() {
                line.insert_str(0, &s);
            }

            return;
        }

        let diff = self.org.1 - self.pos.1;

        // Grow to up
        if diff > 0 {
            self.org.1 = self.pos.1;

            let s = " ".repeat(self.size as usize);

            (0..diff as usize).for_each(|_| self.grid.insert(0, s.clone()));

            return;
        }

        let diff = self.pos.0 - (self.org.0 + self.size) + 1;

        // Grow to right
        if diff > 0 {
            let s = " ".repeat(diff as usize);

            self.size += diff;
            for line in self.grid.iter_mut() {
                line.push_str(&s);
            }

            return;
        }

        let diff = self.pos.1 - (self.org.1 + self.grid.len() as isize) + 1;

        // Grow to down
        if diff > 0 {
            let s = " ".repeat(self.size as usize);

            (0..diff as usize).for_each(|_| self.grid.push(s.clone()));
        }
    }

    fn trace_path(&mut self, old: (isize, isize)) {
        match self.dir {
            Direction::Up => {
                let pos = (self.pos.0 - self.org.0) as usize;
                let org = self.org.1;
                let lines = &mut self.grid[(self.pos.1-org) as usize..(old.1-org) as usize];

                for line in lines.iter_mut() {
                    line.replace_range(pos..=pos, "*");
                }
            }

            Direction::Right => {
                let s = "*".repeat((self.pos.0 - old.0) as usize);
                let org = self.org.0;
                let line = &mut self.grid[(self.pos.1-self.org.1) as usize];

                line.replace_range((old.0+1-org) as usize..=(self.pos.0-org) as usize, s.as_str());
            }

            Direction::Down => {
                let pos = (self.pos.0 - self.org.0) as usize;
                let org = self.org.1;
                let lines = &mut self.grid[(old.1+1-org) as usize..=(self.pos.1-org) as usize];

                for line in lines.iter_mut() {
                    line.replace_range(pos..=pos, "*");
                }
            }

            Direction::Left => {
                let s = "*".repeat((old.0 - self.pos.0) as usize);
                let org = self.org.0;
                let line = &mut self.grid[(self.pos.1-self.org.1) as usize];

                line.replace_range((self.pos.0-org) as usize..(old.0-org) as usize, s.as_str());
            }
        }
    }

    fn do_move(&mut self, rot: Rotation, count: isize) {
        if let Rotation::None = rot {
            let old = self.pos;

            self.dir.next(&mut self.pos, count);
            self.grow();
            self.trace_path(old);
        } else {
            self.dir.change(rot, count);
        }
    }

    fn serialize(&self) -> String {
        self.grid.join("\r\n")
    }
}

pub fn expand_instructions(code: &mut Peekable<impl Iterator<Item=char>>) -> String {
    let mut res = String::new();
    let mut sub_str = String::new();
    let mut in_group = false;
    let mut count: Option<u32> = None;

    while let Some(ch) = code.peek() {
        if in_group {
            match ch.to_digit(10) {
                Some(n) => {
                    let v = (count.unwrap_or_default() * 10) + n;

                    count.replace(v);
                    code.next();
                }
                None => {
                    let s = if let Some(n) = count {
                        count = None;
                        sub_str.repeat(n as usize)
                    } else {
                        sub_str
                    };

                    res.push_str(&s);

                    sub_str = String::new();
                    in_group = false;
                }
            }
        } else {
            let ch = *ch;

            code.next();

            match ch {
                ')' => { break; }
                '(' => {
                    sub_str = expand_instructions(code);
                    in_group = true;
                }
                ch => { res.push(ch); }
            }
        }
    }

    if !sub_str.is_empty() {
        if let Some(n) = count {
            sub_str = sub_str.repeat(n as usize);
        };

        res.push_str(&sub_str);
    }

    res
}

fn parse_instruction(code: &str) -> (char, isize) {
    let c = code.chars().next().unwrap();
    let n_str = code.trim_start_matches(c);
    let sz = n_str.len() as isize;
    let mut n = code.len() as isize - sz;

    if sz > 0 {
        n += n_str.parse::<isize>().unwrap() - 1;
    }

    (c, n)
}

pub fn execute(code: &str) -> String {
    let code = {
        let mut it = code.chars().peekable();

        expand_instructions(&mut it)
    };

    let mut grid = TheGridForTron::new();

    for m in Regex::new(r"F+\d*|L+\d*|R+\d*").unwrap().find_iter(&code) {
        let (action, count) = parse_instruction(m.as_str());

        match action {
            'F' => { grid.do_move(Rotation::None, count); }
            'L' => { grid.do_move(Rotation::Left, count); }
            'R' => { grid.do_move(Rotation::Right, count); }
            _ => {}
        }
    }

    grid.serialize()
}
__________________________
pub fn execute(code: &str) -> String {
    let instructions = parser::parse(code);
    let mut robot = Robot::new();
    robot.interpret(&instructions);
    let field = robot.get_field();
    field_to_string(field)
}

#[derive (PartialEq, Debug)]
enum Direction {
    Top,
    Bottom,
    Left,
    Right
}

#[derive (PartialEq, Clone, Debug)]
enum Cell {
    Visited,
    NotVisited
}

#[derive (Debug)]
pub enum Instruction {
    Step(u32),
    TurnLeft(u32),
    TurnRight(u32),
    Block(Vec<Instruction>, u32)
}

#[derive (Debug)]
struct Position {
    pub x: usize,
    pub y: usize
}

#[derive (Debug)]
struct Robot {
    direction: Direction,
    field: Vec<Vec<Cell>>,
    position: Position
}

impl Robot {
    fn new() -> Robot {
        Robot {
            direction: Direction::Right,
            field: vec![vec![Cell::Visited]],
            position: Position {x: 0, y: 0}
        }
    }

    fn interpret(&mut self, instructions: &[Instruction]) {
        use Instruction::*;

        for instruction in instructions.iter() {
            match instruction {
                Step(times) =>
                    (0 .. *times).for_each(|_| self.step()),
                TurnLeft(times) =>
                    (0 .. *times).for_each(|_| self.turn_left()),
                TurnRight(times) =>
                    (0 .. *times).for_each(|_| self.turn_right()),
                Block(instructions, times) =>
                    (0 .. *times).for_each(|_| self.interpret(&instructions)),
            }
        }
    }

    fn get_field(&mut self) -> &[Vec<Cell>] {
        &self.field
    }

    fn turn_left(&mut self) {
        use Direction::*;

        self.direction = match self.direction {
            Top => Left,
            Left => Bottom,
            Bottom => Right,
            Right => Top
        }
    }

    fn turn_right(&mut self) {
        use Direction::*;

        self.direction = match self.direction {
            Top => Right,
            Right => Bottom,
            Bottom => Left,
            Left => Top
        }
    }

    fn step(&mut self) {
        use Direction::*;

        match self.direction {
            Right => self.step_right(),
            Left => self.step_left(),
            Top => self.step_top(),
            Bottom => self.step_bottom()
        }
    }

    fn step_right(&mut self) {
        if self.position.x + 1 >= self.field[self.position.y].len() {
            for y in 0 .. self.field.len() {
                self.field[y].push(Cell::NotVisited);
            }
        }

        self.position.x += 1;
        self.mark_visited();
    }

    fn step_left(&mut self) {
        if self.position.x == 0 {
            for y in 0 .. self.field.len() {
                self.field[y].insert(0, Cell::NotVisited);
            }
        } else {
            self.position.x -= 1;
        }

        self.mark_visited();
    }

    fn step_bottom(&mut self) {
        if self.position.y + 1 >= self.field.len() {
            self.field.push(
                vec![Cell::NotVisited; self.field[self.position.y].len()]
            )
        }

        self.position.y += 1;
        self.mark_visited();
    }

    fn step_top(&mut self) {
        if self.position.y == 0 {
            self.field.insert(0,
                vec![Cell::NotVisited; self.field[0].len()]
            );
        } else {
            self.position.y -= 1;
        }

        self.mark_visited();
    }

    fn mark_visited(&mut self) {
        self.field[self.position.y][self.position.x] = Cell::Visited;
    }
}

pub mod parser {
    use super::*;
    use super::combinators::*;

    pub fn parse(input: &str) -> Vec<Instruction> {
        let mut instructions = vec![];
        let mut input = input;

        while let Some((next_input, instruction)) = instruction().parse(input) {
            instructions.push(instruction);
            input = next_input;
        }

        instructions
    }

    fn number(input: &str) -> ParseRes<u32> {
        let mut matched = String::new();
        let mut chars = input.chars();

        match chars.next() {
            Some(ch) => {
                if ch.is_numeric() {
                    matched.push(ch);
                } else {
                    return None;
                }
            },
            None => {
                return None;
            }
        }

        while let Some(ch) = chars.next() {
            if ch.is_numeric() {
                matched.push(ch);
            } else {
                break;
            }
        }

        let next_index = matched.len();
        let num = matched.parse::<u32>().unwrap();
        Some((&input[next_index .. ], num))
    }

    fn char<'a>(ch: char)
        -> impl Parser<'a, char>
    {
        move |input: &'a str| {
            match input.chars().next() {
                Some(input_ch) => if input_ch == ch {
                    Some((&input[1..], ch))
                } else {
                    None
                },
                None => None
            }
        }
    }

    fn step<'a>() ->
        impl Parser<'a, Instruction>
    {
        map(char('F'), |_| Instruction::Step(1))
    }

    fn turn_left<'a>() ->
        impl Parser<'a, Instruction>
    {
        map(char('L'), |_| Instruction::TurnLeft(1))
    }

    fn turn_right<'a>() ->
        impl Parser<'a, Instruction>
    {
        map(char('R'), |_| Instruction::TurnRight(1))
    }

    fn step_n<'a>() ->
        impl Parser<'a, Instruction>
    {
        map(
            pair(char('F'), number),
            |(_, n)| Instruction::Step(n)
        )
    }

    fn turn_left_n<'a>() ->
        impl Parser<'a, Instruction>
    {
        map(
            pair(char('L'), number),
            |(_, n)| Instruction::TurnLeft(n)
        )
    }

    fn turn_right_n<'a>() ->
        impl Parser<'a, Instruction>
    {
            map(
                pair(char('R'), number),
                |(_, n)| Instruction::TurnRight(n)
            )
    }

    fn block<'a>() ->
        impl Parser<'a, Instruction>
    {
        left(
            right(
                char('('),
                zero_or_more(lazy(instruction)),
            ),
            char(')')
        )
        .map(|instructions| Instruction::Block(instructions, 1))
    }

    fn block_n<'a>() ->
        impl Parser<'a, Instruction>
    {
        pair(
            left(
                right(
                    char('('),
                    zero_or_more(lazy(instruction)),
                ),
                char(')')
            ),
            number
        )
        .map(|(instructions, n)| Instruction::Block(instructions, n))
    }

    fn instruction<'a>() ->
        impl Parser<'a, Instruction>
    {
        step_n()
            .or(turn_left_n())
            .or(turn_right_n())
            .or(step())
            .or(turn_left())
            .or(turn_right())
            .or(block_n())
            .or(block())
    }

}

pub mod combinators {
    pub type ParseRes<'a, Output> = Option<(&'a str, Output)>;

    pub trait Parser<'a, Output> {
        fn parse(&self, input: &'a str) -> ParseRes<'a, Output>;

        fn map<F, NewOutput>(self, map_fn: F)
            -> BoxedParser<'a, NewOutput>
        where
            Self: Sized + 'a,
            Output: 'a,
            NewOutput: 'a,
            F: Fn(Output) -> NewOutput + 'a
        {
            BoxedParser::new(map(self, map_fn))
        }

        fn or<P>(self, parser: P)
            -> BoxedParser<'a, Output>
        where
            Self: Sized + 'a,
            Output: 'a,
            P: 'a,
            P: Parser<'a, Output>
        {
            BoxedParser::new(or(self, parser))
        }
    }

    impl<'a, F, Output> Parser<'a, Output> for F
    where
        F: Fn(&'a str) -> ParseRes<Output>,
    {
        fn parse(&self, input: &'a str) -> ParseRes<'a, Output> {
            self(input)
        }
    }

    pub struct BoxedParser<'a, Output> {
        parser: Box<dyn Parser<'a, Output> + 'a>,
    }

    impl<'a, Output> BoxedParser<'a, Output> {
        pub fn new<P>(parser: P) -> Self
        where
            P: Parser<'a, Output> + 'a
        {
            BoxedParser {
                parser: Box::new(parser)
            }
        }
    }

    impl<'a, Output> Parser<'a, Output> for BoxedParser<'a, Output> {
        fn parse(&self, input: &'a str) -> ParseRes<'a, Output> {
            self.parser.parse(input)
        }
    }

    pub struct LazyParser<'a, Output> {
        constructor: Box<dyn Fn() -> BoxedParser<'a, Output> + 'a>
    }

    impl<'a, Output> LazyParser<'a, Output> {
        pub fn new<F>(constructor: F) -> Self
        where
            F: Fn() -> BoxedParser<'a, Output> + 'a
        {
            LazyParser { constructor: Box::new(constructor) }
        }
    }

    impl<'a, Output> Parser<'a, Output> for LazyParser<'a, Output> {
        fn parse(&self, input: &'a str) -> ParseRes<'a, Output> {
            (self.constructor)().parse(input)
        }
    }

    pub fn map<'a, P, F, A, B>(parser: P, map_fn: F) -> impl Parser<'a, B>
    where
        P: Parser<'a, A>,
        F: Fn(A) -> B
    {
        move |input|
            parser.parse(input)
                .map(|(next_input, res)| (next_input, map_fn(res)))
    }

    pub fn pair<'a, P1, P2, R1, R2>(parser1: P1, parser2: P2)
        -> impl Parser<'a, (R1, R2)>
    where
        P1: Parser<'a, R1>,
        P2: Parser<'a, R2>
    {
        move |input| match parser1.parse(input) {
            Some((next_input, result1)) => match parser2.parse(next_input) {
                Some((final_input, result2)) => Some((final_input, (result1, result2))),
                None => None,
            },
            None => None,
        }
    }

    pub fn left<'a, P1, P2, R1, R2>(parser1: P1, parser2: P2) -> impl Parser<'a, R1>
    where
        P1: Parser<'a, R1>,
        P2: Parser<'a, R2>,
    {
        map(pair(parser1, parser2), |(left, _right)| left)
    }

    pub fn right<'a, P1, P2, R1, R2>(parser1: P1, parser2: P2) -> impl Parser<'a, R2>
    where
        P1: Parser<'a, R1>,
        P2: Parser<'a, R2>,
    {
        map(pair(parser1, parser2), |(_left, right)| right)
    }

    pub fn zero_or_more<'a, P, T>(parser: P)
        -> impl Parser<'a, Vec<T>>
    where
        P: Parser<'a, T>
    {
        move |mut input| {
            let mut res = vec![];

            while let Some((next_input, val)) = parser.parse(input) {
                input = next_input;
                res.push(val);
            }

            Some((input, res))
        }
    }

    pub fn or<'a, P1, P2, T>(parser1: P1, parser2: P2)
        -> impl Parser<'a, T>
    where
        P1: Parser<'a, T>,
        P2: Parser<'a, T>,
    {
        move |input| match parser1.parse(input) {
            some @ Some(_) => some,
            None => parser2.parse(input)
        }
    }

    pub fn lazy<'a, P, T, F>(f: F)
        -> LazyParser<'a, T>
    where
        P: Parser<'a, T> + 'a,
        F: Fn() -> P + 'a,
    {
        LazyParser::new(move || BoxedParser::new(f()))
    }

}

fn field_to_string(field: &[Vec<Cell>]) -> String {
    use Cell::*;

    field.iter()
        .map(|row| row.iter()
            .map(|cell|
                match *cell {
                    Visited => '*',
                    NotVisited => ' '
            })
            .collect::<String>()
        )
        .collect::<Vec<String>>()
        .join("\r\n")
}
__________________________
#[derive(Copy, Clone)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

use crate::Direction::*;

fn new_direction(pos:Direction, rot:char) -> Direction {
    match (pos,rot) {
        (Up,    'L') => Left,
        (Down,  'L') => Right,
        (Left,  'L') => Down,
        (Right, 'L') => Up,
        (Up,    'R') => Right,
        (Down,  'R') => Left,
        (Left,  'R') => Up,
        _            => Down,
    }
}

fn new_position(d:Direction, p:(i32,i32)) -> (i32,i32) {
    match d {
        Up    => (p.0, p.1-1),
        Down  => (p.0, p.1+1),
        Left  => (p.0-1, p.1),
        Right => (p.0+1, p.1),
    }
}

fn parse_str (strn:&str) -> String {
    
    let mut s = strn.to_string();
    
    while s.contains('(') {

        let v = s.match_indices(|x| x == '(' || x == ')').collect::<Vec<_>>();
        let mut open = v.iter().filter(|x| x.1 == "(").collect::<Vec<_>>();
        let close = v.iter().filter(|x| x.1 == ")").collect::<Vec<_>>();
        let mut z:Vec<(usize, usize)> = vec![];
    
        for i in close {
            let x = open.iter().enumerate().take_while(|x| x.1.0 < i.0).last().unwrap();
            let id = x.0;
            z.push((x.1.0, i.0));
            open.remove(id);
        }

        let (x,y) = z.pop().unwrap();
        let n = match &s[y+1..].chars().take_while(|x| x.is_numeric()).collect::<String>().parse::<usize>() {
            Ok(num) => (*num, num.to_string().len()),
            _       => (1,0),
        };
        let p_str = &s[x+1..y].repeat(n.0);

        s = [&s[0..x], p_str, &s[y+1+n.1..]].join("");
    }
    s
}

pub fn execute(code: &str) -> String {

    let new_code = parse_str(code);
    let nums:Vec<&str> = new_code.split(char::is_alphabetic).filter(|x| !x.is_empty()).collect();
    let chrs = new_code.split(char::is_numeric)
                   .filter(|x| !x.is_empty())
                   .map(|s| s.chars().map(|ch| (ch,1)).collect::<Vec<_>>())
                   .enumerate()
                   .map(|(i, mut vch)| {
                                 match nums.get(i) {
                                    Some(n) => { if let Some(l) = vch.last_mut() { *l = (l.0,n.parse::<i32>().unwrap()) } vch},
                                    None    => vch,
                                }
                             })
                   .collect::<Vec<_>>().concat();
    let mut dir:Direction = Right;
    let mut pos:(i32,i32) = (0,0);
    let mut coords:Vec<(i32,i32)> = vec![(0,0)];

    for (ch,d) in chrs.iter() {
        if *ch == 'R' || *ch == 'L' {
            for _ in 0..*d {
                dir = new_direction(dir, *ch);
            }
        } else {
            for _ in 0..*d {
                pos = new_position(dir,pos);
                coords.push(pos);
            }
        }
    }

    let min_x = coords.iter().min_by_key(|a| a.0).unwrap().0.abs();
    let min_y = coords.iter().min_by_key(|a| a.1).unwrap().1.abs();

    let pos_coords = coords.iter().map(|(x,y)| (x+min_x,y+min_y)).collect::<Vec<_>>();

    let max_x = pos_coords.iter().max_by_key(|a| a.0).unwrap().0 as usize;
    let max_y = pos_coords.iter().max_by_key(|a| a.1).unwrap().1 as usize;

    let mut res = vec![vec![' ';max_x+1];max_y+1];

    for (x,y) in pos_coords.iter() {
        res[*y as usize][*x as usize] = '*'
    }

    res.iter().map(|x| x.iter().collect::<String>()).collect::<Vec<_>>().join("\r\n")
}
