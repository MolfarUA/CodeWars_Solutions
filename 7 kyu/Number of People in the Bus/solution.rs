fn number(bus_stops:&[(i32,i32)]) -> i32 {
    bus_stops.iter().fold(0,|acc,x| acc + x.0 - x.1)
}
_____________________________________
fn number(bus_stops: &[(i32, i32)]) -> i32 {
    bus_stops.iter().fold(0, |acc, &(entered, exited)| {
        acc + entered - exited
    })
}
_____________________________________
fn number(bus_stops:&[(i32,i32)]) -> i32 {
    bus_stops
        .into_iter()
        .map(|n| n.0 - n.1)
        .sum()
}
_____________________________________
fn number(bus_stops:&[(i32,i32)]) -> i32 {
    let mut number: i32 = 0;
    
    for &(i,o) in bus_stops {
        number += i;
        number -= o;
    }
    number
}
_____________________________________
fn number(bus_stops:&[(i32,i32)]) -> i32 {
    let mut total = 0;
    for (a,b) in bus_stops.iter() {
        total += a;
        total -= b;
    }
    total
}
