57eadb7ecd143f4c9c0000a3


section .text

global abbrev_name
; void abbrev_name(const char *name, char *output)
abbrev_name:
                mov     eax, `\0.\0\0`
                or      al, byte [rdi]
.loop:          inc     rdi
                cmp     [rdi], byte ' '
                jne     .loop
                movzx   edx, byte [rdi + 1]
                shl     edx, 16
                or      eax, edx
                and     eax, ~(('A' ^ 'a') | ('A' ^ 'a') << 16)
                mov     [rsi], eax
                ret

_________________________
global abbrev_name

; <-- ro [byte RAX] abbrev_name(ro [byte RDI] name, [byte RSI] output[4] -->
abbrev_name:
    mov dl, [rdi]           ; loading DL with copying <*name> as <ch>
    and dl, 0hDF            ; converting <ch> to the upper case
    mov [rsi], dl           ; copying <ch> to <*output>
    mov byte [rsi+1], '.'   ; copying '.' to <*(name+1)>
.loop:
    inc rdi                 ; pointing <name> to the next character
    cmp byte [rdi], ' '     ; whether <*name> is a space character
    jne .loop               ; otherwise, jumping to the next iteration
    mov dl, [rdi+1]         ; loading <ch> with <*name>
    and dl, 0hDF            ; converting <ch> to the upper case
    mov [rsi+2], dl         ; copying <ch> to <*(name+2)>
    mov byte [rsi+3], `\0`  ; terminating <output>
    ret
; -----> endof abbrev_name <-----
_________________________
section .text
table db '................................ !.#$%&.()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`ABCDEFGHIJKLMNOPQRSTUVWXYZ{|}~'
global abbrev_name
; void abbrev_name(const char *name, char *output)
; Take the input `name` and write the output to `output`.
; Don't forget to add a null byte at the end!
abbrev_name:
  mov rdx, rbx
  lea rbx, [rel table]
  xchg rdi, rsi
  lodsb
  xlatb
  stosb
  mov al, '.'
  stosb
  xchg rdi, rsi
  mov al, ' '
  xor ecx, ecx
  dec ecx
  repne scasb
  xchg rdi, rsi
  lodsb
  xlatb
  stosb
  xor eax, eax
  stosb
  mov rbx, rdx
  ret
