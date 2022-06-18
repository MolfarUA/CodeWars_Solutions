#lang racket

(provide find-needle)

(define (find-needle lst)
  (format "found the needle at position ~a"
          (index-of lst "needle")))
________________________
#lang racket

(provide find-needle)

(define (find-needle lst)
  (string-append "found the needle at position " (number->string (index-of lst "needle")))
)
________________________
#lang racket

(provide find-needle)

(define (find-needle lst)
  (let ([pos (~a (index-of lst "needle"))]
        [str "found the needle at position "])
    (string-append str pos)))
________________________
#lang racket

(provide find-needle)

(define (needle-idx lst)
  (if (equal? (car lst) "needle") 0 (+ 1 (needle-idx (cdr lst)))))

(define (find-needle lst)
  (format "found the needle at position ~a" (needle-idx lst)))
________________________
#lang racket

(provide find-needle)

(define (find-needle lst)
  (let ([lst-tail (member "needle" lst)]
        [found-msg "found the needle at position "])
    (when lst-tail
      (~a found-msg
          (apply - (map length
                        (list lst lst-tail)))))))
