global sumintvls
extern free, malloc, memcpy, qsort

; int sumintvls(const struct intvl *v, size_t n)
sumintvls:
                push    r12
                mov     r12, rdi
                push    rbp
                mov     rbp, rsi
                push    rbx
                lea     rdi, [rsi * 8]
                call    malloc
                mov     rbx, rax
                mov     rdi, rax
                mov     rsi, r12
                lea     rdx, [rbp * 8]
                call    memcpy
                mov     rdi, rbx
                mov     rsi, rbp
                mov     rdx, 8
                lea     rcx, [rel cmpintvls]
                call    qsort
                xor     r12d, r12d
                mov     esi, 80000000h
                mov     rax, rbx
.loop:          mov     ecx, [rax]
                cmp     esi, ecx
                cmovg   ecx, esi
                mov     edx, [rax + 4]
                cmp     esi, edx
                cmovg   edx, esi
                mov     esi, edx
                sub     edx, ecx
                add     r12d, edx
                add     rax, 8
                dec     rbp
                jnz     .loop
                mov     rdi, rbx
                call    free
                pop     rbx
                pop     rbp
                mov     rax, r12
                pop     r12
                ret

cmpintvls:
                mov     edx, [rdi]
                xor     eax, eax
                xor     ecx, ecx
                cmp     edx, [rsi]
                setg    al
                setl    cl
                sub     eax, ecx
                ret
                
___________________________________
global sumintvls

; Best practice blah blah

extern qsort

; <-- EAX sumintvls(ro [struct intvl RDI] v, RSI n) -->
sumintvls:
    push rbx                    ; save non-volatile registers
    push r12
    push r13                    
    mov rbx, rsi                ; array length into rbs - to preserve it from qsort calls
    mov rax, 4                  ; multiply length of the argument array by 4
    mul rsi                     ;  which is half its length in bytes (into rax)      
    mov r12, rax                ; copy half-length into r12
    add rax, r12                ; double half-length to get the full length       
    mov r13, rax                ; save this full amount in r13 
    sub rsp, rax                ; and this much space on the stack    
    add r12, rsp                ; set r12 to be the pointer to the second half of the stack space
    xor r9, r9
    xor r8, r8
    ; copy the first number in each interval into an array starting at rsp
    ; copy the second number into an array pointed to by r12 (half way into the created stack space)
    xor rcx, rcx
    .array_copy:
        mov rax, [rdi + r8]     ; read both number into rax
        mov [rsp + rcx], eax    ; first number into first array
        shr rax, 32             ; rotate rax to get other number
        mov [r12 + rcx], eax    ; put it into second array
        add rcx, 4              ; move destination array offset
        add r8, 8               ; move source array offset
        cmp r8, r13
    jne .array_copy             ; exit loop when source has been read
    ; sort 1st stack array (low-end of intervals) from low to high
    mov rdi, rsp                ; pointer to first array for qsort
    mov rsi, rbx                ; array length for qsort
    mov rdx, 4                   ; array element size for qsort
    mov rcx, compare             ; comparison for qsort
    sub rsp, 0x38               ; shadow space and aligh stack
    call qsort
    ; sort 2nd stack array (high-end of intervals) from low to high    
    mov rdi, r12                ; pointer for 2nd stack array for qsort
    mov rsi, rbx                ; array length for qsort
    mov rdx, 4                   ; array element size for qsort
    mov rcx, compare
    call qsort
    add rsp, 0x38               ; remove shadow space
    ; now calculate the answer      
    ; intervals have been sorted but are still equivalent, so can simply skip overlap
    ; by checking current low-end is not lower than previous high-end, and if it is
    ; subsituting the previous high for the current low
    ; do first loop iteration manually to avoid having to special case it (no previous high)
    mov edx, [rsp]              ; first low-end
    mov edi, [r12]              ; first high-end
    mov r8d, edi                ; will become previous high-end in loop
    sub edi, edx                ; calculate first interval
    mov eax, edi                ; eax holds running total
    cmp rbx, 1                  ; skip loop if only 1 element, since loop test is at the end would go beyond array bounds
    je .after_loop                  
    mov r10, rsp                ; first array pointer (second is r12 - no need to save its start position)  
    add r10, 4                  ; move both pointers one element on since first iteration is done
    add r12, 4
    mov rcx, rbx                
    dec rcx                     ; loop counter set to array length -1, since starting on 2nd elements
    .calc_loop:
        mov edx, [r10]          ; low end of interval
        mov edi, [r12]          ; high end of interval
        cmp r8d, edx            ; compare current-low-end to previous-high-end
        jle .edx_is_set         ; if current-low is lower than previous-high
          mov edx, r8d          ; then subsitute current high for previous low
        .edx_is_set:
        mov r8d, edi            ; save current high for next iteration
        sub edi, edx            ; calculate interval: current high - (either current low or previous high)
        add eax, edi            ; add it to running total
        add r10, 4              ; move pointers
        add r12, 4
    loop .calc_loop
    .after_loop:
    add rsp, r13                ; cleanup the stack arrays
    pop r13                     ; restore non-volatile registers
    pop r12                     
    pop rbx                     
    ret
    
