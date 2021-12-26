use rand::{prelude::ThreadRng, Rng};

pub fn solve_n_queens(n: usize, fixed: (usize, usize)) -> Option<String> {
    match n {
        2 | 3 => None,
        4 if NO_SOLUTIONS_4.iter().any(|x| x == &fixed) => None,
        6 if NO_SOLUTIONS_6.iter().any(|x| x == &fixed) => None,
        _ => Some(QueenSearch2::new(n, fixed.1, fixed.0).solution()),
    }
}

/// Adaptation of the algorithm from the paper ["Fast Search Algorithms for the N-Queens Problem"][paper].
/// Based on [monadius's C++ solution][monadius].
///
/// [paper]: https://pdfs.semanticscholar.org/79d2/fa13d4a5cfc02ff6936b6083bb620e4e0ce1.pdf
/// [monadius]: https://www.codewars.com/kata/reviews/59887255903747bef30000a1/groups/5eb38cb298558a00014f8a1b
struct QueenSearch2 {
    n: usize,
    fixed_row: usize,
    queens: Vec<usize>,
    diags: Vec<usize>,
    attack: Vec<usize>,
    rng: ThreadRng,
}

const C1: f64 = 0.45;
const C2: usize = 32;

impl QueenSearch2 {
    pub fn new(n: usize, row: usize, col: usize) -> Self {
        let mut queens: Vec<usize> = (0..n).collect();
        queens[row] = col;
        queens[col] = row;
        QueenSearch2 {
            n,
            fixed_row: row,
            queens,
            diags: vec![0; 4 * n],
            attack: vec![0; n],
            rng: rand::thread_rng(),
        }
    }

    pub fn solution(&mut self) -> String {
        let mut board = vec![b'.'; self.n * (self.n + 1)];
        loop {
            if self.search() {
                for (i, &q) in self.queens.iter().enumerate() {
                    board[i * (self.n + 1) + q] = b'Q';
                    board[i * (self.n + 1) + self.n] = b'\n';
                }
                return String::from_utf8(board).expect("valid utf8");
            }
        }
    }

    fn search(&mut self) -> bool {
        self.permutation();

        let mut collisions = self.compute_collisions();
        if collisions == 0 {
            return true;
        }

        let mut limit = (C1 * collisions as f64) as usize;
        let mut num_attacks = self.compute_attacks();
        let mut r = 0;
        while r < self.n * C2 {
            let mut k = 0;
            while k < num_attacks {
                let i = self.attack[k];
                let j = self.rng.gen_range(0..self.n);
                if i != j && i != self.fixed_row && j != self.fixed_row {
                    let dc = self.swap_collisions(i, j);
                    if dc > 0 {
                        self.perform_swap(i, j);
                        if collisions <= dc {
                            return true;
                        }

                        collisions -= dc;
                        if collisions < limit {
                            limit = (C1 * collisions as f64) as usize;
                            num_attacks = self.compute_attacks();
                        }
                    }
                }
                k += 1;
            }
            r += num_attacks;
        }

        false
    }

    fn permutation(&mut self) {
        for i in (1..self.n).rev() {
            let j = self.rng.gen_range(0..i);
            if i != j && i != self.fixed_row && j != self.fixed_row {
                self.queens.swap(i, j);
            }
        }
    }

    fn compute_collisions(&mut self) -> usize {
        for v in self.diags.iter_mut() {
            *v = 0;
        }

        let mut collisions = 0;
        for i in 0..self.n {
            let a = self.dn(i, i);
            let b = self.dp(i, i);
            self.diags[a] += 1;
            self.diags[b] += 1;

            if self.diags[a] >= 2 {
                collisions += 1;
            }
            if self.diags[b] >= 2 {
                collisions += 1;
            }
        }
        collisions
    }

    fn compute_attacks(&mut self) -> usize {
        let mut attacks = 0;
        for i in 0..self.n {
            if self.diags[self.dn(i, i)] > 1 || self.diags[self.dp(i, i)] > 1 {
                self.attack[attacks] = i;
                attacks += 1;
            }
        }
        attacks
    }

