5861487fdb20cff3ab000030


#include <stdlib.h>
#include <stdbool.h>
// Boolfuck Interpreter. ////////////////////////////////////////////////
// Make a doubly linked list to represent an infinitely long tape.
struct Node {
    bool data;
    struct Node *next;
    struct Node *prev;
};

// Helpers. ////////////////////////////////////////////////
// Pad last character with zeros.
void padWithZeros(char *out) {
    int start = strlen(out);
    int size = 8 - (strlen(out) % 8);
    int i;
    for(i = start; i < start + size; ++i)
        out[i] = '0';
    out[i] = '\0';
}

// Reverse string.
void strrev(char *str) {
    char *p1, *p2;
    if (! str || ! *str)
        return;
    for (p1 = str, p2 = str + strlen(str) - 1; p2 > p1; ++p1, --p2) {
        *p1 ^= *p2;
        *p2 ^= *p1;
        *p1 ^= *p2;
    } 
    return;
}

void writeBlock(char *result, char *out, int i) {
    char buffer[9] = {0};
    memcpy(buffer, out + i, 8);
    // Reverse block to get a normal big-endian bit representation.
    strrev(buffer);
    char c = strtol(buffer, 0, 2);
    sprintf(result, "%s%c", result, c);
}

// Convert binary data to char string.
char* convertToCharacters(char *out) {
    // If output length is not multiple of eight, pad it with zeros.
    if(strlen(out) % 8 != 0)
        padWithZeros(out);
        
    char *result = (char*) calloc(4096, sizeof(char));
    for(int i = 0; i < strlen(out); i += 8)
        writeBlock(result, out, i);     
    return result;
}

void match(char bracket_a, char *code, int *code_ptr) {
    int count_a = 1, count_b = 0;
    if(bracket_a == '[') {
        char bracket_b = ']';
        *code_ptr += 1;
        while(count_a != count_b) {
            if(code[*code_ptr] == '[') count_a += 1;
            else if(code[*code_ptr] == ']') count_b += 1;
            *code_ptr += 1;
        }
        *code_ptr -= 1;
    }
    else if(bracket_a == ']') {
        char bracket_b = '[';
        *code_ptr -= 1;
        while(count_a != count_b) {
            if(code[*code_ptr] == ']') count_a += 1;
            else if(code[*code_ptr] == '[') count_b += 1;
            *code_ptr -= 1;
        }
        *code_ptr += 1;
    }  
}

char* intToBinaryString(int n) {
    int c, d, count;
    char* pointer;
    count = 0;
    pointer = (char*) malloc(8 + 1);
    for (c = 7; c >= 0; c--) {
        d = n >> c;
        if (d & 1)
            * (pointer + count) = 1 + '0';
        else
            *(pointer + count) = 0 + '0';
        count++;
    }
    *(pointer + count) = '\0';
    return  pointer;
}

// Command handlers. ////////////////////////////////////////////////
// Flips the value of the bit under the pointer.
void plusCommandHandler(struct Node *tape, int *code_ptr) {
    tape->data = !tape->data;
    *code_ptr += 1;
}

// Reads a bit from the input stream, storing it under the pointer.
void commaCommandHandler(char *in, int *in_ptr, struct Node *tape, int *code_ptr) {
    int input_size = strlen(in);
    int current_character = *in_ptr / 8;
    int current_bit = *in_ptr % 8;
    // If the end-of-file has been reached.
    if(current_character >= input_size) {
        tape->data = 0;
        *code_ptr += 1;
        return;
    }
    char *buffer;
    buffer = intToBinaryString(in[current_character]);
    strrev(buffer);
    tape->data = buffer[current_bit] - '0';
    *in_ptr += 1;
    *code_ptr += 1;  
    return;
}

// Outputs the bit under the pointer to the output stream.
void semicolonCommandHandler(struct Node *tape, char *out, int *code_ptr) {
    sprintf(out, "%s%d", out, tape->data);
    *code_ptr += 1;
}

// Moves the pointer left by 1 bit.
void leftarrowCommandHandler(struct Node **tape, int *code_ptr) {
    if((*tape)->prev != NULL) {
        (*tape) = (*tape)->prev;
        *code_ptr += 1;
        return;
    }
    else {
        (*tape)->prev = (struct Node*) malloc(1 * sizeof(struct Node));
        (*tape)->prev->data = 0; 
        (*tape)->prev->prev = NULL; 
        (*tape)->prev->next = (*tape);
        (*tape) = (*tape)->prev;
        *code_ptr += 1;
        return;
    }
}

// Moves the pointer right by 1 bit.
void rightarrowCommandHandler(struct Node **tape, int *code_ptr) {
    if((*tape)->next != NULL) {
        (*tape) = (*tape)->next;
        *code_ptr += 1;
        return;
    }
    else {
        (*tape)->next = (struct Node*) malloc(1 * sizeof(struct Node));
        (*tape)->next->data = 0;
        (*tape)->next->next = NULL;
        (*tape)->next->prev = (*tape);
        (*tape) = (*tape)->next;
        *code_ptr += 1;
        return;
    }
}

