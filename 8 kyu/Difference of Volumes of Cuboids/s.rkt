58cb43f4256836ed95000f97


#lang racket
(provide find-difference)

(define (find-difference a b)
  (abs (- (apply * a) (apply * b))))
________________________
#lang racket
(provide find-difference)

(define (find-difference a b)
  (abs (- (mySum a) (mySum b)))
  )
  
(define (mySum lst)
 (foldr * 1 lst))
________________________
#lang racket
(provide find-difference)

(define (cuboid-volume dims)
  (apply * dims))

(define (find-difference a b)
  (abs (- (cuboid-volume a) (cuboid-volume b))))
