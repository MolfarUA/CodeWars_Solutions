#lang racket

(provide dna->rna)

(define (dna->rna dna)
  (string-replace dna "T" "U"))
  
_____________________________
#lang racket

(provide dna->rna)

(define (dna->rna dna)
  ; replace 't' with 'u'
 (string-replace dna "T" "U"))
 
_____________________________
#lang racket

(provide dna->rna)

(define (dna->rna dna)
  (regexp-replace* #rx"T" dna "U"))
  
_____________________________
#lang racket

(provide dna->rna)

(define (swap-thymine a) (if (char=? a #\T) #\U a))

(define (dna->rna dna)
   (list->string (reverse (for/fold ([rna null])
            ([a (string->list dna)])
    (list* (swap-thymine a) rna)))))
    
_____________________________
#lang racket

(provide dna->rna)

(define (dna->rna dna)
  (string-append* (map (lambda (character) (if (char=? character #\T) "U" (string character))) (string->list dna))))
