%ifndef FMTDURATION_ASM
%define FMTDURATION_ASM

global fmtduration
extern malloc

; <--- [byte RAX] fmtduration(EDI n) --->
fmtduration:
    push rdi
    sub rsp, 40h
    mov rcx, 128
    call malloc             ; create 128 byte buffer for output string
    add rsp, 40h
    mov rdi, rax            ; rdi holds pointer to output string buffer
    mov r10, rax            ; r10 also holds a copy - kept unmodified for comparison and return
    pop rax                 ; function parameter (total seconds) is now in eax
    test eax, eax
    jz .return_now          ; exit early on 0 seconds        
    mov r9d, 10
    mov ecx, 31536000       ; seconds per year
    mov r8, year 
    call write_time
    mov ecx, 86400          ; seconds per day
    mov r8, day
    call write_time
    mov ecx, 3600           ; seconds per hour
    mov r8, hour
    call write_time
    mov ecx, 60             ; seconds per minute
    mov r8, minute
    call write_time
    mov ecx, 1              ; seconds per second
    mov r8, second    
    call write_time
    mov byte [rdi], 0   ; terminator
    mov rax, r10 ; pointer to string start into rax for return
    ret
            
    .return_now:
    mov dword [rdi], "now"    
    mov rax, rdi
    ret

;helper function that writes a numeric portion of the output and the time unit name 
;expects eax to have the amount of seconds
;expects ecx to be the number of seconds in the time unit being written
;expects rdi to be pointer to write chars at
;expects r8 to be pointer to string containing plural name of time unit
;expects r9d to contain the base the number is to be written in (so 10) - need in register for division
;expects r10 to hold the start of the string being written to (to detect if it has been written to yet)
;returns seconds remaining eax
;returns rdi pointing to after last char written
;r9 & r10 unchanged
;clobbers rcx, rdx, r8
write_time:    
    cmp eax, ecx            
    jb .end_write_time      ; no number to write if smaller than the size of the time unit
    xor edx, edx
    div dword ecx
    push rdx                ; save the seconds remaining not in this time unit
    push rax                ; save the number of time units    
    cmp rdi, r10            ; if current and inital string pointers are equal, no need for comma or " and " before number
    je .ready_to_read       
      test rdx, rdx         ; if remainder is not zero, this is not the last number, its a comma, if it is zero its " and "
      jnz .do_comma
        mov byte [rdi], ' ' ; add an " and " to the string
        inc rdi
        mov dword [rdi], "and " ; over 2 moves, which can probably be done better
        add rdi, 4
        jmp .ready_to_read
      .do_comma:
      mov word [rdi], ", "
      add rdi, 2    
    .ready_to_read:    
    xor ecx, ecx            ; char counter for .char_read_loop 
    .char_read_loop:        ; get digits in reverse order and push to stack
        xor edx, edx
        div r9d
        add edx, '0'
        push rdx
        inc rcx
    test eax, eax
    jnz .char_read_loop     ; pop digits in correct order from stack and write to output string
    .char_write_loop:
        pop rdx
        mov [rdi], dl
        inc rdi
    loop .char_write_loop    
    mov byte [rdi], ' '     ; add a space
    inc rdi
    xor rdx, rdx
    .name_copy_loop:
        mov dl, [r8]
        inc r8
        mov [rdi], dl
        inc rdi        
    test edx, edx           ; test for terminator (edx is gauranteed to be empty apart from low byte)    
    jnz .name_copy_loop    
    dec rdi                 ; don't want the terminator that has just been written
    pop rax                 ; recover the number of time units (the number that has just been written out)
    cmp eax, 1
    ja .s_is_done           ; keep the 's' if more than 1 unit
      dec rdi
    .s_is_done:    
    pop rax                 ; recover the seconds remaining not in this time unit
    .end_write_time:
    ret

section .data
now: db "now", 0
year: db "years", 0
day: db "days", 0
hour: db "hours", 0
minute: db "minutes", 0
second: db "seconds", 0

%endif

__________________________________________________
%ifndef FMTDURATION_ASM
%define FMTDURATION_ASM

global fmtduration
extern strdup
extern sprintf

; <--- [byte RAX] fmtduration(EDI n) --->
fmtduration:
    test edi, edi               ; whether <n> is zero
    jne .start                  ; otherwise, jumping to .start
    mov rdi, .now               ; pointing RDI to <.now>
    jmp strdup                  ; jumping to (strdup) and exiting from here
