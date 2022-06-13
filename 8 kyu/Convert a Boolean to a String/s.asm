SECTION .data
true db "true", 0
false db "false", 0

SECTION .text
global boolean_to_string

boolean_to_string:
  mov rax, false
  test rdi, rdi
  jz .q
  mov rax, true
.q:
  ret
_________________________________
section .rodata
true: db "true", 0
false: db "false", 0

section .text
global boolean_to_string
boolean_to_string:
  mov rax, false
  cmp rdi, 0
  je .end
  mov rax, true
.end:
  ret
_________________________________
SECTION .text
global boolean_to_string

boolean_to_string:
  cmp    edi, 1
  je     true_bool
  cmp    edi, 0
  je     false_bool
  
true_bool:
  mov    rax, true
  ret

false_bool:
  mov    rax, false
  ret
  
SECTION .data
  false   DW   'false'
  true    DW   'true'
_________________________________
SECTION .data
str_true: db "true", 0h
str_false: db "false", 0h

SECTION .text
global boolean_to_string

; Returns a string representation of a boolean
; NOTE: Please return a pointer to a string initialized by psuedo-opcode "db" or similar
; arg0         = (bool)         The boolean.
; return value = (const char *) The string representation of the boolean.
boolean_to_string:
  test dil, 1
  jz .false
  mov rax, str_true
  ret
.false
  mov rax, str_false
  ret
