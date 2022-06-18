59568be9cc15b57637000054

use num::{BigInt, Signed, ToPrimitive};
use std::ops::BitXor;

fn elder_age(m: u64, n: u64, l: u64, t: u64) -> u64 {
    let sum = elder_age_remaining(
        &BigInt::from(m),
        &BigInt::from(n),
        &BigInt::from(l),
        &BigInt::from(0),
        &BigInt::from(0),
    );

    sum_with_overflow(&sum, &BigInt::from(t))
}

fn elder_age_remaining(m: &BigInt, n: &BigInt, l: &BigInt, offset_m: &BigInt, offset_n: &BigInt) -> BigInt {
    if m == &BigInt::from(0) || n == &BigInt::from(0) {
        return BigInt::from(0);
    }

    if m == &BigInt::from(1) && n == &BigInt::from(1) {
        return (offset_m.bitxor(offset_n) - l).max(BigInt::from(0));
    }

    if n > m {
        return elder_age_remaining(n, m, l, offset_n, offset_m);
    }

    let pow_m = &max_pow2_lt_x(m);
    let pow_n = &max_pow2_lt_x(n);

    if pow_m >= n {
        return elder_age_pow2(pow_m, n, l, offset_m, offset_n)
            + elder_age_remaining(&(m - pow_m), n, l, &(offset_m + pow_m), offset_n);
    }

    elder_age_pow2(pow_m, pow_n, l, offset_m, offset_n)
        + elder_age_pow2(pow_m, &(n - pow_n), l, offset_m, &(offset_n + pow_n))
        + elder_age_remaining(&(m - pow_m), n, l, &(offset_m + pow_m), offset_n)
}

fn max_pow2_lt_x(x: &BigInt) -> BigInt {
    BigInt::from(2).pow((x.to_f64().unwrap()).log2().floor() as u32)
}

fn elder_age_pow2(m: &BigInt, n: &BigInt, l: &BigInt, offset_m: &BigInt, offset_n: &BigInt) -> BigInt {
    if n > m {
        return elder_age_pow2(n, m, l, offset_n, offset_m);
    }

    let mut start = offset_m.bitxor(offset_n) - l;
    let shift = (offset_m - offset_n) % m;
    
    start -= shift;
    let end = &start + m - BigInt::from(1);

    let row_sum = gauss_sum_range(&start, &end);
    let result = row_sum * n;

    result
}

fn gauss_sum_range(start: &BigInt, end: &BigInt) -> BigInt {
    gauss_sum(end) - gauss_sum(&(start - &BigInt::from(1)))
}

fn gauss_sum(n: &BigInt) -> BigInt {
    if *n < BigInt::from(0) {
        BigInt::from(0)
    } else {
        n * (n + &BigInt::from(1)) / &BigInt::from(2)
    }
}

fn sum_with_overflow(sum: &BigInt, t: &BigInt) -> u64 {
    let remainder = sum % t;

    if remainder == BigInt::from(0) {
        sum.to_u64().unwrap()
    } else {
        remainder.to_u64().unwrap()
    }
}
______________________________________________
use num::{BigInt, Signed, ToPrimitive};
use std::ops::BitXor;

fn elder_age(m: u64, n: u64, l: u64, t: u64) -> u64 {
    let sum = elder_age_remaining(
        &BigInt::from(m),
        &BigInt::from(n),
        &BigInt::from(l),
        &BigInt::from(0),
        &BigInt::from(0),
    );

    sum_with_overflow(&sum, &BigInt::from(t))
}

fn elder_age_remaining(m: &BigInt, n: &BigInt, l: &BigInt, offset_m: &BigInt, offset_n: &BigInt) -> BigInt {
    if m == &BigInt::from(0) || n == &BigInt::from(0) {
        return BigInt::from(0);
    }

    if m == &BigInt::from(1) && n == &BigInt::from(1) {
        return (offset_m.bitxor(offset_n) - l).max(BigInt::from(0));
    }

    if n > m {
        return elder_age_remaining(n, m, l, offset_n, offset_m);
    }

    let pow_m = &max_pow2_lt_x(m);
    let pow_n = &max_pow2_lt_x(n);

    if pow_m >= n {
        return elder_age_pow2(pow_m, n, l, offset_m, offset_n)
            + elder_age_remaining(&(m - pow_m), n, l, &(offset_m + pow_m), offset_n);
    }

    elder_age_pow2(pow_m, pow_n, l, offset_m, offset_n)
        + elder_age_pow2(pow_m, &(n - pow_n), l, offset_m, &(offset_n + pow_n))
        + elder_age_remaining(&(m - pow_m), n, l, &(offset_m + pow_m), offset_n)
}

fn max_pow2_lt_x(x: &BigInt) -> BigInt {
    BigInt::from(2).pow((x.to_f64().unwrap()).log2().floor() as u32)
}

