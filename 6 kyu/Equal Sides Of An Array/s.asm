global find_even_index

section .text

; <--- int find_even_index(const int *values, int len) --->
find_even_index:
    xor r8d, r8d            ; resetting R8D as <rsum>
    test esi, esi           ; whether <len> is zero
    cmove eax, r8d          ; resetting <inx>
    je .exit                ; jumping to exit
    mov eax, -1             ; setting <inx> to "not found"
    mov ecx, esi            ; setting ECX to <len> as <i>
    xor r9d, r9d            ; resetting R9D as <lsum>
.lpsum:
    dec ecx                 ; decrementing <i>
    jl .loop                ; jumping to the .loop label if less than zero
    add r8d, [rdi+rcx*4]    ; adding <*(arr+i)> to <rsum>
    jmp .lpsum              ; jumping to the next .lpsum iteration
.loop:
    inc ecx                 ; incrementing <i>
    cmp ecx, esi            ; whether <i> and <len> are equal
    je .exit                ; jumping to exit
    mov edx, [rdi+rcx*4]    ; coppying <*(arr+i)> to EDX as <curr>
    sub r8d, edx            ; subtracting <curr> from <rsum>
    cmp r8d, r9d            ; whether <rsum> and <lsum> are equal
    cmove eax, ecx          ; setting <inx> to <i>
    je .exit                ; jumping to exit
    add r9d, edx            ; adding <curr> to <lsum>
    jmp .loop               ; jumping to the next iteration
.exit:
    ret
; ---------> endof find_even_index <---------
________________________
global find_even_index
section .text
find_even_index:
  xor rcx,rcx
  mov rdx,rsi
  .b:add ecx,dword[rdi+rsi*4-4]
     dec rsi
  jne .b
  xor r8,r8
  xor rax,rax
  .c:sub ecx,dword[rdi+rax*4]
     cmp ecx,r8d
     je .q
     add r8d,dword[rdi+rax*4]
     inc rax
     dec rdx
  jne .c   
  mov rax, -1
  .q:
  ret
________________________
global find_even_index
section .text
; input: rdi = values, esi = length
; output: rax
; callee saved registers: rbx, rsp, rbp, r12-r15
find_even_index:
  test rsi, rsi
  jz .failure
  xor eax, eax
  lea r8d, [eax + 1]
  cmp rsi, r8
  je .success
  xor ecx, ecx
.init_loop:
  add ecx, [rdi + r8 * 4]
  inc r8
  cmp r8, rsi
  jne .init_loop
  xor edx, edx
.split_loop:
  cmp ecx, edx
  je .success
  add edx, [rdi + rax * 4]
  inc rax
  cmp rax, rsi
  je .failure
  sub ecx, [rdi + rax * 4]
  jmp .split_loop
.failure:
  mov rax, -1
.success:
  ret
________________________
global find_even_index
section .text
; input: rdi = values, esi = length
; output: rax
; callee saved registers: rbx, rsp, rbp, r12-r15
find_even_index:
  test rsi, rsi
  jz .failure
  xor eax, eax
  mov r8d, 1
  cmp rsi, r8
  je .success
.init:
  xor ecx, ecx
.init_loop:
  add ecx, [rdi + r8 * 4]
  inc r8
  cmp r8, rsi
  jne .init_loop
  xor edx, edx
.split_loop:
  cmp ecx, edx
  je .success
  add edx, [rdi + rax * 4]
  inc rax
  cmp rax, rsi
  je .failure
  sub ecx, [rdi + rax * 4]
  jmp .split_loop
.failure:
  mov rax, -1
.success:
  ret
________________________
global find_even_index
section .text
; input: rdi = values, esi = length
; output: rax
; callee saved registers: rbx, rsp, rbp, r12-r15
find_even_index:
  test rsi, rsi
  jz .failure
  xor eax, eax
  cmp rsi, 1
  je .success
.init:
  mov r8d, 1
  xor ecx, ecx
.init_loop:
  add ecx, [rdi + r8 * 4]
  inc r8
  cmp r8, rsi
  jne .init_loop
  xor edx, edx
.split_loop:
  cmp ecx, edx
  je .success
  add edx, [rdi + rax * 4]
  inc rax
  cmp rax, rsi
  je .failure
  sub ecx, [rdi + rax * 4]
  jmp .split_loop
.failure:
  mov rax, -1
.success:
  ret
