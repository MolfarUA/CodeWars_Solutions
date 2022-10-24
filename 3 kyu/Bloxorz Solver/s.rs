5a2a597a8882f392020005e5

pub mod blox {
    fn unchecked_width(map: &[&str]) -> usize {
        // SAFETY: the map is never empty, this is asserted in `blox_solver()`.
        unsafe { map.get_unchecked(0).len() }
    }

    #[derive(Clone, Copy, PartialEq, Eq)]
    struct Point {
        y: u8,
        x: u8,
    }

    fn find_byte(map: &[&str], b: u8) -> Option<Point> {
        for (y, line) in map.iter().enumerate() {
            if let Some(x) = line.bytes().position(|bil| bil == b) {
                return Some(Point {y: y as u8, x: x as u8})
            }
        }
        None
    }

    #[derive(Clone, Copy, PartialEq, Eq)]
    enum BlockOrientation {
        Upright,
        Horizontal,
        Vertical,
    }

    use self::BlockOrientation::{Upright, Horizontal, Vertical};

    #[derive(Clone, Copy, PartialEq, Eq)]
    struct BlockPos{
        top_left: Point,
        orientation: BlockOrientation,
    }

    impl BlockPos {
        fn bottom_right(&self) -> Point {
            match self.orientation {
                Upright => self.top_left,
                Horizontal => Point {y: self.top_left.y, x: self.top_left.x + 1},
                Vertical => Point {y: self.top_left.y + 1, x: self.top_left.x},
            }
        }

        fn direction_to(&self, other: &BlockPos) -> u8 {
            use std::cmp::Ordering::{Greater, Less};
            let y_cmp = other.top_left.y.cmp(&self.top_left.y);
            let x_cmp = other.top_left.x.cmp(&self.top_left.x);
            match (y_cmp, x_cmp) {
                ( Less  ,    _   ) => b'U',
                (Greater,    _   ) => b'D',
                (   _   ,  Less  ) => b'L',
                (   _   , Greater) => b'R',
                (   _   ,    _   ) => unreachable!("assume other != self"),
            }
        }

