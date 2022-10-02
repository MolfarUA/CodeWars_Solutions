5547cc7dcad755e480000004


#lang racket
(provide remove-nb)

(define (remove-nb n)
  (define sum (* n (+ n 1) 1/2))
  (for*/list ([x (in-range 1 (+ n 1))]
              [y (in-value (/ (- sum x) (+ 1 x)))]
              #:when (and (<= y n) (integer? y)))
    (cons x y)))
______________________________
#lang racket
(provide remove-nb)

(define (fdta n b response)
  (if (empty? b)
      response
      (let* ([sum (quotient (* n (add1 n)) 2)]
             [b-val (first b)]
             [x (- sum b-val)]
             [y (add1 b-val)]
             [a-val (quotient x y)]
             [a-rem (remainder x y)])
        (if (and (= a-rem 0) (<= a-val n))
            (fdta n (rest b) (append response (list (cons b-val a-val))))
            (fdta n (rest b) response))
        )
      )
  )

(define (remove-nb n)
  (fdta n (range (add1 n)) '()))
______________________________
#lang racket
(provide remove-nb)

(define (remove-nb n)
  (define m (* n (add1 n) 1/2))
  (for*/list ([x (in-range 1 (add1 n))]
              [y (in-value (quotient (- m x) (add1 x)))]
              #:when (and (<= y n) (= (* y x) (- m x y))))
    (cons x y)))
