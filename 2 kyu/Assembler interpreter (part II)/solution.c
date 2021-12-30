#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

enum { stackdepth=16 };
char *ip, *callers[stackdepth] = {}, *p, *output;
int regs[26] = {}, lt = 0, eq = 0, gt = 0, sp = stackdepth-1, v, r, x, y;

int (*ws) (int) = isblank, (*num) (int) = isdigit, (*low) (int) = islower;
int noteol (int c) { return c && c!='\n'; }
int notcolon (int c) { return c && c!=':' && !isspace (c); }
int islabel (int c) { return isalnum (c) || c=='_'; }
void skip (int n, int (*equal) (int)) { while (n-- && *ip) ++ip; while (equal (*ip)) ++ip; }
int reg () { return *ip++-'a'; }
int val () { if (low (*ip)) { return regs[reg ()]; } else { v = atoi (ip); skip (1, num); return v; } }
void outs (char *b, char *e) { char *p = output; asprintf (&output, "%s%.*s", p, e-b, b); free (p); }
void outv (int v) { char *p = output; asprintf (&output, "%s%d", p, v); free (p); }
void out () { if (*ip=='\'') { ++ip; outs (ip, p=strchr (ip, '\'')); ip=++p; } else { outv (val ()); }; }

void jump (const char* labels) {
  char *l = ip; skip (0, islabel);
  char *label = calloc (3+ip-l, 1); label[0]='\n'; strncpy (label+1, l, ip-l); label[ip-l+1]=':';
  ip += strstr (labels, label) + 2 - l;
  free (label);
}

char* assembler_interpreter (const char* program) {
  ip = program; output = calloc (1, 1); sp = stackdepth-1;
  while (*ip) {
    skip (0, ws);
    if (!strncmp (ip, "mov ", 4)) {
      skip (4, ws);  r = reg (); skip (1, ws); regs[r] = val ();
    } else if (!strncmp (ip, "inc ", 4)) {
      skip (4, ws);  ++regs[reg ()];
    } else if (!strncmp (ip, "dec ", 4)) {
      skip (4, ws);  --regs[reg ()];
    } else if (!strncmp (ip, "add ", 4)) {
      skip (4, ws);  r = reg (); skip (1, ws); regs[r] += val ();
    } else if (!strncmp (ip, "sub ", 4)) {
      skip (4, ws);  r = reg (); skip (1, ws); regs[r] -= val ();
    } else if (!strncmp (ip, "mul ", 4)) {
      skip (4, ws);  r = reg (); skip (1, ws); regs[r] *= val ();
    } else if (!strncmp (ip, "div ", 4)) {
      skip (4, ws);  r = reg (); skip (1, ws); regs[r] /= val ();
    } else if (!strncmp (ip, "jmp ", 4)) {
      skip (4, ws); jump (program);
    } else if (!strncmp (ip, "cmp ", 4)) {
      skip (4, ws); x = val (); skip (1, ws); y = val (); lt=x<y; eq=x==y; gt=x>y;
    } else if (!strncmp (ip, "jne ", 4)) {
      skip (4, ws); if (!eq) jump (program);
    } else if (!strncmp (ip, "je ", 3)) {
      skip (3, ws); if (eq) jump (program);
    } else if (!strncmp (ip, "jge ", 4)) {
      skip (4, ws); if (!lt) jump (program);
    } else if (!strncmp (ip, "jg ", 3)) {
      skip (3, ws); if (gt) jump (program);
    } else if (!strncmp (ip, "jle ", 4)) {
      skip (4, ws); if (!gt) jump (program);
    } else if (!strncmp (ip, "jl ", 3)) {
      skip (3, ws); if (lt) jump (program);
    } else if (!strncmp (ip, "call ", 5)) {
      skip (5, ws); if (!sp) break; callers[--sp] = 1+strchr (ip, '\n'); jump (program);
    } else if (!strncmp (ip, "msg ", 4)) {
      ip+=3; do { skip (1, ws);  out (); } while (*ip==',');
    } else if (!strncmp (ip, "ret", 3) && (isspace (*(ip+3)) || !*(ip+3))) {
      ip = callers[sp++]; if (sp>=stackdepth) break; continue;
    } else if (!strncmp (ip, "end", 3) && (isspace (*(ip+3)) || !*(ip+3))) {
      return output;
    }
    skip (0, ws); skip (0, *ip==';'?noteol:notcolon); *ip && ++ip;
  }
  return free (output), -1;
}

____________________________________________________
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
/* Disclosure:
 *    Initially intented to implement a Just-In-Time or On-The-Fly-Compiler
 *    but decided the tricks to be left for the next POSSIBLE part three.
 *    Also have thrown MANY DEFS and hashing labels and smth else to make a long story short
 */
#define JMP(arg, src, pos, lim) \
    sprintf((arg) + (lim), ":"); \
    (pos) = strstr((src), (arg)) - (src) + (lim) + 1; \
    continue;
#define RIMM(regs, imm, src, endp) \
    (imm) = strtol((src), &(endp), 10); \
    if (*(endp)) (imm) = (regs)[*(endp) - 'a'];
#define BLKSZ           1024
typedef enum { CPU_ZF, CPU_SF, CPU_NFLAGS } cpuf_t;

unsigned short myhash(const char *s, size_t n)
{
    unsigned short h = 0;
    while (n--) h = (h << 2) + *s++;
    return h;
}

