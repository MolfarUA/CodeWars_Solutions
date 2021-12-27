; The pointer to the string is passed on with RDI
; Place the number of duplicate letters and digits in EAX when returning

global duplicate_count
section .text
duplicate_count:
      mov ecx, 0xff                 ; loop for every char
      call zero_array
      mov rsi, rdi                  ; from passed in pointer
      call count_chars
      mov ecx, 0xff                 ; loop for every char
      xor eax, eax                  ; zero eax to hold output
      call count_not_null
      ret

zero_array:
      mov dword [count + ecx*4], 0
      loop zero_array
      ret

count_chars:
      cld                           ; forward
      xor eax, eax                  ; zero eax as we will need to read al from it
      lodsb                         ; load char and advance
      cmp al, 'a'                   ; if <a skip
      jb count_chars_skip
      cmp al, 'z'                   ; if >z skip
      ja count_chars_skip
      sub al, 0x20                  ; convert to upper
      count_chars_skip:
      inc dword [count + eax*4]     ; incriment count at the array index of the char
      cmp al, 0                     ; if null return
      jne count_chars
      ret

count_not_null:
    cmp dword [count + ecx*4], 1
    jle count_not_null_skip
    inc eax
    count_not_null_skip:
    loop count_not_null
    ret

section .bss
count: resd 256
_______________________________
global duplicate_count
section .text
duplicate_count:
                mov     r8d, 1
                xor     eax, eax
                xor     ecx, ecx
.loop:          movzx   edx, byte [rdi]
                inc     rdi
                shrx    esi, edx, r8d
                and     esi, 0x20
                andn    edx, esi, edx
                shlx    rsi, r8, rdx
                and     rsi, rcx
                or      rax, rsi
                bts     rcx, rdx
                test    edx, edx
                jnz     .loop
                popcnt  rax, rax
                ret
                
_______________________________
; The pointer to the string is passed on with RDI
; Place the number of duplicate letters and digits in EAX when returning
global duplicate_count
section .text
duplicate_count:
enter 8, 0
xor rax, rax
xor rcx, rcx
mov dword[rsp], 0x00370057
mov dword[rsp + 4], 0x00250030
cmp byte[rdi], 0x0
jz end
.loop:
mov dl, byte[rdi]
cmp dl, 0x7b
cmovl si, word[rsp]
cmp dl, 0x5b
cmovl si, word[rsp + 2]
cmp dl, 0x3a
cmovl si, word[rsp + 4]
sub dl, sil
movsx rsi, dword[rsp + 6]
bts rcx, rdx
cmovc rsi, rdx
bts rax, rsi
inc rdi
cmp byte[rdi], 0x0
jnz .loop
btr rax, 0x25
popcnt rax, rax
end:
leave
ret

_____________________________
; The pointer to the string is passed on with RDI
; Place the number of duplicate letters and digits in EAX when returning
; counts number of duplicate alphanumeric characters in string
; case insensitive
global duplicate_count
section .text
duplicate_count:
enter 36, 0              ;allocate 36 bytes on stack
mov qword[rsp], 0        ;zero out first 8 bytes
mov qword[rsp + 8], 0    ;next 8 bytes
mov qword[rsp + 16], 0   ;next 8 bytes
mov qword[rsp + 24], 0   ;next 8 bytes
mov dword[rsp + 32], 0   ;next 4 bytes
                         ;essentially int arr[36] = {0}
xor rax, rax             ;int result = 0
loop:
xor rcx, rcx             ;int ch = 0
mov cl, byte[rdi]        ;int ch = byte of rdi
cmp cl, 0x0              ;if null (end of string)
jz end                   ;jmp to end
cmp cl, 0x3a             ;else if number
jl num                   ;jmp to num
cmp cl, 0x5b             ;else if uppercase
jl upper                 ;jmp to upper
lower:                   ;else lower
sub cl, 0x57             ;97 - 122 to 10 - 35
jmp setArr               ;skip upper and num case
upper:                   ;handles uppercase
sub cl, 0x37             ;65 - 80 to 10 - 35
jmp setArr               ;skip num case
num:                     ;handles numbers
sub cl, 0x30             ;48 - 57 to 0 - 9
setArr:                  ;set array values
inc byte[rsp + rcx]      ;*(array + offset) += 1
inc rdi                  ;increment string pointer
jmp loop                 ;continue loop
end:                     ;counts occurences of string
xor rcx, rcx             ;int counter = 0
endloop:                 ;do
cmp byte[rsp + rcx], 1   ;compare *(array + counter) to 1
jle continue             ;if less than or equal to 1 jmp continue
inc rax                  ;else result++
continue:
inc rcx                  ;counter++
cmp rcx, 36              ;while(
jnz endloop              ;counter != 36)
leave                    ;reset rsp and rbp
ret                      ;return
