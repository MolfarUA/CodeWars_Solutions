section .data
  K dq 273.15
  R dq 0.082
  
section .text
global total_pressure

; double total_pressure(
;        double molar_mass1 (xmm0), double molar_mass2 (xmm1),
;        double given_mass1 (xmm2), double given_mass2 (xmm3),
;        double v (xmm4), double t (xmm5));

total_pressure:
.moles:
  divsd xmm2, xmm0
  divsd xmm3, xmm1
  addsd xmm2, xmm3
  
.pressure:
  addsd xmm5, [K]
  mulsd xmm2, [R]
  mulsd xmm2, xmm5
  divsd xmm2, xmm4
  
  movq xmm0, xmm2
  ret
  
##############
section .text
global total_pressure

R dq 0.082
K dq 273.15

; double total_pressure(
;        double mM1 (xmm0), double mM2 (xmm1), double gM1 (xmm2), 
;        double gM2 (xmm3), double v (xmm4), double t (xmm5));

total_pressure:
  vunpcklpd xmm0, xmm1
  vunpcklpd xmm2, xmm3
  vdivpd xmm2, xmm0
  vhaddpd xmm0, xmm2, xmm2
  vaddsd xmm5, [K]
  vmulsd xmm0, [R]
  vmulsd xmm0, xmm5
  vdivsd xmm0, xmm4
  ret
  
###############
section .data
  K dq 273.15
  R dq 0.082
  
section .text
global total_pressure

; double total_pressure(
;        double molar_mass1 (xmm0), double molar_mass2 (xmm1),
;        double given_mass1 (xmm2), double given_mass2 (xmm3),
;        double v (xmm4), double t (xmm5));

total_pressure:
 ; result = xmm0
.molews:    
  divsd xmm2, xmm0
  divsd xmm3, xmm1
  addsd xmm2, xmm3
  
.pressure:
  addsd xmm5, [K]
  mulsd xmm2, [R]
  mulsd xmm2, xmm5
  divsd xmm2, xmm4
  
  movq xmm0, xmm2
  ret
  
#################
section .text
global total_pressure
; double total_pressure(
;        double molar_mass1 (xmm0), double molar_mass2 (xmm1),
;        double given_mass1 (xmm2), double given_mass2 (xmm3),
;        double v (xmm4), double t (xmm5));

K:   dq 273.15
R:   dq 0.082

total_pressure:
    divsd xmm2, xmm0
    divsd xmm3, xmm1
    addsd xmm2, xmm3
    addsd xmm5, [K]
    mulsd xmm2, xmm5
    mulsd xmm2, [R]
    divsd xmm2, xmm4
    movsd xmm0, xmm2
    ret
    
#############
section .data
  a dq 0.082
  b dq 273.15
section .text
global total_pressure

; double total_pressure(
;        double molar_mass1 (xmm0), double molar_mass2 (xmm1),
;        double given_mass1 (xmm2), double given_mass2 (xmm3),
;        double v (xmm4), double t (xmm5));

total_pressure:
  divsd xmm2,xmm0
  divsd xmm3,xmm1
  addsd xmm2,xmm3
  movq xmm0,qword[a]
  mulsd xmm2,xmm0
  movq xmm0,qword[b]
  addsd xmm5,xmm0
  mulsd xmm2,xmm5
  divsd xmm2,xmm4
  movsd xmm0,xmm2
    ret
