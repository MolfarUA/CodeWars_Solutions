#include <stdbool.h>

bool isValidWalk(const char *walk) {
  if (strlen(walk) != 10) return 0;
  
  int h = 0, v = 0;
  while(*walk) {
    switch(*walk) {
      case 'n': ++v; break;
      case 's': --v; break;
      case 'e': ++h; break;
      case 'w': --h; break;
    }
    ++walk;
  }
  return h == 0 && v == 0;
}
__________________________________________
#include <stdbool.h>

bool isValidWalk(const char *walk) {
     int i=0, north_south=0, vest_est=0; 
     for(; i< walk[i]; i++){
       if(walk[i] == 'n' ) north_south++;
       if(walk[i] == 's' ) north_south--;
       if(walk[i] == 'e' ) vest_est++;
       if(walk[i] == 'w' ) vest_est--;
        
     }
     if(i==10 && north_south==0 && vest_est==0) return true; else return false;

}
__________________________________________
#include <stdbool.h>

bool isValidWalk(const char *walk) {

   char* c = walk;
   int up, right, count;
   up = right = count = 0;
   while( *c !='\0' ){
     switch(*c){
       case 'n':
         count++;
         up++;
         break;
       case 's':
         count++;
         up--;
         break;
       case 'e':
         count++;
         right++;
         break;
       case 'w':
         count++;
         right--;
         break;
     
     }
     c++;    
   }
   return up == 0 && right == 0 && count == 10;
}
__________________________________________
#include <stdbool.h>

bool isValidWalk(const char *s) {
  if (strlen(s) != 10) return false;
  int x = 0, y = 0;
  for (; *s; s++) *s == 'n' ? y-- : *s == 's' ? y++ : *s == 'w' ? x-- : x++;
  return !x && !y;
}
