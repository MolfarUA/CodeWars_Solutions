#lang racket
(provide iter-pi)

(define (walk epsilon pi4 sign denom iterations)
  (if (< (abs (- (* 4.0 pi4) pi)) epsilon)
      (list iterations (/ (round (* (* 4.0 pi4) 1e10)) 1e10))
      (let ([pi4n (+ pi4 (* sign (/ 1.0 denom)))]
            [signn (* sign -1.0)]
            [denomn (+ 2.0 denom)]
            [iterationsn (add1 iterations)])
        (walk epsilon pi4n signn denomn iterationsn))))

(define (iter-pi epsilon)
  (walk epsilon 1.0 -1.0 3.0 1))
________________________________________
#lang racket/base
(provide iter-pi)

(require (only-in racket/math pi)
         racket/flonum
         racket/fixnum)

; round x with: (/ (round (* x 1e10)) 1e10)
(define (iter-pi epsilon)
  (leibnitz epsilon 1.0 1))

(define (leibnitz epsilon approx n)
  (cond [(< (abs (fl- pi (fl* 4.0 approx))) epsilon)
         (list n (round-ten (fl* 4.0 approx)))]
        [else
         (when (zero? (modulo n 1000)) (println (round-ten (fl* 4.0 approx))))
         (leibnitz epsilon
                   (fl+ approx (exact->inexact (/ (expt -1 n) (fx+ (fx* 2 n) 1))))
                   (add1 n))]))

(define (round-ten x)
  (fl/ (round (fl* x 1e10)) 1e10))
________________________________________
#lang racket
(provide iter-pi)

; round x with: (/ (round (* x 1e10)) 1e10)
(define (iter-pi epsilon)
  (define (round-pi x)
    (/ (round (* x 1e10)) 1e10))
  
  (define (helper-plus base acc iterations)
    (cond [(< (abs (- (* acc 4) pi)) epsilon) `(,iterations ,(round-pi (* acc 4)))]
           [else (helper-minus (+ base 2) (+ acc (/ 1 base)) (+ iterations 1))]))
  
  (define (helper-minus base acc iterations)
    (cond [(< (abs (- (* acc 4) pi)) epsilon) `(,iterations ,(round-pi (* acc 4)))]
           [else (helper-plus (+ base 2) (- acc (/ 1 base)) (+ iterations 1))]))
  
  (helper-minus 3.0 1.0 1))
________________________________________
#lang racket
(provide iter-pi)

(define (iter-pi epsilon)
  (define (round-result x)
    (/ (round (* x 1e10)) 1e10))
  (let loop ([x 1.0] [S 0.0] [s 1.0] [c 0])
    (if (< (abs (- (* 4 S) pi)) epsilon)
        (list c (round-result (* 4 S)))
        (loop (+ x 2.0) (+ S (/ s x)) (* s -1.0) (+ c 1)))))

