57f75cc397d62fc93d000059


section .text
global calc

; int calc(const char *source);
calc:
  xor ecx, ecx
  mov r8b, 10
.loop:
  mov dl, [rdi]
  test dl, dl
  je .done
  movsx eax, dl
  xor esi, esi
  idiv r8b
  movsx eax, ah
  cmp al, 7
  sete sil
  add dl, -70
  add ecx, esi
  cmp dl, 10
  adc ecx, 0
  inc rdi
  jmp .loop
.done:
  imul eax, ecx, 6
  ret
__________________________________
section .text
global calc

; 
; int calc(const char *source);
calc:
    xor r8, r8 ; sum
    jmp char
nextchar:
    add rdi, 1
char:
    movzx eax, byte [rdi] 
    
    cmp eax, 0
    je return
    
    cmp eax, 77
    je add12
    
    mov edx, 0
    mov r9, 10
    div r9
    
    cmp edx, 7
    je add6
    cmp eax, 7
    je add6
    
    jmp nextchar
add12:
    add r8, 6
add6:
    add r8, 6
    jmp nextchar
return:
    mov rax, r8
    ret
__________________________________
section .text
global calc

; int calc(const char *source);
calc:
        mov rsi, rdi
        xor rax, rax    
        xor edi, edi
        mov dh, 100
        mov dl, 10
        mov r11d, 7
.loadchar:
        lodsb
        test  al, al
        jz  .eofstr
.above100:
        cmp al, dh
        jb .below100
        sub al, dh
        jmp .above100
.below100:
        xor ecx, ecx
.above10:
        cmp al, dl
        jb .below10
        inc ecx
        sub al, dl
        jmp .above10
.below10:
        mov r9d, 6
        mov r8d, eax
        xor eax, eax
        cmp r8d, r11d
        cmovz eax, r9d
        add edi, eax
        xor eax, eax
        cmp ecx, r11d
        cmovz eax, r9d
        add edi, eax
        jmp .loadchar

.eofstr:
        mov eax, edi
        ret