char *assembler_interpreter(const char *src)
{
    size_t stk[BLKSZ << 4], pos, lim, stksz, outpsz, outplen;
    long imm, imm1, regs['z' - 'a' + 1] = { 0 };
    cpuf_t flags[CPU_NFLAGS] = { 0 };
    char arg[BLKSZ], *outp, *s;
    unsigned short ophsh;
    pos = lim = stksz = outpsz = outplen = (size_t)(outp = 0);
    while (src[pos]) {
        pos += strspn(src + pos, " \t\n");
        if (src[pos] == ';') {
            pos += strcspn(src + pos, "\n");
            continue;
        }
        pos += (lim = strcspn(src + pos, " \t\n"));
        if (src[pos - 1] == ':')
            continue;
        switch (ophsh = myhash(src + pos - lim, lim)) {
        case 2344:  /* OP_RET */
            if (!stksz)
                return (char *)-1;
            pos = stk[--stksz];
            continue;
        case 2156:  /* OP_END */
            return outp ? outp : (char *)-1;
        }
        pos += strspn(src + pos, " \t");
        if (ophsh == 2307) /* OP_MSG */ {
            while (src[pos] != ';' && src[pos] != '\n') {
                if (src[pos] == '\'')
                    pos += (lim = strcspn(s = (char *)src + pos + 1, "'")) + 2;
                else
                    lim = sprintf(s = arg, "%ld", regs[src[pos++] - 'a']);
                if (outplen + lim > outpsz && !(outp = realloc(outp, outpsz = outpsz << 1 | BLKSZ)))
                    return free(outp), (char *)-1;
                outplen += sprintf(outp + outplen, "%.*s", (int)lim, s);
                pos += strspn(src + pos, ", \t");
            }
            continue;
        }
        lim = strcspn(src + pos, ", \t\n");
        sprintf(arg, "%.*s", (int)lim, src + pos);
        switch (ophsh) {
        case 2219:  /* OP_INC */
            ++regs[src[pos++] - 'a'];
            continue;
        case 2103:  /* OP_DEC */
            --regs[src[pos++] - 'a'];
            continue;
        case 525:       /* OP_JE */
            if (flags[CPU_ZF])
                JMP(arg, src, pos, lim);
        case 527:   /* OP_JG */
            if (!flags[CPU_ZF] && !flags[CPU_SF])
                JMP(arg, src, pos, lim);
        case 532:   /* OP_JL */
            if (!flags[CPU_ZF] && flags[CPU_SF])
                JMP(arg, src, pos, lim);
        case 2209:  /* OP_JGE */
            if (flags[CPU_ZF] || !flags[CPU_SF])
                JMP(arg, src, pos, lim);
        case 2229:  /* OP_JLE */
            if (flags[CPU_ZF] || flags[CPU_SF])
                JMP(arg, src, pos, lim);
        case 2237:  /* OP_JNE */
            if (!flags[CPU_ZF])
                JMP(arg, src, pos, lim);
        case 2244:  /* OP_JMP */
            JMP(arg, src, pos, lim);
        case 8428:  /* OP_CALL */
            stk[stksz++] = pos + lim;
            JMP(arg, src, pos, lim);
        }
        pos += lim;
        pos += strspn(src + pos, ", \t");
        lim = strcspn(src + pos, " \t\n");
        sprintf(arg + (BLKSZ >> 1), "%.*s", (int)lim, src + pos);
        RIMM(regs, imm1, arg + (BLKSZ >> 1), s);
        RIMM(regs, imm, arg, s);
        pos += lim;
        if (ophsh == 2132)          /* OP_CMP */
            if (!(imm - imm1))
                flags[CPU_ZF] = 1;
            else
                flags[CPU_SF] = imm - imm1 < 0, flags[CPU_ZF] = 0;
        else {
            if (ophsh == 2052)      /* OP_ADD */
                imm1 += imm;
            else if (ophsh == 2138) /* OP_DIV */
                imm1 = imm / imm1;
            else if (ophsh == 2320) /* OP_MUL */
                imm1 *= imm;
            else if (ophsh == 2406) /* OP_SUB */
                imm1 = imm - imm1;
            regs[*arg - 'a'] = imm1; /* OP_MOV (detect yourself) */
        }
    }
    if (outp)
        free(outp);
    return (char *)-1;
}

____________________________________________________
#import <string.h>

#define INST_LIMIT 50
#define CHAR_LIMIT 80

int find_label_line(char instructions[INST_LIMIT][CHAR_LIMIT], char label[]) {
  char alabel[CHAR_LIMIT]; int a;
  for (int line = 0; line < INST_LIMIT; line++) {
    a = 0;
    for (int i = 0; i < CHAR_LIMIT; i++) {
      if (instructions[line][i] == ':') {
        alabel[a+1] = 0;
        int equals = 1;
        for (int k = 0; label[k] != 0; k++) {
          if (label[k] != alabel[k]) { equals = 0; }
        }
        if (equals) {
          return line;
        }
      }
      if (instructions[line][i] != ' ') {
        alabel[a++] = instructions[line][i];
      }
    }
  }
  return -1;
}