    fn swap_collisions(&self, i: usize, j: usize) -> usize {
        if i == j {
            return 0;
        }

        let mut c = 0;
        let i1 = &[self.dn(i, i), self.dp(i, i), self.dn(j, j), self.dp(j, j)];
        let i2 = &[self.dn(i, j), self.dp(i, j), self.dn(j, i), self.dp(j, i)];

        for k in 0..4 {
            if self.diags[i1[k]] >= 2 {
                c -= 1;
            }
            if self.diags[i2[k]] >= 1 {
                c += 1
            }
        }
        if i1[0] == i1[2] && self.diags[i1[0]] == 2 {
            c += 1;
        }
        if i1[1] == i1[3] && self.diags[i1[1]] == 2 {
            c += 1;
        }
        if i2[0] == i2[2] && self.diags[i2[0]] == 0 {
            c += 1;
        }
        if i2[1] == i2[3] && self.diags[i2[1]] == 0 {
            c += 1;
        }

        // Changed to return the count to decrease instead of a signed integer.
        if c < 0 {
            -c as usize
        } else {
            0
        }
    }

    fn perform_swap(&mut self, i: usize, j: usize) {
        if i == j {
            return;
        }

        for &k in &[self.dn(i, i), self.dp(i, i), self.dn(j, j), self.dp(j, j)] {
            self.diags[k] -= 1;
        }
        self.queens.swap(i, j);
        for &k in &[self.dn(i, i), self.dp(i, i), self.dn(j, j), self.dp(j, j)] {
            self.diags[k] += 1;
        }
    }

    #[inline]
    fn dn(&self, i: usize, j: usize) -> usize {
        i + self.queens[j]
    }

    #[inline]
    fn dp(&self, i: usize, j: usize) -> usize {
        3 * self.n + i - self.queens[j]
    }
}

#[rustfmt::skip]
const NO_SOLUTIONS_4: [(usize, usize); 8] = [
    (0, 0), (0, 3),
    (1, 1), (1, 2),
    (2, 1), (2, 2),
    (3, 0), (3, 3),
];

#[rustfmt::skip]
const NO_SOLUTIONS_6: [(usize, usize); 12] = [
    (0, 0), (0, 5),
    (1, 1), (1, 4),
    (2, 2), (2, 3),
    (3, 2), (3, 3),
    (4, 1), (4, 4),
    (5, 0), (5, 5),
];
  
  
###################################
pub fn solve_n_queens(n: usize, mandatory_coords: (usize, usize)) -> Option<String> {
    for i in 0..n {
        let mut queens = vec![i; n];
        queens[mandatory_coords.1] = mandatory_coords.0;
        let mut cols = vec![0; n];
        let mut diag1 = vec![0; 2 * n];
        let mut diag2 = vec![0; 2 * n];
        for r in 0..n {
            let q = queens[r];
            cols[q] += 1;
            diag1[r + q] += 1;
            diag2[n - 1 + r - q] += 1;
        }
        for _ in 0..12 {
            for r in (0..n).filter(|&i| i != mandatory_coords.1) {
                let q = queens[r];
                // if cols[q] == 1 && diag1[r + q] == 1 && diag2[n - 1 + r - q] == 1 {
                //     continue;
                // }
                cols[q] -= 1;
                diag1[r + q] -= 1;
                diag2[n - 1 + r - q] -= 1;
                let mut min_col = 0;
                let mut min_conf = n;
                for c in 0..n {
                    let conf = cols[c] + diag1[c + r] + diag2[n - 1 + r - c];
                    if conf < min_conf || (conf == min_conf && c != q) {
                        min_conf = conf;
                        min_col = c;
                    }
                    if min_conf == 0 {
                        break;
                    }
                }
                queens[r] = min_col;
                cols[min_col] += 1;
                diag1[r + min_col] += 1;
                diag2[n - 1 + r - min_col] += 1;
            }
            if cols.iter().all(|&i| i == 1)
                && diag1.iter().all(|&i| i <= 1)
                && diag2.iter().all(|&i| i <= 1)
            {
                dbg!(i);
                return Some(
                    queens
                        .iter()
                        .map(|&q| format!("{}Q{}\n", ".".repeat(q), ".".repeat(n - 1 - q)))
                        .collect(),
                );
            }
        }
    }
    None
}
                                               
                                               
################################
use rand::Rng;
use std::time::Instant;
use itertools::Itertools;