        fn neighbors<'a>(&'a self, map: &'a[&'a str]) -> impl Iterator<Item = Self> + 'a {
            let mut i: u8 = 0;
            std::iter::from_fn(move || {
                if i == 0 {
                    i = 1;
                    if let Some(pos) = self.move_up() {
                        return Some(pos);
                    }
                }
                if i == 1 {
                    i = 2;
                    if let Some(pos) = self.move_down(map.len()) {
                        return Some(pos);
                    }
                }
                if i == 2 {
                    i = 3;
                    if let Some(pos) = self.move_left() {
                        return Some(pos);
                    }
                }
                if i == 3 {
                    i = 4;
                    if let Some(pos) = self.move_right(unchecked_width(map)) {
                        return Some(pos);
                    }
                }
                None
            }).filter(move |p| {
                let bottom_right = p.bottom_right();
                let (top_y, left_x) = (p.top_left.y as usize, p.top_left.x as usize);
                let (bottom_y, right_x) = (bottom_right.y as usize, bottom_right.x as usize);
                // SAFETY: move_* methods already make sure
                // to return only valid bound-checked positions.
                unsafe {
                    *map.get_unchecked(top_y).as_bytes().get_unchecked(left_x) != b'0' &&
                    *map.get_unchecked(bottom_y).as_bytes().get_unchecked(right_x) != b'0'
                }
            })
        }

        /// Return the new position after rolling up, or `None`
        /// if the map edge is encountered. Ignore `0`s on the map.
        fn move_up(&self) -> Option<Self> {
            if self.top_left.y == 0 || (self.orientation == Upright && self.top_left.y == 1) {
                return None
            }
            let (new_top_y, new_orientation) = match self.orientation {
                Upright    => (self.top_left.y - 2, Vertical),
                Horizontal => (self.top_left.y - 1, Horizontal),
                Vertical   => (self.top_left.y - 1, Upright),
            };
            let new_top_left = Point {y: new_top_y, x: self.top_left.x};
            Some(Self {top_left: new_top_left, orientation: new_orientation})
        }

        /// Return the new position after rolling down, or `None`
        /// if the map edge is encountered. Ignore `0`s on the map.
        fn move_down(&self, map_len: usize) -> Option<Self> {
            let (new_top_y, new_orientation) = match self.orientation {
                Upright    => (self.top_left.y + 1, Vertical),
                Horizontal => (self.top_left.y + 1, Horizontal),
                Vertical   => (self.top_left.y + 2, Upright),
            };
            let new_bottom_y = match new_orientation {
                Vertical => new_top_y + 1,
                Horizontal | Upright => new_top_y,
            };
            if new_bottom_y as usize >= map_len {
                return None
            }
            let new_top_left = Point {y: new_top_y, x: self.top_left.x};
            Some(Self {top_left: new_top_left, orientation: new_orientation})
        }

        /// Return the new position after rolling left, or `None`
        /// if the map edge is encountered. Ignore `0`s on the map.
        fn move_left(&self) -> Option<Self> {
            if self.top_left.x == 0 || (self.orientation == Upright && self.top_left.x == 1) {
                return None
            }
            let (new_left_x, new_orientation) = match self.orientation {
                Upright    => (self.top_left.x - 2, Horizontal),
                Horizontal => (self.top_left.x - 1, Upright),
                Vertical   => (self.top_left.x - 1, Vertical),
            };
            let new_top_left = Point {y: self.top_left.y, x: new_left_x};
            Some(Self {top_left: new_top_left, orientation: new_orientation})
        }

        /// Return the new position after rolling right, or `None`
        /// if the map edge is encountered. Ignore `0`s on the map.
        fn move_right(&self, map_width: usize) -> Option<Self> {
            let (new_left_x, new_orientation) = match self.orientation {
                Upright    => (self.top_left.x + 1, Horizontal),
                Horizontal => (self.top_left.x + 2, Upright),
                Vertical   => (self.top_left.x + 1, Vertical),
            };
            let new_right_x = match new_orientation {
                Horizontal => new_left_x + 1,
                Vertical | Upright => new_left_x,
            };
            if new_right_x as usize >= map_width {
                return None
            }
            let new_top_left = Point {y: self.top_left.y, x: new_left_x};
            Some(Self {top_left: new_top_left, orientation: new_orientation})
        }
    }

    /// The puzzle can contain up to 15x20 non-0 points.
    /// In the worst case when all points are non-0,
    /// each point (apart from the bottom-right edge) can be
    /// the top-left point of either an
    /// upright(1), horizontal(2) or vertical(3) block.
    const MAX_N_POSITIONS: usize = 15 * 20 * 3;

    /// A very fast array-based map, specialized for this kata.
    ///
    /// On my local 15x20 benchmark, it's 5x faster than `HashMap<BlockPos, u16>`.
    ///
    /// This is made possible by the fact that there will ever be only
    /// `MAX_N_POSITIONS` unique BlockPos keys, and these keys can be very
    /// efficiently converted to contiguous array indexes.
    ///
    /// `u16` values are the length of the shortest known path from `'B'` to
    /// the given position, or `u16::MAX` if there's no known path. This value
    /// doesn't require any additional branching. Like any inefficient path,
    /// it's just going to be overwritten by more efficient paths. The
    /// actual paths are much shorter, no greater than `MAX_N_POSITIONS`.
    struct BlockPosMap {
        data: [u16; MAX_N_POSITIONS],
    }

    impl BlockPosMap {
        fn new() -> Self {
            Self {data: [u16::MAX; MAX_N_POSITIONS]}
        }

        fn insert(&mut self, k: BlockPos, v: u16) {
            let index = Self::reduce_to_index(k);
            // SAFETY: handled by
            // - Map size asserts in `blox_solver()`.
            // - `reduce_to_index()` returning values in `0..MAX_N_POSITIONS`
            //     for maps of these sizes.
            unsafe {
                *self.data.get_unchecked_mut(index) = v;
            }
        }

        fn get(&self, k: BlockPos) -> u16 {
            let index = Self::reduce_to_index(k);
            // SAFETY: handled by
            // - Map size asserts in `blox_solver()`.
            // - `reduce_to_index()` returning values in `0..MAX_N_POSITIONS`
            //     for maps of these sizes.
            unsafe {
                *self.data.get_unchecked(index)
            }
        }

        fn reduce_to_index(pos: BlockPos) -> usize {
            let y_part = (pos.top_left.y as usize) * 20 * 3;
            let x_part = (pos.top_left.x as usize) * 3;
            let orientation_part: usize = match pos.orientation {
                Upright => 0,
                Horizontal => 1,
                Vertical => 2,
            };
            y_part + x_part + orientation_part
        }
    }

    struct Solver<'a> {
        map: &'a[&'a str],
        visited: BlockPosMap,
        hole: Point,
    }

    impl<'a> Solver<'a> {
        fn new(puzzle: &'a[&'a str]) -> Self {
            let map = puzzle;
            let visited = BlockPosMap::new();
            let hole = find_byte(map, b'X').expect("map should always have an 'X'");
            Solver { map, visited, hole }
        }

        fn solve(&mut self) -> String {
            let b: Point = find_byte(self.map, b'B').expect("map should always have a 'B'");
            let start_pos = BlockPos {
                top_left: b,
                orientation: BlockOrientation::Upright,
            };
            self.fill_visited(start_pos, 0);
            self.construct_result()
        }

        fn fill_visited(&mut self, pos: BlockPos, step: u16) {
            self.visited.insert(pos, step);
            if pos.top_left == self.hole && pos.orientation == Upright {
                return
            }
            let next_step = step + 1;
            for next_pos in pos.neighbors(self.map) {
                if self.visited.get(next_pos) > next_step {
                    // Found a shorter path, visit again.
                    self.fill_visited(next_pos, next_step);
                }
            }
        }

        fn construct_result(&self) -> String {
            let hole_pos = BlockPos {top_left: self.hole, orientation: Upright};
            let n_steps = self.visited.get(hole_pos);
            let mut result = vec![b'\0'; n_steps as usize];
            let mut pos = hole_pos;
            // Navigate the path and build the string in reverse order:
            for prev_step in (0..n_steps).rev() {
                let prev_point = pos
                                .neighbors(self.map)
                                .find(|n| self.visited.get(*n) == prev_step)
                                .expect("there should always be a prev_point");
                let direction = prev_point.direction_to(&pos);
                // SAFETY: `result` is preallocated with `len() == n_steps`,
                // and `prev_step` is in `(0..n_steps).rev()`.
                unsafe {
                    *result.get_unchecked_mut(prev_step as usize) = direction;
                }
                pos = prev_point;
            }
            // SAFETY: `result` consists only of ascii "UDLR"
            // returned from `direction_to()`.
            unsafe { String::from_utf8_unchecked(result) }
        }
    }

    pub fn blox_solver(puzzle: &[&str]) -> String {
        // The map should be non-empty and no bigger than 15x20,
        // this solution heavily depends on this and leads to UB otherwise.
        assert!(!puzzle.is_empty());
        assert!(puzzle.len() <= 15);
        assert!(unchecked_width(puzzle) <= 20);
        Solver::new(puzzle).solve()
    }
}
_________________________________
mod blox{
    use std::{
        collections::{HashMap, VecDeque},
        hash::Hash,
    };
    const DIRECTIONS: [char; 4] = ['L', 'R', 'U', 'D'];

