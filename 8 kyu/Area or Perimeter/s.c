5ab6538b379d20ad880000ab


int area_or_perimeter(int a , int b) {
  return a == b ? a * b : 2 * (a + b);
}
________________________
int area_or_perimeter(int l , int w) {
  return (l == w) ? l * l : (w * 2) + (l *2);
}
________________________
int area_or_perimeter(int l , int w) {
  int area=0;
  int perimeter=0;
  if(l==w){
    area=l*w;
    return area;
  }else{
    perimeter=l+l+w+w;
    return perimeter;
  }
}
