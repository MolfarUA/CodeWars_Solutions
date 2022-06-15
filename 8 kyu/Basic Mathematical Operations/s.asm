SECTION .text
global basic_op

; double basic_op(char op, double a, double b)
; params:
;   DIL  <- op
;   XMM0 <- a
;   XMM1 <- b
basic_op:
  ; xorps xmm0, xmm0    ; XMM0 <- the result
  
  cmp dil, '+'
  je .add
  cmp dil, '-'
  je .subtract
  cmp dil, '*'
  je .multiply
  cmp dil, '/'
  je .divide
  jmp .end
  
  .add:
    addsd xmm0, xmm1
    jmp .end
  .subtract:
    subsd xmm0, xmm1
    jmp .end
  .multiply:
    mulsd xmm0, xmm1
    jmp .end
  .divide:
    divsd xmm0, xmm1
  .end:
  ret
  ________________________________
  SECTION .text
global basic_op

basic_op:
  jmp [.case+rdi*8-'*'*8]
    .mul:mulsd xmm0,xmm1
         ret
   .plus:addsd xmm0,xmm1 
         ret
  .minus:subsd xmm0,xmm1
         ret 
    .div:divsd xmm0,xmm1
         ret
    
  .case dq .mul,.plus,0,.minus,0,.div
________________________________
SECTION .text
global basic_op

; double basic_op(char op, double a, double b)
; params:
;   DIL  <- op
;   XMM0 <- a
;   XMM1 <- b
basic_op:
  add edi, -42
  lea rax, [.switchbase]
  movsxd rcx, dword [rax + 8*rdi]
  add rcx, rax
  jmp rcx
.mul:
  vmulsd xmm0, xmm0, xmm1
  ret
.div:
  vdivsd xmm0, xmm0, xmm1
  ret
.add:
  vaddsd xmm0, xmm0, xmm1
  ret
.sub:
  vsubsd xmm0, xmm0, xmm1
  ret
.switchbase:
  dq .mul-.switchbase
  dq .add-.switchbase
  dq .sub-.switchbase
  dq .sub-.switchbase
  dq .sub-.switchbase
  dq .div-.switchbase
________________________________
extern mprotect
global basic_op


SECTION .bss
  alignb  4
mc:
  resb  0x2000

SECTION .data
op: 
  db 0x59, 0x58, 0x00, 0x5c, 0x00, 0x5e

SECTION .text

; double basic_op(char op, double a, double b)
; params:
;   DIL  <- op
;   XMM0 <- a
;   XMM1 <- b
basic_op:

  ; use mprotect to set up writable and executable BSS space
  xor r12, r12
  mov dword r12, (mc + 0x1000)
  and dword r12, 0xfffff000

  push rdi
  push rsi
  push rdx
  mov rdi, r12
  mov rsi, 0x1000
  mov rdx, 7
  call mprotect
  pop rdx
  pop rsi
  pop rdi

  ; compute opcode for operation on ascii offset
  lea rsi, [rel op]
  add rsi, rdi
  sub rsi, 0x2a
  mov byte cl, [rsi]
  
  ; write modifiable code based on opcode and execute it
  mov rax, r12
  mov byte [rax], 0xf2
  mov byte [rax + 1], 0x0f
  mov byte [rax + 2], cl
  mov byte [rax + 3], 0xc1
  mov byte [rax + 4], 0xc3
  jmp r12
