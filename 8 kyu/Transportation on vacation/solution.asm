568d0dd208ee69389d000016


global rental_car_cost

section .text

; <--- unsigned rental_car_cost(unsigned d) --->
rental_car_cost:
    mov eax, 0h28       ; moving to EAX forty
    mul edi             ; multiplying by <d> to get the usual cost
    cmp edi, 0h02       ; whether the rent is less than two days
    jle .exit           ; jumping to exit
    sub eax, 0h14       ; subtracting twenty from the cost
    cmp edi, 0h06       ; whether the rent is less than six days
    jle .exit           ; jumping to exit
    sub eax, 0h1E       ; subtracting thirty from the cost
.exit:
    ret
; -----> end of rental_car_cost <-----
__________________________
global rental_car_cost

section .text

; unsigned rental_car_cost(unsigned d)
rental_car_cost:
                lea     eax, [edi * 5]
                lea     eax, [rax * 8]
                lea     ecx, [rax - 20]
                lea     edx, [rax - 50]
                cmp     edi, 3
                cmovae  eax, ecx
                cmp     edi, 7
                cmovae  eax, edx
.done:          ret
__________________________
global rental_car_cost

section .text

; <--- unsigned rental_car_cost(unsigned d) --->
rental_car_cost:
  imul eax, edi, 40
  lea edx, [eax - 20]  
  cmp edi, 3
  cmovae eax, edx
  lea edx, [eax - 30]
  cmp edi, 7
  cmovae eax, edx
  ret
; -----> end of rental_car_cost <-----
