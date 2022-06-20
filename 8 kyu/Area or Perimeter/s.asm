5ab6538b379d20ad880000ab


global area_or_perimeter

section .text

; <----- int area_or_perimeter(int length, int width) ----->
area_or_perimeter:
    cmp   rdi, rsi
    je    square
    lea   rax, [rdi+rsi*2]
    add   rax, rdi
    jmp   done
square:
    mov   rax, rdi
    mul   rax
done:
    ret
; ---------> end of area_or_perim <---------
________________________
; 2021 nomennescio
global area_or_perimeter

section .text

; <----- int area_or_perimeter (int length, int width) ----->
area_or_perimeter:
    mov eax, edi
    cmp edi, esi
    je square
    
rectangle:
    add eax, esi
    shl eax, 1
    ret
    
square:
    imul eax, esi
    ret
; ---------> end of area_or_perim <---------
________________________
global area_or_perimeter

section .text

; <----- int area_or_perimeter(int length, int width) ----->
area_or_perimeter:
    mov eax, edi    ; EAX <- the result
    mul esi
    lea edx, [edi + esi]
    shl edx, 1
    test edi, esi
    cmovns eax, edx
    ret
; ---------> end of area_or_perim <---------