    pub fn blox_solver(puzzle: &[&str]) -> String {
        let mut positions: HashMap<Position, (char, Position)> = HashMap::new();
        let mut queue = VecDeque::new();
        let (start, goal, grid) = parse_puzzle(puzzle);
        queue.push_back(start);
        positions.insert(start, ('B', start));
        'search: loop {
            let pos = queue.pop_front().unwrap();
            for dir in DIRECTIONS {
                let next = roll(pos, dir);
                if is_valid(pos, &grid) && !positions.contains_key(&next) {
                    positions.insert(next, (dir, pos));
                    if next == goal {
                        break 'search;
                    }
                    queue.push_back(next)
                }
            }
        }
        let mut path = Vec::new();
        let mut step = goal;
        let mut dir: char;
        loop {
            (dir, step) = *positions.get(&step).unwrap();
            if dir == 'B' {
                break;
            }
            path.push(dir);
        }
        path.reverse();
        path.into_iter().collect()
    }

    fn parse_puzzle(puzzle: &[&str]) -> (Position, Position, Vec<Vec<bool>>) {
        let grid: Vec<Vec<bool>> = puzzle
            .into_iter()
            .map(|row| row.chars().map(|c| c != '0').collect())
            .collect();
        let goal = find_position(puzzle, 'X');
        let start = find_position(puzzle, 'B');
        (start, goal, grid)
    }

    fn find_position(puzzle: &[&str], c: char) -> Position {
        puzzle
            .iter()
            .enumerate()
            .find_map(|(i, row)| {
                Some(Position::Standing(
                    i as isize,
                    row.char_indices()
                        .find_map(|(j, c2)| if c == c2 { Some(j) } else { None })?
                        as isize,
                ))
            })
            .unwrap()
    }

    #[derive(PartialEq, Eq, Hash, Clone, Copy)]
    enum Position {
        Standing(isize, isize),
        Lying(isize, isize, bool), // true: toward +i, false: toward +j
    }

    fn is_valid(pos: Position, grid: &Vec<Vec<bool>>) -> bool {
        match pos {
            Position::Standing(i, j) => is_in_grid(i, j, grid),
            Position::Lying(i, j, up) => {
                is_in_grid(i, j, grid)
                    && (if up {
                        is_in_grid(i + 1, j, grid)
                    } else {
                        is_in_grid(i, j + 1, grid)
                    })
            }
        }
    }

    fn roll(pos: Position, dir: char) -> Position {
        let (di, dj) = match dir {
            'L' => (0, -1),
            'R' => (0, 1),
            'U' => (-1, 0),
            'D' => (1, 0),
            _ => panic!(),
        };
        match pos {
            Position::Lying(i, j, up) => {
                if (di != 0) ^ up {
                    Position::Lying(i + di, j + dj, up)
                } else {
                    Position::Standing(i + boast(di), j + boast(dj))
                }
            }
            Position::Standing(i, j) => Position::Lying(i - boast(-di), j - boast(-dj), di != 0),
        }
    }

    fn boast(x: isize) -> isize {
        x * (3 + x) / 2
    }

    fn is_in_grid(i: isize, j: isize, grid: &Vec<Vec<bool>>) -> bool {
        if i < 0 || j < 0 {
            return false;
        }
        let i = i as usize;
        let j = j as usize;
        i < grid.len() && j < grid[0].len() && grid[i][j]
    }
}
_________________________________
mod blox {

