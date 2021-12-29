global alphabet_position
extern malloc, realloc

section .text

realloc_str:
  inc rcx

  push rax
  push rdx
  push rdi
  push rcx
    
  mov rdi, rsi
  mov rsi, rcx
  call realloc
  mov rsi, rax
  
  pop rcx
  pop rdi
  pop rdx
  pop rax
    
  mov rbx, rsi
  add rbx, rcx
  dec rbx

  ret

alphabet_position:
  push rdi
  
  mov rdi, 1
  call malloc
  mov rsi, rax
  mov rbx, rax
  
  pop rdi

  xor rcx, rcx
  xor rax, rax
  xor rdx, rdx
  
.loop:
  mov al, byte[rdi]
    
  cmp al, 0
  je .loop_end
    
  cmp al, 'A'
  jl .continue
    
  cmp al, 'z'
  jg .continue
    
  cmp al, 'Z'
  jle .uppercase

  cmp al, 'a'
  jl .continue
  
  sub al, 'a'
  add al, 'A'

.uppercase:

  sub al, 'A'
  inc al
  xor dx, dx
  mov r10w, 10
  div r10w
  cmp al, 0
  je .single_digit
    
  call realloc_str
  add al, '0'
  mov byte[rbx], al
    
.single_digit:
    
  call realloc_str
  add dl, '0'
  mov byte[rbx], dl
    
  call realloc_str
  mov byte[rbx], ' '
    
.continue:
  
  inc rdi
  jmp .loop
  
.loop_end:
  
  mov byte[rbx], 0
  
  mov rax, rsi
  ret
  
_______________________________________________
[BITS 64]
section .text

;;
; C-signature:
;     void *malloc(size_t length)
;     [rax]        [rdi]
extern malloc

;;
; C-signature:
;     void *realloc(void *ptr, size_t new_length)
;     [rax]         [rdi]      [rsi]
extern realloc

global alphabet_position
;;
; C-signature:
;     char *alphabet_position(const char *text)
;     [rax]                   [rdi]
;
; Replace every letter in the input string (text) with its position in the
; alphabet (a = 1, b = 2, ...) and ignore all other characters. Return the
; result in a string with every letter position seperated by one space
; character.
;
; Register usage:
;     [rax] temporary storage and result
;     [rcx] index into the result text
;     [rdx] store the transformed letters
;     [rsi] pointer into (text)
;     [r8]  pointer to the result text
;
; @param text [rdi] pointer to a null-terminated string
; @return null-terminated string with all letters replaced by
;         their position in the alphabet
;
alphabet_position:
  push rdi
  ; First, we determine the length of the input string (text) and allocate
  ; more than enough space to produce our output string. In a worst-case
  ; scenario, the output needs 3 bytes per input character (2 bytes for a
  ; two-digit number and one byte for a space character). We use 4 times the
  ; size of the input string because it is easier to calculate (shift by 2)
  ; and is always large enough.
  call strlen
  ; To make sure we have at least a length of 1, we add 1 to the determined
  ; length. This way, we always have at least 4 characters for our result
  ; even if it only has to contain the null-byte.
  inc rax
  shl rax, 2
  mov rdi, rax
  call malloc WRT ..plt
  pop rsi
  mov rdi, rax
  ; We have to reset our counter as well as rax. We use rax as an index into
  ; our array of BCD numbers. For that we need the upper part of the register
  ; to be zero because we will only manipulate the lower byte of rax.
  xor ecx, ecx
  xor eax, eax
  lea r8, [rel .bcd_numbers]
  ; We want to have the increment at the top of the loop, so to get the
  ; first address right, we decrement right before entering the loop.
  dec rsi
.next:
  inc rsi
  mov al, byte [rsi];
  cmp al, 0
  jz .end
  ; Or'ing the character with 0x20 will set it to lower case (if it was
  ; a letter) and allows us to treat upper case and lower case letters the
  ; same.
  or al, 0x20
  cmp al, 'a'
  jl .next
  cmp al, 'z'
  jg .next
  ; We subtract 'a', which is 0x61 in hexadecimal, to get our zero-based
  ; index into the BCD number array.
  sub al, 'a'
  ; We reset dx holding our two digit result characters. (see below)
  xor edx, edx
  mov dl, byte [r8 + rax]
  ; We space out the two BCD digits by moving the 4 upper bits into the
  ; higher byte and shifting only the lower 4 bits back.
  ; Or'ing with 0x3030 will turn both bytes into the ASCII characters for
  ; the digits ('0' ... '9'). We then decide whether we only need one or both
  ; for the result.
  shl dx, 4
  shr dl, 4
  or dx, 0x3030
  cmp dh, 0x30
  jz .second_digit
  mov byte [rdi + rcx], dh
  inc rcx
