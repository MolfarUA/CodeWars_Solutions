561e9c843a2ef5a40c0000a4


#lang racket
(provide gap)

(define (is-prime? n)
  (define (aux i)
    (cond 
      [(> (* i i) n) #t]
      [(or (zero? (modulo n i)) (zero? (modulo n (+ i 2)))) #f]
      [else (aux (+ i 6))]))
  (cond
    [(or (zero? (modulo n 2)) (zero? (modulo n 3))) (< n 4)]
    [else (aux 5)]))

(define (gap g m n)
  (define (aux i a b)
    (cond 
      [(> i (add1 n)) null]
      [(and (> a 0) (> b 0) (= (- b a) g)) (cons a b)]
      [(is-prime? i) (aux (add1 i) b i)]
      [else (aux (add1 i) a b)]))
  (aux m 0 0))
__________________________________
#lang racket
(provide gap)

(define (gap g m n)
  (define (find-prime k end)
    (define (prime? n)
      (cond ( (< n 2) #f)
            ( (= n 2) #t)
            ( (even? n) #f)
            (else
             (let prime-test ( (d 3) )
               (cond ( (> (sqr d) n) #t)
                     ( (= 0 (remainder n d)) #f)
                     (else (prime-test (+ d 2))))))))
    (if (>= k (add1 end))
        -1
        (if (prime? k)
            k
            (find-prime (add1 k) end))))
  
  (define (search i g end)
    (let ([k i])
      (if (>= k (add1 end))
          null
          (let ([p (find-prime (add1 k) end)])
            (if (= p -1)
                null
                (if (= p (+ i g))
                    (cons i p)
                    (search p g end)))))))
  
  (let ([i (find-prime m n)])
    (if (= i -1)
        null
        (search i g n))))
__________________________________
#lang racket
(provide gap)

(define (prime? n)
  (for/and ([i (in-range 2 (add1 (sqrt n)))])
           (positive? (remainder n i))))

(define (gap g m n)
  (let loop ([i m])
    (cond ((> i n)
           null)
          ((and (prime? i)
                (prime? (+ i g))
                (for/and ([j (in-range (+ i 1) (+ i g))])
                         (not (prime? j))))
           (cons i (+ i g)))
          (else
           (loop (add1 i))))))
