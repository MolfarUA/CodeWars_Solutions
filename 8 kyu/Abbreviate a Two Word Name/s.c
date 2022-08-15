57eadb7ecd143f4c9c0000a3


char *get_initials (const char *full_name, char initials[4])
{
  char *space;
  initials[0] = toupper(full_name[0]);
  initials[1] = '.';
  
  space = strchr(full_name, ' ');
  
  initials[2] = toupper(space[1]);
  initials[3] = '\0';
  
  return initials; // return it
}
_________________________
#include <ctype.h>
#include <string.h>

char *get_initials (const char *full_name, char initials[4])
{
  
  initials[0] = toupper(full_name[0]);
  initials[1] = '.';
  
  for(int i = 0; i < (int)strlen(full_name); i++){
    if(full_name[i] == ' '){
      initials[2] = toupper(full_name[i + 1]);
    }
  }
  
  initials[3] = '\0';
  
  return initials;
}
_________________________
#include <string.h>
#include <ctype.h>

char *get_initials (const char *full_name, char initials[4]) {
  initials[0] = toupper(*full_name);
  initials[1] = '.';
  initials[2] = toupper(*(strchr(full_name, ' ') + 1));
  initials[3] = '\0';
  return initials;
}
