5870fa11aa0428da750000da


use std::cmp;
use std::collections::HashSet;

#[derive(Clone, Copy)]
#[repr(i64)]
enum Direction {
    East = 0,
    South = 1,
    West = 2,
    North = 3
}

struct Turtle {
    direction: Direction,
    x: i64,
    y: i64,
}

struct PooMap {
    traces: HashSet<(i64, i64)>,
    right_edge: i64,
    bottom_edge: i64,
    left_edge: i64,
    top_edge: i64,
}

impl Direction {
    fn from_num(&mut self, num: i64) {
        match (num % 4 + 4) % 4 {
            x if x == Direction::East as i64  => *self = Direction::East,
            x if x == Direction::South as i64 => *self = Direction::South,
            x if x == Direction::West as i64  => *self = Direction::West,
            x if x == Direction::North as i64 => *self = Direction::North,
            _ => {}, //self.from_num(num % 4)
        };
    }
}

impl Turtle {
    fn new() -> Turtle {
        Turtle {
            direction: Direction::East,
            x: 0,
            y: 0,
        }
    }
    
    fn forward(&mut self, steps: i64, map: &mut PooMap) {
        match self.direction {
            Direction::East  => {
                (self.x..(self.x + steps)).for_each(|x| { map.traces.insert((x, self.y)); } );
                self.x += steps;
            },
            Direction::South => {
                (self.y..(self.y + steps)).for_each(|y| { map.traces.insert((self.x, y)); } );
                self.y += steps;
            },
            Direction::West  => {
                ((self.x - steps)..(self.x)).for_each(|x| { map.traces.insert((x, self.y)); } );
                self.x -= steps;
            },
            Direction::North => {
                ((self.y - steps)..(self.y)).for_each(|y| { map.traces.insert((self.x, y)); } );
                self.y -= steps;
            },
        };
    }
    
    fn turn_left(&mut self, steps: i64) {
        let mut dir = self.direction as i64;
        dir = dir.wrapping_sub(steps);
        self.direction.from_num(dir);
    }
    
    fn turn_right(&mut self, steps: i64) {
        let mut dir = self.direction as i64;
        dir = dir.wrapping_add(steps);
        self.direction.from_num(dir);
    }
    
    fn make_poo(&mut self, map: &mut PooMap) {
        map.right_edge  = cmp::max(map.right_edge,  self.x);
        map.bottom_edge = cmp::max(map.bottom_edge, self.y);
        map.left_edge   = cmp::min(map.left_edge,   self.x);
        map.top_edge    = cmp::min(map.top_edge,    self.y);
        map.traces.insert((self.x, self.y));
    }
}

impl PooMap {
    fn new() -> PooMap {
        PooMap {
            traces: HashSet::new(),
            right_edge: 0,
            bottom_edge: 0,
            left_edge: 0,
            top_edge: 0,
        }
    }
    
    fn dump(&self) -> String {
        let mut map_printout = String::new();
        for y in self.top_edge..self.bottom_edge + 1 {
            if y != self.top_edge {
                map_printout.push('\r');
                map_printout.push('\n');  
            }
        
            for x in self.left_edge..self.right_edge + 1 {
                if self.traces.contains(&(x,y)) { map_printout.push('*'); }
                else { map_printout.push(' '); }
            }
        }
        map_printout
    }
}

pub fn execute(code: &str) -> String {
  let mut map = PooMap::new();
  let mut turtle = Turtle::new();
  let mut program = code.chars().peekable();
  
  turtle.make_poo(&mut map);
  
  loop {
      if let Some(instruction) = program.next() {
          let mut repeat: i64 = 0;
          while let Some(value) = program.peek().unwrap_or(&'!').to_digit(10) {
              repeat = repeat * 10 + value as i64;
              program.next();
          }
          repeat = if repeat == 0 { 1 } else { repeat };
          match instruction {
              'F' => { turtle.forward(repeat, &mut map); },
              'L' => { turtle.turn_left(repeat); },
              'R' => { turtle.turn_right(repeat); },
              _ => {},
          }
          turtle.make_poo(&mut map);
      } else {
          break;
      }
  }
  
  map.dump()
}
__________________________
extern crate regex;

use regex::Regex;
use std::collections::HashSet;

#[derive(Clone, Copy)]
enum Direction {
    North,
    East,
    South,
    West,
}

struct Robot {
    x: i32,
    y: i32,
    dir: Direction,
}

impl Robot {
    fn new() -> Self {
        Self {
            x: 0,
            y: 0,
            dir: Direction::East,
        }
    }