; for qsort    
compare:
    mov eax, [rdi]
    cmp eax, [rsi]
    jg .cmp_true
    xor rax, rax
    ret
    .cmp_true:
    mov rax, 1
    ret
    
____________________________________________
global sumintvls

; BestBractice is to use the structure fields even though the offsets are known
struc intvl
    .first:     resd    1
    .second:    resd    1
endstruc

intvl_sz:       equ 0h8

; <-- EAX sumintvls(ro [struct intvl RDI] v, RSI n) -->
sumintvls:
    push rbp
    mov rbp, rsp
    
    ; If there is only one interval then do a simple substraction.
    cmp rsi, 1
    jne normal_execution
    
    xor rax, rax
    mov eax, [rdi + 4]
    sub eax, [rdi]
    jmp sumintvls_end
    
normal_execution:
    ; Sort the intervals based on their .first field
    
    ; This is a nice implementation of bubble sort which I find
    ; pretty elegant. https://gist.github.com/jibsen/8afc36995aadb896b649
sortintvls:
    mov rcx, rsi
    dec rcx
    
.outterloop:
    push rcx
    push rsi
    push rdi
    
    mov rsi, rdi
    
.innerloop:
    mov eax, [rsi]
    mov edx, [rsi + 4]
    add rsi, intvl_sz
    
    cmp eax, [rsi]
    jle short .order_ok
    xchg eax, [rsi]
    xchg edx, [rsi + 4]
    
.order_ok:
    mov [rdi], eax
    mov [rdi + 4], edx
    add rdi, intvl_sz
    
    loop .innerloop
    
    pop rdi
    pop rsi
    pop rcx
    
    loop .outterloop
    
overlapping:
    ; Push the first interval on stack.
    ; Save how many intervals are pushed in <RDX>
    push qword [rdi]
    mov rdx, 0x01
    
    ; Loop through intervals. If intervals overlap the
    ; one on stack then update the stack interval, otherwise
    ; push a new independent interval.
    ;
    ; At the end of this part we should have all combined intervals.
    
    ; <RCX> is used as counter.
    mov rcx, rsi
    dec rcx
    ; Loop starts from the second element because the first was already pushed
    ; on stack.
    add rdi, intvl_sz
    
.intvls_loop:
    ; If intvls[i].first > stack_intvl.second then intvls[i] does not overlap.
    mov eax, [rdi]
    cmp eax, [rsp + 4]
    jg .push_intvl
    
    ; stack_intvl.first = min(stack_intvl.first, intvls[i].first)
    cmp eax, [rsp]
    cmovg eax, [rsp]
    mov [rsp], eax
    
    ; stack_intvl.second = max(stack_intvl.second, intvls[i].second)
    mov eax, [rdi + 4]
    cmp eax, [rsp + 4]
    cmovl eax, [rsp + 4]
    mov [rsp + 4], eax
    
    jmp .intvls_loop_reload

.push_intvl:
    ; Push an independent interval on stack(an interval that does not overlap
    ; with the one that is already on stack).
    push qword [rdi]
    inc rdx
    
.intvls_loop_reload:
    add rdi, intvl_sz
    loop .intvls_loop
    
