5a479247e6be385a41000064


#[derive(Clone, Copy)]
enum Cell {
    Certain(bool),
    Uncertain,
}
const N: usize = 5;
type Board<const N: usize> = [[Cell; N]; N];

fn solve_nonogram<const N: usize>(
    (top_clues, left_clues): ([&[u8]; N], [&[u8]; N]),
) -> [[u8; N]; N] {
    let mut board = [[Cell::Uncertain; N]; N];
    f(&top_clues, &left_clues, &mut board, 0);
    let mut result = [[0; N]; N];
    for (i, row) in board.iter().enumerate() {
        for (j, c) in row.iter().enumerate() {
            result[i][j] = matches!(c, Cell::Certain(true)) as u8;
        }
    }
    result
}

fn f<const N: usize>(
    top_clues: &[&[u8]],
    left_clues: &[&[u8]],
    board: &mut Board<N>,
    n: usize,
) -> bool {
    if n == N * N {
        return true;
    }
    let r = n / N;
    let c = n % N;
    if matches!(board[r][c], Cell::Certain(_)) {
        return f(top_clues, left_clues, board, n + 1);
    }
    for yn in [true, false] {
        board[r][c] = Cell::Certain(yn);
        if match_clue(board, 0, c, 1, 0, top_clues[c])
            && match_clue(board, r, 0, 0, 1, left_clues[r])
            && f(top_clues, left_clues, board, n + 1)
        {
            return true;
        }
        board[r][c] = Cell::Uncertain;
    }
    false
}

fn match_clue<const N: usize>(
    board: &Board<N>,
    r: usize,
    c: usize,
    dr: usize,
    dc: usize,
    clue: &[u8],
) -> bool {
    let mut continuous = 0;
    let mut result = vec![];
    for delta in 0..N {
        match board[r + dr * delta][c + dc * delta] {
            Cell::Certain(true) => continuous += 1,
            Cell::Certain(false) => {
                if continuous > 0 {
                    result.push(continuous);
                    continuous = 0;
                }
            }
            Cell::Uncertain => return true,
        }
    }
    if continuous > 0 {
        result.push(continuous);
    }
    result == clue
}
__________________________
use itertools::Itertools;
use std::convert::TryInto;

fn solve_nonogram(
    (top_clues, left_clues): ([&[u8]; 5], [&[u8]; 5]),
) -> [[u8; 5]; 5] {
    let find_permutations = |clues: [&[u8]; 5]| {
        clues
            .iter()
            .flat_map(|clue| CLUE_PERMUTATIONS.iter().find(|(c, _)| c == clue))
            .map(|(_, ps)| *ps)
            .collect::<Vec<&[[u8; 5]]>>()
    };
    let row_permutations = find_permutations(left_clues);
    let col_permutations = find_permutations(top_clues);
    for perm in row_permutations.into_iter().multi_cartesian_product() {
        let col = || Vec::with_capacity(5);
        let mut columns = [col(), col(), col(), col(), col()];
        for row in &perm {
            for i in 0..5 {
                columns[i].push(row[i]);
            }
        }
        let ok = (0..5).all(|i| {
            col_permutations[i]
                .iter()
                .find(|p| p[..] == columns[i][..])
                .is_some()
        });
        if ok {
            return perm
                .into_iter()
                .copied()
                .collect::<Vec<[u8; 5]>>()
                .try_into()
                .unwrap();
        }
    }
    panic!("No solution found")
}

const CLUE_PERMUTATIONS: [(&[u8], &[[u8; 5]]); 14] = [
    (&[], &[[0, 0, 0, 0, 0]]),
    (
        &[1],
        &[
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
        ],
    ),
    (
        &[1, 1],
        &[
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0],
            [0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1],
        ],
    ),
    (&[1, 1], &[[1, 0, 1, 0, 1]]),
    (
        &[2],
        &[
            [1, 1, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 1, 1],
        ],
    ),
    (&[1, 1, 1], &[[1, 0, 1, 0, 1]]),
    (
        &[2, 1],
        &[[1, 1, 0, 1, 0], [1, 1, 0, 0, 1], [0, 1, 1, 0, 1]],
    ),
    (
        &[1, 2],
        &[[1, 0, 1, 1, 0], [1, 0, 0, 1, 1], [0, 1, 0, 1, 1]],
    ),
    (&[3], &[[1, 1, 1, 0, 0], [0, 1, 1, 1, 0], [0, 0, 1, 1, 1]]),
    (&[3, 1], &[[1, 1, 1, 0, 1]]),
    (&[1, 3], &[[1, 0, 1, 1, 1]]),
    (&[2, 2], &[[1, 1, 0, 1, 1]]),
    (&[4], &[[1, 1, 1, 1, 0], [0, 1, 1, 1, 1]]),
    (&[5], &[[1, 1, 1, 1, 1]]),
];
__________________________
use std::convert::TryInto;

fn solve_nonogram((top_clues, left_clues): ([&[u8]; 5], [&[u8]; 5])) -> [[u8; 5]; 5] {
    for &a in get_comb(left_clues[0]) {
    for &b in get_comb(left_clues[1]) {
    for &c in get_comb(left_clues[2]) {
    for &d in get_comb(left_clues[3]) {
    for &e in get_comb(left_clues[4]) {
        let test = [a, b, c, d, e];
        if transpose(test).iter().zip(top_clues.iter()).all(|(&t, &c)| get_clue(t) == c) {
            return test.iter()
                .map(|r| [r & 1, r >> 1 & 1, r >> 2 & 1, r >> 3 & 1, r >> 4 & 1])
                .collect::<Vec<_>>().try_into().unwrap();            
        }
    }
    }
    }
    }
    }
    return [[0; 5]; 5];
}

fn transpose(from: [u8; 5]) -> [u8; 5] {
    let mut to = [0; 5];
    for (n, f) in from.iter().enumerate() {
        for (i, t) in to.iter_mut().enumerate() {
            *t |= (f >> i & 1) << n;
        }
    }
    to
}

fn get_comb(clues: &[u8]) -> &'static [u8] {
    match clues {
        &[] => &[0],
        &[1] => &[1, 2, 4, 8, 16],
        &[1,1] => &[5, 9, 10, 17, 18, 20],
        &[1,1,1] => &[21],
        &[1,2] => &[13, 25, 26],
        &[1,3] => &[29],
        &[2] => &[3, 6, 12, 24],
        &[2,1] => &[11, 19, 22],
        &[2,2] => &[27],
        &[3] => &[7, 14, 28],
        &[3,1] => &[23],
        &[4] => &[15, 30],
        &[5] => &[31],
        _ => panic!("{:?}", clues),
    }
}

fn get_clue(comb: u8) -> &'static [u8] {
    match comb {
        0 => &[],
        1 | 2 | 4 | 8 | 16 => &[1],
        5 | 9 | 10 | 17 | 18 | 20 => &[1, 1],
        21 => &[1, 1, 1],
        13 | 25 | 26 => &[1, 2],
        29 => &[1,3],
        3 | 6 | 12 | 24 => &[2],
        11 | 19 | 22 => &[2, 1],
        27 => &[2,2],
        7 | 14 | 28 => &[3],
        23 => &[3,1],
        15 | 30 => &[4],
        31 => &[5],
        _ => panic!("{:?}", comb),
    }
}
