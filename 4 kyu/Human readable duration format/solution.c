52742f58faf5485cae000b9a


#include <stdlib.h>
#include <stdio.h>

#define MINUTE 60
#define HOUR (MINUTE * 60)
#define DAY (HOUR * 24)
#define YEAR (DAY * 365)

static void  store(int num, size_t *ai, char storage[5][32], const char *str)
{
  if (num > 0)
  {
    if (num == 1)
    {
      sprintf(storage[*ai], "%d %s", num, str);
    }
    else
    {
      sprintf(storage[*ai], "%d %ss", num, str);
    }
    *ai += 1;
  }
}

char *formatDuration (int n) {
  char    *output;
  char    storage[5][32];
  size_t  i = 0;
  
  if (n == 0)
  {
    asprintf(&output, "now");
  }
  else
  {
    store(n / YEAR, &i, storage, "year");
    n %= YEAR;
    store(n / DAY, &i, storage, "day");
    n %= DAY;
    store(n / HOUR, &i, storage, "hour");
    n %= HOUR;
    store(n / MINUTE, &i, storage, "minute");
    n %= MINUTE;
    store(n, &i, storage, "second");
    if (i == 1)
      asprintf(&output, "%s", storage[0]);
    else if (i == 2)
      asprintf(&output, "%s and %s", storage[0], storage[1]);
    else if (i == 3)
      asprintf(&output, "%s, %s and %s", storage[0], storage[1], storage[2]);
    else if (i == 4)
      asprintf(&output, "%s, %s, %s and %s", storage[0], storage[1], storage[2], storage[3]);
    else
      asprintf(&output, "%s, %s, %s, %s and %s", storage[0], storage[1], storage[2], storage[3], storage[4]);
  }
  return output;
}

___________________________________________________
#include <string.h>
#include <stdio.h>

#define FMT_DUR    0x40
#define NDUR       5

char *formatDuration (int n)
{
    const char *fmt[] = { "year", "day", "hour", "minute", "second" };
    char fmtdur[FMT_DUR] = { 0 };
    int dur[NDUR] = { 31536000, 86400, 3600, 60, 0 };
    int i, m, d, pos;
    if (!n)
        return strdup("now");
    for (m = i = 0; i < 4 && n; n %= d, ++i)
        if (dur[i] = n / (d = dur[i]))
            ++m;
    if (n)
        ++m, dur[i++] = n;
    for (pos = n = 0; n < i; ++n)
        if (d = dur[n])
            pos += sprintf(fmtdur+pos, "%d %s%s%s", d, *(fmt+n), d > 1 ? "s" : "", m > 2 ? ", " : m > 1 ? " and " : ""), --m;
    return strdup(fmtdur);
}

___________________________________________________
#include <stddef.h>
#include <string.h>
#include <stdlib.h>

