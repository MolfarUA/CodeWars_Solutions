global get_sum
section .text

; int get_sum(int a, int b)
get_sum:
    xor eax, eax
    cmp edi, esi
    jge .loop
    xchg edi, esi
.loop:
    add eax, edi
    dec edi
    cmp edi, esi
    jge .loop
    ret
    
_______________________________________
global get_sum

section .text

; <--- int get_sum(int a, int b) --->
get_sum:
  lea eax, [rdi + rsi]
  sub edi, esi
  mov ecx, edi
  neg edi
  cmovns ecx, edi
  inc ecx
  imul ecx
  sar eax, 1
  ret
; -----> endof get_sum <-----

_______________________________________
global get_sum

section .text

; int get_sum(int a, int b)
get_sum:
                lea     eax, [rdi + rsi]
                mov     edx, esi
                sub     edx, edi
                sub     edi, esi
                cmovs   edi, edx
                inc     edi
                imul    eax, edi
                sar     eax, 1
                ret
                
_______________________________________
global get_sum

section .text

; <--- int get_sum(int a, int b) --->
get_sum:
    xor  eax, eax        ; EAX <- the result
    cmp  edi, esi
;    jge  .loop     ;edi>=esi, sf=of=0
    jle  .loop
    xchg  edi, esi ;edi<->esi 
.loop:
;    add  eax, edi
    add  eax, esi
;    dec  edi
    dec  esi
    cmp  edi, esi
;    jge  .loop
    jle  .loop
    ret
; -----> endof get_sum <-----

_______________________________________
global get_sum

section .text

; <--- int get_sum(int a, int b) --->
get_sum:
    xor eax, eax
    cmp edi, esi
    jg _swap
_sum:
    add eax, edi
    inc edi
    cmp edi, esi
    jle _sum
    ret
    
_swap:
  mov ecx, edi
  mov edi, esi
  mov esi, ecx
  jmp _sum
; -----> endof get_sum <-----

_______________________________________
global get_sum

section .text

; <--- int get_sum(int a, int b) --->
get_sum:
    cmp edi, esi
    jg _swap
    mov ebx, edi
    mov ecx, esi
    jmp _set
_swap:
    mov ebx, esi
    mov ecx, edi
_set:
    inc ecx
    xor eax, eax
    mov edx, ebx
_accumulate:
    cmp edx, ecx 
    je _done
    add eax, edx
    inc edx
    jmp _accumulate
_done:
    ret
; -----> endof get_sum <-----