.start:
    push r15                        ; saving R15 in the stack
    push r14                        ; saving R14 in the stack
    push r13                        ; saving R13 in the stack
    push r12                        ; saving R12 in the stack
    push rbp                        ; saving RBP in the stack
    push rbx                        ; saving RBX in the stack
    sub rsp, 0h98                   ; allocating storage for <fmtdur> and <dur>
    lea rbp, [rsp+0h40]             ; pointing RBP to <fmtdur>
    mov rbx, rsp                    ; pointing RBX to <dur>
    mov qword [rbp-0h08], .singl    ; saving <.singl> locally
    mov qword [rbp-0h10], .plurl    ; saving <.plurl> locally
    mov qword [rbp-0h18], .disj     ; saving <.disj> locally
    mov qword [rbp-0h20], .conj     ; saving <.conj> locally
    mov dword [rbx], 31_536_000     ; saving year duration in <*dur>
    mov dword [rbx+0h04], 86400     ; saving day duration in <*(dur+1)>
    mov dword [rbx+0h08], 3600      ; saving hour duration in <*(dur+2)>
    mov dword [rbx+0h0C], 60        ; saving minute duration in <*(dur+3)>
    mov dword [rbx+0h10], 0         ; saving second duration in <*(dur+4)>
    xor ecx, ecx                    ; resetting ECX as duration <i>terations to extract
    xor esi, esi                    ; resetting ESI as <m>odifications
.loopd:
    mov eax, edi                ; copying <n> to EAX
    xor edx, edx                ; resetting EDX before division
    div dword [rbx]             ; dividing <n> by <*dur>
    mov edi, edx                ; resaving <n> with the reminder from division
    mov [rbx], eax              ; saving the duration in <*dur>
    add rbx, 4                  ; pointing <dur> to the next duration
    test eax, eax               ; whether the duration iz zero
    je $+0h4                    ; skipping the next instruction
    inc esi                     ; incrementing <esi>
    inc ecx                     ; incrementing <i>
    cmp ecx, 4                  ; whether <i> is less than four durations to extract
    jl .loopd                   ; jumping to the next .loopd iteartion if <i> is positive
    test edi, edi               ; whether <n> is not zero
    je $+0h6                    ; otherwise, skipping the next two instructions
    mov [rbx], edi              ; saving the second duration in <*dur>
    inc esi                     ; incrementing <m>
    inc ecx                     ; incrementing <i>
    mov rbx, rsp                ; pointing RBX to the start of <dur>
    mov r12, rbp                ; pointing R12 to <fmtdur>
    xor r13d, r13d              ; resetting R13D as <n>
    mov r14d, ecx               ; moving <i> to R14D
    mov r15d, esi               ; moving <m> to R15D
.loopf:
    mov edx, [rbx+r13*4]        ; copying <*(dur+n)> to EDX as <d>
    test edx, edx               ; whether <d> is zero
    je .exit                    ; jumping to exit
    mov rdi, r12                ; loading RDI with <fmtdur>
    mov rsi, .fmtdur            ; loading RSI with <.fmtdur>
    lea rcx, [.fmt+r13*8]       ; loading RCX with <*(.fmt+n)>
    cmp edx, 1                  ; whether <d> is equal to one
    cmove r8, [rbp-0h08]        ; loading R8 with <.singl>
    cmovg r8, [rbp-0h10]        ; otherwise, loading R8 with <.plurl>
    cmp r15d, 2                 ; whether <m> is less than two
    cmovl r9, [rbp-0h08]        ; loading R9 with <.singl>
    cmovg r9, [rbp-0h18]        ; otherwise, loading R9 with <.disj>
    cmove r9, [rbp-0h20]        ; otherwise, loading R9 with <.conj>
    xor eax, eax                ; resetting EAX forced by monadius though actually there's no need in it
    call sprintf                ; printing to <fmtdur>
    add r12, rax                ; shifting <fmtdur> by EAX characters
    dec r15d                    ; decrementing <m>