// Not deterministic.
pub fn solve_n_queens(n: usize, mandatory_coords: (usize, usize)) -> Option<String> {
    let start = Instant::now();
    let mandatory_coords = (mandatory_coords.1, mandatory_coords.0);
    loop {
        let mut column_pool = (0..n).into_iter().collect::<Vec<_>>();
        column_pool.remove(mandatory_coords.1);
        let mut columns = Vec::new();
        while column_pool.len() > 0 {
            let numbers_left = column_pool.len();
            columns.push(column_pool.remove(rand::thread_rng().gen_range(0..numbers_left)));
        }
        columns.insert(mandatory_coords.0, mandatory_coords.1);

        let mut neg_diagonal = vec![0; 2 * n -1];
        let mut pos_diagonal = vec![0; 2 * n -1];
        for row in 0..n {
            neg_diagonal[row + columns[row]] += 1;
            pos_diagonal[n - 1 + row - columns[row]] += 1;
        }
        reduce_collisions(&mut columns, &mut pos_diagonal, &mut neg_diagonal, n, mandatory_coords.0);

        if pos_diagonal.iter().chain(neg_diagonal.iter()).max().unwrap() <= &1 {
            return Some(
                columns.into_iter().map(|j| format!("{}{}{}\n", ".".repeat(j), 'Q', ".".repeat(n - 1 - j))).join("")
            );
        }

        if start.elapsed().as_millis() > 2000 {
            return None;
        }
    }

    fn reduce_collisions(columns: &mut Vec<usize>, pos_diagonal: &mut Vec<i32>, neg_diagonal: &mut Vec<i32>,
                         n: usize, fixed: usize) {
        loop {
            let mut swaps_performed = 0;
            for i in 0..(n - 1) {
                for j in (i + 1)..n {
                    if i == fixed || j == fixed {
                        continue;
                    }
                    let col_diff = if neg_diagonal[j + columns[i]] > 0 { 1 } else { 0 }
                        + if neg_diagonal[i + columns[j]] > 0 { 1 } else { 0 }
                        + if pos_diagonal[n - 1 + j - columns[i]] > 0 { 1 } else { 0 }
                        + if pos_diagonal[n - 1 + i - columns[j]] > 0 { 1 } else { 0 }
                        - if neg_diagonal[i + columns[i]] > 1 { 1 } else { 0 }
                        - if neg_diagonal[j + columns[j]] > 1 { 1 } else { 0 }
                        - if pos_diagonal[n - 1 + i - columns[i]] > 1 { 1 } else { 0 }
                        - if pos_diagonal[n - 1 + j - columns[j]] > 1 { 1 } else { 0 };
                    if col_diff < 0 {
                        swaps_performed += swaps_performed;
                        neg_diagonal[i + columns[i]] -= 1;
                        neg_diagonal[j + columns[j]] -= 1;
                        pos_diagonal[n - 1 + i - columns[i]] -= 1;
                        pos_diagonal[n - 1 + j - columns[j]] -= 1;

                        let temp = columns[i];
                        columns[i] = columns[j];
                        columns[j] = temp;

                        neg_diagonal[i + columns[i]] += 1;
                        neg_diagonal[j + columns[j]] += 1;
                        pos_diagonal[n - 1 + i - columns[i]] += 1;
                        pos_diagonal[n - 1 + j - columns[j]] += 1;
                    }
                }
            }
            if swaps_performed == 0 {
                break;
            }
        }
    }
}
                                   
###########################
use rand::seq::SliceRandom;
use rand::thread_rng;
use std::collections::HashSet;
use std::fmt::{Display, Formatter, Write};

type Position = (isize, isize);

#[derive(Clone)]
struct Board {
    n: isize,
    mandatory_queen: Position,
    queens: HashSet<Position>,
    square_threats: Vec<isize>,
}

impl Board {
    pub fn new(n: usize, mandatory_queen: Position) -> Self {
        let mut board = Board {
            n: n as isize,
            square_threats: vec![0; n * n],
            mandatory_queen,
            queens: HashSet::new(),
        };

        board.set_queen(&mandatory_queen, true);

        board
    }

    pub fn solve(&mut self) {
        while !self.is_solved() {
            self.improve();
        }
    }

    pub fn is_solved(&self) -> bool {
        for queen in self.queens.iter() {
            if self.square_threats[Board::index(self.n, queen)] > 1 {
                return false;
            }
        }

        true
    }

    pub fn is_solvable(&self) -> bool {
        if self.n < 2 {
            return true;
        }

        if self.n == 2 || self.n == 3 {
            return false;
        }

        let mandatory_queen = self.queens.iter().next().unwrap();

        if mandatory_queen.0 == mandatory_queen.1 {
            return false;
        }

        true
    }