char* assembler_interpreter (const char* program) {
  printf("%s\n", program);
  
  // parse code into set of array instructions
  char instructions[INST_LIMIT][CHAR_LIMIT];
  
  int line = 0, ch = 0;
  for (int i = 0; program[i] != 0; i++) {
    if (program[i] == '\n') {
      instructions[line][ch] = 0;
      line++; 
      ch = 0;
    } else {  
      instructions[line][ch] = program[i];
      ch++;
    }
  }
  
//   // Print Instructions
//   for (line = 0; line < 30; line++) {
//     printf("%d\t%s\n", line, instructions[line]); 
//   }
//   printf("\n\n");
  
  // Registers & Initilaization
  int a = 0, b = 0, c = 0, d = 0, e = 0, x, y, cmpflag = 0;
  int f = 0, g = 0, h = 0, i = 0, j = 0, k = 0, l = 0, m = 0,
      n = 0, o = 0, p = 0, q = 0, r = 0, s = 0, t = 0, u = 0,
      v = 0, w = 0, x0 = 0, y0 = 0, z = 0;
  int returnline[10], returnlinep = 0;
  char *output = calloc(CHAR_LIMIT, sizeof(char));
  char label[CHAR_LIMIT];
  char command[5];
  int end = 0;
  int loop_counter = 0;
  
  // Loop Execution
  line = 0;
  while (!end) {
    int eof = 0;
    for (int ii = 0; ii < CHAR_LIMIT; ii++) {
      if (instructions[line][ii] == '\26') { 
        eof = 1;
        break; 
      }
    }
    if (eof) break;
    
    printf("%d %d %s\n", loop_counter, line, instructions[line]);
    for (int ki = 0; ki < CHAR_LIMIT; ki++) {
      command[ki] = 0;
    }
    for (ch = 0; ch < CHAR_LIMIT; ch++) {
      if (instructions[line][ch] != ';'  && 
          instructions[line][ch] != ' '  &&
          instructions[line][ch] != '\t' &&
          instructions[line][ch] != '\n' ) {
        for (int ki = 0; ki < CHAR_LIMIT; ki++) {
          if (instructions[line][ch+ki] == ';'  || 
            instructions[line][ch+ki] == ' '  ||
            instructions[line][ch+ki] == '\t' ||
            instructions[line][ch+ki] == '\n' ) {
            command[ki] = 0;
            ch += ki;
            break;
          } else { 
            command[ki] = instructions[line][ch+ki];
          }
        }
        break;
      }
      if (instructions[line][ch] == ';') {
        break;
      }
    }
    
    // obtain y if possible
    if ( !strcmp(command, "mov") |
         !strcmp(command, "add") |
         !strcmp(command, "sub") |
         !strcmp(command, "mul") |
         !strcmp(command, "div") |
         !strcmp(command, "cmp") ) {
      int ti = 1, ji = ch;
      while(instructions[line][ji] == ' ') ji++;
      char num[CHAR_LIMIT];
      switch(instructions[line][ji+3]) {
        case 'a': y = a; break;
        case 'b': y = b; break;
        case 'c': y = c; break;
        case 'd': y = d; break;
        case 'e': y = e; break;
        case 'f': y = f; break;
        case 'g': y = g; break;
        case 'h': y = h; break;
        case 'i': y = i; break;
        case 'j': y = j; break;
        case 'k': y = k; break;
        case 'l': y = l; break;
        case 'm': y = m; break;
        case 'n': y = n; break;
        case 'o': y = o; break;
        case 'p': y = p; break;
        case 'q': y = q; break;
        case 'r': y = r; break;
        case 's': y = s; break;
        case 't': y = t; break;
        case 'u': y = u; break;
        case 'v': y = v; break;
        case 'w': y = w; break;
        case 'x': y = x0; break;
        case 'y': y = y0; break;
        case 'z': y = z; break;
        default:
          for (int ii = 3; ii+j < CHAR_LIMIT; ii++) {
            if (instructions[line][ji+ii] >= '0' && instructions[line][ji+ii] <= '9') {
              num[ii-3] = instructions[line][ji+ii];
            } else {
              num[ii-3] = 0;
              break; 
            }
          }
          y = atoi(num);
      }
    }
    
    
    // obtain label if possible
    if ( !strcmp(command, "call") |
         !strcmp(command, "jmp") |
         !strcmp(command, "jne") |
         !strcmp(command, "je") |
         !strcmp(command, "jge") |
         !strcmp(command, "jg") |
         !strcmp(command, "jle") |
         !strcmp(command, "jl") ) {
      int ji = ch;
      while(instructions[line][ji] == ' ' || instructions[line][ji] == '\t') ji++;
      for (int ii = 0; ii < CHAR_LIMIT; ii++) {
        if (instructions[line][ii+ji] != ';'  || 
            instructions[line][ii+ji] != ' '  ||
            instructions[line][ii+ji] != '\t' ||
            instructions[line][ii+ji] != '\n' ) {
          label[ii] = instructions[line][ii+ji];
        } else {
          label[ii] = 0;
          break;
        }
      }
    }
    
    
    if (!strcmp(command, "mov")) { while(instructions[line][ch] == ' ') ch++;
      switch(instructions[line][ch]) {
        case 'a': a = y; break;
        case 'b': b = y; break;
        case 'c': c = y; break;
        case 'd': d = y; break;
        case 'e': e = y; break;
        case 'f': f = y; break;
        case 'g': g = y; break;
        case 'h': h = y; break;
        case 'i': i = y; break;
        case 'j': j = y; break;
        case 'k': k = y; break;
        case 'l': l = y; break;
        case 'm': m = y; break;
        case 'n': n = y; break;
        case 'o': o = y; break;
        case 'p': p = y; break;
        case 'q': q = y; break;
        case 'r': r = y; break;
        case 's': s = y; break;
        case 't': t = y; break;
        case 'u': u = y; break;
        case 'v': v = y; break;
        case 'w': w = y; break;
        case 'x': x0 = y; break;
        case 'y': y0 = y; break;
        case 'z': z = y; break;
      }
    } else
    if (!strcmp(command, "inc")) { while(instructions[line][ch] == ' ') ch++;
      switch(instructions[line][ch]) {
        case 'a': a++; break;
        case 'b': b++; break;
        case 'c': c++; break;
        case 'd': d++; break;
        case 'e': e++; break;
        case 'f': f++; break;
        case 'g': g++; break;
        case 'h': h++; break;
        case 'i': i++; break;
        case 'j': j++; break;
        case 'k': k++; break;
        case 'l': l++; break;
        case 'm': m++; break;
        case 'n': n++; break;
        case 'o': o++; break;
        case 'p': p++; break;
        case 'q': q++; break;
        case 'r': r++; break;
        case 's': s++; break;
        case 't': t++; break;
        case 'u': u++; break;
        case 'v': v++; break;
        case 'w': w++; break;
        case 'x': x0++; break;
        case 'y': y0++; break;
        case 'z': z++; break;
      }
    } else
    if (!strcmp(command, "dec")) { while(instructions[line][ch] == ' ') ch++;
      switch(instructions[line][ch]) {
        case 'a': a--; break;
        case 'b': b--; break;
        case 'c': c--; break;
        case 'd': d--; break;
        case 'e': e--; break;
        case 'f': f--; break;
        case 'g': g--; break;
        case 'h': h--; break;
        case 'i': i--; break;
        case 'j': j--; break;
        case 'k': k--; break;
        case 'l': l--; break;
        case 'm': m--; break;
        case 'n': n--; break;
        case 'o': o--; break;
        case 'p': p--; break;
        case 'q': q--; break;
        case 'r': r--; break;
        case 's': s--; break;
        case 't': t--; break;
        case 'u': u--; break;
        case 'v': v--; break;
        case 'w': w--; break;
        case 'x': x0--; break;
        case 'y': y0--; break;
        case 'z': z--; break;
      }
    } else
    if (!strcmp(command, "add")) { while(instructions[line][ch] == ' ') ch++;
      switch(instructions[line][ch]) {
        case 'a': a += y; break;
        case 'b': b += y; break;
        case 'c': c += y; break;
        case 'd': d += y; break;
        case 'e': e += y; break;
        case 'f': f += y; break;
        case 'g': g += y; break;
        case 'h': h += y; break;
        case 'i': i += y; break;
        case 'j': j += y; break;
        case 'k': k += y; break;
        case 'l': l += y; break;
        case 'm': m += y; break;
        case 'n': n += y; break;
        case 'o': o += y; break;
        case 'p': p += y; break;
        case 'q': q += y; break;
        case 'r': r += y; break;
        case 's': s += y; break;
        case 't': t += y; break;
        case 'u': u += y; break;
        case 'v': v += y; break;
        case 'w': w += y; break;
        case 'x': x0 += y; break;
        case 'y': y0 += y; break;
        case 'z': z += y; break;
      }
    } else
    if (!strcmp(command, "sub")) { while(instructions[line][ch] == ' ') ch++;
      switch(instructions[line][ch]) {
        case 'a': a -= y; break;
        case 'b': b -= y; break;
        case 'c': c -= y; break;
        case 'd': d -= y; break;
        case 'e': e -= y; break;
        case 'f': f -= y; break;
        case 'g': g -= y; break;
        case 'h': h -= y; break;
        case 'i': i -= y; break;
        case 'j': j -= y; break;
        case 'k': k -= y; break;
        case 'l': l -= y; break;
        case 'm': m -= y; break;
        case 'n': n -= y; break;
        case 'o': o -= y; break;
        case 'p': p -= y; break;
        case 'q': q -= y; break;
        case 'r': r -= y; break;
        case 's': s -= y; break;
        case 't': t -= y; break;
        case 'u': u -= y; break;
        case 'v': v -= y; break;
        case 'w': w -= y; break;
        case 'x': x0 -= y; break;
        case 'y': y0 -= y; break;
        case 'z': z -= y; break;
      }
    } else
    if (!strcmp(command, "mul")) { while(instructions[line][ch] == ' ') ch++;
      switch(instructions[line][ch]) {
        case 'a': a *= y; break;
        case 'b': b *= y; break;
        case 'c': c *= y; break;
        case 'd': d *= y; break;
        case 'e': e *= y; break;
        case 'f': f *= y; break;
        case 'g': g *= y; break;
        case 'h': h *= y; break;
        case 'i': i *= y; break;
        case 'j': j *= y; break;
        case 'k': k *= y; break;
        case 'l': l *= y; break;
        case 'm': m *= y; break;
        case 'n': n *= y; break;
        case 'o': o *= y; break;
        case 'p': p *= y; break;
        case 'q': q *= y; break;
        case 'r': r *= y; break;
        case 's': s *= y; break;
        case 't': t *= y; break;
        case 'u': u *= y; break;
        case 'v': v *= y; break;
        case 'w': w *= y; break;
        case 'x': x0 *= y; break;
        case 'y': y0 *= y; break;
        case 'z': z *= y; break;
      }
    } else
    if (!strcmp(command, "div")) { while(instructions[line][ch] == ' ') ch++;
      switch(instructions[line][ch]) {
        case 'a': a /= y; break;
        case 'b': b /= y; break;
        case 'c': c /= y; break;
        case 'd': d /= y; break;
        case 'e': e /= y; break;
        case 'f': f /= y; break;
        case 'g': g /= y; break;
        case 'h': h /= y; break;
        case 'i': i /= y; break;
        case 'j': j /= y; break;
        case 'k': k /= y; break;
        case 'l': l /= y; break;
        case 'm': m /= y; break;
        case 'n': n /= y; break;
        case 'o': o /= y; break;
        case 'p': p /= y; break;
        case 'q': q /= y; break;
        case 'r': r /= y; break;
        case 's': s /= y; break;
        case 't': t /= y; break;
        case 'u': u /= y; break;
        case 'v': v /= y; break;
        case 'w': w /= y; break;
        case 'x': x0 /= y; break;
        case 'y': y0 /= y; break;
        case 'z': z /= y; break;
      }
    } else
    if (!strcmp(command, "call")) { while(instructions[line][ch] == ' ') ch++;
      returnline[returnlinep++] = line;
      line = find_label_line(instructions, label);
    } else
    if (!strcmp(command, "jmp")) {
      line = find_label_line(instructions, label);
    } else
    if (!strcmp(command, "cmp")) { while(instructions[line][ch] == ' ') ch++;
      char num[CHAR_LIMIT];
      switch(instructions[line][ch]) {
        case 'a': x = a; break;
        case 'b': x = b; break;
        case 'c': x = c; break;
        case 'd': x = d; break;
        case 'e': x = e; break;
        case 'f': x = f; break;
        case 'g': x = g; break;
        case 'h': x = h; break;
        case 'i': x = i; break;
        case 'j': x = j; break;
        case 'k': x = k; break;
        case 'l': x = l; break;
        case 'm': x = m; break;
        case 'n': x = n; break;
        case 'o': x = o; break;
        case 'p': x = p; break;
        case 'q': x = q; break;
        case 'r': x = r; break;
        case 's': x = s; break;
        case 't': x = t; break;
        case 'u': x = u; break;
        case 'v': x = v; break;
        case 'w': x = w; break;
        case 'x': x = x0; break;
        case 'y': x = y0; break;
        case 'z': x = z; break;
        default:
          for (int ii = 3; ii+ch < CHAR_LIMIT; ii++) {
            if (instructions[line][ch+ii] > '0' && instructions[line][ch+ii] < '9') {
              num[ii-3] = instructions[line][ch+ii];
            } else {
              num[ii-3] = 0;
              break; 
            }
          }
          x = atoi(num);
      }
      
      cmpflag = x != y ? cmpflag | 0x01 : cmpflag & 0x3e;
      cmpflag = x == y ? cmpflag | 0x02 : cmpflag & 0x3d;
      cmpflag = x >= y ? cmpflag | 0x04 : cmpflag & 0x3b;
      cmpflag = x >  y ? cmpflag | 0x08 : cmpflag & 0x37;
      cmpflag = x <= y ? cmpflag | 0x10 : cmpflag & 0x2f;
      cmpflag = x <  y ? cmpflag | 0x20 : cmpflag & 0x1f;
      
    } else
    if (!strcmp(command, "jne")) {
      if (cmpflag & 0x01)
        line = find_label_line(instructions, label);      
    } else
    if (!strcmp(command, "je")) {
      if (cmpflag & 0x02)
        line = find_label_line(instructions, label);      
    } else
    if (!strcmp(command, "jge")) {
      if (cmpflag & 0x04)
        line = find_label_line(instructions, label);      
    } else
    if (!strcmp(command, "jg")) {
      if (cmpflag & 0x08)
        line = find_label_line(instructions, label);      
    } else
    if (!strcmp(command, "jle")) {
      if (cmpflag & 0x10)
        line = find_label_line(instructions, label);      
    } else
    if (!strcmp(command, "jl")) {
      if (cmpflag & 0x20)
        line = find_label_line(instructions, label);      
    } else
    if (!strcmp(command, "ret")) {
      line = returnline[--returnlinep];
    } else
    if (!strcmp(command, "msg")) { 
      while(instructions[line][ch] == ' ') ch++;
      
      int out = 0;
      while (out < CHAR_LIMIT) {
        if (instructions[line][ch] == '\'') {
          ch++;
          while (instructions[line][ch] != '\'') {
            output[out++] = instructions[line][ch++];
          }
          ch++;
        } else {
          int num;
          switch (instructions[line][ch]) {
            case 'a': num = a; break;
            case 'b': num = b; break;
            case 'c': num = c; break;
            case 'd': num = d; break;
            case 'e': num = e; break;
            case 'f': num = f; break;
            case 'g': num = g; break;
            case 'h': num = h; break;
            case 'i': num = i; break;
            case 'j': num = j; break;
            case 'k': num = k; break;
            case 'l': num = l; break;
            case 'm': num = m; break;
            case 'n': num = n; break;
            case 'o': num = o; break;
            case 'p': num = p; break;
            case 'q': num = q; break;
            case 'r': num = r; break;
            case 's': num = s; break;
            case 't': num = t; break;
            case 'u': num = u; break;
            case 'v': num = v; break;
            case 'w': num = w; break;
            case 'x': num = x0; break;
            case 'y': num = y0; break;
            case 'z': num = z; break;
          }
          if (num == 0) {
            output[out++] = '0';
          }
          if (num < 0) {
            output[out++] = '-';
            num *= -1;
          }
          char str[20]; int pi;
          while (num != 0) {
            int rem = num % 10;
            str[pi++] = rem + '0';
            num /= 10;
          }
          while (pi > 0) {
            output[out++] = str[--pi];
          }
          ch++;
        }
        
        if (instructions[line][ch] != ',') break;
        ch += 2;
      }
      output[out] = 0;
    } else
    if (!strcmp(command, "end")) {
      
      return output;
    }
    
    printf("'%s' x=%d y=%d\ncmp=%d l='%s' ret=",
           command, x, y, cmpflag, label);
    for (int si = 0; si < returnlinep; si++) {
      printf("%d ", returnline[si]);
    }
    printf("\n");
    if (a != 0) printf("a=%d ", a);
    if (b != 0) printf("b=%d ", b);
    if (c != 0) printf("c=%d ", c);
    if (d != 0) printf("d=%d ", d);
    if (e != 0) printf("e=%d ", e);
    if (f != 0) printf("f=%d ", f);
    if (g != 0) printf("g=%d ", g);
    if (h != 0) printf("h=%d ", h);
    if (i != 0) printf("i=%d ", i);
    if (j != 0) printf("j=%d ", j);
    if (k != 0) printf("k=%d ", k);
    if (l != 0) printf("l=%d ", l);
    if (m != 0) printf("m=%d ", m);
    if (n != 0) printf("n=%d ", n);
    if (o != 0) printf("o=%d ", o);
    if (p != 0) printf("p=%d ", p);
    if (q != 0) printf("q=%d ", q);
    if (r != 0) printf("r=%d ", r);
    if (s != 0) printf("s=%d ", s);
    if (t != 0) printf("t=%d ", t);
    if (u != 0) printf("u=%d ", u);
    if (v != 0) printf("v=%d ", v);
    if (w != 0) printf("w=%d ", w);
    if (x0 != 0) printf("x=%d ", x0);
    if (y0 != 0) printf("y=%d ", y0);
    if (z != 0) printf("z=%d ", z);
    printf("\n\n");
    
    line++;
    loop_counter++;    
    if (loop_counter > 100 || line > INST_LIMIT) {
      printf("Program ran too long / far\n");
      return -1;
    }
  }
  
  return -1;
}

