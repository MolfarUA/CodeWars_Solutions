59aac7a9485a4dd82e00003e


fn cockroaches(sroom: &[&str]) -> [u32; 10] {
    
    let mut r = [0; 10];
    let (h, w) = (sroom.len() as i32, sroom[0].len() as i32);
    let mut room:Vec<Vec<_>> = sroom.iter().map(|s| s.chars().collect()).collect();
    let (mut y0, mut x0, mut y, mut x, mut dy, mut dx, mut p) = (-1i32, -1i32, 0i32, 0i32, 0i32, 1i32, '\0');
    let d = |c| (c as u8 - 48) as usize;
    
    loop {
        if (x+1==w && dx>0) || (x==0 && dx<0) || (y+1==h && dy>0) || (y==0 && dy<0) { (dy, dx) = (dx, -dy); }
        if room[y as usize][x as usize].is_digit(10) {
            p = room[y as usize][x as usize];
            if y0 == -1 { (y0, x0) = (y, x); } else if y0==y && x0==x { break; }
        } else if p != '\0' { room[y as usize][x as usize] = p; }
        (y, x) = (y + dy, x + dx);
    }
    
    for y in 0..h {
        for x in 0..w {
            match room[y as usize][x as usize] {
                'U' => r[d(room[0][x as usize])] += 1,
                'D' => r[d(room[(h-1) as usize][x as usize])] += 1,
                'R' => r[d(room[y as usize][(w-1) as usize])] += 1,
                'L' => r[d(room[y as usize][0])] += 1,
                _ => ()
            }
        }
    }
    
    r
}
________________________________
fn cockroaches(room: &[&str]) -> [u32; 10] {
    let mut xs = [0,0,0,0,0,0,0,0,0,0];
    let l = room.len();
    let m = room[0].len();
    let r:Vec<Vec<_>> = room.iter().map(|x| x.chars().collect()).collect();
    let c: Vec<char> =
    room.first().unwrap().chars().rev()
    .chain(
        room.iter().map(|x| x.chars().next().unwrap())
    )
    .chain(
        room.last().unwrap().chars()
    )
    .chain(
        room.iter().rev().map(|x| x.chars().last().unwrap())
    )
    .collect();
    let f = |k:char| k.is_digit(10);
    let u = |i| (*c[i..].iter().find(|k| f(**k)).unwrap_or(c.iter().find(|k| f(**k)).unwrap()) as u8 - 48) as usize;
    for (i, j) in itertools::iproduct!(1..m-1, 1..l-1) {
        match r[j][i] {
            'U' => xs[u(m - i - 1)] += 1,
            'L' => xs[u(m + j)] += 1,
            'D' => xs[u(m + l + i)] += 1,
            'R' => xs[u(2 * (l + m) - j - 1)] += 1,
            _ => ()
        }
    }
    xs
}
________________________________
fn cockroaches(room: &[&str]) -> [u32; 10] {
    let mut xs = [0,0,0,0,0,0,0,0,0,0];
    let l = room.len();
    let m = room[0].len();
    let r:Vec<Vec<_>> = room.iter().map(|x| x.chars().collect()).collect();
    let mut c: Vec<char> =
    room.first().unwrap().chars().rev()
    .chain(
        room.iter().map(|x| x.chars().next().unwrap())
    )
    .chain(
        room.last().unwrap().chars()
    )
    .chain(
        room.iter().rev().map(|x| x.chars().last().unwrap())
    )
    .collect();
    c.extend(c.clone().iter());
    let u = |i| (c[i..].iter().find(|k| k.is_digit(10)).unwrap().clone() as u8 - 48) as usize;
    for (i, j) in itertools::iproduct!(1..m-1, 1..l-1) {
        match r[j][i] {
            'U' => xs[u(m - i - 1)] += 1,
            'L' => xs[u(m + j)] += 1,
            'D' => xs[u(m + l + i)] += 1,
            'R' => xs[u(2 * (l + m) - j - 1)] += 1,
            _ => ()
        }
    }
    xs
}
