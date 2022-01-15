global samecase

; <-- EAX samecase(DIL a, SIL b) -->
samecase:
    xor eax, eax
    mov ecx, 1
    mov dl, byte [rel lut + rdi]
    add dl, byte [rel lut + rsi]
    cmovpo eax, ecx
    cmovnc eax, dword [rel lut + 256]
    ret
; -----> endof samecase <-----

lut:
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,144,0,0,0,0,0,0,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    dd -1
__________________________
extern isalpha
global samecase

; <-- EAX samecase(DIL a, SIL b) -->
samecase:
    mov al, sil
    xor al, dil
    and al, 32
    shr al, 5
    xor al, 1           ; compare cases
    push rax
    push rsi
    call isalpha        ; isalpha(a)
    pop rdi 
    test eax, eax
    jz .isntalpha
    call isalpha        ; isalpha(b)
    test eax, eax
    jz .isntalpha
    pop rax
    ret
.isntalpha:
    pop rax
    mov eax, -1
    ret
; -----> endof samecase <-----
__________________________
global samecase

; <-- EAX samecase(DIL a, SIL b) -->
samecase:
    mov eax,edi
    or al,32
    sub al,'a'
    cmp al,26
    jae .invalid
    mov al,sil
    or al,32
    sub al,'a'
    cmp al,26
    jae .invalid
    mov al,dil
    xor al,sil
    sar al,5
    xor al,1
    ret
.invalid:
    mov eax,-1
    ret
; -----> endof samecase <-----
__________________________
extern islower, isupper, isalpha

SECTION .text
global samecase

samecase:
  call case
  jz samecase_nonalpha
  mov r8b, cl
  mov rdi, rsi
  call case
  jz samecase_nonalpha
  xor rax, rax
  xor r8b, cl
  sete al
  ret
samecase_nonalpha:
  mov rax, -1
  ret
  
case:
  call isupper
  cmp ah, 1
  sete cl
  call islower
  cmp ah, 0
  sete cl
  call isalpha
  ret
__________________________
SECTION .text
global samecase

samecase:
  call isUpperLower
  mov r8, rax
  mov dil, sil
  call isUpperLower
  xor rax, r8
  sete al
  cmp rax, 0
  jl samecase_nonalpha
  cmp r8, 0
  jl samecase_nonalpha
  ret
samecase_nonalpha:
  mov rax, -1
  ret

isUpperLower:
  xor rax, rax
  cmp dil, 'A'
  jl isUpperLower_nonalpha
  cmp dil, 'Z'
  jle isUpperLower_upper
  cmp dil, 'a'
  jl isUpperLower_nonalpha
  cmp dil, 'z'
  jle isUpperLower_lower
isUpperLower_nonalpha:
  mov rax, -1
  ret
isUpperLower_upper:
  mov rax, 1
isUpperLower_lower:
  ret