____________________________________________________
#define _GNU_SOURCE

#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#define dbg0(...) /*__VA_ARGS__*/
#define dbgx(...) /*__VA_ARGS__*/
#define dbg1(...) /*__VA_ARGS__*/
#define dbg2(...) /*__VA_ARGS__*/

enum          TokID {_mov,_inc,_dec,_add,_sub,_mul,_div,_jmp,_cmp,_jne,_je,_jge,_jg,_jle,_jl,_call,_ret,_msg,_end };
const char *pzCmds="\3mov\3inc\3dec\3add\3sub\3mul\3div\3jmp\3cmp\3jne\2je\3jge\2jg\3jle\2jl\4call\3ret\3msg\3end\0";
const char   Parm[]={0x31,0x01,0x01,0x31,0x31,0x31,0x31,  8 ,0x31,  8 , 8 ,  8 , 8 ,  8 , 8 ,  8  , 0x0, -1 , 0x0 };
dbg0(const char *zParm[]={"","Reg ","Imm ","Reg/Imm ","Str ","5?","6?","...","Label","9?","10?","11?","12?","13?","14?","Varargs"};)

int GetToken( const char* pzTok, int iLen) {  
  if (iLen<2 || iLen>4) { return -1; }
  int iNum=0,iSz,iPos=0;
  while ((iSz=pzCmds[iPos++])) {
    if ((iLen==iSz) && (!memcmp(pzCmds+iPos,pzTok,iSz))) return iNum;
    iNum++ ; iPos += iSz;
  }
  return -1;
}
int GetLabel( const char* pzName, int iLen, const char* pzLabels) {  
  int iSz,iPos=0;
  while ((iSz=pzLabels[iPos++])) {
    dbg2(printf("{%i '%s'}\n",iSz,pzLabels+iPos);)
    if ((iLen==iSz) && (!memcmp(pzLabels+iPos,pzName,iSz))) return *((int*)(pzLabels+iPos+iSz));
    iPos += iSz+4;
  }
  return -1;
}

