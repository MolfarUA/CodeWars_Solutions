56c5847f27be2c3db20009c3


global subtract_sum
subtract_sum:
  mov rax, s
  ret ; fruit name like "apple"

s:
  db "apple", 0
_______________________________________
section .data
  m db "apple",0
  
section .text
global subtract_sum
subtract_sum:
  xor rax,rax
  mov rax,m
  ret ; fruit name like "apple"
_______________________________________
global subtract_sum
section .data
  fruit_map:  
        db  0, 1, 0, 2, 3, 2, 3, 4, 5, 4, 6, 4
        db  6, 7, 8, 7, 8, 5, 8, 9, 1, 9, 1, 0
        db  2, 0, 5, 3, 2, 3, 4, 3, 4, 6, 7, 5
        db  7, 8, 7, 8, 9, 1, 9, 1, 5, 1, 0, 2
        db  0, 2, 3, 4, 3, 5, 6, 4, 6, 7, 6, 7
        db  8, 9, 5, 9, 1, 9, 1, 0, 1, 0, 2, 5
        db  2, 3, 4, 3, 4, 6, 4, 6, 5, 8, 7, 8
        db  9, 8, 9, 1, 9, 5, 0, 2, 0, 2, 3, 2
        db  3, 4, 5, 4

  _f1:  db "kiwi", 0
  _f2:  db "pear", 0
  _f3:  db "banana", 0
  _f4:  db "melon", 0
  _f5:  db "pineapple", 0
  _f6:  db "apple", 0
  _f7:  db "cucumber", 0
  _f8:  db "orange", 0
  _f9:  db "grape", 0
  _f10: db "cherry", 0    

  fruit_labels:
        dq _f1, _f2, _f3, _f4, _f5, _f6, _f7, _f8, _f9, _f10
        
section .text
  subtract_sum:
    mov ecx, 10
    loop0:
      xor r8d, r8d
      mov eax, edi
      loop1:
        xor rdx, rdx
        div ecx
        add r8d, edx
        cmp eax, 0
      jnz  loop1
      sub edi, r8d
      cmp edi, 100
    jnb loop0

    dec edi
    movzx edi, byte [fruit_map + edi]
    mov rax, [fruit_labels + edi*8]
  
    ret
