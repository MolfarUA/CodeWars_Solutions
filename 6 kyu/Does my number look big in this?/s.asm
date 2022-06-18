global narcissistic

section .text

; <--- bool narcissistic(int num) --->
narcissistic:
  mov esi, 10
  mov eax, edi
  xor ecx, ecx
.loop1:
  xor edx, edx
  div esi
  push rdx
  inc ecx
  test eax, eax
  jnz .loop1
  mov esi, ecx  
.loop2:
  pop r8
  mov edx, esi
  mov eax, 1
.pow:
  imul eax, r8d
  dec edx
  jnz .pow
  sub edi, eax
  dec ecx
  jnz .loop2
  test edi, edi
  setz al
  ret
; ---------> endof narcissistic <---------
________________________
global narcissistic

section .rodata

Tab dd 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474
    dd 54748, 92727, 93084, 548834, 1741725, 4210818, 9800817, 9926315
    dd 24678050, 24678051, 88593477, 146511208, 472335975, 534494836
    dd 912985153

section .text

; eax                   edi
; bool narcissistic(int num) --->
narcissistic:
  mov eax, edi
  mov rdi, Tab
  mov ecx, 32
  repne scasd
  jrcxz .false
  mov eax, 1
  ret
.false:
  xor eax, eax
  ret
________________________
    section .data
log10:  dq  0.3010299957    ; value of 1 / log_2(10)

    section .text
    global narcissistic
narcissistic:
    push rbp
    mov rbp, rsp
    sub rsp, 8              ; prologue

    mov r10, 10             ; we're doing calculations in base 10
    mov r9, 0               ; initialize variable for aggregation

    mov [rsp], rdi          ; prepare input value for FPU
    fld qword [log10]       ; load 1/log_2(10) constant
    fild qword [rsp]        ; load input value into FPU stack
    fyl2x                   ; calculate input / log_2(10)
    fisttp qword [rsp]      ; return truncated result of previous operation
    inc qword [rsp]         ; dignum = floor(log_10(n)) + 1
    mov r11, [rsp]          ; move dignum into register
    mov [rsp], rdi          ; put input value onto stack

.digit_loop:
    xor rdx, rdx            ; clear high part of RDX:RAX for division
    mov rax, rdi            ; load current value into RAX
    div r10                 ; divide RAX by 10
    mov rdi, rax            ; save quotient into RDI

    mov r12, rdx            ; save reminder into non-volatile register
    mov rax, 1              ; prepare variable for multiplication
    mov rcx, r11            ; put dignum into counter register

.power:
    mul r12                 ; we're raising reminder to power of the dignum
    loop .power             ; loop until RCX != 0

    add r9, rax             ; increment overall result by current value
    test rdi, rdi           ; check if our number == 0
    jnz .digit_loop         ; if not then loop back to the start of the loop
    
    cmp r9, [rsp]           ; compare result of the loop with the input
    setz al                 ; if is the same then the number is narcissistic

    mov rsp, rbp            ; epilogue
    pop rbp
    ret