char* GenerateBytecode( const char* program ) {
  char *bytecode = malloc(4096), *label = malloc(4096); int *forward = malloc(4096);
  char iTokType=0,iCmd=-1,iParm=0,iTokSz=0, iDone=0;; *label=0;
  int iToken=-1,iLine=0,iCmdPos=0,iPos=0,iLabel=0,iForward=0,iOut=0,iChar=0;  
      
  dbg0(
    char *tmp,*dbg = strdup(program);  
    if ((tmp = strchr(dbg+iPos,'\n'))) { *tmp=0; printf("%03i [%s]\n",0,dbg+iPos); }
  )
    
  while ((iChar=program[iPos++]),!iDone) {
    dbg2(printf("%i %i %c\n",iPos-1,iChar,iChar<32?'?':iChar);)
    //exception for the case a command have no arguments and no spaces after the command
    if ((iChar=='\r' || iChar=='\n') && iToken!=-1 && iCmd==-1) { iChar=' ';iPos--; }
    switch (iChar) {    
    case ' ': case 9: case 0://found space ignore spaces
      {
        if (iCmd==-1 && iToken!=-1) {
          //process command token
          bytecode[iOut++] = (iCmd = GetToken(program+iToken,iTokSz))*2;
          iParm=Parm[(int)iCmd];          
          dbg1(char iL=dbg[iToken+iTokSz]; dbg[iToken+iTokSz]=0; printf("token='(%i)%s' %s%s\n",iCmd,dbg+iToken,zParm[iParm&15],zParm[(iParm>>4)&7]); dbg[iToken+iTokSz]=iL;)
          iToken=-1; iCmdPos=iOut-1; iTokType=0; iTokSz=0;
        }        
        if (!iChar) { iDone++ ; continue; }
        //printf("[%i %i %c]\n",iPos-1,iChar,iChar<32?'?':iChar);
        while ((iChar=program[iPos])==' ' || iChar==9) iPos++;
        continue;
      }
    case ',': //next parameter (falltrough)
      {
        dbg0(
          if (iCmd==-1) { printf("expected command, found ',' at '%s'\n",dbg+iLine); return NULL; }
          if (iToken==-1) { printf("expected parameter, found ',' at '%s'\n",dbg+iLine); return NULL; }
          if (!iParm) { printf("parameter count mismatch at '%s'\b",dbg+iLine); return NULL; }
        )
      }
    case '\n': case '\r': //end of line
      { 
        dbg1(
          if (iToken!=-1 || iParm) printf("iParm=%X iToken=%i iTokType=%i iTokSz=%i\n",iParm&255,iToken,iTokType,iTokSz);
          if (iToken!=-1) {
            char old = dbg[iToken+iTokSz]; dbg[iToken+iTokSz] = 0;
            printf("Parm={%s}\n",dbg+iToken); dbg[iToken+iTokSz] = old;
          }          
        )
        dbg0(if ((iChar != ',') && (iParm>=0x10)) { printf("expected paramater, found end of line at '%s'\n",dbg+iLine); return NULL; })
        if (iParm && iToken!=-1) {
          if (((iParm & 0xF)==8) && iTokType==1) iTokType=8; //registers and labels can be 1 char 
          dbg0(if (!((iParm & 0xF) & iTokType)) { printf("Bad Parameter at '%s'",dbg+iLine); return NULL; })
          if (iCmd==_msg) bytecode[iOut++]=iTokType;
          if (iTokType==1) { bytecode[iOut++]=(program[iToken]|32)-'a';} //which register
          if (iTokType==2) { bytecode[iCmdPos]|=1; *((int*)(bytecode+iOut))=atoi(program+iToken); iOut+=4; } //immediate
          if (iTokType==4) { memcpy(bytecode+iOut,program+iToken,++iTokSz); iOut += iTokSz; bytecode[iOut++]=0; } //string
          if (iTokType==8) { 
            int iOffset = GetLabel(program+iToken,iTokSz,label);
            //if label does not exist yet, add it to the forward jump list
            dbg1(if (iOffset==-1) printf("adding forward: '%s' sz=%i\n",dbg+iToken,iTokSz);)
            if (iOffset==-1) { iOffset=(iToken<<8)+iTokSz; forward[iForward++]=iOut; }
            *((int*)(bytecode+iOut))=iOffset; iOut+=4; 
          }
          if (iToken=-1 , iParm >>= 4 , iChar == ',') { iTokSz=0; iTokType=0; continue; }
        }        
        if (iCmd==_msg) bytecode[iOut++]=0;
        dbg0(
          if (iToken!=-1) { puts("Premature end of line..."); return NULL; }
          if ((tmp = strchr(dbg+iPos,'\n'))) { *tmp=0; if (dbg[iPos]) (printf("%03i [%s]\n",iOut,dbg+iPos));}
        )
        iParm=0; iTokSz=0; iTokType=0; iCmd=-1; iLine=iPos; iToken=-1; continue;
      }
    case ':': //label
      {
        //not checking for duplicated label or if it first token        
        dbg1(char iL=dbg[iToken+iTokSz]; dbg[iToken+iTokSz]=0; printf("New Label: '%s'(%i)\n",dbg+iToken,iTokSz); dbg[iToken+iTokSz]=iL;)
        label[iLabel] = iTokSz; iLabel += iTokSz+5; //label sz
        memcpy(label+iLabel-(iTokSz+4),program+iToken,iTokSz); //label name        
        *(int*)(label+iLabel-4) = iOut; label[iLabel]=0;//label offset        
        iLine=iPos; iToken=-1; iTokType=8; iTokSz=0; continue;
      }
    case '0'...'9': case '-': //number
      { //not validating if - is on correct place lol
        if (iToken==-1) { iToken=iPos-1 ; iTokType=2; }
        iTokSz++; continue;
      }
    case '\'': //string
      {
        if (iToken==-1) { iToken=iPos ; iTokType=4 ; while ((iChar=program[++iPos])!='\'') {iTokSz++;} iPos++; }
        continue;
      }
    case 'A'...'Z': case 'a'...'z': case '_': case '.': //label or register
      {
        //set token start if not did already
        if (iToken==-1) { 
          iToken=iPos-1; iTokType=1; 
        } else {
          dbg0(
            if ((iTokType)==2) {              
              printf("invalid number at '%s'\n",dbg+iLine);
              return NULL;
            }
          )
          if (iTokType==1) iTokType=8; //becomes label if >1
        }
        iTokSz++; continue;
      }
    case ';': //comment
      {
        //locate end of line
        while ((iChar=program[++iPos])!='\n');        
        continue;
      }
    default: //unknown
      {
        dbg0(
          printf("Invalid char '%c' at '%s'\n",iChar,dbg+iLine);
          return NULL;
        )
      }
    }
  }
  //process forward labels
  for (int i=0;i<iForward;i++) {
    int* piOffset = (int*)(bytecode+forward[i]);
    int iLabelOff = (*piOffset)>>8, iLabelSz = (*piOffset)&255;
    dbg2(printf("resolving forward: %i='%s' %i\n",iLabelOff,dbg+iLabelOff,iLabelSz);)
    *piOffset = GetLabel(program+iLabelOff,iLabelSz,label);
    dbg0(if ((*piOffset)==-1) { dbg[iLabelOff+iLabelSz]=0; printf("Failed to locate label '%s'\n",dbg+iLabelOff); })
  }
  
  bytecode[iOut++] = -1;
  free(forward); free(label);
  return bytecode;
}

