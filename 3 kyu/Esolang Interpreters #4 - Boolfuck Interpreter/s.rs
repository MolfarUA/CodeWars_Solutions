5861487fdb20cff3ab000030


use std::collections::HashMap;

fn boolfuck(code: &str, input: Vec<u8>) -> Vec<u8> {
    let code = code.as_bytes();
    let mut input = input.into_iter().flat_map(|b| (0u8..8).map(move |i| (b >> i) & 1));
    let mut output = Vec::new();
    let mut tape = HashMap::new();
    let mut stack = Vec::new();
    let mut cp = 0;
    let mut tp = 0;

    while cp < code.len() {
        match code[cp] {
            b'+' => {
                let t = tape.entry(tp).or_insert(0);
                *t = if *t == 0 { 1 } else { 0 }
            },
            b',' => { input.next().map(|x| tape.insert(tp, x)); },
            b';' => output.push(*tape.get(&tp).unwrap_or(&0)),
            b'<' => tp -= 1,
            b'>' => tp += 1,
            b'[' => {
                if *tape.get(&tp).unwrap_or(&0) == 0 {
                    cp = matching_bracket(code, cp).unwrap();
                } else {
                    stack.push(cp);
                }
            },
            b']' => cp = stack.pop().unwrap().wrapping_sub(1),
            _ => (),
        }
        cp = cp.wrapping_add(1);
    }

    output.chunks(8).map(|b| b.iter().rev().fold(0, |acc, x| (acc << 1) | x)).collect()
}

fn matching_bracket(code: &[u8], open: usize) -> Option<usize> {
    let mut stack = 0;
    for (i, &c) in code[open..].iter().enumerate() {
        match c {
            b'[' => stack += 1,
            b']' => { stack -= 1; if stack == 0 { return Some(open + i); } },
            _ => (),
        }
    }
    None
}
_____________________________
use std::collections::VecDeque;

trait BitToByte {
    fn to_bytes(self) -> Vec<u8>;
}
trait ByteToBit {
    fn to_bits(self) -> Vec<bool>;
}

impl BitToByte for Vec<bool> {
    fn to_bytes(self) -> Vec<u8> {
        let mut bytes = Vec::with_capacity(self.len() / 8);

        let mut bits = VecDeque::from(self);

        while !bits.is_empty() {
            let mut byte = 0u8;
            for i in 0..8 {
                let bit = bits.pop_front().unwrap_or_default();
                byte |= (bit as u8) << i;
            }
            bytes.push(byte);
        }

        bytes
    }
}

impl ByteToBit for Vec<u8> {
    fn to_bits(self) -> Vec<bool> {
        let mut bits = Vec::with_capacity(self.len() * 8);
        for byte in self {
            for i in 0..8 {
                let mask = 1 << i;
                bits.push(byte & mask > 0);
            }
        }
        bits
    }
}

struct Interpreter<'a> {
    // The code to run
    code: &'a [u8],
}

impl<'a> Interpreter<'a> {
    const fn new(code: &'a str) -> Self {
        Self {
            code: code.as_bytes(),
        }
    }

    fn run(&mut self, input: Vec<u8>) -> Vec<u8> {
        let mut input = VecDeque::from(input.to_bits());
        let mut output = Vec::new();
        let mut tape = Tape::new();
        let mut ip = 0;

        'run: loop {
            if let Some(c) = self.code.get(ip) {
                match *c as char {
                    '+' => tape.flip(),
                    ',' => tape.set(input.pop_front().unwrap_or_default()),
                    ';' => output.push(tape.get()),
                    '<' => tape.left(),
                    '>' => tape.right(),
                    '[' => {
                        if !tape.get() {
                            ip += 1;
                            let mut seen_braces = 0;
                            'left_brace: loop {
                                match *self.code.get(ip).expect("Unmached [") {
                                    b'[' => seen_braces += 1,
                                    b']' => {
                                        if seen_braces == 0 {
                                            break 'left_brace;
                                        }
                                        seen_braces -= 1;
                                    }
                                    _ => (),
                                }
                                ip += 1;
                            }
                        }
                    }
                    ']' => {
                        if tape.get() {
                            ip -= 1;
                            let mut seen_braces = 0;
                            'right_brace: loop {
                                match *self.code.get(ip).expect("Unmached ]") {
                                    b']' => seen_braces += 1,
                                    b'[' => {
                                        if seen_braces == 0 {
                                            break 'right_brace;
                                        }
                                        seen_braces -= 1;
                                    }
                                    _ => (),
                                }
                                ip -= 1;
                            }
                        }
                    }
                    _ => (),
                }
                ip += 1;
            } else {
                break 'run;
            }
        }

        output.to_bytes()
    }
}