// If the value under the pointer is 0 then skip to the corresponding ].
void leftbracketCommandHandler(struct Node *tape, char *code, int *code_ptr) {
    if(tape->data == 1) {
        *code_ptr += 1;
        return;
    }
    else {
        match('[', code, code_ptr);
        return;
    }
}

// If the value under the pointer is 1 jump back to the corresponding [.
void rightbracketCommandHandler(struct Node *tape, char *code, int *code_ptr) {
    if(tape->data == 0) {
        *code_ptr += 1;
        return;
    }
    else {
        match(']', code, code_ptr);
        return;
    }
}

char* boolfuck (char *code, char *in) {
    int *code_ptr = (int*) calloc(1, sizeof(int));
    int *in_ptr = (int*) calloc(1, sizeof(int));
    char current_instruction = code[*code_ptr];
    char *out = (char*) calloc(32768, sizeof(char));
    struct Node *tape = (struct Node*) malloc(1 * sizeof(struct Node));
    tape->data = 0; 
    tape->prev = NULL; 
    tape->next = NULL;
    
    while(current_instruction != '\0') {
        if(current_instruction == '+') plusCommandHandler(tape, code_ptr);
        else if(current_instruction == ',') commaCommandHandler(in, in_ptr, tape, code_ptr);
        else if(current_instruction == ';') semicolonCommandHandler(tape, out, code_ptr);  
        else if(current_instruction == '<') leftarrowCommandHandler(&tape, code_ptr);
        else if(current_instruction == '>') rightarrowCommandHandler(&tape, code_ptr); 
        else if(current_instruction == '[') leftbracketCommandHandler(tape, code, code_ptr); 
        else if(current_instruction == ']') rightbracketCommandHandler(tape, code, code_ptr); 
        else *code_ptr += 1;
        current_instruction = code[*code_ptr];
    }
    char *result = convertToCharacters(out);
    // Free allocated memory.
    free(code_ptr);
    free(in_ptr);
    free(out);
    while(tape->prev != NULL)
        tape = tape->prev;
    while(tape->next != NULL) {
        tape = tape->next;
        free(tape->prev);
    }
    free(tape);
    
    return result;
}
_____________________________
#include <stdlib.h>
#include <string.h>
#define bcase break;case

unsigned char data[100000];
unsigned char *dp = data+50000;

char *boolfuck(char *code, char *in) {
  memset(data, 0, sizeof(data));
  char *out = calloc(1, 10000);
  char *o = out;
  int ib = 0, ob = 0, s;
  while (*code)
    switch (*code++) {
    bcase '+': *dp = !*dp;
    bcase ',':
      if (ib == 8) {
        ib = 0;
        in++;
      }
      if (ib == 0 && *in == 0) {
        *dp = 0;
        break;
      }
      *dp = !!(*in & (1<<ib++));
    bcase ';':
      if (ob == 8)
        ob = 0, o++;
      *o |= *dp << ob++;
    bcase '<': dp--;
    bcase '>': dp++;
    bcase '[':
      if (*dp)
        break;
      for (s = 1; s; code++) {
        if (*code == ']')
          s--;
        if (*code == '[')
          s++;
      }
    bcase ']':
      code -= 2;
      for (s = 1; s; code--) {
        if (*code == ']')
          s++;
        if (*code == '[')
          s--;
      }
      code++;
    }
  return out;
}
_____________________________
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define BUFFSIZE 1024
#define BUFFER 30000
#define MID BUFFER/2
#define CODE *(code + index)

int loop (char *code, int index) {
    int pile = 0;
    const bool fwd = CODE == '[' ? true : false; 

    while (CODE) {
       if (CODE == '[') pile++;
       if (CODE == ']') pile--;
       if (pile == 0) return index;

       fwd == true ? index++ : index--;
    }
    return false;
}
char* boolfuck (char *code, char *input) {
    char *output = calloc (BUFFSIZE , sizeof (char)), *byte = output;
    unsigned index = 0, bit = 0, bin = 0;
    bool tape[BUFFER] = {0}, *data = &tape[MID] ;

    while (CODE) {
        switch (CODE) {
            case '+' : *data = ((*data == 0) ? 1 : 0); break;
            case ',' : if (bin == 8)
                          input++, bin = 0;

                       *data = *input >> bin++ &1;
                       break;

            case ';' : if (bit == 8)
                          byte++, bit = 0;
     
                       *byte += *data << bit++;  // little endian
                       break;

            case '<' : data--; break;
            case '>' : data++; break;
            case '[' : if (*data == NULL) index = loop (code,index); break;
            case ']' : if (*data != NULL) index = loop (code,index); break;
            default : break;
        }
        index++;
        
    }
    while (bit < 8)
        *byte += 0 << bit++;

    *(byte + 1) = '\0';
    return output;
}
