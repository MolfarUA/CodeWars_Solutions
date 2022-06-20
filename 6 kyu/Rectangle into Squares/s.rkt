55466989aeecab5aac00003e


#lang racket
(provide sq-in-rect)

(define (sq-in-rect lng wdth)
  (letrec ((helper
            (lambda (l w)
              (let ((dim1 (max l w)) (dim2 (min l w)))
                (cond
                  ((eq? 0 dim2) '())
                  (#t (cons dim2 (helper (- dim1 dim2) dim2) ))
                )
              )
            )))
    (if (eq? lng wdth) '() (helper lng wdth)))
  )
______________________________
#lang racket
(provide sq-in-rect)

(define (sq-in-rect x y) (if (= x y) '() (to-list x y)))

(define (to-list x y)
  (cond
    [(= x y) `(,y)]
    [(< x y) (to-list y x)]
    [else (cons y (to-list (- x y) y))]))
______________________________
#lang racket
(provide sq-in-rect)

(define (sq-in-rect lng wdth)
  (define (aux a b acc)
    (if (or (<= a 0) (<= b 0))
        acc
        (let* ([c (if (> a b) b a)]
               [a1 (if (> a b) (- a b) a)]
               [b1 (if (> a b) b (- b a))])
        (aux a1 b1 (append acc (list c))))))
  (if (= lng wdth)
    null
    (aux lng wdth null)))