.second_digit:
  mov byte [rdi + rcx], dl
  inc rcx
  ; We add a space character after each number added to our result string.
  mov byte [rdi + rcx], ' '
  inc rcx
  jmp .next
.end:
  ; If our result string is not empty, we override the last space character
  ; with a zero-byte to terminate our string. The length of the string is
  ; then one byte longer. After that, we re-allocate the memory to get rid
  ; of the unused temporary memory. If our result string was empty, we only
  ; skip moving back one character in our result string.
  cmp rcx, 0
  jz .empty_string
  dec rcx
.empty_string:
  mov byte [rdi + rcx], 0
  inc rcx
  mov rsi, rcx
  call realloc WRT ..plt
  ret

; This array of BCD numbers represents a compact way of translating the
; hexadecimal values 0x00 to 0x1a into packed BCD. This allows us to then
; convert them into printable digits.
;
; Example: We have 0xd (=13). This indexes 0x14 in our BCD array which is
;          converted into '14' representing 'n'. 'n' is 0x6e in ASCII. If we
;          subtract 'a' from it we get 0x6e - 0x61 = 0x0d => 13. So we have
;          successfully translated from 'n' to '14'. (q.e.d.)
;
align 8, db 0
.bcd_numbers:
db  0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08
db  0x09, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16
db  0x17, 0x18, 0x19, 0x20, 0x21, 0x22, 0x23, 0x24
db  0x25, 0x26

;;
; C-signature:
;    size_t strlen(const char *s)
;    [rax]         [rdi]
;
; Calculate the length of the given null-terminated string (s).
;
; Register usage:
;     [rax] temporary storage and result
;     [rcx] length counter
;     [rdi] pointer to the next character in the string
;
; @param s [rdi]  string to measure
; @return the length of the string (s)
;
align 8, db 0
strlen:
  ; Note: We scan the given string for a null-byte.
  ; We use rcx as a counter and make it as high as possible
  ; by switching all bits on (actually becomes a negative number)
  ; so that the rep prefix will not abort before scanning through
  ; the whole string. Instead we will abort the repetion using 
  ; the not-zero (nz) condition. To get the positive size we have
  ; to negate the result which will then be one larger than the
  ; length of the string.
  xor ecx, ecx
  xor al, al
  not rcx
  cld
  repnz scasb
  neg rcx
  dec rcx
  mov rax, rcx
  ret
  
_______________________________________________
global alphabet_position
extern malloc, realloc

section .text

; <----- char *alphabet_position(const char *text) ----->
alphabet_position:
    push rbx                    ; saving RBX in the stack
    sub rsp, 8                  ; aligning the stack boundary
    push rdi                    ; saving <text> in the stack
    xor rax, rax                ; resetting RAX
    test rdi, rdi               ; whether <text> is NULL
    je .exit                    ; jumping to exit
    dec rax                     ; the initial value for <len>
.strlen:
    inc rax                     ; incrementing <len>
    cmp byte [rdi+rax], 0       ; whether <str+len> is an empty character
    jne .strlen                 ; otherwise jumping to .strlen
    inc rax                     ; adding an extra byte for the null character
    imul rdi, rax, 0h3          ; target bytes for <abcpos>
    call malloc                 ; allocating memory
    test rax, rax               ; whether the memory is allocated
    je .exit                    ; otherwise, jumping to exit
    mov rbx, [rsp]              ; restoring <text> from the stack
    mov rdi, rax                ; copying the <abcpos> pointer to RDI
    xor rsi, rsi                ; resetting RSI as <pos>
    mov r10d, 10                ; will be used to get digits
    mov r9d, 'a'                ; copying 'a' to R9B as will be used frequently
    mov r8d, 'A'                ; copying 'A' to R8B as will be used frequently
    mov byte [rdi], 0           ; copying the empty character for an empty string case
