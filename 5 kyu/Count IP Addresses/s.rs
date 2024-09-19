use std::net::Ipv4Addr;

fn ips_between(start: &str, end: &str) -> u32 {
    let start: u32 = start.parse::<Ipv4Addr>().unwrap().into();
    let end: u32 = end.parse::<Ipv4Addr>().unwrap().into();
    end - start
}
____________________
use core::iter;
//4294967296
const POWER_256: [u64; 4] = [16777216, 65536, 256, 1];

fn ips_between(start: &str, end: &str) -> u32 {
    let start: Vec<u32> = start.split(".").map(|x| x.parse::<u32>().unwrap()).collect();
    let end: Vec<u32> = end.split(".").map(|x| x.parse::<u32>().unwrap()).collect();

    let start_int = {
        let mut s: u64 = 0;
        for (v, n) in iter::zip(start, POWER_256) {
            s += v as u64 * n;
        }
        s
    };
    let end_int = {
        let mut s: u64 = 0;
        for (v, n) in iter::zip(end, POWER_256) {
            s += v as u64 * n;
        }
        s
    };
    return (end_int - start_int) as u32
}
________________
fn split_ip_address(ip: &str) -> Vec<i64> {
    ip.split('.').rev()
        .enumerate()
        .map(|(i, s)| {
            s.parse::<i64>().unwrap() * 256i64.pow(i as u32)
        }).collect::<Vec<i64>>()
}

fn ips_between(start: &str, end: &str) -> u32 {
    let ip_1 = split_ip_address(start);
    let ip_2 = split_ip_address(end);
    let result = ip_2.iter().zip(ip_1).map(|(&i2, i1)| { i2 - i1 }).sum::<i64>();
    result as u32
}
__________________________
use std::{net::Ipv4Addr, str::FromStr};

fn convert(addr: &str) -> u32 {
    Ipv4Addr::from_str(addr).unwrap().into()
}

fn ips_between(start: &str, end: &str) -> u32 {
    let starting = convert(start);
    let ending   = convert(end);
    ending - starting
}