    fn go_forward(&mut self) {
        match self.dir {
            Direction::North => {
                self.y -= 1;
            }
            Direction::East => {
                self.x += 1;
            }
            Direction::South => {
                self.y += 1;
            }
            Direction::West => {
                self.x -= 1;
            }
        }
    }

    fn turn_left(&mut self) {
        self.dir = match self.dir {
            Direction::North => Direction::West,
            Direction::East => Direction::North,
            Direction::South => Direction::East,
            Direction::West => Direction::South,
        };
    }

    fn turn_right(&mut self) {
        self.dir = match self.dir {
            Direction::North => Direction::East,
            Direction::East => Direction::South,
            Direction::South => Direction::West,
            Direction::West => Direction::North,
        };
    }

    fn position(&self) -> (i32, i32) {
        (self.x, self.y)
    }
}

struct Path {
    visited: HashSet<(i32, i32)>,
    min_x: i32,
    max_x: i32,
    min_y: i32,
    max_y: i32,
}

impl Path {
    fn new((x, y): (i32, i32)) -> Self {
        let mut visited = HashSet::new();
        visited.insert((x, y));
        Self {
            visited,
            min_x: x,
            max_x: x,
            min_y: y,
            max_y: y,
        }
    }

    fn insert(&mut self, (x, y): (i32, i32)) {
        use std::cmp::{max, min};

        self.visited.insert((x, y));

        self.min_x = min(self.min_x, x);
        self.max_x = max(self.max_x, x);
        self.min_y = min(self.min_y, y);
        self.max_y = max(self.max_y, y);
    }

    fn to_string(&self) -> String {
        (self.min_y..self.max_y + 1)
            .map(|y| {
                (self.min_x..self.max_x + 1)
                    .map(|x| {
                        if self.visited.contains(&(x, y)) {
                            '*'
                        } else {
                            ' '
                        }
                    }).collect::<String>()
            }).collect::<Vec<_>>()
            .join("\r\n")
    }
}

pub fn execute(code: &str) -> String {
    let re = Regex::new(r#"(\d+)|([FLR]+)"#).unwrap();

    let mut robot = Robot::new();
    let mut path = Path::new(robot.position());

    {
        let mut run = |cmd| {
            match cmd {
                'F' => robot.go_forward(),
                'L' => robot.turn_left(),
                'R' => robot.turn_right(),
                _ => panic!("invalid command {:?}", cmd),
            }
            path.insert(robot.position());
        };

        let mut last_cmd = '\0';
        for block in re.captures_iter(code) {
            if let Ok(n) = block[0].parse::<i32>() {
                for _ in 1..n {
                    run(last_cmd);
                }
            } else {
                for cmd in block[0].chars() {
                    run(cmd);
                    last_cmd = cmd;
                }
            }
        }
    }

    path.to_string()
}
__________________________
use std::collections::{HashSet, VecDeque};

use regex::Regex;

pub fn execute(code: &str) -> String {
    let mut space: HashSet<(i32, i32)> = HashSet::new();
    let mut directions: VecDeque<(i32, i32)> = vec![(0, 1), (-1, 0), (0, -1), (1, 0)].into();
    let (mut r, mut c) = (0, 0);
    space.insert((r, c));
    for capture in Regex::new(r#"([FLR])(\d*)"#).unwrap().captures_iter(code) {
        let instruction = capture.get(1).unwrap().as_str();
        let repeat = match capture.get(2).unwrap().as_str() {
            "" => 1,
            n => n.parse().unwrap(),
        };
        match instruction {
            "L" => directions.rotate_left(repeat % 4),
            "R" => directions.rotate_right(repeat % 4),
            _ => {
                let (dr, dc) = directions[0];
                for _ in 0..repeat {
                    r += dr;
                    c += dc;
                    space.insert((r, c));
                }
            }
        }
    }
    let r_min = space.iter().min_by_key(|pos| pos.0).unwrap().0;
    let r_max = space.iter().max_by_key(|pos| pos.0).unwrap().0;
    let c_min = space.iter().min_by_key(|pos| pos.1).unwrap().1;
    let c_max = space.iter().max_by_key(|pos| pos.1).unwrap().1;
    (r_min..=r_max)
        .map(|r| {
            (c_min..=c_max)
                .map(|c| if space.contains(&(r, c)) { '*' } else { ' ' })
                .collect::<String>()
        })
        .collect::<Vec<_>>()
        .join("\r\n")
}
