58cb43f4256836ed95000f97
  
  
int findDifference(List<int> a, List<int> b) => (a.reduce((x, y) => x * y) - b.reduce((x, y) => x * y)).abs();
________________________
int findDifference(List<int> a, List<int> b) => (a[0] * a[1] * a[2] - b[0] * b[1] * b[2]).abs();
________________________
int findDifference(List<int> a, List<int> b) {
  var sum_a = a.reduce((a, b) => a * b);
  var sum_b = b.reduce((a, b) => a * b);
  return (sum_a - sum_b).abs();
}
________________________
int findDifference(List<int> a, List<int> b) {
    return (a.reduce((c, d) => c * d) - b.reduce((e, f) => e * f)).abs();
}
