52f677797c461daaf7000740


#lang racket
(provide solution)

(define (solution lst)
  (* (length lst)
     (foldl gcd 0 lst))
)
_______________________________
#lang racket
(provide solution)

(define (solution lst)
  (* (length lst)
     (apply gcd lst)))
_______________________________
#lang racket/base

(provide solution)

(define (solution xs) (* (length xs) (apply gcd xs)))
