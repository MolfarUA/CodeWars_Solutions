global hamming
extern free, malloc
section .text
; uint64_t hamming(int n)
hamming:
%define max_n 13282
%define xs_end rcx
%define x2 rdx
%define x3 rsi
%define x5 r8
%define p2 r9
%define p3 r10
%define p5 r11
                mov     rax, [.xs + (edi - 1) * 8]
                test    rax, rax
                jz      .calculate
                ret
.calculate:     mov     xs_end, .xs
                mov     p2, .xs
                mov     p3, .xs
                mov     p5, .xs
                mov     x2, 1
                mov     x3, 1
                mov     x5, 1
.loop:          mov     rax, x2
                cmp     x3, x2
                cmovb   rax, x3
                cmp     x5, rax
                cmovb   rax, x5
                mov     [xs_end], rax
                add     xs_end, 8
                cmp     rax, x2
                jne     .done_next_x2
                imul    x2, [p2], 2
                add     p2, 8
.done_next_x2:  cmp     rax, x3
                jne     .done_next_x3
                imul    x3, [p3], 3
                add     p3, 8
.done_next_x3:  cmp     rax, x5
                jne     .done_next_x5
                imul    x5, [p5], 5
                add     p5, 8
.done_next_x5:  cmp     xs_end, .xs + max_n * 8
                jne     .loop
                mov     rax, [.xs + (edi - 1) * 8]
                ret
section .bss
.xs             resq max_n

___________________________________________________
global hamming

section .text

; Design:
;   spinning threads instead of duplicating jobs
;   until the locking thread has done the job
;   so the long result is only computed once.
;   also implementing AVX512 VPMINUQ and VPMULLQ instructions
;   so running with native AVX512 instead has full benefit!

%macro hambusy 1
    push rbx
    mov rbx, hamlk
%if %1 == 0
    mov [rbx], dword 0
%else
    xor eax, eax
    xor ecx, ecx
    inc ecx
%%loop:
    xor eax, eax
    cmpxchg dword [rbx], ecx
    cmp eax, 1
    je %%loop
%endif
    pop rbx
%endmacro

%macro vpminuq 2                          ; VPMINUQ supported only starting from AVX512
    vmovdqu [rsp], %2
    vpcmpgtq %2, %1, %2
    vpgatherqq %1, [rsp+ymm7*8], %2
%endmacro

%macro vpmullq 3                          ; VPMULLQ supported only starting from AVX512
    vpsrlq %1, %3, 32
    vpmuludq %1, %2
    vpsrlq ymm5, %2, 32
    vpmuludq ymm5, %3
    vpaddq %1, ymm5
    vpsllq %1, 32
    vpmuludq %2, %3
    vpaddq %1, %2
%endmacro

; <-- RAX hamber(EDI n) -->
hamber:
hamming:
    hambusy 1                               ; spin-locking
    mov rdx, hambers                        ; loading the address of <hambers>
    mov rsi, [rdx+0h3FFF*8]                 ; loading <i>
    cmp edi, esi                            ; whether <n> is greater than <i>
    jle .exit                               ; otherwise, jumping to exit
    cmp edi, 0h33E2                         ; whether <n> is greater than <lim>
    cmovg rdi, [rdx]                        ; then reseting <n>
    jg .exit                                ; and jumping to exit
    sub rsp, 0h20                           ; reserving memory for YMM register
    vmovdqa ymm7, [rdx]                     ; loading indices <inx>
    mov rax, .hamuls                        ; loading the address of multipliers
    vmovdqa ymm6, [rax]                     ; loading the multipliers
    xor ecx, ecx                            ; resetting RCX
    inc rcx                                 ; setting RCX to one as <inxmsk>
    vmovq xmm1, rcx                         ; loading XMM1 with <inxmsk>
    vpbroadcastq ymm1, xmm1                 ; extending index mask
    neg rcx                                 ; setting RCX to minus one as <cpymsk>
    vmovq xmm2, rcx                         ; loading XMM2 <cpymsk>
    vpbroadcastq ymm2, xmm2                 ; extending <cpymsk>
    mov rax, hamxps                         ; loading the address of <hamxps>
    vmovdqa ymm3, [rax]                     ; loading <hamxps>
    mov rcx, haminx                         ; loading the address of <haminx>
    vmovdqa ymm0, [rcx]                     ; loading <haminx>
.loop:
    vmovdqa ymm4, ymm3                      ; copying <hamxps>
    vpermq ymm5, ymm4, 0b01001110           ; permuting [1234] to [3412]
    vpminuq ymm4, ymm5                      ; loading minimus YMM4
    vpermq ymm5, ymm4, 0b01010011           ; permuting [1234] to [4123]
    vpminuq ymm4, ymm5                      ; getting a broadcast minimum <min>, i.e a hamber
    inc esi                                 ; incrementing <i>
    vmovsd [rdx+rsi*8], xmm4                ; saving the hamber in <hambers[i]>
    vpcmpeqq ymm4, ymm3                     ; getting mask whether <min> is equal to <hamxps>
    vpand ymm4, ymm1                        ; getting masked indices
    vpaddq ymm0, ymm4                       ; incrementing <haminx>
    vmovdqa ymm5, ymm2                      ; copying <cpymsk> to YMM5
    vpgatherqq ymm4, [rdx+ymm0*8], ymm5     ; loading YMM4 with <hambers[...haminx] using <cpymsk> as <ihmbrs>
    vpmullq ymm3, ymm4, ymm6                ; multiplying <ihmbrs> by <hamuls> and saving in <hamxps>
    cmp esi, edi                            ; whether <i> is equal to <n>
    jl .loop                                ; otherwise, jumping to the next iteration
    vmovdqa [rcx], ymm0                     ; updating <haminx>
    vmovdqa [rax], ymm3                     ; updating <hamxps>
    mov [rdx+0h3FFF*8], rdi                 ; updating <i>
    add rsp, 0h20                           ; restoring local memory
