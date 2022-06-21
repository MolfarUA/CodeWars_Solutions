5545f109004975ea66000086


#lang racket

(provide is-divisible)

(define (is-divisible n x y)
  (= 0 (+ (modulo n x) (modulo n y))))
_____________________
#lang racket

(provide is-divisible)

(define (is-divisible n x y)
  (zero? (+ (remainder n x) (remainder n y))))
_____________________
#lang racket

(provide is-divisible)

(define (is-divisible n x y)
  (and (integer? (/ n x)) (integer? (/ n y))))