    pub fn improve(&mut self) {
        let mut worst_threat = 0;
        let mut worst_queens = vec![];

        for queen in self
            .queens
            .iter()
            .filter(|&queen| queen != &self.mandatory_queen)
            .cloned()
        {
            let threats = self.square_threats[Board::index(self.n, &queen)];
            if threats > worst_threat {
                worst_threat = threats;
                worst_queens.clear();
            }

            if threats >= worst_threat {
                worst_queens.push(queen);
            }
        }

        worst_queens.shuffle(&mut thread_rng());
        let worst_queen = worst_queens[0];

        self.set_queen(&worst_queen, false);

        let mut best_rows = vec![];
        let mut lowest_threat = isize::MAX;

        for row in 0..self.n {
            let threats = self.square_threats[Board::index(self.n, &(worst_queen.0, row))];

            if threats < lowest_threat {
                lowest_threat = threats;
                best_rows.clear();
            }

            if threats <= lowest_threat {
                best_rows.push(row);
            }
        }

        best_rows.shuffle(&mut thread_rng());
        let best_row = best_rows[0];

        self.set_queen(&(worst_queen.0, best_row), true);
    }

    pub fn set_queen(&mut self, position: &Position, is_placed: bool) {
        if is_placed {
            self.queens.insert(*position);
        } else {
            self.queens.remove(position);
        }

        let threat = if is_placed { 1 } else { -1 };

        let square_threats = &mut self.square_threats;

        let threat_before = square_threats[Board::index(self.n, position)];

        for x in 0..self.n {
            square_threats[Board::index(self.n, &(x, position.1))] += threat;
        }

        for y in 0..self.n {
            square_threats[Board::index(self.n, &(position.0, y))] += threat;
        }

        let is_valid = |n: isize, p: &Position| p.0 >= 0 && p.1 >= 0 && p.0 < n && p.1 < n;

        for d in 1..self.n {
            let a = &(position.0 - d, position.1 - d);
            let b = &(position.0 - d, position.1 + d);
            let c = &(position.0 + d, position.1 - d);
            let d = &(position.0 + d, position.1 + d);

            for square in [a, b, c, d] {
                if is_valid(self.n, square) {
                    square_threats[Board::index(self.n, square)] += threat;
                }
            }
        }

        square_threats[Board::index(self.n, position)] = threat_before + threat;
    }

    pub fn place_initial_queens(&mut self) {
        let initial_queen_pos = *self.queens.iter().next().unwrap();

        let mut rows = (0..self.n).filter(|&n| n != initial_queen_pos.1).collect::<Vec<_>>();
        rows.shuffle(&mut thread_rng());
        let mut rows = rows.into_iter();

        for col in (0..self.n).filter(|&n| n != initial_queen_pos.0) {
            self.set_queen(&(col, rows.next().unwrap()), true);
        }
    }

    fn index(n: isize, position: &Position) -> usize {
        (position.1 * n + position.0) as usize
    }
}

impl Display for Board {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        for y in 0..self.n {
            for x in 0..self.n {
                match self.queens.get(&(x, y)) {
                    None => f.write_char('.').unwrap(),
                    Some(_) => f.write_char('Q').unwrap(),
                }
            }
            f.write_char('\n').unwrap();
        }
        Ok(())
    }
}

pub fn solve_n_queens(n: usize, mandatory_coords: (usize, usize)) -> Option<String> {
    let mut board = Board::new(n, (mandatory_coords.0 as isize, mandatory_coords.1 as isize));

    if !board.is_solvable() {
        return None;
    }

    board.place_initial_queens();
    board.solve();

    Some(board.to_string())
}
                      
###############################
use rand::seq::SliceRandom;
use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashSet};
use std::convert::TryFrom;
use std::fmt::{Display, Formatter};

//--------------------------------------------------------------------------------------
//--Structs that make up a Space on the game board, and their methods and traits
//--------------------------------------------------------------------------------------

/// Indicates whether a Space is Empty or contains a Queen
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum SpaceKind {
    Empty,
    Queen,
}


/// Used to keep track of the "threat" on a particular space. The "threat" is the 
/// number of different directions from which that space can be attacked.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Threat {
    row: usize,
    diag_up: usize,
    diag_down: usize,
}