.exit:
    mov rax, [rdx+rdi*8]                    ; loading RAX with <hambers[n]>
    hambusy 0                               ; unlocking (no spinning)
    ret
align 32
.hamuls:        dq  2,2,3,5
; -----> endof hamber <-----

section .data   align=32
hamlk:      dq  0,0,0,0
haminx:     dq  4,4,3,2
hamxps:     dq  8,8,9,10
hambers:    dq  0,1,2,3,4,5,6
;           dq  0h3FF8 dup (?)              ; supported syntax only starting from NASM 2.15.05
            times 0h3FF8 dq 0               ; the current supported environment version is 2.11
            dq  6
            
___________________________________________________
global hamming
section .text

; uint64_t hamming(int n)
; Parameter:    EDI (1 <= n <= 13282)
; Return value: RAX  n'th hamming number
hamming:
  push rbp
  mov rbp, rsp
  lea eax, [8 * rdi]
  sub rsp, rax
  mov qword [rsp], 1
  mov r8, rsp
  mov r9, rsp
  mov r10, rsp
  xor eax, eax
  jmp .cond
.loop:
  mov rdi, qword [r8]
  add rdi, rdi
  mov rdx, qword [r9]
  lea rdx, [3 * rdx]
  mov rcx, qword [r10]
  lea rcx, [5 * rcx]
  mov rsi, rdi
  cmp rsi, rdx
  cmova rsi, rdx
  cmp rsi, rcx
  cmova rsi, rcx
  mov qword [rsp], rsi
  cmp rdi, rsi
  sete al
  lea r8, [r8 + 8 * rax]
  cmp rdx, rsi
  sete al
  lea r9, [r9 + 8 * rax]
  cmp rcx, rsi
  sete al
  lea r10, [r10 + 8 * rax]
.cond:
  add rsp, 8
  cmp rsp, rbp
  jnz .loop
  mov rax, qword [rsp - 8]
  pop rbp
  ret
  
___________________________________________________
        global hamming
        section   .data
num  times 13282 dq (0)
i: dd 0
j: dd 0
k: dd 0
        section .text
; uint64_t hamming(int n)
; Parameter:    EDI (1 <= n <= 13282)
; Return value: RAX  n'th hamming number
hamming:
        mov dword[i], 0
        mov dword[j], 0
        mov dword[k], 0
        
        cmp edi, 1
        jne more     
          mov rax, 1 ; if (N == 1) return 1
          ret
        more:
        mov dword[num], 1
        mov edx, 1
        push dx
        for:
          xor edx, edx
          pop dx
          cmp edx, edi
          je for_end   ; for(edx < N)
          push dx
          mov eax, dword[i]
          mov rax, [num + eax*8] ; eax = num[i]
          
          mov rbx, 2           
          mul rbx              ; eax = num[i] * 2
          mov rbx, rax         ; ebx = eax
          mov eax, dword[j]
          mov rax, [num + eax*8] ; eax = num[j]
          mov rcx, 3
          mul rcx              ; eax = num[j] * 3
          mov rcx, rax         ; ecx = eax
          cmp rbx, rcx 
          jl min2
            mov rbx, rcx ; if (ebx > ecx) ebx = ecx
          min2:
          mov eax, dword[k]
          mov rax, [num + eax*8] ; eax = num[k]
          mov rcx, 5
          mul rcx              ; eax = num[k] * 5
          mov rcx, rax         ; ecx = eax
          cmp rbx, rcx 
          jl append
            mov rbx, rcx ; if (ebx > ecx) ebx = ecx
          append:
          ; ebx = min(num[i]*2, num[j]*3, num[k]*5)
          xor edx, edx
          pop dx
          mov [num + edx*8], rbx
          inc edx
          push dx
        
          
          ; if 2*num[i] <= ebx: i += 1
          mov eax, dword[i]
          mov rax, [num + eax*8] ; ecx = num[i]
          mov rcx, 2
          mul rcx                ; ecx = num[i] * 2
          mov rcx, rax
          cmp rcx, rbx
          jg next_comp1
            mov ecx, dword[i]    ; if (ecx <= ebx) i++
            inc ecx
            mov dword[i], ecx
          next_comp1:
          
          mov eax, dword[j]
          mov rax, [num + eax*8] ; ecx = num[j]
          mov rcx, 3
          mul rcx              ; ecx = num[j] * 3
          mov rcx, rax
          cmp rcx, rbx
          jg next_comp2
            mov ecx, dword[j]
            inc ecx
            mov dword[j], ecx
          next_comp2:
          
          mov eax, dword[k]
          mov rax, [num + eax*8] ; eax = num[k]
          mov rcx, 5
          mul rcx                
          mov rcx, rax           ; ecx = eax * 5
          cmp rcx, rbx
          jg for
          
          mov ecx, dword[k]
          inc ecx
          mov dword[k], ecx
          jmp for
          
        for_end:
        dec edx
        xor rax, rax
        mov rax, QWORD[num + edx*8]
        ret
