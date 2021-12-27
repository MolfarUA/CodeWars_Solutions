#lang racket
(provide sum-of-intervals)

(define (sum-of-intervals intervals)
  (define sorted-intervals (sort intervals < #:key first))
  (for*/fold ([sum 0]
              [max-e (caar sorted-intervals)]
              #:result sum)
             ([i sorted-intervals]
              [b (in-value (first i))]
              [e (in-value (second i))]
              [b1 (in-value (max b max-e))]
              [e1 (in-value (max e max-e))])
    (values (+ sum (- e1 b1)) e1)))
    
___________________
#lang racket
(provide sum-of-intervals)

(define (sum-of-intervals lst)
  (set-count
    (for*/set ([p (in-list lst)]
               [i (in-range (car p) (cadr p))])
      i)))
      
______________________
#lang racket

(module+ test
  (require rackunit))

(provide sum-of-intervals)


;; (List (List Number Number)) -> Integer
;; given a list of intervals, return the sum of all the interval lengths.
;; - overlapping intervals are counted only once
;; ASSUME:
;; - intervals are represented by a pair of numbers
;; - the first number is always less than the second

;; Best conceivable runtime: O(n)
;; Actual runtime: ?

;; idea: first compare the pairs of intervals merging the overlapping ones, then
;; sum up lengths of intervals in the resulting list.
(define (sum-of-intervals lst)
 (apply + (map int-length (merge-overlapping lst))))

(module+ test
  (check-equal? (sum-of-intervals (list (list -22 -9) (list -52 -8) (list -5 24) (list -12 84))) 136)
  (check-equal? (sum-of-intervals (list (list -19 7) (list -14 8) (list -2 46) (list -10 -1))) 65)
  (check-equal? (sum-of-intervals (list (list -56 11) (list -37 23) (list -42 50) (list -40 -20))) 106)
  (check-equal? (sum-of-intervals (list (list -54 -25) (list -54 35) (list -10 46) (list -50 -18))) 100))


;; (List (List Number Number)) -> (List (List Number Number))
;; merge overlapping intervals, if any
;; idea: sort first
(define (merge-overlapping lst)
  (define (loop accum lst)
    (cond
      [(empty? lst) accum]
      [(= (length lst) 1) (append accum lst)]
      [(if (overlap? (first lst) (second lst))
           (loop accum (cons (merge-two (first lst) (second lst)) (rest (rest lst))))
           (loop (append accum `(,(first lst))) (rest lst)))]))
  (loop '() (sort lst < #:key car)))
     
(module+ test
  (check-equal? (merge-overlapping '((1 4) (7 10) (3 5))) '((1 5) (7 10))))


;; (List Number Number) (List Number Number) -> Boolean
;; given two intervals, return #t if they overlap, #f otherwise
(define (overlap? i1 i2)
  (or
   (and (<= (int-start i1) (int-start i2))
        (> (int-end i1) (int-start i2)))
   (and (<= (int-start i2) (int-start i1))
        (> (int-end i2) (int-start i1)))))

(module+ test
  (check-equal? (overlap? '(1 4) '(3 5)) #t)
  (check-equal? (overlap? '(3 5) '(1 4)) #t)
  (check-equal? (overlap? '(3 5) '(7 10)) #f)
  (check-equal? (overlap? '(1 4) '(1 4)) #t)
  (check-equal? (overlap? '(3 7) '(3 7)) #t))


;; (List Number Number) (List Number Number) -> (List Number Number)
;; merge two overlapping intervals
(define (merge-two i1 i2)
  `(,(argmin identity (list (int-start i1) (int-start i2)))
    ,(argmax identity (list (int-end i1) (int-end i2)))))

(module+ test
  (check-equal? (merge-two '(1 4) '(3 5)) '(1 5)))


;; utils


;; (List Number Number) -> Number
;; return the start of the interval
(define (int-start i)
  (first i))


;; (List Number Number) -> Number
;; return the start of the interval
(define (int-end i)
  (second i))

;; (List Number Number) -> Number
;; return the length of the given interval
(define (int-length i)
  (- (int-end i) (int-start i)))
  
_________________________________
#lang racket
(provide sum-of-intervals)

(define (sum-of-intervals lst)
  (length (remove-duplicates (flatten (for*/list 
    ([e lst]
     [i (in-range (first e) (second e))])
    i)))))
