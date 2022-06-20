58cb43f4256836ed95000f97


global find_diff
find_diff:
  mov  eax,[rdi]
  mul  dword[rdi+4]
  mul  dword[rdi+8]
  mov  edx,[rsi]
  imul edx,[rsi+4]
  imul edx,[rsi+8]
  sub  eax,edx
  sbb  edx,edx
  xor  eax,edx
  sub  eax,edx
ret
________________________
global find_diff

; Reminder: If you can, try writing it in one line of code. (chuckle)
;    troll:D

; <-- EAX find_diff(ro [dword RDI] a[3], ro [dword RSI] b[3]) -->
find_diff:
  mov ecx, [rsi]
  imul ecx, [rsi+4]
  imul ecx, [rsi+8]
  mov eax, [rdi]
  imul eax, [rdi+4]
  imul eax, [rdi+8]
  cmp eax, ecx
  jng tb
  sub eax, ecx
  ret
  tb:
  sub ecx, eax
  mov eax, ecx
  ret
________________________
global find_diff

find_diff: 
  xor rax, rax
  mov eax, dword [rdi+0*4]
  imul dword [rdi+1*4]
  imul dword [rdi+2*4]
  mov edx, dword [rsi+0*4]
  imul edx, dword [rsi+1*4]
  imul edx, dword [rsi+2*4]
  sub eax, edx
  cmp eax, 0
  jge .positive
  neg eax
.positive:
ret
