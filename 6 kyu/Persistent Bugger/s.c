int persistence(int n)
{
    int m, p = 0;
    while (n > 9) {
        ++p;
        m = n % 10;
        while (n /= 10)
            m *= n % 10;
        n = m;
    }
    return p;
}
________________________________________
int persistence(int n) {
    int p = 1;
    if (n < 10) { return 0; } 
    while (n > 0) { p = (n % 10) * p; n /= 10; }
    return persistence(p) + 1; 
}
________________________________________
int persistence(int n) {
  for (int m, i = 0;; n = m, ++i) {
    if (n < 10) return i;
    for (m = n % 10; n > 9; n /= 10, m *= n % 10);
  }
}
________________________________________
int mul_digits(int n) {
    if ((n / 10) < 1) return n;
    else return ((n % 10) * mul_digits(n / 10));
}

int persistence(int n) {
    if ((n / 10) < 1) return 0;
    else return (1 + persistence(mul_digits(n)));
}
________________________________________
int persistence(int n) {

    int counter = 0, i=0, rem, product;
    
    do
      {
        product = 1;
        while(n)
        {
          rem = n%10;        // take the last digit
          product *= rem;    // find the product of digits
          if (product == 0)
          {
            counter++;
            break;
          }
          n /= 10;
          i++;               // store number of digits
        }
        if((product/10) != 0)
        {
          counter++;
          n = product;
        }
        else if(product != 0 && (product/10) == 0)
        {
          if (i != 1)
          {
            counter++;
          }
        }
      } while((product/10) != 0);
    
  return counter;
}
