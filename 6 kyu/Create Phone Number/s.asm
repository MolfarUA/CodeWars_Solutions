global create_phone_number

section .text

create_phone_number:
  mov [rdi], byte 0x28 ; left paren
  mov eax, [rsi]
  add eax, 0x30303030 ; convert 4 bytes to ascii digits
  mov [rdi+1], eax
  mov [rdi+4], word 0x2029 ; right paren and space
  mov eax, [rsi+3]
  add eax, 0x30303030
  mov [rdi+6], eax
  mov [rdi+9], byte 0x2d ; hypen
  mov eax, [rsi+6]
  add eax, 0x30303030
  mov [rdi+10], eax
  mov rax, rdi
  ret
_______________________________
global create_phone_number

section .text

; <--- char *create_phone_number(char phnum[15], const unsigned char nums[10]) --->
create_phone_number:
  mov ecx, 0x30303030
  mov byte [rdi], '('
  mov eax, dword [rsi]
  add eax, ecx
  mov dword [rdi + 1], eax
  mov word [rdi + 4], ") "
  mov eax, dword [rsi + 3]
  add eax, ecx
  mov dword [rdi + 6], eax
  mov byte [rdi + 9], '-'
  mov eax, dword [rsi + 6]
  add eax, ecx
  mov dword [rdi + 10], eax
  mov byte [rdi + 14], 0
  mov rax, rdi
  ret
; ---------> endof create_phone_number <---------
_______________________________
global create_phone_number

section .text

; <--- char *create_phone_number(char phnum[15], const unsigned char nums[10]) --->
create_phone_number:
    mov rax, rdi            ; copying <phnum> to RAX
    mov rcx, -1             ; setting RCX as <pos> to one position back
    lea r8, [.fmt-1]        ; pointing R8 to one byte before <.fmt>
.loop:
    inc rcx                 ; incrementing <pos>
    inc r8                  ; pointing <.fmt> to the next character
    mov dl, [r8]            ; copying <*.fmt> to DL as <ch>
    cmp dl, 'x'             ; whether <ch> is 'x'
    jne .set                ; otherwise, jumping to the .set label
    mov dl, '0'             ; setting <ch> to the ASCII code of zero
    add dl, [rsi]           ; converting <*nums> to the ASCII representation
    inc rsi                 ; pointing <nums> to the next number
.set:
    mov [rax+rcx], dl       ; copying <ch> to <*(phnum+pos)>
    test dl, dl             ; whether <ch> is the null character
    jne .loop               ; otherwise, jumping to the next iteration
    ret

; local read-only data
.fmt:   db "(xxx) xxx-xxxx",0h0
; ---------> endof create_phone_number <---------
_______________________________
global create_phone_number

section .text
; char *create_phone_number(char phnum[15], const unsigned char nums[10])
create_phone_number:
                mov     rax, [rsi]
                shl     eax, 8
                add     eax, '(000'
                mov     [rdi], eax
                mov     [rdi + 4], word ') '
                mov     eax, [rsi + 3]
                and     eax, 0ffffffh
                add     eax, '000-'
                mov     [rdi + 6], eax
                mov     eax, [rsi + 6]
                add     eax, '0000'
                mov     [rdi + 10], eax
                mov     [rdi + 14], byte 0
                mov     rax, rdi
                ret