fn elder_age_pow2(m: &BigInt, n: &BigInt, l: &BigInt, offset_m: &BigInt, offset_n: &BigInt) -> BigInt {
    if n > m {
        return elder_age_pow2(n, m, l, offset_n, offset_m);
    }

    let mut start = offset_m.bitxor(offset_n) - l;
    let shift = ((offset_m - offset_n).abs()).max(BigInt::from(0)) % m;

    start -= shift;
    let end = &start + m - BigInt::from(1);

    let row_sum = gauss_sum_range(&start, &end);
    let result = row_sum * n;

    result
}

fn gauss_sum_range(start: &BigInt, end: &BigInt) -> BigInt {
    gauss_sum(end) - gauss_sum(&(start - &BigInt::from(1)))
}

fn gauss_sum(n: &BigInt) -> BigInt {
    if *n < BigInt::from(0) {
        BigInt::from(0)
    } else {
        n * (n + &BigInt::from(1)) / &BigInt::from(2)
    }
}

fn sum_with_overflow(sum: &BigInt, t: &BigInt) -> u64 {
    let remainder = sum % t;

    if remainder == BigInt::from(0) {
        sum.to_u64().unwrap()
    } else {
        remainder.to_u64().unwrap()
    }
}
_______________________________________________
use std::cmp::{max, min};
use std::convert::TryInto;
use num::BigUint;


struct MagicRectangle {
    length: u64,
    width: u64,
    loss: u64,
    offset: u64,
}

impl MagicRectangle {
    fn new(length: u64, width: u64, loss: u64) -> Self {
        MagicRectangle {
            length,
            width,
            loss,
            offset: 0,
        }
    }

    fn new_with_offset(length: u64, width: u64, loss: u64, offset: u64) -> Self {
        MagicRectangle {
            length,
            width,
            loss,
            offset,
        }
    }

    fn value(&self) -> BigUint {
        // Start by identifying a unit square, that is, a square whose sides are a
        // length of a power of 2, small enough to fit inside the magic rectangle.
        let smallest_dim = min(self.width, self.length);
        let largest_power_of_2 = (smallest_dim as f64).log(2.).trunc() as u32;
        let square_dim = 2u64.pow(largest_power_of_2) as u64;

        // Calculate the number of squares (or partial squares) contained within the
        // length and width of the magic rectangle.
        let squares_wide = (self.width as f64 / square_dim as f64).ceil() as u64;
        let squares_long = (self.length as f64 / square_dim as f64).ceil() as u64;

        let mut total = BigUint::from(0u64);
        for width_offset in 0..squares_wide {
            for length_offset in 0..squares_long {
                // The number of rows and columns may be less than a perfect square for
                // square sections along the right and bottom edges of the rectangle
                let rows = min(self.width - (width_offset * square_dim), square_dim);
                let cols = min(self.length - (length_offset * square_dim), square_dim);
                let largest_dim = max(rows, cols);

                // The value in each square (or part of a square) is directly proportional
                // to the degree that the square is offset from the origin.
                let scaled_width_offset = width_offset * square_dim;
                let scaled_length_offset = length_offset * square_dim;
                let offset = (scaled_width_offset ^ scaled_length_offset) + self.offset;

                // Need to apply loss to a single row/column from the unit square, to
                // be applied to all rows/columns present in the current square (or
                // part of a square). This is accomplished efficiently by using the
                // Gaussian method for determining the sum of a sequence, with the
                // loss factor accounted for with the `saturating_sub` calls.
                let seq_start = offset.saturating_sub(self.loss) as u128;
                let seq_end = (offset + largest_dim).saturating_sub(self.loss + 1) as u128;
                let num_addends = (seq_end - seq_start) + 1;
                let dim_value = BigUint::from(((seq_start + seq_end) * num_addends) / 2);

                // Determine the value contributed by each square or part of a square
                let square_value = if rows < square_dim && cols < square_dim {
                    // If the square is smaller in both dimensions, it must be in the
                    // bottom right of the magic rectangle. Find it's value by treating
                    // it as a new rectangle with an inherent offset.
                    let width = rows as u64;
                    let length = cols as u64;
                    let mini_rect = MagicRectangle::new_with_offset(length, width, self.loss, offset);
                    mini_rect.value()
                } else if rows < square_dim {
                    // If this part of a square has the same length as a unit square,
                    // then it's value can be determined based on the value of a row
                    // in the unit square, adjusted by the current offset.
                    dim_value * rows
                } else if cols < square_dim {
                    // If this part of a square has the same width as a unit square,
                    // then it's value can be determined based on the value of a column
                    // in the unit square, adjusted by the current offset.
                    dim_value * cols
                } else {
                    // If this square is the same size as the unit square, it's value
                    // is just the value of a unit square adjusted by it's current offset.
                    // unit_square_value + (square_dim * square_dim * offset)
                    dim_value * square_dim
                };

                total += square_value;

                // println!(
                //     "Rect Origin: {}; Offset: ({},{}); Multiplier: {}; Value: {}; Largest Dim: {}",
                //     self.offset,
                //     scaled_width_offset,
                //     scaled_length_offset,
                //     offset,
                //     square_value,
                //     largest_dim
                // );
            }
        }
        total
    }
}