char* assembler_interpreter (const char* program) {
  
  dbg0(setvbuf(stdout,NULL,_IONBF,0);)
  char *bytecode = GenerateBytecode(program), *result = malloc(4096);
  int iResuSz=0,iP=0,iSz=0,iParm,iOpcode=0,iSub=0, Regs[32]={0};
  int CallStack[32], iStack=0;
  
  #define Disasm0(_S) dbgx(printf("%03i: %s\n",iP-1,_S)); continue;
  #define DisasmJ(_S) dbgx(printf("%03i: %s :%i\n",iP-1,_S,*(int*)(bytecode+iP))); continue;
  #define Disasm1(_S) dbgx(printf("%03i: %s %c\n",iP-1,_S,bytecode[iP]+'a')); continue;
  #define Disasm2(_S) dbgx(printf("%03i: %s ",iP-1,_S);if (iParm==31){ printf("%c,%i\n",bytecode[iP]+'a',Regs[iParm]); } else { printf("%c,%c\n",bytecode[iP]+'a',iParm+'a'); };) continue;
  #define DoOpc(_Op,_Pa) Regs[(int)bytecode[iP]] _Op _Pa
  #define DoTst(_Op,_Pa) iSub = (Regs[(int)bytecode[iP]] _Op _Pa)
  #define DoJmp(_C) if ((iSub _C)) { iSz=*(int*)(bytecode+iP)-iP; } else { iSz=4; }
  #define DoCall() CallStack[iStack++]=iP+4; DoJmp(|1)
  #define DoRet() iSz=CallStack[--iStack]-iP;
  #define None ;iSz--;
  #define Parm2 Regs[iParm]
  
  dbg0(puts("-----------------------------------------------");)
    
  while (iOpcode != (_end*2)) {        
    iP += iSz; iSz=1; iOpcode=bytecode[iP++];
    
    //for (int i=-1;i<15;i++) printf("%i ",bytecode[iP+i]); puts("");
    //for (int i=0;i<3;i++) printf("%c=%i ",i+'a',Regs[i]); printf("flags=[%i]\n",iSub);
    
    if (iOpcode&1) { iParm=31; Regs[31]=*(int*)(bytecode+iP+1); iSz=5; } else { iParm=bytecode[iP+1]; iSz=2; }
    switch ( (iOpcode>>1) ) {
      case _mov: DoOpc( =,Parm2); Disasm2("mov");
      case _inc: DoOpc(++, None); Disasm1("inc");
      case _dec: DoOpc(--, None); Disasm1("dec");
      case _add: DoOpc(+=,Parm2); Disasm2("add");
      case _sub: DoOpc(-=,Parm2); Disasm2("sub");
      case _mul: DoOpc(*=,Parm2); Disasm2("mul");
      case _div: DoOpc(/=,Parm2); Disasm2("div");
      case _jmp: DoJmp(||1)     ; DisasmJ("jmp");
      case _cmp: DoTst( -,Parm2); Disasm2("cmp");
      case _jne: DoJmp(!=0)     ; DisasmJ("jne");
      case _je : DoJmp(==0)     ; DisasmJ("je" );
      case _jge: DoJmp(>=0)     ; DisasmJ("jge");
      case _jg : DoJmp( >0)     ; DisasmJ("jg" );
      case _jle: DoJmp(<=0)     ; DisasmJ("jle");
      case _jl : DoJmp( <0)     ; DisasmJ("jl" );
      case _call:DoCall()       ; DisasmJ("call");        
      case _ret: DoRet()        ; Disasm0("ret");        
      case _msg:
        {
          iSz=0; dbgx(printf("%03i: %s",iP-1,"msg '"));
          while ((iParm=bytecode[iP+iSz++])) {            
            switch (iParm) {
            case 1: //Register Content 
              dbgx(printf("%i", Regs[(int)bytecode[iP+iSz]]);)
              iResuSz += sprintf(result+iResuSz,"%i",Regs[(int)bytecode[iP+iSz]]); 
              iSz++; break;
            case 2: //Immediate Number
              dbgx(printf("%i", *(int*)(bytecode+iP+iSz));)
              iResuSz += sprintf(result+iResuSz,"%i",*(int*)(bytecode+iP+iSz)); 
              iSz += 4; break;
            case 4: //Immediate String
              dbgx(printf("%s",bytecode+iP+iSz);)
              iResuSz += sprintf(result+iResuSz,"%s",bytecode+iP+iSz);
              iSz += strlen(bytecode+iP+iSz)+1; break;
            default:
              dbgx(puts("Bad msg type...");) return NULL;
            }
          }
          dbgx(puts("'");); continue;
        }
      case _end:                ; Disasm0("end");        
      case -1  : free(result); result = (void*)-1; iOpcode = _end*2;
    }
  }

  free(bytecode);
  return result;
}

        Best Practices0
        Clever1
    0
    Fork
    Link

