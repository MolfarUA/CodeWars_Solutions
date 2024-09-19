lastDigit = (a) -> a.reduceRight(((p, c, i) -> Math.pow((if !i then c % 10 else if c < 4 then c else c % 4 + 4), (if p < 4 then p else p % 4 + 4))), 1) % 10
___________
function is_zero(lst) {
  if (lst.length == 0) return false;
  if (lst[0] == 0) return !is_zero(lst.slice(1));
  return false;
}
function is_one(lst) {
  if (lst.length == 0 || lst[0] == 1) return true;
  return is_zero(lst.slice(1));
}
function is_odd(lst) {
  if (lst.length == 0) return true;
  return lst[0] % 2 == 1 || is_zero(lst.slice(1));
}
function ld(lst) {
  if (lst.length == 0) return 1;
  if (lst[0] == 0) return +is_zero(lst.slice(1));
  switch (lst[0] % 4) {
    case 0:
      return is_zero(lst.slice(1)) ? 1 : 4; 
    case 1:
      return 1;
    case 2:
      return is_zero(lst.slice(1)) ? 1 : is_one(lst.slice(1)) ? 2 : 4;
    default:
      return is_odd(lst.slice(1)) ? 3 : 1;
  }
}
function lastDigit(lst) {
  if (lst.length == 0) return 1;
  return (lst[0] % 10) ** ld(lst.slice(1)) % 10
}
____________________
lastDigit = (as) ->
  return 1 if !as.length
  r = 1
  f = 0
  for i in [as.length - 1..0]
    x = as[i]
    [r, f] = [(x % (if i then 4 else 10)) ** (r + 4 * f) % (if i then 4 else 10), if x <= 1 then 0 else if x <= 3 && r <= 1 then f else 1]
  r
