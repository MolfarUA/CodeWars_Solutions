SECTION .text
global xo

xo:
  xor ecx, ecx
.loop_cond:
  mov al, [rdi]
  test al, al
  jz .ret
.loop:
  inc rdi
  or al, 32        ; I couldn't get tolower to work for whatever reason, so here's my hack
  cmp al, 'x'
  jne .loop_checkO
  inc ecx
  jmp .loop_cond
.loop_checkO:
  cmp al, 'o'
  jne .loop_cond
  dec ecx
  jmp .loop_cond
.ret:
  test ecx, ecx
  setz cl
  movzx rax, cl
  ret
__________________________________
SECTION .text
global xo

xo:
  xor ecx, ecx
  xor edx, edx
  
.loop:
  mov al, [rdi]
  inc rdi
  cmp al, 'X'
  je .x
  cmp al, 'x'
  je .x
  cmp al, 'O'
  je .o
  cmp al, 'o'
  je .o
  test al, al
  jnz .loop
  
  cmp ecx, edx
  sete al
  ret
  
.x:
  inc ecx
  jmp .loop

.o:
  inc edx
  jmp .loop
__________________________________
SECTION .text
global xo

; bool xo(const char *str)
; str: rdi
xo:
    push rbp
    mov rbp, rsp
    
    xor r8, r8  ; num_o: r8
    xor r9, r9  ; num_x: r9
    xor rcx, rcx
.l0:
    mov al, [rdi + rcx]
    cmp al, 0
    je .exit_loop
    
    cmp al, 'a'
    jge .next
    add al, 32
.next:    
    cmp al, 'o'
    jne .l1
    inc r8
    jmp .l2
.l1:
    cmp al, 'x'
    jne .l2
    inc r9
.l2:
    inc rcx
    jmp .l0
.exit_loop:
    cmp r8, r9
    jne .false
    mov rax, 1
    jmp .end
.false:
    xor rax, rax
.end:
    mov rsp, rbp
    pop rbp
    ret
__________________________________
SECTION .text
global xo

xo:
  xor rcx, rcx
  xor rdx, rdx
@next:
  cmp byte [rdi], 0
  je @end
  cmp byte [rdi], 'x'
  je @incx
  cmp byte [rdi], 'X'
  je @incx
  cmp byte [rdi], 'o'
  je @inco
  cmp byte [rdi], 'O'
  je @inco
  inc rdi
  jmp @next
@end:
  cmp rcx, rdx
  je @true
  mov rax, 0
  ret
@true:
  mov rax, 1
  ret
@incx:
  inc rcx
  inc rdi
  jmp @next
@inco:
  inc rdx
  inc rdi
  jmp @next