intvls_sum:
    ; Now all intervals from the stack will be popped and 
    ; intvl.second - intvl.first will be added to sum which is saved
    ; in <EAX>

    ; <RCX> is used as counter.
    mov rcx, rdx
    xor rax, rax
    
.compute_sum:
    add eax, [rsp + 4]
    sub eax, [rsp]
    
    add rsp, 8
    loop .compute_sum
    
sumintvls_end:
    mov rsp, rbp
    pop rbp
    ret
; -----> endof sumintvls <-----

________________________________________
global sumintvls
extern qsort

struc intvl
    .first:     resd    1
    .second:    resd    1
endstruc

intvl_sz:       equ 0h8

; <-- EAX intvlcmp(ro [struct intvl RDI] v1, ro [struct intvl RSI] v1) -->
intvlcmp:
    xor eax, eax                    ; resetting the result
    mov ecx, [rdi+intvl.first]      ; setting ECX to <v1->first> as <first>
    mov edx, [rsi+intvl.first]      ; setting EDX to <v2->second> as <second>
    mov edi, 1                      ; setting EDI to one
    mov esi, -1                     ; setting ESI to minus one
    cmp ecx, edx                    ; whether <first> is equal to <second>
    cmovg eax, edi                  ; otherwise, if greater, setting the result to one
    cmovl eax, esi                  ; otherwise, if less, setting the result to minus one
    ret
; -----> endof intvlcmp <-----

; <-- EAX sumintvls(ro [struct intvl RDI] v, RSI n) -->
sumintvls:
    push rbx                        ; saving RBX onto the stack
    imul rax, rsi, intvl_sz         ; the target bytes to store <v>
    or rax, 0h8                     ; aligning the number of bytes to the boundary <nalign>
    sub rsp, rax                    ; allocating storage for <m>
    mov rbx, rsp                    ; pointing RBX to <m>
    push rax                        ; saving <nalign> onto the stack
    push rsi                        ; saving <n> in the stack
    mov rcx, rsi                    ; copying <n> to RCX
    mov rax, rbx                    ; pointing RAX to <m>
.lpcpy:
    mov rdx, [rdi]                  ; copying <*v> to RDX as <intvl>
    mov [rax], rdx                  ; saving <intvl> in the local storage <m>
    add rdi, intvl_sz               ; pointing <v> to the next interval
    add rax, intvl_sz               ; pointing <m> to the next free location
    dec rcx                         ; decrementing <n>
    ja .lpcpy                       ; jumping to the next .lpcpy iteration if above zero
    mov rdi, rbx                    ; pointing RDI to the start of <m>
    mov rdx, intvl_sz               ; setting RDX to the size of interval structure
    mov rcx, intvlcmp               ; pointing RCX to the function to compare
    call qsort                      ; quick sorting <m>
    pop rsi                         ; restoring <n> from the stack
    pop r11                         ; restoring <nalign> from the stack
    xor eax, eax                    ; resetting EAX as <sum>
    mov edi, [rbx+intvl.first]      ; setting EDI to <m->first> as <extramax>
    sub rbx, intvl_sz               ; pointing <m> before the first interval
    inc rsi                         ; incrementing <n> to start from decrementing
    jmp .exit                       ; jumping to exit
.loop:
    add rbx, intvl_sz               ; pointing <m> to the next interval
    mov ecx, [rbx+intvl.first]      ; setting <min> to <m->first>
    mov edx, [rbx+intvl.second]     ; setting <max> to <m->second>
    cmp edx, edi                    ; whether <max> is greater than <extramax>
    jle .exit                       ; otherwise, jumping to exit
    cmovg r8d, edi                  ; setting <extra> to <max>
    cmp ecx, edi                    ; whether <min> is less than <extramax>
    cmovge r8d, ecx                 ; otherwise, setting <extra> to <min>
    add eax, edx                    ; adding <max> to <sum>
    sub eax, r8d                    ; subtracting <extra> from <sum>
    mov edi, edx                    ; updating <extramax> with <max>
.exit:
    dec rsi                         ; decrementing <n>
    jnz .loop                       ; jumping to the next iteration if above zero
    add rsp, r11                    ; destroying the local storage <m>
    pop rbx                         ; restoring the original RBX from the stack
    ret
; -----> endof sum_intervals <-----
