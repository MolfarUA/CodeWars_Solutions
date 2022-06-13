global find_it
section .text

find_it:
                xor     eax, eax
.loop:          xor     eax, [rdi]
                add     rdi, 4
                dec     rsi
                jnz     .loop
                ret
_______________________________
SECTION .text
global find_it

; Finds the number which appears an odd amount of times in an array
; arg0         = (int32_t*) The array of numbers
; arg1         = (size_t)   The length of arg0
; return value = (int32_t)  The number which appears an odd amount of times
find_it:
  shl rsi, 2
  mov rbx, -4
A:add rbx, 4
  mov eax, [rdi + rbx]
  test eax, eax
  jz A
  push rbx
  mov dl, 0
C:cmp eax, [rdi + rbx]
  jne B
  inc dl
  mov dword [rdi + rbx], 0
B:add rbx, 4
  cmp rbx, rsi
  jne C
  pop rbx
  test dl, 1
  jz A
  ret
_______________________________
global  find_it

SECTION .text


find_it:
    mov r9, 0   ; main loop i
    mov r10, 0  ; internal loop j
    mov r11, 0  ; counter

.main_loop:
    mov r11, 0  ; reset counter

;---internal loop---
    mov r10, 0  ;internal j loop
    mov rax, [rdi]
    nop
.internal_loop:
    mov r12d, dword [rdi+r9*4]
    mov r13d, dword [rdi+r10*4]
    cmp r12d, r13d ; compare arr[i] arr[j]
    nop
    jne .arr_i_arr_j_not_equals
.arr_i_arr_j_equals:
    inc r11
.arr_i_arr_j_not_equals:
    inc r10
    cmp r10, rsi
    jne .internal_loop
;---end of internal loop---


;--check if r11 % 2 != 0 if so, return counter--
    push rdx
    push rcx

    mov rdx, 0
    mov rax, r11
    mov rcx, 2
    div rcx
    
    cmp rdx, 0
    
    pop rcx
    pop rdx
    jne .return_element_with_odd_counter
    
;-------------

    inc r9
    cmp r9, rsi
    jne .main_loop
.return_element_with_odd_counter:
    mov rax, [rdi+r9*4] ; arr[i]
    ret
_______________________________
; When the arrays reach a certain length it would make sense to sort them using e.g. qsort
; instead of keeping track of which values are already done in a seperate array- from a performance perspective

SECTION .text
global find_it
extern malloc, free

find_it:    push rdi
            push rsi
            shl rsi,2
            mov rdi,rsi
            call malloc
            mov r10,rax        ; Base of ints counted 
            xor r11,r11        ; Number of ints counted
            pop rsi
            pop rdi
            mov rcx,-1        ; Index of integers to search
@main_loop: inc rcx
            mov edx,[rdi + rcx * 4]
            test r11,r11
            jz @add_count
            xor rax, rax      ; Index for searching already counted ints
@s_counted: cmp [r10 + rax * 4],edx
            je @main_loop
            inc rax
            cmp rax,r11
            jl @s_counted
@add_count: mov [r10 + r11 * 4],edx
            inc r11
@do_count:  lea r8,[rcx + 1]   ; Index while searching the remainder of the array
            mov r9,1           ; Holds count
@search_l:  cmp dword [rdi + r8 * 4],edx
            jne @not_match
            inc r9
@not_match: inc r8
            cmp r8,rsi        ; Done yet ?
            jl @search_l
            shr r9,1          ; If no odd count, go count next
            jnc @main_loop
            push rdx
            mov rdi,r10
            call free
            pop rax
            ret
_______________________________
SECTION .text
global find_it

; Finds the number which appears an odd amount of times in an array
; arg0         = (int32_t*) The array of numbers
; arg1         = (size_t)   The length of arg0
; return value = (int32_t)  The number which appears an odd amount of times
find_it:
  xor eax, eax
  jmp loop_cond
  
  loop:
    dec rsi
    xor eax, DWORD [rdi + rsi * 4]
  
  loop_cond:
    test rsi, rsi
    jnz loop
    
  ret
_______________________________
SECTION .text
global find_it
find_it:
 xor rax,rax
 .b:xor eax,[rdi+rsi*4-4]
    dec rsi
 jne .b
ret
