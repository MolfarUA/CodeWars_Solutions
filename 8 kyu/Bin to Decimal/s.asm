57a5c31ce298a7e6b7000334


global bin_to_dec

section .text

; <--- unsigned bin_to_dec(const char *bin) --->
bin_to_dec:
  xor eax, eax
  xor rcx, rcx
.loop:
  mov dl, byte [rdi+rcx]
  test dl, dl
  jz .end
  shl eax, 1
  and dl, 1
  or al, dl
  inc rcx
  jmp .loop
.end:
  ret
_________________________
global bin_to_dec

section .text

; <--- unsigned bin_to_dec(const char *bin) --->
bin_to_dec:
    xor eax, eax            ; resetting EAX as <dec>
    xor ecx, ecx            ; resetting ECX as <dig>
    movsx edx, byte [rdi]   ; extending <*bin> to EDX as <c>
.loop:
    cmp edx, '1'            ; whether <c> is equal to '1'
    sete cl                 ; setting <dig> to one, otherwise, to zero
    sal eax, 1              ; shifting <dec> one position left
    add eax, ecx            ; adding <dig> to <dec>
    inc rdi                 ; pointing <bin> to the next character
    movsx edx, byte [rdi]   ; extending <*bin> to EDX as <c>
    test edx, edx           ; whether <c> is the null character
    jne .loop               ; otherwise, jumping to the next iteration
    ret
; ---------> endof bin2dec <---------
_________________________
global bin_to_dec
extern strtoul

section .text

; unsigned bin_to_dec(const char *bin)
bin_to_dec:
                xor     esi, esi
                mov     edx, 2
                jmp     strtoul