impl Threat {
    fn new() -> Self {
        Threat { row: 0, diag_up: 0, diag_down: 0 }
    }
}

impl From<Threat> for usize {
    fn from(threat: Threat) -> usize {
        let mut value = 0;
        if threat.row > 0 { value += 1; }
        if threat.diag_up > 0 { value += 1; }
        if threat.diag_down > 0 { value += 1; }
        value
    }
}

impl PartialOrd for Threat {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Threat {
    fn cmp(&self, other: &Self) -> Ordering {
        let own_threat = usize::from(*self);
        let other_threat = usize::from(*other);
        own_threat.cmp(&other_threat)
    }
}


/// Used to indicate from which direction a Space is receiving Threat.
#[derive(Clone, Copy, Debug)]
enum Direction {
    Row,
    DiagUp,
    DiagDown,
}


/// Represents a Space on the game Board. A Space has a kind (Empty or Queen), knows
/// it's location (Coordinate), and from how many directions it is currently 
/// threatend by Queen spaces.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Space {
    kind: SpaceKind,
    coordinate: Coordinate,
    threat: Threat,
}

impl Space {
    /// Returns an iterator over all the Coordinates potentially threatened by this
    /// Space, along with the direction of the threat. Obviously this is meaningless for
    /// Empty spaces, but is used on Empty spaces that are being prepared to have a 
    /// Queen placed there.
    fn threatened(&self, bc: BoundedCoordinate) -> impl Iterator<Item=(Coordinate, Direction)> {
        let BoundedCoordinate { coordinate, .. } = bc;
        let row_iter = bc.row_iter().map(|c| (c, Direction::Row));
        let diag_up_iter = bc.diag_up_iter().map(|c| (c, Direction::DiagUp));
        let diag_down_iter = bc.diag_down_iter().map(|c| (c, Direction::DiagDown));
        row_iter
            .chain(diag_up_iter)
            .chain(diag_down_iter)
            .filter(move |c| c.0 != coordinate)
    }

    fn incr_threat(&mut self, direction: Direction) {
        match direction {
            Direction::Row => self.threat.row += 1,
            Direction::DiagUp => self.threat.diag_up += 1,
            Direction::DiagDown => self.threat.diag_down += 1,
        }
    }

    fn decr_threat(&mut self, direction: Direction) {
        match direction {
            Direction::Row => self.threat.row = self.threat.row.saturating_sub(1),
            Direction::DiagUp => self.threat.diag_up = self.threat.diag_up.saturating_sub(1),
            Direction::DiagDown => self.threat.diag_down = self.threat.diag_down.saturating_sub(1),
        }
    }
}

impl PartialOrd for Space {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

/// Sort Space in reverse threat order, to allow choosing the minimum threat
/// Space from a BinaryHeap
impl Ord for Space {
    fn cmp(&self, other: &Self) -> Ordering {
        let own_threat = usize::from(self.threat);
        let other_threat = usize::from(other.threat);
        match own_threat.cmp(&other_threat) {
            Ordering::Greater => Ordering::Less,
            Ordering::Less => Ordering::Greater,
            Ordering::Equal => Ordering::Equal,
        }
    }
}

//--------------------------------------------------------------------------------------
//--Iterators over board Spaces that share a row, column, or diagonal with
//--an indicated space. Note that this *includes* the indicated space.
//--------------------------------------------------------------------------------------

/// Iterator over the Coordinates in a row
struct RowIter {
    current: Option<Coordinate>,
    bounds: usize,
}

impl From<BoundedCoordinate> for RowIter {
    fn from(value: BoundedCoordinate) -> Self {
        let BoundedCoordinate { coordinate, bounds } = value;
        let Coordinate { row, .. } = coordinate;
        let first_coord = Coordinate::from((row, 0));
        Self {
            current: Some(first_coord),
            bounds,
        }
    }
}

impl Iterator for RowIter {
    type Item = Coordinate;

    fn next(&mut self) -> Option<Self::Item> {
        let result = self.current;
        if let Some(Coordinate { row, col }) = self.current {
            self.current = if col < self.bounds - 1 {
                Some(Coordinate::from((row, col + 1)))
            } else {
                None
            }
        }
        result
    }
}


/// Iterator over the Coordinates in a Column
struct ColIter {
    current: Option<Coordinate>,
    bounds: usize,
}

impl From<BoundedCoordinate> for ColIter {
    fn from(value: BoundedCoordinate) -> Self {
        let BoundedCoordinate { coordinate, bounds } = value;
        let Coordinate { col, .. } = coordinate;
        let first_coord = Coordinate::from((0, col));
        Self {
            current: Some(first_coord),
            bounds,
        }
    }
}

impl Iterator for ColIter {
    type Item = Coordinate;

