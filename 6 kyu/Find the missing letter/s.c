char findMissingLetter(char array[], int arrayLength)
{
  for (int i = 1;i < arrayLength;i++){
    if (array[i - 1] + 1 != array[i])
      return array[i-1] + 1;
  }
}
________________________
char findMissingLetter(char array[], int arrayLength)
{
    while (++*array == *++array);
    return --*array;
}
________________________
char findMissingLetter(char array[], int arrayLength)
{
  int i = 0;
  for (i = 0; i < arrayLength; i++){
    if (array[i + 1] != array[i] + 1){
      return array[i] + 1;
    }
  }
  return ' ';
}
________________________
char findMissingLetter(char array[], int arrayLength)
{
  char c = array[0];
  while (c++ == *(array++));
  return c - 1;
}
________________________
char findMissingLetter(char array[], int arrayLength)
{
  char c = array[0];
  for (int i = 1; i < arrayLength; ++i)
  {
    c++;
    if (c != array[i])
      return c;
  }
}
