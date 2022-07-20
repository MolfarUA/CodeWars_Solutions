57a5c31ce298a7e6b7000334


unsigned bin_to_decimal(const char *bin)
{
  return strtol(bin, 0, 2);
}
_________________________
unsigned bin_to_decimal(const char *bin)
{
    unsigned dec = 0;
    while (*bin)
        dec = dec * 2 + *bin++ - '0';
    return dec;
}
_________________________
unsigned bin_to_decimal(const char *bin) {    
  int dec_value = 0; 
  int base = 1; 
  
  for (int i = strlen(bin) - 1; i >= 0; i--) { 
    if (bin[i] == '1') 
      dec_value += base; 
    base = base * 2; 
  } 
  return dec_value; 
} 
_________________________
unsigned bin_to_decimal(const char *bin) {
  unsigned int x = 0;
  while (*bin) x = x * 2 + *bin++ - '0';
  return x;
}
