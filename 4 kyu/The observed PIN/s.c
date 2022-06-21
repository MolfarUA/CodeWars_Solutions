5263c6999e0f40dee200059d


#include <stdlib.h>
#include <string.h>

static const char * const possibilities[] = {
    "08", "124", "2135", "326", "4157", "52468", "6359", "748", "85790", "968"
};
static const size_t counts[] = { 2, 3, 4, 3, 4, 5, 4, 3, 5, 3 };

const char** get_pins(const char* observed, size_t* count) {

    size_t amt = 1;
    for (const char* p = observed; *p; ++p) {
        amt *= counts[*p - '0'];
    }
    size_t pin_len = strlen(observed);
    size_t pins_buff_len = amt * (pin_len + 1);
    size_t toc_buff_len = sizeof(const char *) * amt;
    void* buff = malloc(toc_buff_len + pins_buff_len);
    char** toc_buff = (char**)buff;
    char* pins_buff = ((char*)buff) + toc_buff_len;

    for (size_t i = 0; i < amt; ++i) {
        toc_buff[i] = pins_buff;
        size_t p = i;
        for (size_t c = 0; c < pin_len; ++c, ++pins_buff) {
            int pin_num = observed[c] - '0';
            const char* candidates = possibilities[pin_num];
            size_t candidates_count = counts[pin_num];
            div_t d = div(p, candidates_count);
            p = d.quot;
            *pins_buff = candidates[d.rem];
        }
        *(pins_buff++) = '\0';
    }
    *count = amt;
    return toc_buff;
}

void free_pins(const char ** pins) {
    free((void*)pins);
}
______________________________
#include <stdlib.h>
#include <string.h>
#include <stddef.h>

static const char *adjacent_pins[] = {
  "08",    // 0
  "124",   // 1
  "1235",  // 2
  "236",   // 3
  "1457",  // 4
  "24568", // 5
  "3569",  // 6
  "478",   // 7
  "05789", // 8
  "689"    // 9
};
static const size_t adjacent_pins_len[] = {
  2,3,4,3,4,5,4,3,5,3
};

/* Keep track of each digits individually stepping through all combinations */
static void update_counter(size_t counters[], const size_t limits[], const char* observed, size_t count)
{
  size_t i = 0;
  for (i = 0; i < count; i++) {
    counters[i] = (counters[i]+1) % limits[observed[i]-'0'];
    
    /* If it overflows, we need to update the next one */
    if (counters[i] != 0) {
      break;
    }
  }
}

//Function should return an array of c-strings with all possible PINs.
//Upon return, count should contain the amount of returned PINs.
const char** get_pins(const char* observed, size_t* count)
{
  size_t i = 0;
  size_t j = 0;
  size_t len_input = strlen(observed);
  size_t *index_i = malloc(sizeof(size_t)*len_input);
   
  /* Need to be one for the combinatorics calculation */
  size_t out_num = 1;
  char **output = NULL;
  
  /* Clear counter indicies */
  memset(index_i, 0, sizeof(size_t)*len_input);
  
  /* Calculate number of output strings */
  for (i = 0; i < len_input; i++) {
    out_num *= adjacent_pins_len[observed[i] - '0'];
  }
  output = malloc(sizeof(char*)*out_num+1);
  
  /* Add a null-terminator for the array */
  output[out_num] = NULL;
  
  /* Allocate individual strings */
  for (i = 0; i < out_num; i++) {
    output[i] = malloc(sizeof(char)*len_input+1);
  }
  
  /* Process possible combinations */
  for (i = 0; i < out_num; i++) {
    for (j = 0; j < len_input; j++) {
      output[i][j] = adjacent_pins[observed[j]-'0'][index_i[j]];
    }
    output[i][j] = '\0';
    
    /* Update all counters to the next iteration */
    update_counter(index_i, adjacent_pins_len, observed, len_input);
  }
  
  /* Free counters */
  free(index_i);
  
  *count = out_num;
  return (const char **)output;
}

void free_pins(const char ** pins)
{
  int i = 0;
  for (i = 0; pins[i] != NULL; i++) {
    free((void*)pins[i]);
  }
  free(pins);
}
______________________________
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

char* neighbourFinder(char digit){  //Finds the neighbours of given digit
  char* result = (char*)malloc (6 * sizeof (char));
  switch (digit) {
      case '0': result="08";break;
      case '1': result="124";break;//{'1','2','4','\0'};break;
      case '2': result="1235";break;
      case '3': result="236";break;
      case '4': result="1457";break;
      case '5': result="24568";break;
      case '6': result="3569";break;
      case '7': result="478";break;
      case '8': result="05789";break;
      case '9': result="689";break;
      default: result="0000";
  }
  return result;
}

const char** get_pins(const char* observed, size_t* count) {
  *count = 1;  
  int size = strlen(observed); //length of observed string
  
  char **neighbours = malloc(size * sizeof(char *)); // 2-D neighbours declaration
  for(int k = 0; k < size; k++)                      // 2-D neighbours declaration
    neighbours[k] = malloc(6 * sizeof(char));        // 2-D neighbours declaration
    
  for(int i=0; i<size; i++)
    neighbours[i]=neighbourFinder(observed[i]); //finds all neighbours for every digit given in observed
  
  int expectedCount=1;
  for(int i=0; i<size; i++)
    expectedCount=expectedCount*strlen(neighbours[i]);  //Calculates the total count
  
  *count=(size_t)expectedCount;
  
  char **result = (char**) calloc(expectedCount, sizeof(char *)); // 2-D neighbours declaration
  for(int k = 0; k < expectedCount; k++)                          // 2-D neighbours declaration
    result[k] = (char*) calloc(size, sizeof(char));               // 2-D neighbours declaration
  
  int repeatCount=1;
  for(int i=0; i<size; i++){
    expectedCount=expectedCount/strlen(neighbours[i]);            //possible combinations occured right side of the digit.
    for(int p=0; p<repeatCount; p++){
      for(int j=0; j<strlen(neighbours[i]); j++){
        if(size==1) result[j][i]=neighbours[i][j];
        else{
          for(int k=0; k<expectedCount; k++){
            result[p*expectedCount*strlen(neighbours[i])+j*expectedCount+k][i]=neighbours[i][j];
            //k-> required repeat for each neighbour
            //j-> number of neighbour
            //p-> repeat times for each neighbour
          }
        }
      }
    }
    repeatCount=repeatCount*strlen(neighbours[i]);              //possible combinations occured left side of the digit
  } 
  free(neighbours);
  return result;
}
void free_pins(const char ** pins) {
  free(pins);
}