.loop:
    movzx eax, byte [rbx]       ; copying <*str> to <c>
    test eax, eax               ; whether <c> is an empty character
    je .pos                     ; jumping to the position section
    cmp eax, r8d                ; whether <c> is below 'A'
    jl .inc                     ; jumping to the increment section
    cmp eax, 'Z'                ; whether <c> is inside the [A-Z] range
    jle .cpy                    ; jumping to the copy section
    cmp eax, r9d                ; whether <c> is below 'a'
    jl .inc                     ; jumping to the increment section
    cmp eax, 'z'                ; whether <c> is inside the [a-z] range
    jg .inc                     ; jumping to the increment section
.cpy:
    cmp eax, r9d                ; whether <c> is in the upper case
    cmovl ecx, r8d              ; copying 'A'
    cmovge ecx, r9d             ; otherwise, copying 'a'
    sub eax, ecx                ; getting the difference between ASCII codes
    inc eax                     ; getting the alphabet position
    mov rcx, 1                  ; setting the <pos> shift to one
    cmp eax, r10d               ; whether the position contains one digit
    jl .alone                   ; jumping to the alone digit section
    xor edx, edx                ; resetting EDX before the division
    div r10d                    ; separating digits
    add edx, '0'                ; getting the second digit ASCII code
    mov byte [rdi+rsi+1], dl    ; copying to <*(abcpos+pos+1)>
    inc rcx                     ; incrementing the <pos> shift because there are two digits
.alone:
    add eax, '0'                ; getting the first digit ASCII code
    mov [rdi+rsi], al           ; copying to <*(abcpos+pos)>
    add rsi, rcx                ; increasing <pos> with the shift
    mov byte [rdi+rsi], ' '     ; copying a space character to <*(abcpos+pos)>
    inc rsi                     ; incrementing <pos>
.inc:
    inc rbx                     ; moving the <text> pointer to the next character
    jmp .loop                   ; jumping to the next iteration
.pos:
    test rsi, rsi               ; whether <pos> is zero
    je .re                      ; jumping to the reallocation section
    dec rsi                     ; decrementing <pos> to clear a space character
    mov byte [rdi+rsi], 0       ; setting the null character instead
.re:
    inc rsi                     ; incrementing <pos>
    call realloc                ; shrinking the memory to the <abcpos> capacity
.exit:
    add rsp, 16                 ; destroying local storage and restoring the stack boundary
    pop rbx                     ; restoring RBX from the stack
    ret
; ---------> end of abcpos <---------

_______________________________________________
global alphabet_position
extern malloc, realloc

section .text

alphabet_position:
    push rdi
    xor rdi, rdi
    call malloc
    pop rdi           ; rax is a pointer to where we want to build the return string
    xor rcx, rcx      ; to hold the length of the return string
.loop:
    mov dl, [rdi]
    inc rdi
    cmp dl, 0
    je .break         ; end of input string detected
    cmp dl, 'a'
    jl .notlowercase
    sub dl, 20h
.notlowercase:
    cmp dl, 'A'
    setge r9b
    cmp dl, 'Z'
    setle r10b
    and r9b, r10b
    jz .loop          ; continue reading input string, if read byte isn't a letter
    sub dl, 64
    cmp dl, 10        ; dl now is the number we want to write
    jl .onedigit
    push rax
    xor ax, ax
    mov al, dl
    mov r8b, 10
    div r8b
    mov dl, ah
    mov r8b, al
    pop rax
                      ; I've aligned these instructions because it will work without them
                      ; if you initially allocate a large enough memory to pass the tests, however without
                      ; any prior assurances on the length of the string, they should be left in
                      ; in essence it is our realloc call, with lots of registers pushed to the stack
                      ; I haven't been super efficient with these calls, two calls can certainly be avoided
                      push rdi
                      mov rdi, rax
                      lea rsi, [rcx+1]
                      push rdx
                      push rcx
                      push r8
                      call realloc
                      pop r8
                      pop rcx
                      pop rdx
                      pop rdi
    add r8b, 48
    mov [rax+rcx], r8b
    inc rcx
.onedigit:
                      push rdi
                      mov rdi, rax
                      lea rsi, [rcx+2]
                      push rdx
                      push rcx
                      call realloc
                      pop rcx
                      pop rdx
                      pop rdi
    add dl, 48
    mov [rax+rcx], dl
.space:
    inc rcx
    mov [rax+rcx], byte 20h
    inc rcx
    jmp .loop
.break:
    test rcx, rcx
    jz .end
    dec rcx
.end:
    mov [rax+rcx], byte 0
    ret
