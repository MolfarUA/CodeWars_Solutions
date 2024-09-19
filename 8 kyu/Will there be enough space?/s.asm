5875b200d520904a04000003

section .text
global enough

; int enough(int cap, int on, int wait)
enough:
                add     esi, edx
                xor     eax, eax
                sub     esi, edi
                cmovae  eax, esi
                ret
____________________________
global enough
enough:    
  xor    eax,eax
  add    edx,esi
  sub    edx,edi
  cmovnl eax,edx
ret
____________________________
section .text
global enough

; int enough(int cap, int on, int wait);
; cap := edi
; on := esi
; wait = edx
enough:
  xor eax, eax ; eax the result
  sub edi,esi
  cmp edi,edx
  jl other
  ret

other:
  sub edx,edi
  mov eax,edx
  ret
____________________________
section .text
global enough

; int enough(int cap, int on, int wait);
; cap := edi
; on := esi
; wait = edx
not_en:
  neg eax
  jmp end
enough:
  xor eax, eax ; eax the result
  mov eax , edi 
  sub eax , esi
  sub eax, edx
  cmp eax, 0
  jl not_en
  mov eax, 0
end:
  ret
