int digital_root(int Z) {
  return --Z % 9 + 1;
}

________________________________
int digital_root(int n) {
  if (n < 10) return n;
  int r = 0;
  while (n) r += n % 10, n /= 10;
  return digital_root(r);
}

________________________________
int digital_root(int n) {
  return (n-1)%9 + 1;
}

________________________________
int simple_digital_root(int n){
  int result = 0;
  while(n){
    result += n % 10;
    n /= 10;
  }
  return result;
}

int digital_root(int n) {
  do{
    n = simple_digital_root(n);
  }while(n >= 10);
  return n;
}

________________________________
int digital_root(int n) {
  int test = 0;
  int temp = n;
  int temp2 = 0;
  if(n == 0){
    return 0;
  }
  while(temp!=0){
    test++;
    temp2 += temp%10;
    temp = temp/10;
  }
  while(test!=1){
    temp = temp2;
    temp2 = 0;
    test = 0;
    while(temp!=0){
      test++;
      temp2 += temp%10;
      temp = temp/10;
    }
  }
  return temp2;
}