br4dp1tt

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct label {
  char* identifier;
  int address;
} Label;

typedef struct reg {
  char* name;
  int value;
} Register;

/*
  Remove comments and unnecessary whitespace & create a symbol table for labels
  Create an array of commands
*/
int* first_pass(const char* code, char* commands[], Label* symbol_table[]) {
  int* sizes = malloc(sizeof(int) * 2);
  char source_code[strlen(code) + 1];
  strncpy(source_code, code, strlen(code) + 1);
  const char s[2] = "\n";

  int k = 0;
  char* token = strtok(source_code, s);
  while (token != NULL) {
    char cur_command[256];
    int i = 0, j = 0, end_ind = strlen(token) - 1;

    while (token[i] == ' ' || token[i] == '\t') {
      i++;
    }

    while (token[end_ind] == ' ' || token[end_ind] == '\t') {
      end_ind--;
    }

    while (token[i] != ';' && token[i] != '\0' && i <= end_ind) {
      cur_command[j++] = token[i++];
    }

    if (j > 0) {
      cur_command[j] = '\0';
      char* cmd = malloc(sizeof(char) * strlen(cur_command) + 1);
      strncpy(cmd, cur_command, strlen(cur_command) + 1);
      commands[k++] = cmd;
    }

    token = strtok(NULL, s);
  }

  // Create symbol table
  int t = 0;
  for (int i = 0; i < k; i++) {
    for (int j = 0; j < strlen(commands[i]); j++) {
      if (commands[i][j] == ':') {
        char* id = malloc(sizeof(char) * strlen(commands[i]));
        strncpy(id, commands[i], strlen(commands[i]) - 1);
        Label* symbol = malloc(sizeof(Label));
        symbol->identifier = id;
        symbol->address = i;
        symbol_table[t++] = symbol;
      }
    }
  }

  sizes[0] = k;
  sizes[1] = t;
  return sizes;
}

/*
  Search for a register value in the currently initialized array of regs
*/
int get_reg_val(char* name, Register regs[], int len) {
  for (int i = 0; i < len; i++) {
    if (strcmp(regs[i].name, name) == 0) {
      return regs[i].value;
    }
  }
  return -1;
}

/*
  Update the value of a register if it's already initialized or declare (and initialize) a new one if not
*/
void update_reg(char* name, int val, Register regs[], int* len) {
  int exists = 0;
  for (int i = 0; i < *len; i++) {
    if (strcmp(regs[i].name, name) == 0) {
      regs[i].value = val;
      exists = 1;
      break;
    }
  }

  if (!exists) {
    char* nm = malloc(sizeof(char) * strlen(name) + 1);
    strncpy(nm, name, strlen(name) + 1);
    Register reg = {.name = nm, .value = val};
    regs[(*len)++] = reg;
  }
}

/*
  Extract at most 2 operands (x, y) for a single command
*/
char** extract_x_y(char* token, const char delim[2]) {
  char** res = malloc(sizeof(char*) * 2);
  char* x = malloc(sizeof(char) * 256);
  char* y = malloc(sizeof(char) * 256);
  int cnt = 0;
  token = strtok(NULL, delim);
  while (token != NULL) {
    if (cnt == 0) {
      strncpy(x, token, strlen(token) + 1);
    } else {
      strncpy(y, token, strlen(token) + 1);
    }
    cnt++;
    token = strtok(NULL, delim);
  }

  if (cnt == 2) {
    x[strlen(x) - 1] = '\0';
  }

  res[0] = x;
  res[1] = y;
  return res;
}

void free_memory(char* x, char* y, char** xy) {
  free(x);
  free(y);
  free(xy);
}

int calc_val(char* token, int vx, int vy) {
  if (strcmp(token, "add") == 0) {
    return vx + vy;
  } else if (strcmp(token, "sub") == 0) {
    return vx - vy;
  } else if (strcmp(token, "mul") == 0) {
    return vx * vy;
  } else if (strcmp(token, "div") == 0) {
    return vx / vy;
  }

  return -1;
}

// Returns true if command is any kind of jump instruction
int is_jump(char* token) {
  char* cmds[7] = {"jmp", "jne", "je", "jge", "jg", "jle", "jl"};
  for (int i = 0; i < 7; i++) {
    if (!strcmp(token, cmds[i])) {
      return 1;
    }
  }

  return 0;
}

/*
  Look up the symbol table for the address of a label
*/
int symbol_lookup(char* label, Label* symbol_table[], int len) {
  for (int i = 0; i < len; i++) {
    if (!strcmp(label, symbol_table[i]->identifier)) {
      return symbol_table[i]->address;
    }
  }

  return -1;
}

// Add the value of a register to the output message
void add_reg_to_msg(char reg_name[], int r, Register regs[], int reg_len, char* res, int* k) {
  reg_name[r] = '\0';
  int val = get_reg_val(reg_name, regs, reg_len);
  char val_str[100];
  sprintf(val_str, "%d", val);
  strcat(res, val_str);
  *k += strlen(val_str);
}