    #[derive(Debug,Clone, PartialEq, Hash, Eq)]
    pub struct Position {
        x: i8,
        y: i8
    }

    #[derive(Debug, Clone, PartialEq, Hash, Eq)]
    pub enum ShapePosition {
        Square(Position),
        Rectangle(Position, Position),
    }

    #[derive(Debug, Clone, PartialEq, Hash, Eq)]
    pub enum Direction {
        Up,
        Left,
        Down,
        Right,
    }

    use std::hash::{Hash, Hasher};

    #[derive(Debug, Clone)]
    pub struct State {
        shape_position: ShapePosition,
        way: String,
        directions: [Option<Direction>; 4],
    }

    impl Hash for State {
        fn hash<H: Hasher>(&self, state: &mut H) {
            self.shape_position.hash(state);
        }
}

    impl PartialEq for State {
        fn eq(&self, other: &Self) -> bool {
            self.shape_position == other.shape_position
        }
    }

    impl Eq for State {}

    use Direction::Right;
    use Direction::Down;
    use Direction::Up;
    use Direction::Left;

    use ShapePosition::Square;
    use ShapePosition::Rectangle;

    use std::collections::HashSet;

    pub fn new_shape_position(shape_position: &ShapePosition, direction:Direction) -> ShapePosition {
        match *shape_position {
            Square(Position {x, y}) => {
                match direction {
                    Right => Rectangle(Position {x: x+1, y}, Position {x: x+2, y}),
                    Down  => Rectangle(Position {x, y: y-1}, Position {x, y: y-2}),
                    Up    => Rectangle(Position {x, y: y+2}, Position {x, y: y+1}),
                    Left  => Rectangle(Position {x: x-2, y}, Position {x: x-1, y}),
                }
            },
            Rectangle(Position {x:x1, y:y1}, Position {x:x2, y: y2}) => {
                let is_horizon = y1 == y2;
                if is_horizon {
                    match direction {
                        Right => Square(Position {x: x2+1, y: y2}),
                        Down  => Rectangle(Position {x: x1, y: y1-1}, Position {x: x2, y: y2-1}),
                        Up    => Rectangle(Position {x: x1, y: y1+1}, Position {x: x2, y: y2+1}),
                        Left  => Square(Position {x: x1-1, y: y1}),
                    }
                } else {
                    match direction {
                        Right => Rectangle(Position {x: x1+1, y: y1}, Position {x: x2+1, y: y2}),
                        Down  => Square(Position {x: x2, y: y2-1}),
                        Up    => Square(Position {x: x1, y: y1+1}),
                        Left  => Rectangle(Position {x: x1-1, y: y1}, Position {x: x2-1, y: y2}),
                    }
                }
            }
        }
    }