char *formatDuration (int n)
{
    char time[150] = {NULL};
    char buf[20] = {NULL};
    short flag = 0;
    int instances = 0;
    int initial_n = n;

    if (n / 31536000 != 0) instances++;
    n %= 31536000;
    if (n / 86400 != 0) instances++;
    n %= 86400;
    if (n / 3600 != 0) instances++;
    n %= 3600;
    if (n / 60 != 0) instances++;
    n %= 60;


    n = initial_n;

    if (n / 31536000 != 0) // Number of seconds in a year
    {
        if (n / 31536000 == 1) sprintf(buf, "%d year", n / 31536000);
        else sprintf(buf, "%d years", n / 31536000);
        n %= 31536000;
        strcat(time, buf);
        flag = 1;
        if (instances > 1) strcat(time, ", ");
        else strcat(time, " ");
      instances--;
    }

    if (n / 86400 != 0) // Number of seconds in a day
    {
        if (n / 86400 == 1) sprintf(buf, "%d day", n / 86400);
        else sprintf(buf, "%d days", n / 86400);
        n %= 86400;
        strcat(time, buf);
        flag = 1;
        if (instances > 1) strcat(time, ", ");
        else strcat(time, " ");
       instances--;
    }

    if (n / 3600 != 0) // Number of seconds in a hour
    {
        if (n / 3600 == 1) sprintf(buf, "%d hour", n / 3600);
        else sprintf(buf, "%d hours", n / 3600);
        n %= 3600;
        strcat(time, buf);
        flag = 1;
      
      if (n % 60 == 0) strcat(time, " ");
        else if (instances > 1 ) strcat(time, ", ");
      else strcat(time, " ");
        
      instances--;
    }



    if (n / 60 != 0) // Number of seconds in a minute
    {
      if (flag == 1 && n % 60 == 0) strcat(time, "and ");
        if (n / 60 == 1) sprintf(buf, "%d minute ", n / 60);
        else sprintf(buf, "%d minutes ", n / 60);
        n %= 60;
        strcat(time, buf);
        flag = 1;
    }

    if (n) // Number of seconds in a second
    {
        if (flag == 1) strcat(time, "and ");
        if (n == 1) sprintf(buf, "%d second", n);
        else sprintf(buf, "%d seconds", n);
        strcat(time, buf);
        flag = 1;
    }

    if (n == 0 && flag == 0)
        strcat(time, "now");

    strcat(time, "Q");

    int count = 0;

    for (int i = 0; time[i] != 'Q'; i++) count++;

    char *friendly_time = (char*) malloc(sizeof(char)*count+1);

    for (int i = 0; time[i] != 'Q'; i++)
        friendly_time[i] = time[i];

    if (friendly_time[count-1] == ' ') friendly_time[count-1] = '\0';
    else friendly_time[count] = '\0';

    return friendly_time;
}

___________________________________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *formatDuration (int n) {
  char* tmp = calloc(sizeof(char), 8192);
  
  if (n == 0) {
    sprintf(tmp, "now");
  }
  else {
    int years = 0;
    int days = 0;
    int hours = 0;
    int minutes = 0;
    int seconds = 0;

    years = n / (365 * 24 * 60 * 60);
    n -= years * (365 * 24 * 60 * 60);

    days = n / (24 * 60 * 60);
    n -= days * (24 * 60 * 60);

    hours = n / (60 * 60);
    n -= hours * (60 * 60);

    minutes = n / (60);
    n -= minutes * (60);

    seconds = n;

    int delta = 0;

    if (years > 0) {
      delta += sprintf(tmp, "%d year%s", years, (years > 1) ? "s" : "");
    }

    if (days > 0) {
      if (years > 0) {
        if ((hours + minutes + seconds) == 0) {
          delta += sprintf(tmp + delta, " and ");
        }
        else {
          delta += sprintf(tmp + delta, ", ");
        }
      }
      delta += sprintf(tmp + delta, "%d day%s", days, (days > 1) ? "s" : "");
    }

    if (hours > 0) {
      if ((years + days) > 0) {
        if ((minutes + seconds) == 0) {
          delta += sprintf(tmp + delta, " and ");
        }
        else {
          delta += sprintf(tmp + delta, ", ");
        }
      }
      delta += sprintf(tmp + delta, "%d hour%s", hours, (hours > 1) ? "s" : "");
    }

    if (minutes > 0) {
      if ((years + days + hours) > 0) {
        if ((seconds) == 0) {
          delta += sprintf(tmp + delta, " and ");
        }
        else {
          delta += sprintf(tmp + delta, ", ");
        }
      }
      delta += sprintf(tmp + delta, "%d minute%s", minutes, (minutes > 1) ? "s" : "");
    }

    if (seconds > 0) {
      if ((years + days + hours + minutes) > 0) {
        delta += sprintf(tmp + delta, " and ");
      }
      delta += sprintf(tmp + delta, "%d second%s", seconds, (seconds > 1) ? "s" : "");
    }
  }
  
  size_t len = strlen(tmp);
  char* ret = calloc(sizeof(char), len + 1);
  memcpy(ret, tmp, len * sizeof(char));
  return ret;
}
