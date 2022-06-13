global are_coprime

section .text
      
; bool are_coprime(unsigned a, unsigned b)
are_coprime:
                mov     eax, edi
                or      eax, esi
                and     eax, 1
                jz      .done
                tzcnt   eax, edi
                tzcnt   edx, esi
                shrx    edi, edi, eax
                shrx    esi, esi, edx
.loop:          mov     eax, edi
                sub     eax, esi
                tzcnt   ecx, eax
                mov     edx, esi
                sub     edx, edi
                cmovb   edx, eax
                cmovb   edi, esi
                shrx    esi, edx, ecx
                jnz     .loop
                cmp     edi, 1
                sete    al
.done:          ret
___________________________
global are_coprime

section .text
      
are_coprime:
  mov eax, edi
  mov ecx, esi
_loop:
  test ecx, ecx
  jz _exit
  xor edx, edx
  div ecx
  mov eax, edx
  xchg eax, ecx
  jmp _loop
_exit:
  cmp eax, 1
  je _ret
  xor al, al
_ret:
  ret
;<--    end of are_coprime -->