    pub fn is_valid_shape_position(shape_position: &ShapePosition, puzzle: &[&str]) -> bool {
        let max_y = puzzle.len() as i8;
        let max_x = puzzle[0].len() as i8;

        let is_valid_coordinate = |a:i8, max_a: i8| a >=0 && a < max_a;
        match shape_position {
            &Square(Position {x, y}) => {
                is_valid_coordinate(x, max_x) &&
                is_valid_coordinate(y, max_y) &&
                get_place(&Position {x, y}, puzzle) != '0'
            },
            &Rectangle(Position {x: x1, y: y1}, Position {x: x2, y: y2}) => {
                is_valid_coordinate(x1, max_x) && is_valid_coordinate(x2, max_x) &&
                is_valid_coordinate(y1, max_y) && is_valid_coordinate(y2, max_y) &&
                get_place(&Position {x: x1, y: y1}, puzzle) != '0' && get_place(&Position {x: x2, y: y2}, puzzle) != '0'
            },
        }
    }

    pub fn new_states(state:State, puzzle: &[&str]) -> Vec<State> {
        let State {way, directions, shape_position} = state;
        let mut res = vec![];

        for direction in directions {
            if direction.is_some() {
                match direction.as_ref().unwrap() {
                    Down  => { 
                        let shape_position = new_shape_position(&shape_position, direction.unwrap());
                        if is_valid_shape_position(&shape_position, puzzle) {
                            res.push(
                                State {
                                    way:format!("{}D",way),
                                    directions:[None, Some(Left), Some(Down), Some(Right)],
                                    shape_position,
                                }
                            )
                        }
                    },
                    Right  => { 
                        let shape_position = new_shape_position(&shape_position, direction.unwrap());
                        if is_valid_shape_position(&shape_position, puzzle) {
                            res.push(
                                State {
                                    way: format!("{}R",way),
                                    directions: [Some(Up), None, Some(Down), Some(Right)],
                                    shape_position,
                                }
                            )
                        }
                    },
                    Up  => { 
                        let shape_position = new_shape_position(&shape_position, direction.unwrap());
                        if is_valid_shape_position(&shape_position, puzzle) {
                            res.push(
                                State {
                                    way: format!("{}U",way),
                                    directions: [Some(Up), Some(Left), None, Some(Right)],
                                    shape_position,
                                }
                            )
                        }
                    },
                    Left  => {
                        let shape_position = new_shape_position(&shape_position, direction.unwrap());
                        if is_valid_shape_position(&shape_position, puzzle) {
                            res.push(
                                State {
                                    way: format!("{}L",way),
                                    directions: [Some(Up), Some(Left), Some(Down), None],
                                    shape_position,
                                }
                            )
                        }
                    },
                }
            }
        }
        res
    }

    pub fn get_place(position: &Position, puzzle: &[&str]) -> char {
        let Position {x,y} = *position;
        puzzle[y as usize].chars().nth(x as usize).unwrap()
    }

    pub fn get_position(puzzle: &[&str], ch: char) -> Position {

        for y in 0..puzzle.len() {
            if puzzle[y].contains(ch) {
                let x = puzzle[y].chars().position(|x| x == ch).unwrap() as i8;
                let y = y as i8;
                return Position {x, y}
            }
        }
        Position {x:0, y:0}
    }

    pub fn blox_solver(puzzle: &[&str]) -> String {
        let rev_puzzle = &puzzle.into_iter().rev().cloned().collect::<Vec<_>>()[..];

        let start = get_position(rev_puzzle, 'B');
        let finish = Square(get_position(rev_puzzle, 'X'));

        let start_state = State {
            way: "".to_string(),
            shape_position: Square(start),
            directions: [Some(Up), Some(Right), Some(Down), Some(Left)],
        };
        let mut states = HashSet::new();
        states.insert(start_state);

        let mut res = "".to_string();

        while res.is_empty() {
            let mut b_states = HashSet::new();
            for state in states {
                let State {way, shape_position, ..} = &state;
                if shape_position == &finish {
                    res = way.to_string();
                    break;
                }
                for new_state in new_states(state, rev_puzzle) {
                    b_states.insert(new_state);
                }
            }
            states = b_states;
        }
        res
    }
}