fn elder_age(m: u64, n: u64, l: u64, t: u64) -> u64 {
    let magic_rectangle = MagicRectangle::new(m, n, l);
    let total_seconds = magic_rectangle.value();
    (total_seconds % t).try_into().expect("Something bad happened!")
}
___________________________________________________________
const SAFE_LIMIT: u64 = 1 << 31;

/// Avoid overflow when t < 2^32
fn multiply_with_mod_t(mut a: u64, mut b: u64, t: u64) -> u64 {
    a %= t;
    b %= t;
    if a <= SAFE_LIMIT && b <= SAFE_LIMIT {
        return a * b % t;
    }
    let (halve_a, halve_b) = (a / 2, b / 2);
    a -= halve_a;
    b -= halve_b;
    ((a * b) % t + (a * halve_b) % t + (halve_a * b) % t + (halve_a * halve_b) % t) % t
}

// Fast computing of log2 for 64-bit integers, from
// https://stackoverflow.com/a/11398748/100297
const TAB64: [u64; 64] = [
    63, 0, 58, 1, 59, 47, 53, 2, 60, 39, 48, 27, 54, 33, 42, 3, 61, 51, 37, 40, 49, 18, 28, 20, 55,
    30, 34, 11, 43, 14, 22, 4, 62, 57, 46, 52, 38, 26, 32, 41, 50, 36, 17, 19, 29, 10, 13, 21, 56,
    45, 25, 31, 35, 16, 9, 12, 44, 24, 15, 8, 23, 7, 6, 5,
];

fn int_log2(mut value: u64) -> u64 {
    value |= value >> 1;
    value |= value >> 2;
    value |= value >> 4;
    value |= value >> 8;
    value |= value >> 16;
    value |= value >> 32;
    TAB64[(((value - (value >> 1)).wrapping_mul(0x07EDD5E59A4E28C2)) >> 58) as usize]
}

fn triangle(n: u64, t: u64) -> u64 {
    if n % 2 == 0 {
        multiply_with_mod_t(n / 2, n + 1, t)
    } else {
        multiply_with_mod_t(n, (n + 1) / 2, t)
    }
}

fn elder_age(mut m: u64, mut n: u64, mut l: u64, t: u64) -> u64 {
    let mut total = 0;
    while m > 0 && n > 0 {
        if m > n {
            std::mem::swap(&mut m, &mut n);
        }
        let nlog2 = 1 << int_log2(n);
        let ll = if nlog2 > l { 0 } else { l - nlog2 };
        n %= nlog2;
        if nlog2 < m {
            let mlog2 = 1 << int_log2(m);
            m %= mlog2;
            if nlog2 > l {
                if nlog2 - 1 > l {
                    total += multiply_with_mod_t(triangle(nlog2 - 1 - l, t), mlog2, t);
                }
                total += multiply_with_mod_t(multiply_with_mod_t(nlog2 - l, nlog2, t), n, t);
            }
            if nlog2 > ll {
                total += multiply_with_mod_t(triangle(nlog2 - 1 - ll, t), m, t);
            }
            if mlog2 > l {
                total += multiply_with_mod_t(multiply_with_mod_t(mlog2 - l, mlog2, t), m, t);
            }
            if mlog2 - 1 > l {
                total += multiply_with_mod_t(triangle(mlog2 - 1 - ll, t), n, t);
            }
        } else {
            if nlog2 > l {
                if nlog2 - 1 > l {
                    total += multiply_with_mod_t(triangle(nlog2 - 1 - l, t), m, t);
                }
                total += multiply_with_mod_t(multiply_with_mod_t(nlog2 - l, m, t), n, t);
            }
            l = ll;
        }
    }

    total % t
}

fn powerize(n: i128) -> i128 {
    let mut x = 1;
    while (x << 1) <= n {
        x <<= 1;
    }
    x
}

fn points(m: i128, n: i128, l: i128, t: i128) -> i128 {
    if 0 == m || 0 == n { return 0; }
    let (m, n) = if m > n { (m, n) } else { (n, m) };
    
    let m1 = powerize(m);
    let n1 = if m1 < n { m1 } else { n };
    
    let f = if 0 > -l { 0 } else { -l };
    let to = if 0 > m1 - l - 1 { 0 } else { m1 - l - 1 };
    
    let a = n1 % t;
    let b = (to - f + 1) % t;
    let c = (f + to) % t;
    let mut total = (a * b) *  c;
    total >>= 1;
    
    if m > m1 {
        total += points(m - m1, n1, l - m1, t);
    }
    if n > n1 {
        total += points(m1, n - n1, l - n1, t);
    }
    if n > n1 && m > m1 {
        total += points(m - m1, n - n1, l, t);
    }
    total % t
}

fn elder_age2(m: u64, n: u64, l: u64, t: u64) -> u64 {
    points(m as i128, n as i128, l as i128, t as i128) as u64
}
