55b2549a781b5336c0000103


extern log
section .text
global compare_powers
; input: rdi = n1, rsi = n2
; output: eax
; callee saved registers: rbx, rsp, rbp, r12-r15
compare_powers:
  push rbp
  mov rbp, rdi
  push rbx
  mov rbx, rsi
  sub rsp, 24
  cvtsi2sd xmm0, [rdi]
  call log
  cvtsi2sd xmm1, [rbp+4]
  mulsd xmm1, xmm0
  cvtsi2sd xmm0, [rbx]
  movsd [rsp+8], xmm1
  call log
  movsd xmm1, [rsp+8]
  xor eax, eax
  movapd xmm2, xmm0
  cvtsi2sd xmm0, [rbx+4]
  mulsd xmm0, xmm2
  comisd xmm0, xmm1
  seta al
  xor edx, edx
  comisd xmm1, xmm0
  seta dl
  add rsp, 24
  sub eax, edx
  pop rbx
  pop rbp
  ret
________________________________
section .text
global compare_powers
extern log
; input: rdi = n1, rsi = n2
; output: eax
; callee saved registers: rbx, rsp, rbp, r12-r15
compare_powers:
  push rbx
  push rdi
  push rsi
  
  cvtsi2sd xmm0, [rdi]
  call log
  mov rdi, [rsp+8]
  cvtsi2sd xmm1, [rdi+4]
  mulsd xmm0, xmm1
  movsd [rsp+8], xmm0
  
  mov rsi, [rsp]
  cvtsi2sd xmm0, [rsi]
  call log
  mov rsi, [rsp]
  cvtsi2sd xmm1, [rsi+4]
  mulsd xmm0, xmm1
  
  mov eax, 1
  xor ecx, ecx
  mov edx, -1

  ucomisd xmm0, [rsp+8]
  cmovz eax, ecx
  cmovc eax, edx
  
  pop rsi
  pop rdi
  pop rbx
  ret

________________________________
section .text
global compare_powers

extern log2

; input: rdi = n1, rsi = n2
; output: eax
; callee saved registers: rbx, rsp, rbp, r12-r15
compare_powers:
  cvtsi2sd xmm0, [rdi]  ; base0 => double
  
  push rbx
  mov ebx, [rdi + 4]
  
  push rbp
  mov ebp, [rsi]
  
  push r14
  mov r14d, [rsi + 4]

  call log2
  
  cvtsi2sd xmm1, ebx    ; exponent0 => double
  mulsd xmm0, xmm1      ; base0 * exponent0
  movq rbx, xmm0        ; preserve in rbx
  
  cvtsi2sd xmm0, rbp    ; base1 => double
  call log2
  cvtsi2sd xmm1, r14d   ; exponent1 => double
  mulsd xmm0, xmm1      ; base1 * exponent1
  movq rdx, xmm0        ; extract as integer data

  xor eax, eax
  mov ecx, 1
  mov edi, -1
  
  cmp rbx, rdx
  cmova eax, edi
  cmovb eax, ecx
  
  pop r14
  pop rbp
  pop rbx
  ret
