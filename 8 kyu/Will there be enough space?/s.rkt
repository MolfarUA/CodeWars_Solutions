5875b200d520904a04000003

#lang racket

(provide enough)

(define (enough cap on wait)
  (max 0 (- (+ on wait) cap)))
______________________________
#lang racket

(provide enough)

(define (normalize x) 
  (cond 
   ((>= x 0) 0)
   (else (abs x))))

(define (enough cap on wait)
  (normalize (- cap (+ on wait))))
______________________________
#lang racket

(provide enough)

(define (enough cap on wait)
  (let 
    ([x (-(- cap on wait))])
    (if (<= x 0) 0 x)
  )
)
______________________________
#lang racket

(provide enough)

(define (enough cap on wait)
  (max 0 (+ on (- wait cap))))
