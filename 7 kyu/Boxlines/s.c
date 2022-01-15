unsigned long long f(long long x, long long y, long long z) {
  return 3*(x*y*z) +2*(x*y+x*z+y*z) + x+y+z;
}
_____________________________________
unsigned long long f(unsigned short x, unsigned short y, unsigned short z) {
  return x * (y + 1ull) * (z + 1) + (x + 1ull) * y * (z + 1ull) + (x + 1ull) * (y + 1ull) * z;
}
_____________________________________
unsigned long long f(unsigned long long x, unsigned long long y, unsigned long long z) {
  return (x * (y + 1) + y * (x + 1)) * (z + 1) + z * (x + 1) * (y + 1);
}
_____________________________________
unsigned long long f(unsigned int a,unsigned int b, unsigned int c){
  unsigned long long x=a,y=b,z=c;
  return z*(3*x*y+1+2*(x+y))+2*x*y+x+y;
}
_____________________________________
unsigned long long f(unsigned long long x, unsigned long long y, unsigned long long z) {
  return (y*(x+1)+x*(y+1))*(z+1)+z*(x+1)*(y+1);
}
