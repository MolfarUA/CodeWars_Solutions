515decfd9dcfc23bb6000006


#include <arpa/inet.h>

/* Return 1 is addr is a valid IP address, return 0 otherwise */
int is_valid_ip(const char *addr) {
  struct sockaddr_in sockaddr;
  return inet_pton(AF_INET, addr, &(sockaddr.sin_addr)) ? 1 : 0;
}
_____________________________
#include <stdio.h>

int is_valid_ip(const char *addr)
{
 unsigned n[4], i, nc;
 
 // Must be 4 integers separated by dots:
 if( sscanf(addr, "%d.%d.%d.%d%n", &n[0], &n[1], &n[2], &n[3], &nc) != 4 )
   return 0;
   
 // Leftover characters at the end are not allowed:
 if( nc != strlen(addr) )
   return 0;
   
 // Leading zeros and space characters are not allowed:
 if( addr[0] == '0' || strstr(addr, ".0") || strchr(addr, ' ') )
   return 0;
 
 // Values > 255 are not allowed:
 for(i=0; i<4; i++)
   if( n[i] > 255 )
     return 0;
  
 return 1;
};
_____________________________
/* Return 1 is addr is a valid IP address, return 0 otherwise */
#include <string.h>
#include <stdio.h>

int is_valid_ip(const char * addr) {
  unsigned char a,b,c,d;
  char test[30];
  sscanf(addr, "%hhu.%hhu.%hhu.%hhu", &a, &b, &c, &d);
  snprintf(test, 30, "%hhu.%hhu.%hhu.%hhu", a, b, c, d);
  return strcmp(addr, test)==0;
};