/*
  Parse message
*/
char* parse_msg(char* msg, Register regs[], int reg_len) {
  char* res = malloc(sizeof(char) * 10000);
  res[0] = '\0';
  int is_in_quotes = 0, end_ind = strlen(msg) - 1, k = 0, i = 0;
  int is_in_reg = 0, r = 0, last_reg = 0;
  char reg_name[256];

  while (msg[i] == ' ' || msg[i] == '\t') {
    i++;
  }

  while (msg[end_ind] == ' ' || msg[end_ind] == '\t') {
    end_ind--;
  }

  int y;
  for (y = 0; i <= end_ind; i++, y++) {
    if (!is_in_quotes && msg[i] == '\'') {
      is_in_quotes = 1;
    } else if (is_in_quotes && msg[i] == '\'') {
      is_in_quotes = 0;
    } else if (is_in_quotes) {
      res[k++] = msg[i];
    } else if (!is_in_quotes && (msg[i] == ' ' || msg[i] == '\t')) {
      continue;
    } else if (!is_in_quotes && !is_in_reg && msg[i] == ',') {
      is_in_reg = 1;
    } else if ((is_in_reg && msg[i] != ',') || (y == 0 && msg[i] != '\'')) {
      reg_name[r++] = msg[i];
      if (i == end_ind) {
        last_reg = 1;
      }
      if (!is_in_reg) is_in_reg = 1;
    } else if (is_in_reg && msg[i] == ',') {
      is_in_reg = 0;
      add_reg_to_msg(reg_name, r, regs, reg_len, res, &k);
      r = 0;
    }
  }

  if (last_reg) {
    add_reg_to_msg(reg_name, r, regs, reg_len, res, &k);
  }

  res[k] = '\0';
  return res;
}

/*
  Execute assembly and produce an output
*/
char* second_pass(char* commands[], int k, Label* symbol_table[], int t) {
  char* output = malloc(sizeof(char) * 10000);
  output[0] = '\0';
  Register regs[1000];
  int i = 0, reg_len = 0;
  const char delim[2] = " ";
  int jne = 0, je = 0, jge = 0, jg = 0, jle = 0, jl = 0;
  int return_addr[10000], stack_ptr = 0;

  while (i < k) {
    char cmd_buffer[1000];
    strncpy(cmd_buffer, commands[i], strlen(commands[i]) + 1);
    char* token = strtok(cmd_buffer, delim);
    char* end;
    if (strcmp(token, "mov") == 0) {
      char** xy = extract_x_y(token, delim);
      char* x = xy[0];
      char* y = xy[1];

      int val = (int) strtol(y, &end, 10);
      if (*end != '\0') {
        // register
        int v = get_reg_val(y, regs, reg_len);
        update_reg(x, v, regs, &reg_len);
      } else {
        // integer
        update_reg(x, val, regs, &reg_len);
      }

      free_memory(x, y, xy);
    } else if (!strcmp(token, "inc") || !strcmp(token, "dec")) {
      char** xy = extract_x_y(token, delim);
      char* x = xy[0];
      char* y = xy[1];
      int v = get_reg_val(x, regs, reg_len);
      int va = v - 1;
      if (!strcmp(token, "inc")) {
        va = v + 1;
      }
      update_reg(x, va, regs, &reg_len);

      free_memory(x, y, xy);
    } else if (!strcmp(token, "add") || !strcmp(token, "sub") || !strcmp(token, "mul") || !strcmp(token, "div")) {
      char** xy = extract_x_y(token, delim);
      char* x = xy[0];
      char* y = xy[1];
      int vx = get_reg_val(x, regs, reg_len);

      int val = (int) strtol(y, &end, 10);
      if (*end != '\0') {
        // register
        int vy = get_reg_val(y, regs, reg_len);
        int final = calc_val(token, vx, vy);
        update_reg(x, final, regs, &reg_len);
      } else {
        // integer
        int final = calc_val(token, vx, val);
        update_reg(x, final, regs, &reg_len);
      }
    } else if (is_jump(token)) {
      char** xy = extract_x_y(token, delim);
      char* label = xy[0];
      char* y = xy[1];

      if (!strcmp(token, "jmp") || (!strcmp(token, "jne") && jne) || (!strcmp(token, "je") && je) ||
          (!strcmp(token, "jge") && jge) || (!strcmp(token, "jg") && jg) || (!strcmp(token, "jle") && jle) ||
          (!strcmp(token, "jl") && jl)) {
        i = symbol_lookup(label, symbol_table, t) - 1;
      }

      free_memory(label, y, xy);
    } else if (!strcmp(token, "cmp")) {
      char** xy = extract_x_y(token, delim);
      char* x = xy[0];
      char* y = xy[1];

      int vx = (int) strtol(x, &end, 10);
      if (*end != '\0') {
        // register
        vx = get_reg_val(x, regs, reg_len);
      }

      int vy = (int) strtol(y, &end, 10);
      if (*end != '\0') {
        // register
        vy = get_reg_val(y, regs, reg_len);
      }

      jne = 0, je = 0, jge = 0, jg = 0, jle = 0, jl = 0;

      if (vx != vy) {
        jne = 1;
      }

      if (vx == vy) {
        je = 1;
      }

      if (vx >= vy) {
        jge = 1;
      }

      if (vx > vy){
        jg = 1;
      }

      if (vx <= vy) {
        jle = 1;
      }

      if (vx < vy) {
        jl = 1;
      }

      free_memory(x, y, xy);
    } else if (!strcmp(token, "call")) {
      char** xy = extract_x_y(token, delim);
      char* label = xy[0];
      char* y = xy[1];

      return_addr[stack_ptr++] = i + 1;
      i = symbol_lookup(label, symbol_table, t) - 1;

      free_memory(label, y, xy);
    } else if (!strcmp(token, "ret")) {
      i = return_addr[--stack_ptr] - 1;
    } else if (!strcmp(token, "msg")) {
      char pmes[10000];
      int pl = 0;
      for (int l = 3; l < strlen(commands[i]); l++) {
        pmes[pl++] = commands[i][l];
      }
      pmes[pl] = '\0';
      char* mes = parse_msg(pmes, regs, reg_len);
      strcat(output, mes);
    } else if (!strcmp(token, "end")) {
      for (int i = 0; i < reg_len; i++) {
        free(regs[i].name);
      }

      return output;
    }
    i++;
  }

  for (int i = 0; i < reg_len; i++) {
    free(regs[i].name);
  }

  free(output);

  return (char*)-1;
}

char* assembler_interpreter(const char* program) {
  char* commands[10000];
  Label* symbol_table[1000];
  int* sizes = first_pass(program, commands, symbol_table);
  char* output = second_pass(commands, sizes[0], symbol_table, sizes[1]);

  // Free memory
  for (int i = 0; i < sizes[0]; i++) {
    free(commands[i]);
  }

  for (int i = 0; i < sizes[1]; i++) {
    free(symbol_table[i]->identifier);
    free(symbol_table[i]);
  }

  free(sizes);
  return output;
}
