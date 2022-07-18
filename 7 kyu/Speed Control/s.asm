56484848ba95170a8000004d


;    int gps(int s, int sz, double* x);
;    s  := edi
;    sz := esi
;    *x := rdx

global gps

section .text

gps:
    xor eax, eax
    xorps xmm0, xmm0
    xorps xmm1, xmm1
_loop:
    dec esi
    test esi, esi
    jz _exit
    movsd xmm0, [rdx + rsi * 8]
    subsd xmm0, [rdx + (rsi - 1) * 8]
    comisd xmm0, xmm1
    ja _update
    jmp _loop
_update:
    movsd xmm1, xmm0
    jmp _loop
_exit:
    mulsd xmm1, [f]
    cvtsi2sd xmm0,edi
    divsd xmm1, xmm0
    cvttsd2si  eax, xmm1
    ret
    
    
section .data
    f dq 0x40ac200000000000
_____________________________
;    int gps(int s, int sz, double* x);
;    s  := edi
;    sz := esi
;    *x := rdx

global gps

section .text

gps:
    xor eax, eax
    xorps xmm0, xmm0
    xorps xmm1, xmm1
_loop:
    dec esi
    test esi, esi
    jz _exit
    movsd xmm0, [rdx + rsi * 8]
    subsd xmm0, [rdx + (rsi - 1) * 8]
    comisd xmm0, xmm1
    ja _update
    jmp _loop
_update:
    movsd xmm1, xmm0
    jmp _loop
_exit:
    mulsd xmm1, [f]
    cvtsi2sd xmm0,edi
    divsd xmm1, xmm0
    cvttsd2si  eax, xmm1
    ret
    
    
section .data
    f dq 0x40ac200000000000