struct Tape {
    inner: Vec<bool>,
    cursor: usize,
}

impl Tape {
    fn new() -> Self {
        const INITIAL_SIZE: usize = 64;
        Self {
            inner: vec![false; INITIAL_SIZE],
            cursor: INITIAL_SIZE / 2,
        }
    }

    fn flip(&mut self) {
        self.inner[self.cursor] ^= true;
    }

    fn set(&mut self, bit: bool) {
        self.inner[self.cursor] = bit;
    }

    fn get(&self) -> bool {
        self.inner[self.cursor]
    }

    fn right(&mut self) {
        if self.cursor == self.inner.len() - 1 {
            self.extend_front();
        }
        self.cursor += 1;
    }
    fn left(&mut self) {
        if self.cursor == 0 {
            self.extend_back();
        }
        self.cursor -= 1;
    }

    fn extend_front(&mut self) {
        self.inner.append(&mut vec![false; self.inner.len()]);
    }
    fn extend_back(&mut self) {
        self.cursor += self.inner.len();

        let mut new_inner = vec![false; self.inner.len()];
        new_inner.append(&mut self.inner);

        self.inner = new_inner;
    }
}

fn boolfuck(code: &str, input: Vec<u8>) -> Vec<u8> {
    let mut interpreter = Interpreter::new(code);
    interpreter.run(input)
}
_____________________________
struct BitBuf {
    buffer: Vec<u8>,
    ptr: usize,
}

impl BitBuf {
    fn new(init: Vec<u8>) -> Self {
        Self {
            buffer: init,
            ptr: 0,
        }
    }

    fn rigth(&mut self) {
        self.ptr += 1;
        let byte = self.ptr / 8;
        if self.buffer.len() <= byte {
            self.buffer.push(0);
        }
    }

    fn left(&mut self) {
        if self.ptr <= 0 {
            self.ptr = 7;
            self.buffer.insert(0, 0);
        } else {
            self.ptr -= 1;
        }
    }

    fn flip(&mut self) {
        let bit = self.ptr % 8;
        let byte = self.ptr / 8;
        let mask = 1u8 << bit;
        self.buffer[byte] ^= mask;
    }

    fn get(&self) -> u8 {
        let bit = self.ptr % 8;
        let byte = self.ptr / 8;
        let mask = 1u8 << bit;
        if (self.buffer[byte] & mask) > 0 {
            1
        } else {
            0
        }
    }

    fn set(&mut self, v: u8) {
        let bit = self.ptr % 8;
        let byte = self.ptr / 8;
        if self.buffer.len() == 0 {
            self.buffer.push(0);
        }
        let mask = 1u8 << bit;
        if v == 0 {
            self.buffer[byte] &= !(mask);
        } else {
            self.buffer[byte] |= mask;
        }
    }
}

fn jump_tuple(code: &str) -> Vec<(usize, usize)> {
    let mut stack = Vec::new();
    let mut result = Vec::new();

    for (idx, cmd) in code.chars().enumerate() {
        match cmd {
            '[' => stack.push(idx),
            ']' => result.push((stack.pop().unwrap(), idx)),
            _ => {}
        }
    }

    result
}

fn boolfuck(code: &str, input: Vec<u8>) -> Vec<u8> {
    let mut input = BitBuf::new(input);
    let mut output = BitBuf::new(vec![]);
    let mut tape = BitBuf::new(vec![0]);
    let jumps = jump_tuple(code);
    let code = code.chars().collect::<Vec<_>>();
    let mut is_first = true;

    let mut cursor: usize = 0;
    while let Some(cmd) = code.get(cursor) {
        match cmd {
            ';' => {
                if !is_first {
                    output.rigth();
                }
                output.set(tape.get());
                is_first = false;
            }
            '+' => tape.flip(),
            ',' => {
                tape.set(input.get());
                input.rigth();
            }
            '>' => tape.rigth(),
            '<' => tape.left(),
            '[' => {
                if tape.get() == 0 {
                    let jmp = jumps.iter().find(|&p| p.0 == cursor);
                    cursor = jmp.unwrap().1;
                }
            }
            ']' => {
                if tape.get() == 1 {
                    let jmp = jumps.iter().find(|&p| p.1 == cursor);
                    cursor = jmp.unwrap().0;
                }
            }
            _ => {}
        }
        cursor += 1;
    }
    output.buffer
}
