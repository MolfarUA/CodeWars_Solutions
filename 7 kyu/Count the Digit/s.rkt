566fc12495810954b1000030


#lang racket
(provide nb-dig)

(define (nb-dig n d)
  (define c (string-ref (~a d) 0))
  (for/sum [(k (range (add1 n)))]
           (count (curry equal? c) 
                  (string->list (number->string (sqr k))))))
____________________________
#lang racket
(provide nb-dig)

(define (digits n) 
  (let loop ((acc '()) (i n)) 
    (if (< i 10) 
        (cons i acc) 
        (loop 
         (cons (remainder i 10) acc) 
         (floor (/ i 10))))))

(define (nb-dig n d)
  (let loop ((i 0) (sum 0))
    (if (> i n) sum
        (loop (add1 i) 
          (+ sum (count 
            (lambda (x) (eq? x d)) 
            (digits (* i i))))))))
____________________________
#lang racket
(provide nb-dig)

(define (check-digits number k l digit counter)
  (if (= l 0) (nb-dig2 number k digit counter)
    (let ([i (remainder l 10)])
      (if (eq? i digit) (check-digits number k (quotient l 10) digit (+ counter 1)) 
        (check-digits number k  (quotient l 10) digit counter))))
)

(define (nb-dig2 number k digit counter)
  (if (= k number) counter 
    (let ([l (expt (+ k 1) 2)])
      (check-digits number (+ k 1) l digit counter)))
)

(define (nb-dig n d)
  (if (= d 0) (nb-dig2 n -1 d 1)
    (nb-dig2 n -1 d 0))
)
