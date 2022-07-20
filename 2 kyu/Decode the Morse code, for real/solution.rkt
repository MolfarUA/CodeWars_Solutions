54acd76f7207c6a2880012bb


#lang racket
(require "preloaded.rkt")
(provide decode-bits-advanced decode-morse)

(define (decode-bits-advanced bits)
  (let ([result ""]
        [groups (regexp-match* #px"0+|1+" (regexp-replace* #px"^0*|0*$" bits ""))])
    (if (empty? groups) result
        (let* ([dash (apply max (map string-length (regexp-match* #px"1+" bits)))]
               [shortest (apply min (map string-length groups))]
               [dash (if (= shortest dash) (* 2 dash) dash)]
               [dot (/ dash 2)]
               [space (+ dash 3)]        
               [dictionary (hash #\0 '("" " " "   ") #\1 '("." "-"))])
          (for ([group groups])
            (let* ([len (string-length group)]
                   [index (if (<= len dot) 0 (if (>= len space) 2 1))]
                   [type (hash-ref dictionary (string-ref group 0))]
                   [code (list-ref type index)])
                   (set! result (string-append result code))))))
    result))

(define (decode-morse morse-code)
  (define (split-words morse-code)
    (string-split (string-trim morse-code) "   "))
  (define (decode-word word)
    (define (split-letters word)
      (string-split word " "))
    (define (decode-letter letter)
      (hash-ref MORSE-CODE letter ""))  
    (string-join (map decode-letter (split-letters word)) ""))
  (string-join (map decode-word (split-words morse-code)) " "))
