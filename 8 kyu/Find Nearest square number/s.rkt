5a805d8cafa10f8b930005ba


#lang racket
(provide nearest-square)

(define (nearest-square n) (expt (exact-round (sqrt n)) 2))
__________________________
#lang racket
(provide nearest-square)

(define (nearest-square n)
  (inexact->exact (expt (round (sqrt n)) 2)))
__________________________
#lang racket
(provide nearest-square)

(define (nearest-square n)
  (inexact->exact (sqr (round (sqrt n)))))
