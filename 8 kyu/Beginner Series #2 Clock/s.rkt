55f9bca8ecaa9eac7100004a


#lang racket

(provide past)
 
(define (past h m s)
  (* 1000
     (+ s
        (* m 60)
        (* h 3600))))
__________________________
#lang racket

(provide past)
 
(define (past h m s)
  (+ (* h 60 60 1000) (* m 60 1000) (* s 1000)))
__________________________
#lang racket

(provide past)
 
(define (past h m s)
  (* 1000 (+ s (* 60 (+ m (* 60 h))))))
__________________________
#lang racket

(provide past)
 
(define (past h m s)
  (+ (+ (* h 3600000) (* m 60000)) (* s 1000)))
__________________________
#lang racket

(provide past)
 
(define (past h m s)
  (* 1000 (+ s (* 60 (+ m (* h 60))))))
