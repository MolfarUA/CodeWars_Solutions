57eb8fcdf670e99d9b000272


extern malloc
section .text
global highestScoringWord
highestScoringWord:
push rbp
mov rbp, rsp
  mov r8, rdi ; r8 - pointer to max scored word
  xor r9, r9 ; r9 - size of max scored word
  xor rdx, rdx ; rdx - max score
  xor rcx, rcx ; rcx - current word score
  xor rsi, rsi ; rsi - current word size

  dec rdi
  .word_loop:
    inc rdi
    xor rax, rax
    mov al, [rdi] ; al - current letter
    cmp al, ' ' ; al == ' ' ?
    jg .is_not_space
      cmp rcx, rdx ; current score > max score ?
      jle .not_max_score
        mov rdx, rcx ; set rdx to new max score
        mov r8, rdi ; set r8 to address after the word
        mov r9, rsi ; set r9 to size of new word
      .not_max_score:
      xor rcx, rcx ; reset current word score
      xor rsi, rsi ; reset current word size
      jmp .continue_loop
    .is_not_space:
    inc rsi
    sub al, 'a'-1 ; ASCII code -> letter score
    add rcx, rax
    .continue_loop:
    cmp byte [rdi], 0 ; *rdi == \0
  jne .word_loop
  sub r8, r9 ; set pointer to word beginning
  
  ; allocate array for result string
  mov rdi, r9
  inc rdi ; for '\0'
  push r8
  push r9
  call malloc
  pop r9
  pop r8
  
  ; copy word from r8 to new array
  mov byte [rax+r9], 0 ; set '\0'
  xor rcx, rcx
  .copy_word:
    dec r9
    mov cl, [r8+r9]
    mov [rax+r9], cl
    cmp r9, 0
  jg .copy_word
leave
ret
_____________________________________________
extern malloc
section .text
global highestScoringWord
highestScoringWord:
push rbp
mov rbp, rsp
  mov r8, rdi ; r8 - points to max scored word
  xor r9, r9 ; r9 - size of max scored word
  xor rdx, rdx ; rdx - max score
  xor rcx, rcx ; rcx - current score
  xor rsi, rsi ; rsi - current word size
  dec rdi
  .loop:
    inc rdi
    xor rax, rax
    mov al, [rdi] ; al - current letter
    ; al == ' ' ?
    cmp al, 96
    jg .is_not_space
      cmp rcx, rdx ; current score > max score ?
      jle .not_max_score
        mov rdx, rcx ; set rdx to new max score
        mov r8, rdi
        sub r8, rsi ; set r8 to beginning of word
        mov r9, rsi ; set r9 to size of new word
      .not_max_score:
      xor rcx, rcx ; reset current word score
      xor rsi, rsi ; reset current word score
      jmp .continue_loop
    .is_not_space:
    inc rsi
    sub al, 96 ; ASCII code -> letter score
    add rcx, rax
    .continue_loop:
    cmp byte [rdi], 0 ; *rdi == \0
  jne .loop
  
  mov rdi, r9
  inc rdi ; for '\0'
  push r8
  push r9
  call malloc
  pop r9
  pop r8
  mov rdx, rax
  xor rcx, rcx
.copy_word:
  mov cl, [r8]
  mov [rdx], cl
  inc r8
  inc rdx
  dec r9
  jnz .copy_word
  mov byte [rdx], 0 ; set '\0'
leave
ret
_____________________________________________
extern malloc
extern printf
section .data
  fmt db "%s"
section .text
global highestScoringWord
highestScoringWord:
push rbp
mov rbp, rsp
  mov r8, rdi ; r8 - points to max scored word
  xor r9, r9 ; r9 - size of max scored word
  xor rdx, rdx ; rdx - max score
  xor rcx, rcx ; rcx - current score
  xor rsi, rsi ; rsi - current word size
  dec rdi
  .find_max_score:
    inc rdi
    xor rax, rax
    mov al, [rdi] ; al - current letter
    ; al == ' ' ?
    cmp al, 96
    jg .is_not_space
      cmp rcx, rdx ; current score > max score ?
      jle .not_max_score
        mov rdx, rcx ; set rdx to new max score
        mov r8, rdi
        sub r8, rsi ; set r8 to beginning of word
        mov r9, rsi ; set r9 to size of new word
      .not_max_score:
      xor rcx, rcx ; reset current word score
      xor rsi, rsi ; reset current word score
      jmp .continue_loop
    .is_not_space:
    inc rsi
    sub al, 96 ; ASCII code -> letter score
    add rcx, rax
    .continue_loop:
    cmp byte [rdi], 0 ; *rdi == \0
  jne .find_max_score
  
  ; allocate array for result string
  mov rdi, r9
  inc rdi ; for '\0'
  push r8
  push r9
  call malloc
  pop r9
  pop r8
  
  ; copy word from r8 to new array
  mov byte [rax+r9], 0 ; set '\0'
  xor rcx, rcx
  .copy_word:
    dec r9
    mov cl, [r8+r9]
    mov [rax+r9], cl
    cmp r9, 0
  jg .copy_word
leave
ret
_____________________________________________
extern malloc
extern printf
section .data
  fmt db "%s"
section .text
global highestScoringWord
highestScoringWord:
push rbp
mov rbp, rsp
  mov r8, rdi ; r8 - points to max scored word
  xor r9, r9 ; r9 - size of max scored word
  xor rdx, rdx ; rdx - max score
  xor rcx, rcx ; rcx - current score
  xor rsi, rsi ; rsi - current word size
  dec rdi
  .loop:
    inc rdi
    xor rax, rax
    mov al, [rdi] ; al - current letter
    ; al == ' ' ?
    cmp al, 96
    jg .is_not_space
      cmp rcx, rdx ; current score > max score ?
      jle .not_max_score
        mov rdx, rcx ; set rdx to new max score
        mov r8, rdi
        sub r8, rsi ; set r8 to beginning of word
        mov r9, rsi ; set r9 to size of new word
      .not_max_score:
      xor rcx, rcx ; reset current word score
      xor rsi, rsi ; reset current word score
      jmp .continue_loop
    .is_not_space:
    inc rsi
    sub al, 96 ; ASCII code -> letter score
    add rcx, rax
    .continue_loop:
    cmp byte [rdi], 0 ; *rdi == \0
  jne .loop
  
  mov rdi, r9
  inc rdi ; for '\0'
  push r8
  push r9
  call malloc
  pop r9
  pop r8
  mov rdx, rax
  xor rcx, rcx
.copy_word:
  mov cl, [r8]
  mov [rdx], cl
  inc r8
  inc rdx
  dec r9
  jnz .copy_word
  mov byte [rdx], 0 ; set '\0'
leave
ret
