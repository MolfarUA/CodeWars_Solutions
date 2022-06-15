section     .text
global      fakebin

fakebin:
    xor     rax, rax
    xor     rdx, rdx
    xor     rcx, rcx

    dec     rdx
    
_loop:
    inc     rdx
    mov     cl, [rdi + rdx]

    cmp     cl, 0
    jz      _exit

    cmp     cl, 0x35
    jge     _one

    cmp     cl, 0x35
    jl      _zero

    jmp     _loop

_one:
    mov     [rsi + rdx], BYTE '1'
    jmp     _loop

_zero:
    mov     [rsi + rdx], BYTE '0'
    jmp     _loop
    

_exit:
    mov     [rsi + rdx], BYTE 0
    mov     rax, rsi
    ret
__________________________________
global fakebin

section .text

fakebin:    
    push rsi
    mov r15,rdi
    mov rdi,rsi
l1: cmp byte [r15], 0
    je _done
    cmp byte [r15],'5'
    setae al
    add al,'0'
    stosb
    inc r15
    jmp l1
_done:
    mov byte [rdi],0
    pop rax
    ret
__________________________________
global fakebin

section .text

fakebin:    
    push rsi
l1: cmp byte [rdi],0
    je _done
    cmp byte [rdi],'5'
    setae dl
    add dl,'0'
    mov byte [rsi],dl
    inc rsi
    inc rdi
    jmp l1
_done:
    mov byte [rsi],0
    pop rax
    ret
__________________________________
global fakebin

section .text

; <----- char *fakebin(const char *digits, char *buffer) ----->
fakebin:    
    ; rax should return the pointer to <buffer>
    xchg rsi, rdi
    push rdi
    
.loop:
    lodsb
    test al, al
    jz .end
    cmp al, '5'
    jl .zero
    jmp .one
    
.zero:
    mov al, '0'
    stosb
    jmp .loop
    
.one:
    mov al, '1'
    stosb
    jmp .loop
    
.end:
    stosb
    pop rax
    ret
; ---------> end of fakebin <---------
