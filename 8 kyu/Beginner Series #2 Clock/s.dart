55f9bca8ecaa9eac7100004a
  
  
int past(int h, int m, int s) {
  return new Duration(hours: h, minutes: m, seconds: s).inMilliseconds;
}
__________________________
int past(int h, int m, int s) {
  return (h * 3600 + m * 60 + s) * 1000;
}
__________________________
int past(int h, int m, int s) => (s + (m + h * 60) * 60) * 1000;
__________________________
int past(int h, int m, int s) {
  m += h *60 ; 
  s += m * 60;
  return s* 1000;
}
__________________________
int past(int h, int m, int s) {
  if (0 <= h && h <= 23) {
    if (0 <= m && m <= 59) {
      if (0 <= s && s <= 59) {
        int inMilliseconds =
            Duration(hours: h, minutes: m, seconds: s).inMilliseconds;
        return inMilliseconds;
      }
    }
  }
  throw Exception('Invalid data');
}