.exit:
    inc r13d                    ; decrementing <n>
    cmp r13d, r14d              ; whether <n> is less than <i>
    jl .loopf                   ; jumping to the next .loopf iteration
    mov rdi, rbp                ; loading RDI with <fmtdur>
    call strdup                 ; allocating new space and copying local <fmtdur> into it
    add rsp, 0h98               ; destroying the local storage
    pop rbx                     ; restoring original RBX from the stack
    pop rbp                     ; restoring original RBP from the stack
    pop r12                     ; restoring original R12 from the stack
    pop r13                     ; restoring original R13 from the stack
    pop r14                     ; restoring original R14 from the stack
    pop r15                     ; restoring original R15 from the stack
    ret

; local read-only storages
.fmtdur:
    db  `%u %s%s%s\0`
.singl:
    db  `\0`
.plurl:
    db  `s\0`
.disj:
    db  `, \0`
.conj:
    db  ` and \0`
.fmt:
    db  `year\0\0\0\0`, \
        `day\0\0\0\0\0`, \
        `hour\0\0\0\0`, \
        `minute\0\0`, \
        `second\0\0`
.now:
    db  `now\0`
; -----> endof fmtduration <-----

%endif

__________________________________________________
%ifndef FMTDURATION_ASM
%define FMTDURATION_ASM

global  fmtduration
extern  malloc

; <--- [byte RAX] fmtduration(EDI n) --->
fmtduration:

    ;allocate memory for new string
    xor   rcx,rcx
    mov   ecx,edi
    push  rcx
    mov   rdi,1024
    call  malloc 
    pop   rcx
    push  rax
    mov   rdi,rax

    ;check for zero and UINT_MAX
    cmp   ecx,0
    jg    .write
    cmp   ecx,0xffffffff
    je    .write
    mov   rsi,str_now
    call  write_str
    jmp   .end

.write:
    mov   edx,ecx
    xor   cl,cl
    mov   ebx,60*60*24*365
    mov   rsi,str_year
    call  write_comp
    mov   ebx,60*60*24
    mov   rsi,str_day
    call  write_comp
    mov   ebx,60*60
    mov   rsi,str_hour
    call  write_comp
    mov   ebx,60
    mov   rsi,str_minute
    call  write_comp
    mov   ebx,1
    mov   rsi,str_second
    call  write_comp
.end:
    mov   byte[rdi],0
    pop   rax
    ret

;ebx = seconds per unit
;rsi = unit string
write_comp:
    cmp   edx,0
    je    .end
    mov   eax,edx
    xor   edx,edx
    div   ebx
    cmp   eax,0
    je    .end
    call  write_sep
    call  to_dec
    call  write_units
.end:
    ret

;rsi = source string
write_str:
    push  rsi
    push  rax
.loop:
    lodsb
    cmp   al,0
    je    .end
    stosb
    jmp   .loop
.end:
    pop   rax
    pop   rsi
    ret

;eax = non 1 for adding a final 's'
write_units:
    call  write_str
    cmp   eax,1
    je    .end
    mov   byte[rdi],'s'
    inc   rdi
.end:
    ret

;cl = 0 -> skip separator
;edx = 0 -> " and ", other value -> ", "
write_sep:
    push  rsi
    cmp   cl,0
    je    .end
    cmp   edx,0
    je    .and
.comma:
    mov   byte[rdi],','
    inc   rdi
    jmp   .space
.and:
    mov   rsi,str_and
    call  write_str
.space:
    mov   byte[rdi],' '
    inc   rdi
.end:
    pop   rsi
    ret

;rax = number to convert
;output decimal ascii to rdi and increment it
;cl is set to 1
to_dec:
    push  rax
    push  rbx
    push  rdx
    cmp   eax,100
    jge   .hundreds
    cmp   eax,10
    jge   .tens
    jmp   .units
.hundreds:
    xor   edx,edx
    mov   ebx,100
    div   ebx
    add   al,'0'
    mov   byte[rdi],al
    inc   rdi
    mov   eax,edx
.tens:
    xor   edx,edx
    mov   ebx,10
    div   ebx
    add   al,'0'
    mov   byte[rdi],al
    inc   rdi
    mov   eax,edx
.units:
    add   al,'0'
    mov   byte[rdi],al
    inc   rdi
    mov   cl,1
    pop   rdx
    pop   rbx
    pop   rax
    ret

str_now:
    db  'now',0
str_year:
    db  ' year',0
str_day:
    db  ' day',0
str_hour:
    db  ' hour',0
str_minute:
    db  ' minute',0
str_second:
    db  ' second',0
str_and:
    db  ' and',0


; -----> endof fmtduration <-----

%endif