    fn next(&mut self) -> Option<Self::Item> {
        let result = self.current;
        if let Some(Coordinate { row, col }) = self.current {
            self.current = if row < self.bounds - 1 {
                Some(Coordinate::from((row + 1, col)))
            } else {
                None
            }
        }
        result
    }
}


/// Iterator over the Coordinates in an upward diagonal line
struct DiagUpIter {
    current: Option<Coordinate>,
    bounds: usize,
}

impl From<BoundedCoordinate> for DiagUpIter {
    fn from(value: BoundedCoordinate) -> Self {
        let BoundedCoordinate { coordinate, bounds } = value;
        let Coordinate { row, col } = coordinate;

        // Get the coordinate of the bottom-left space in the upward
        // diagonal containing the space given.
        let first_row = std::cmp::min(bounds - 1, row + col);
        let first_col = col - (first_row - row);
        let first_coord = Coordinate::from((first_row, first_col));
        Self {
            current: Some(first_coord),
            bounds,
        }
    }
}

impl Iterator for DiagUpIter {
    type Item = Coordinate;

    fn next(&mut self) -> Option<Self::Item> {
        let result = self.current;
        if let Some(Coordinate { row, col }) = self.current {
            self.current = if row >= 1 && col < self.bounds - 1 {
                Some(Coordinate::from((row - 1, col + 1)))
            } else {
                None
            }
        }
        result
    }
}


/// Iterator over the Coordinates in a downard diagonal line
struct DiagDownIter {
    current: Option<Coordinate>,
    bounds: usize,
}

impl From<BoundedCoordinate> for DiagDownIter {
    fn from(value: BoundedCoordinate) -> Self {
        let BoundedCoordinate { coordinate, bounds } = value;
        let Coordinate { row, col } = coordinate;

        // Get the coordinate of the top-left space in the downward
        // diagonal containing the space given.
        let min_dim = std::cmp::min(row, col);
        let first_row = row - min_dim;
        let first_col = col - min_dim;
        let first_coord = Coordinate::from((first_row, first_col));
        Self {
            current: Some(first_coord),
            bounds,
        }
    }
}

impl Iterator for DiagDownIter {
    type Item = Coordinate;

    fn next(&mut self) -> Option<Self::Item> {
        let result = self.current;
        if let Some(Coordinate { row, col }) = self.current {
            self.current = if row < self.bounds - 1 && col < self.bounds - 1 {
                Some(Coordinate::from((row + 1, col + 1)))
            } else {
                None
            }
        }
        result
    }
}

//--------------------------------------------------------------------------------------
//--A Coordinate can be used to index a space on the game Board.
//--A BoundedCoordinate is a Coordinate that has been checked to ensure it is valid
//--for a board of given size.
//--------------------------------------------------------------------------------------

#[derive(Clone, Copy, Debug, Hash, PartialEq, Eq)]
struct Coordinate {
    row: usize,
    col: usize,
}

impl From<(usize, usize)> for Coordinate {
    fn from(value: (usize, usize)) -> Self {
        let (row, col) = value;
        Self { row, col }
    }
}

/// Represents a coordinate on a square grid of size given by `bounds`
#[derive(Clone, Copy)]
struct BoundedCoordinate {
    coordinate: Coordinate,
    bounds: usize,
}

impl TryFrom<(Coordinate, usize)> for BoundedCoordinate {
    type Error = &'static str;

    fn try_from(value: (Coordinate, usize)) -> Result<Self, Self::Error> {
        let (coordinate, bounds) = value;
        let Coordinate { row, col } = coordinate;
        if row >= bounds || col >= bounds {
            return Err("Coordinate out of bounds");
        }
        Ok(BoundedCoordinate { coordinate, bounds })
    }
}

impl BoundedCoordinate {
    fn row_iter(&self) -> RowIter {
        RowIter::from(*self)
    }

    fn col_iter(&self) -> ColIter {
        ColIter::from(*self)
    }

    fn diag_up_iter(&self) -> DiagUpIter {
        DiagUpIter::from(*self)
    }

