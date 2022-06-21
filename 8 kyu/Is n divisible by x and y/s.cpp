5545f109004975ea66000086
  
  
bool isDivisible(int n, int x, int y) {
  return n % x == 0 && n % y == 0;
}
_____________________
bool isDivisible(int n, int x, int y) {
  return ((n%x)==0)&&((n%y)==0)?true:false;
}
_____________________
bool isDivisible(int n, int x, int y) {
  return !(n%x|n%y);
}
