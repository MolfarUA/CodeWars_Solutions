segment .text
extern strdup
global disemvowel
disemvowel:
   call strdup
   mov  rdi,rax
   mov  rsi,rax
   @b:movsb
      movzx rcx,byte[rsi-1]  
      bt    [.vowels],rcx
      sbb   rdi,0
      cmp   byte[rsi],0
   jne @b   
   mov byte[rdi],0
 ret
 .vowels: dq 0,0020822200208222h
______________________________
; String to disemvowel will be passed in RDI
; Return pointer to allocated and freeable string in RAX
segment .text
extern malloc, strlen
global disemvowel
disemvowel:
  push rdi
  call strlen
  lea edi, [rax+1]
  call malloc
  pop rsi
  test rax, rax
  jz .quit
  mov rdi, rax
  
.loop:
  mov dl, [rsi]
  inc rsi
  test dl, dl
  jz .done
  cmp dl, 'A'
  je .loop
  cmp dl, 'E'
  je .loop
  cmp dl, 'I'
  je .loop
  cmp dl, 'O'
  je .loop
  cmp dl, 'U'
  je .loop
  cmp dl, 'a'
  je .loop
  cmp dl, 'e'
  je .loop
  cmp dl, 'i'
  je .loop
  cmp dl, 'o'
  je .loop
  cmp dl, 'u'
  je .loop
  mov [rdi], dl
  inc rdi
  jmp .loop
  
.done:
  mov [rdi], dl
.quit:
  ret
______________________________
segment .text
extern malloc, strlen
global disemvowel

disemvowel:
  push rdi
       
  call strlen
       
  mov rdi, rax
  call malloc

  pop rdi
  push rax
  mov rcx, rax
 
  mov al, [rdi]
  test al, al

.loop:
  cmp al, 'a'
  je .continue
 
  cmp al, 'e'
  je .continue
 
  cmp al, 'i'
  je .continue
 
  cmp al, 'o'
  je .continue
 
  cmp al, 'u'
  je .continue
 
  cmp al, 'A'
  je .continue
 
  cmp al, 'E'
  je .continue
 
  cmp al, 'I'
  je .continue
 
  cmp al, 'O'
  je .continue
 
  cmp al, 'U'
  je .continue

  mov BYTE [rcx], al
  inc rcx
 
.continue:
  inc rdi
  mov al, [rdi]
  test al, al
  jnz .loop
 
  mov BYTE [rcx], 0

  pop rax
  ret
______________________________
; String to disemvowel will be passed in RDI
; Return pointer to allocated and freeable string in RAX
segment .text
extern malloc
global disemvowel
disemvowel:
        ; Get the string length so we can malloc a new one.
        ; This includes the null terminator.
        mov rsi, rdi
        xor rdi, rdi
.loop_strlen:
            inc rdi
            cmp byte [rsi + rdi - 1], 0
            jne .loop_strlen

        push rsi
        call malloc
        pop rsi

        ; Copy the string, including the null terminator, but without vowels.
        mov rdi, rax
        mov r10, rax
.loop_copy:
            lodsb
            mov ah, al
            or ah, 0x20 ; Convert uppercase to lowercase for the comparisons.
            cmp ah, 'e'
            je .loop_copy_continue
            cmp ah, 'i'
            je .loop_copy_continue
            cmp ah, 'a'
            je .loop_copy_continue
            cmp ah, 'o'
            je .loop_copy_continue
            cmp ah, 'u'
            je .loop_copy_continue
            stosb
.loop_copy_continue:
            or al, al
            jnz .loop_copy
        mov rax, r10

        ret
