SECTION .text
global dna_to_rna
global dna_to_rna_uses_dynamic_allocation
extern strdup

; Returns a boolean indicating whether the return value of dna_to_rna is allocated on the heap or allocated statically.
; Please allocate a static buffer of 350 characters for the return value of dna_to_rna if this function returns false.
dna_to_rna_uses_dynamic_allocation:
  mov rax, 1
  ret

; Returns a string representation of a DNA sequence converted to an RNA sequence
; arg0         = (const char*) DNA sequence.
; return value = (char*)       RNA sequence.
dna_to_rna:
  call strdup
  mov  rdi, rax
  dec  rdi
next_char:
  inc  rdi
  mov  bl, [rdi]
  test bl, bl
  jz   end_loop
  cmp  bl, 'T'
  jne  next_char
  mov  [rdi], byte 'U'
  jmp  next_char
end_loop:
  ret
  
_____________________________
SECTION .bss

rna:
  resb 350

SECTION .text
global dna_to_rna
global dna_to_rna_uses_dynamic_allocation


; Returns a boolean indicating whether the return value of dna_to_rna is allocated on the heap or allocated statically.
; Please allocate a static buffer of 350 characters for the return value of dna_to_rna if this function returns false.
dna_to_rna_uses_dynamic_allocation:
  mov rax, 0
  ret

; Returns a string representation of a DNA sequence converted to an RNA sequence
; arg0         = (const char*) DNA sequence.
; return value = (char*)       RNA sequence.
dna_to_rna:
  xor rax, rax
  mov rcx, 0
  mov rbx, rna
loop:
  mov BYTE al, [edi]
  mov BYTE [rbx], al
  test al, al
  jz end
  cmp al, 84
  jne loop_end
  mov BYTE [rbx], 85
loop_end:
  inc edi
  inc rbx
  jmp loop
end:
  mov rax, rna
  ret
  
_____________________________
SECTION .text
global dna_to_rna
global dna_to_rna_uses_dynamic_allocation

dna_to_rna_uses_dynamic_allocation:
  mov rax, 0
  ret

dna_to_rna:
  mov rsi,rdi
  mov rdi,RNA
  .b:movsb
     cmp byte[rdi-1],'T'
     sbb byte[rdi-1],-1
     cmp byte[rdi-1],0
  jne .b   
  mov rax,RNA
  ret
  
  SECTION .data
  RNA resb 350
  
_____________________________
SECTION .bss
rna: resb 350

SECTION .text
global dna_to_rna
global dna_to_rna_uses_dynamic_allocation
; Returns a boolean indicating whether the return value of dna_to_rna is allocated on the heap or allocated statically.
; Please allocate a static buffer of 350 characters for the return value of dna_to_rna if this function returns false.
dna_to_rna_uses_dynamic_allocation:
  mov rax, 0
  ret

; Returns a string representation of a DNA sequence converted to an RNA sequence
; arg0         = (const char*) DNA sequence.
; return value = (char*)       RNA sequence.
dna_to_rna:
  mov rsi, rna
  .loop:
  cmp DWORD [rdi], 0x00
  je .end_loop
  mov rdx, 0xFF
  and rdx, [rdi]
  cmp rdx, 0x54
  je .change
  jne .copy
  .increment:
  inc rdi
  inc rsi
  jmp .loop
  .end_loop:
  mov DWORD [rsi], 0
  mov rax, rna
  ret
  .change:
  mov DWORD [rsi], 0x55
  jmp .increment
  .copy:
  mov rdx, [rdi]
  mov [rsi], rdx
  jmp .increment
  
_____________________________
SECTION .text
global dna_to_rna
global dna_to_rna_uses_dynamic_allocation

; Returns a boolean indicating whether the return value of dna_to_rna is allocated on the heap or allocated statically.
; Please allocate a static buffer of 350 characters for the return value of dna_to_rna if this function returns false.
dna_to_rna_uses_dynamic_allocation:
  mov rax, 0
  ret

; Returns a string representation of a DNA sequence converted to an RNA sequence
; arg0         = (const char*) DNA sequence.
; return value = (char*)       RNA sequence.
dna_to_rna:
  push rbp
  mov rbp, rsp
  
  mov r10, 350  ; use stack to hold variable size array (max 350 elements)
  shl r10, 3    ; each element one byte
  sub rsp, r10  ; 'allocate memory on stack'
  
  xor r8, r8
  
.nextchar:
  mov al, byte [rdi + r8]
  cmp al, 0
  jz .exit
  mov byte [rsp + r8], al
  cmp al, 0x54
  jz .change

.continue:
  inc r8
  jmp .nextchar
  
.exit:
  mov byte [rsp + r8], 0  ; null terminatation of string
  mov rax, rsp
  add rsp, r10            ; 'deallocate' on stack
  
  pop rbp
  ret
  
.change:
  mov byte [rsp + r8], 0x55
  jmp .continue
