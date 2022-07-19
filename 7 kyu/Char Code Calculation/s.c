57f75cc397d62fc93d000059


int calc(const char *source)
{
    int result = 0;
    while( *source )
    {
        if( *source%10 == 7 ) result += 6;
        if( *source/10%10 == 7 ) result += 6;
        source++;
    }
    return result;
}
__________________________________
int calc(const char *s)
{
  int d = 0;
  for (; *s; s++) d += (*s / 10 % 10 == 7 ? 6: 0) + (*s % 10 == 7 ? 6 : 0);
  return d;
}
__________________________________
int calc(const char *source)
{
    char s[4], *t;
    int total1 = 0, total2 = 0;
    for (; *source; source++)
    {
        sprintf(s,"%d",((int)*source));
        for (t = s; *t; t++)
        {
            total1 += *t - '0';
            total2 += ('7' == *t ? '1' : *t) - '0';
        }
    }
    return total1 - total2;
}
