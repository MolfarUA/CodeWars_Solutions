566fc12495810954b1000030


global nbdig

section .text
nbdig:    
  xor r8d, r8d
  mov r9, 10
  xor r10d, r10d
.loop:
  cmp r10d, edi
  ja .done
  mov r11d, r10d
  imul r11d, r10d
.nextdigit:
  mov eax, r11d
  xor edx, edx
  xor ecx, ecx
  div r9d
  cmp edx, esi
  sete cl
  add r8d, ecx
  cmp r11d, 9
  mov r11d, eax
  ja .nextdigit
  inc r10d
  jmp .loop
.done:
  mov eax, r8d
  ret
____________________________
global nbdig
section .text
nbdig:    
        xor r10,r10
        xor ebx,ebx     ; counter for digits
        mov r8d,10
        mov r9d,edi      ; will be 'k'
        
@main:  mov  eax,r9d    ; Get the next number
        mul  eax        ; and square it
        
@l2:    xor  edx,edx
        div  r8d         ; divide on 10
        cmp  dx,si       ; and check if digit is what we're looking for
        sete r10b
        add  ebx,r10d    ; add true/false to ebx
        test eax,eax     ; check if remaining digits
        jne  @l2
        
        dec  r9d          ; as long as 'k >= 0'
        jns  @main
        mov  eax,ebx
        ret
____________________________
global nbdig

section .text

; ---> unsigned nbdig(unsigned n, unsigned d) <---
; n - an integer where n >= 0
; d - a digit where 0 <= d <= 9
nbdig:    
    xor rax,rax
    xor r9,r9  ; c
    mov r8,1   ; k
    mov r10,10
_loop:
  cmp r8,rdi
  jg _exit
  mov rax,r8
  imul rax ; rax = k * k
_parse:
  test rax,rax
  jz _inc_and_loop
  xor rdx,rdx
  idiv r10
  cmp rdx,rsi
  je _inc_res
  jmp _parse
_inc_res:
  inc r9
  jmp _parse
_inc_and_loop:
  inc r8
  jmp _loop
_exit:
  mov rax,r9
  test rsi,rsi
  jz _incz
  ret
_incz:
  inc rax
  ret
; -----> end of nbdig <-----
