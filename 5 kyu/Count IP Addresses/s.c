#include <inttypes.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

uint32_t ips_between (const char *start, const char *end)
{
  return ntohl(inet_addr(end)) - ntohl(inet_addr(start));
}
_______________
#include <inttypes.h>
#include <stdio.h>

#define IP2UINT32(i1,i2,i3,i4)  i1<<24|i2<<16|i3<<8|i4

uint32_t ips_between (const char *start, const char *end)
{
  uint32_t is[4], ie[4], s, e;

  sscanf(start, "%d.%d.%d.%d", &is[0], &is[1], &is[2], &is[3]);
  sscanf(end, "%d.%d.%d.%d", &ie[0], &ie[1], &ie[2], &ie[3]);

  s = IP2UINT32(is[0], is[1], is[2], is[3]);
  e = IP2UINT32(ie[0], ie[1], ie[2], ie[3]);
  
  return e - s;
}
_______________
#include <inttypes.h>
#include <stdio.h>

uint32_t ips_between (const char *start, const char *end)
{
  uint32_t a,b,c,d;
  uint32_t s = 0;
  uint32_t e = 0;
  sscanf(start,"%d.%d.%d.%d",&a,&b,&c,&d);
  s = a << 24 | b << 16 | c << 8 | d;
  sscanf(end,"%d.%d.%d.%d",&a,&b,&c,&d);
  e = a << 24 | b << 16 | c << 8 | d;
  return e-s;
}