    fn diag_down_iter(&self) -> DiagDownIter {
        DiagDownIter::from(*self)
    }
}

//--------------------------------------------------------------------------------------
//--The Game Board and it's associated behaviors
//--------------------------------------------------------------------------------------

struct Board {
    size: usize,
    fixed: Coordinate,
    spaces: Vec<Vec<Space>>,
    queens: HashSet<Coordinate>,
}

impl Display for Board {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        for row in self.spaces.iter() {
            for value in row.iter() {
                match value.kind {
                    SpaceKind::Queen => write!(f, "Q")?,
                    SpaceKind::Empty => write!(f, ".")?,
                }
            }
            writeln!(f)?;
        }
        Ok(())
    }
}

impl Board {
    fn new_seeded(size: usize, fixed: Coordinate) -> Self {
        let mut spaces = Vec::with_capacity(size);
        for row_idx in 0..size {
            let mut row = Vec::with_capacity(size);
            for col_idx in 0..size {
                let coordinate = Coordinate::from((row_idx, col_idx));
                let kind = SpaceKind::Empty;
                let space = Space { kind, coordinate, threat: Threat::new() };
                row.push(space);
            }
            spaces.push(row);
        }
        let queens = HashSet::with_capacity(size);
        let mut new_board = Board { size, fixed, spaces, queens };
        new_board.seed().unwrap();
        new_board
    }

    fn get_space_unchecked(&self, coord: Coordinate) -> &Space {
        let Coordinate { row, col } = coord;
        &self.spaces[row][col]
    }

    fn get_space_mut_unchecked(&mut self, coord: Coordinate) -> &mut Space {
        let Coordinate { row, col } = coord;
        &mut self.spaces[row][col]
    }

    fn seed(&mut self) -> Result<(), &'static str> {
        // Add a Queen to the 'fixed' Coordinate first, then remove it from the
        // list of Queens so that it will never be chosen to be randomly moved
        self.add_queen_to_coordinate(self.fixed)?;
        self.queens.remove(&self.fixed);


