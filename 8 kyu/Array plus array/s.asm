5a2be17aee1aaefe2a000151


section .text
global arrplusarr

; <-- RAX arrplusarr([dword RDI] a, [dword RSI] b, RDX na, RCX nb) -->
arrplusarr:
  xor rax, rax
  xor r10, r10
.loop_a:
  dec rdx
  jl .loop_b
  movsx r10, dword[rdi + rdx * 4]
  add rax, r10
  jmp .loop_a
.loop_b:
  dec rcx
  jl .end
  movsx r10, dword[rsi + rcx * 4]
  add rax, r10
  jmp .loop_b
.end:
  ret
_________________________
global arrplusarr

arrplusarr:
  xor rax,rax
  .b:movsx r8,dword[rsi+rcx*4-4]
     add   rax,r8
  loop .b
  .c:movsx r8,dword[rdi+rdx*4-4]
     add   rax,r8
     dec   rdx
  jne .c
ret
_________________________
global arrplusarr

; <-- RAX arrplusarr([dword RDI] a, [dword RSI] b, RDX na, RCX nb) -->
arrplusarr:
    xor rax, rax
.first:
    test rdx, rdx
    jz .next
    dec rdx
    movsx rbx, dword [rdi + rdx * 4]
    add rax, rbx
    jmp .first
.next:
    test rcx, rcx
    jz .exit
    dec rcx
    movsx rbx, dword [rsi + rcx * 4]
    add rax, rbx
    jmp .next
.exit:
    ret
