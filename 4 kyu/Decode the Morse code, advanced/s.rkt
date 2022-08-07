54b72c16cd7f5154e9000457


#lang racket
(require "preloaded.rkt")            ; holds the data structure MORSE-CODE for you
(provide decode-morse decode-bits)

(define (decode-morse morse-code)
  (define codes (string-split morse-code #px" {1,2}"))
  (apply string-append
         (for/list ([code codes])
           (if (string=? code "")
               " "
               (hash-ref MORSE-CODE code)))))

(define (decode-bits bits)
  (define trimmed (string-trim bits "0"))
  (define groups (group-bits (string->list trimmed)))
  (apply string-append
         (for/list ([g (normalize groups)])
           (define c (car g))
           (define count (cdr g))
           (cond [(and (char=? c #\1) (= count 1)) "."]
                 [(char=? c #\1) "-"]
                 [(and (char=? c #\0) (= count 1)) ""]
                 [(and (char=? c #\0) (<= count 3)) " "]
                 [else "   "]))))

(define (group-bits bits)
  (cond [(null? bits) null]
        [else
         (define b (first bits))
         (define-values (chunk rest-bits)
           (splitf-at (rest bits) (lambda (x) (char=? x b))))
         (cons (cons b (add1 (length chunk))) (group-bits rest-bits))]))

(define (normalize groups)
  (define unit-len
    (for/fold ([min-len #f])
              ([g groups])
      (define len (cdr g))
      (if (or (not min-len) (< len min-len))
          len
          min-len)))
  (for/list ([g groups])
    (cons (car g) (quotient (cdr g) unit-len))))
_____________________________
#lang racket
(require "preloaded.rkt")            ; holds the data structure MORSE-CODE for you
(provide decode-morse decode-bits)

(define (decode-morse morse-code)
  (define codes (string-split morse-code #px" {1,2}"))
  (string-join
   (for/list ([code codes])
     (if (string=? code "")
         " "
         (hash-ref MORSE-CODE code)))
   ""))

(define (decode-bits bits)
  (define trimmed (string-trim bits "0"))
  (define groups (group-bits (string->list trimmed)))
  (string-join
   (for/list ([g (normalize groups)])
     (define c (car g))
     (define count (cdr g))
     (cond [(and (char=? c #\1) (= count 1)) "."]
           [(char=? c #\1) "-"]
           [(and (char=? c #\0) (= count 1)) ""]
           [(and (char=? c #\0) (<= count 3)) " "]
           [else "   "]))
   ""))

(define (group-bits bits)
  (cond [(null? bits) null]
        [else
         (define b (first bits))
         (define-values (chunk rest-bits)
           (splitf-at (rest bits) (lambda (x) (char=? x b))))
         (cons (cons b (add1 (length chunk))) (group-bits rest-bits))]))

(define (normalize groups)
  (define unit-len
    (for/fold ([min-len #f])
              ([g groups])
      (define len (cdr g))
      (if (or (not min-len) (< len min-len))
          len
          min-len)))
  (for/list ([g groups])
    (cons (car g) (quotient (cdr g) unit-len))))
_____________________________
#lang racket
(require "preloaded.rkt")            ; holds the data structure MORSE-CODE for you
(provide decode-morse decode-bits)

(define translation-table
  #hash(((#\1 . 1) . ".")
        ((#\1 . 2) . "-") ; what the ...
        ((#\1 . 3) . "-")
        ((#\0 . 3) . " ")
        ((#\0 . 7) . "   ")))

(define (group l)
  (let loop ([l (cdr l)] [c 1] [prev (car l)])
    (if (null? l)
        (list (cons prev c))
        (let ([fst (car l)] [rst (cdr l)])
          (if (eq? prev fst)
              (loop rst (add1 c) prev)
              (cons (cons prev c) (loop rst 1 fst)))))))

(define (decode-bits b)
  (define raw (group (string->list (string-trim b #rx"0"))))
  (define time-unit (cdr (argmin cdr raw)))
  (define (normalize g)
    (cons (car g) (/ (cdr g) time-unit)))
  (define formed-signal
    (map (λ (g) (hash-ref translation-table (normalize g) "")) raw)) 
  (apply string-append formed-signal))

(define (decode-morse code)
  (define l (map string-split (string-split code "   ")))
  (string-join
    (for/list ([w (in-list l)])
      (apply string-append
        (for/list ([c (in-list w)])
          (hash-ref MORSE-CODE c))))))