        // Add a Queen to every other column, randomly
        let fixed_col = self.fixed.col;
        let mut columns: Vec<_> = (0..self.size).filter(|x| *x != fixed_col).collect();
        let mut rng = rand::thread_rng();
        columns.shuffle(&mut rng);
        columns.iter().try_for_each(|col| self.add_queen_to_column(*col))
    }

    fn is_solved(&self) -> bool {
        for queen_coord in self.queens.iter() {
            let queen = self.get_space_unchecked(*queen_coord);
            if usize::from(queen.threat) > 0 { return false; }
        }
        true
    }

    fn move_random_queen(&mut self) -> Result<(), &'static str> {
        let mut rng = rand::thread_rng();
        let mut queen_coords = self.queens.iter().copied().collect::<Vec<_>>();
        queen_coords.shuffle(&mut rng);

        for coord in queen_coords {
            let queen_space = self.get_space_unchecked(coord);
            if usize::from(queen_space.threat) == 0 { continue; }
            if let Ok(bc) = BoundedCoordinate::try_from((coord, self.size)) {
                // Working Theory: collecting spaces to the BinaryHeap directly is
                // too deterministic, and can lead to getting "stuck" in the same 
                // local minimum multiple times for the same board configuration.
                // Randomly shuffling the spaces before adding them to the BinaryHeap
                // seems to help with this.
                let mut col_spaces: Vec<_> = bc.col_iter()
                    .filter(|c| c.row != coord.row)
                    .map(|c| *self.get_space_unchecked(c))
                    .collect();
                col_spaces.shuffle(&mut rng);
                let mut heap = BinaryHeap::from(col_spaces);
                let min_threat_space = heap.pop().unwrap();
                if min_threat_space.threat <= queen_space.threat {
                    self.move_queen(coord, min_threat_space.coordinate)?;
                    return Ok(());
                }   
            }
        }
        Err("All Queens at local minimum")
    }

    fn add_queen_to_column(&mut self, col: usize) -> Result<(), &'static str> {
        let col_coord = Coordinate::from((0, col));
        let bc = BoundedCoordinate::try_from((col_coord, self.size))?;
        let mut heap: BinaryHeap<_> = bc.col_iter()
            .map(|c| *self.get_space_unchecked(c))
            .collect();
        if let Some(space) = heap.pop() {
            self.add_queen_to_coordinate(space.coordinate)?;
            self.queens.insert(space.coordinate);
            return Ok(());
        }
        Err("Could not add Queen to column")
    }

    fn move_queen(&mut self, from: Coordinate, to: Coordinate) -> Result<(), &'static str> {
        self.add_queen_to_coordinate(to)?;
        self.remove_queen_from_coordinate(from)
    }

    fn add_queen_to_coordinate(&mut self, coordinate: Coordinate) -> Result<(), &'static str> {
        let bc = BoundedCoordinate::try_from((coordinate, self.size))?;
        let start_space = self.get_space_unchecked(coordinate);
        match start_space.kind {
            SpaceKind::Queen{..} => Err("Can't add a queen to an occupied space"),
            SpaceKind::Empty => {
                let mut threat = Threat::new();

                for (threatened_coord, direction) in start_space.threatened(bc) {
                    // Increase the threat count of all spaces covered by the
                    // iterators. If the threatened space is a Queen, it will in turn
                    // threaten the Queen being added.
                    let threatened_space = self.get_space_mut_unchecked(threatened_coord);
                    threatened_space.incr_threat(direction);
                    if threatened_space.kind == SpaceKind::Queen { 
                        match direction {
                            Direction::Row => threat.row += 1,
                            Direction::DiagUp => threat.diag_up += 1,
                            Direction::DiagDown => threat.diag_down += 1,
                        }
                    }                       
                }

                let Coordinate { row, col } = coordinate;
                let new_queen = Space { kind: SpaceKind::Queen, coordinate, threat };
                self.spaces[row][col] = new_queen;
                self.queens.insert(coordinate);
                Ok(())
            }
        }
    }

    fn remove_queen_from_coordinate(&mut self, coordinate: Coordinate) -> Result<(), &'static str> {
        let bc = BoundedCoordinate::try_from((coordinate, self.size))?;
        let start_space = self.get_space_unchecked(coordinate);
        match start_space.kind {
            SpaceKind::Empty => Err("Can't remove an empty space"),
            SpaceKind::Queen {..} => {
                let mut threat = Threat::new();

                for (threatened_coord, direction) in start_space.threatened(bc) {
                    // Decrease the threat count of all spaces covered by the
                    // iterators. If the threatened space is a Queen, it will
                    // threaten the Empty space being left behind.
                    let threatened_space = self.get_space_mut_unchecked(threatened_coord);
                    threatened_space.decr_threat(direction);
                    if threatened_space.kind == SpaceKind::Queen {
                        match direction {
                            Direction::Row => threat.row += 1,
                            Direction::DiagUp => threat.diag_up += 1,
                            Direction::DiagDown => threat.diag_down += 1,
                        }
                    }                       
                }

                // After removing this Queen's 'threat' from all other spaces, remove
                // the Queen. Leave behind an empty space with the threat provided by
                // all the Queens we found along the way.
                let Coordinate { row, col } = coordinate;
                let new_space = Space { kind: SpaceKind::Empty, coordinate, threat };
                self.spaces[row][col] = new_space;
                self.queens.remove(&coordinate);
                Ok(())
            }
        }
    }
}

/// Multithreading here gives much more consistent performance on large Boards. There
/// are definitely other performance improvements that could be made, but this one
/// decreases run time range from 0.5s -> 7s+ to a consistent ~1s on boards of 
/// ~750 rows with a `max_attempts` of 10. Decreasing `max_attempts` also seems to 
/// decrease run time, although it is not clear to me why that should be, unless
/// most of the time is spent on generating the handles to the threads.
pub fn solve_n_queens(n: usize, mandatory_coords: (usize, usize)) -> Option<String> {
    let max_attempts = 8;
    let max_queen_moves_per_attempt = 100;
    let (col, row) = mandatory_coords;
    let mut handles = Vec::new();

    for _ in 0..max_attempts {
        let handle = std::thread::spawn(move || {
            let mut test_board = Board::new_seeded(n, Coordinate::from((row, col)));
            for _ in 0..max_queen_moves_per_attempt {
                if test_board.is_solved() { return Some(test_board.to_string()) };
                if test_board.move_random_queen().is_err() { break; }
            } 
            None
        });
        handles.push(handle);
    }

    for handle in handles {
        if let Ok(result) = handle.join() {
            if result.is_some() { return result; }
        }
    }
    None
}   
