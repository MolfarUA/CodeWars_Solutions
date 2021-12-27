#lang racket
(provide calc)

; utility methods

(define (take-while p l)
  (let loop ((o '()) (l l))
    (if (and (not (null? l)) (p (car l)))
        (loop (cons (car l) o) (cdr l))
        (reverse o))))

(define (str-from-chars ls)
  (apply string-append (map (λ (c) (string c)) ls)))

; math expr

(define (norm-exp exp)
  (filter (λ (c) (not (char-whitespace? c))) exp))

(define (number-exp exp)
  (let* ([pre (take-while (λ (c) (or (equal? c #\.) (char-numeric? c))) exp)]
         [pre-num (string->number (str-from-chars pre))]
         [post (list-tail exp (length pre))])
    (list pre-num post)))

(define (expression-exp exp)
  (define (walk n xs)
    (if (empty? xs)
      (list n xs)
      (if (eq? (first xs) #\+)
        (let* ([ys (list-tail xs 1)]
               [nxt (term-exp ys)])
          (walk (+ n (first nxt)) (second nxt)))
        (if (eq? (first xs) #\-)
          (let* ([ys (list-tail xs 1)]
                 [nxt (term-exp ys)])
            (walk (- n (first nxt)) (second nxt)))
          (list n xs)))))
  (let ([num (term-exp exp)])
    (walk (first num) (second num))))

(define (term-exp exp)
  (define (walk n xs)
    (if (empty? xs)
      (list n xs)
      (if (eq? (first xs) #\*)
        (let* ([ys (list-tail xs 1)]
               [nxt (factor-exp ys)])
          (walk (* n (first nxt)) (second nxt)))
        (if (eq? (first xs) #\/)
          (let* ([ys (list-tail xs 1)]
                 [nxt (factor-exp ys)])
            (walk (/ n (first nxt)) (second nxt)))
          (list n xs)))))
  (let ([num (factor-exp exp)])
    (walk (first num) (second num))))

(define (factor-exp exp)
  (if (char-numeric? (first exp))
    (number-exp exp)
    (if (eq? (first exp) #\()
      (let ([num (expression-exp (list-tail exp 1))])
        (list (first num) (list-tail (second num) 1)))
      (if (eq? (first exp) #\-)
      (let ([num (factor-exp (list-tail exp 1))])
        (list (- (first num)) (second num)))
      (list 0 exp)))))

(define (calc exp)
  (define result (expression-exp (norm-exp (string->list exp))))
  (define num (first result))
  (println num)
  num)
____________________________________________________________________
#lang racket
(provide calc)

(define (run-parser p tokens) (car (p tokens)))

(define ((bind p1 p2) s)
  (match (p1 s)
    [#f #f]
    [(cons a s1) ((p2 a) s1)]))

(define ((pure a) s) (cons a s))

(define (<$> f p) (bind p (compose pure f)))

(define (<$ v p) (<$> (const v) p))

(define (<*> p1 p2) (bind p1 (lambda (f) (<$> f p2))))

(define ((choice p q) s)
  (match (p s)
    [#f (q s)]
    [res res]))

(define ((satisfy pred) s)
  (match s
    [(cons (? pred a) s1) (cons a s1)]
    [_ #f]))

(define (peq v) (satisfy (curry equal? v)))

(define (chainl1 p op)
  (define (rest a)
    (choice (bind (<*> (<*> op (pure a)) p) rest) (pure a)))
  (bind p rest))

(define (prefixr p op)
  (choice (<*> op (lambda (s) ((prefixr p op) s))) p))

(define (between p1 p2 p)
  (bind (bind p1 (const p)) (lambda (a) (<$ a p2))))

(define (calc expr)
  (define tokens (regexp-match* #px"\\d+(?:\\.\\d+)?|[-+*/()]" expr))
  (define number (<$> string->number (satisfy string->number)))
  (define neg (<$ - (peq "-")))
  (define add (<$ (curry +) (peq "+")))
  (define sub (<$ (curry -) (peq "-")))
  (define mul (<$ (curry *) (peq "*")))
  (define div (<$ (curry /) (peq "/")))
  (letrec 
    ([atom   (choice number (between (peq "(") (peq ")") (lambda (s) (expr s))))]
     [factor (prefixr atom neg)]
     [term   (chainl1 factor (choice mul div))]
     [expr   (chainl1 term (choice add sub))])
    (run-parser expr tokens)))
________________________________________________
#lang racket
(provide calc)

(define (tokenize s)
  (define (operator? x)
    (or (eq? x #\+)
        (eq? x #\-)
        (eq? x #\*)
        (eq? x #\/)))
  (define (parens? x)
    (or (eq? x #\()
        (eq? x #\))))
  (define first-char->symbol (compose1 string->symbol string car))
  (define (pick-unary l)
    (define xs (cons (if (eq? (car l) '-) '-u (car l)) (cdr l)))
    (let loop ([xs xs])
      (match xs
        ['() '()]
        [(list (? (λ (x) (or (sym-operator? x) (eq? 'lp x))) x) '- xs ...)
         (cons x (loop (cons '-u xs)))]
        [(cons x xs)
         (cons x (loop xs))])))
  (pick-unary
    (let loop ([xs s])
      (define (read-num l)
        (define-values (nums rst)
          (splitf-at l (λ (x) (or (char-numeric? x) (eq? x #\.)))))
        (cons (string->number (apply string nums))
              (loop rst)))
      (define (read-op l)
        (cons (first-char->symbol l)
              (loop (cdr l))))
      (define (read-parens l)
        (cons (if (eq? (car l) #\() 'lp 'rp)
              (loop (cdr l))))
      (match xs
        ['() xs]
        [(cons (? char-numeric?) _)
         (read-num xs)]
        [(cons (? operator?) _)
         (read-op xs)]
        [(cons (? parens?) _)
         (read-parens xs)]
        [(cons _ xs) (tokenize xs)]))))


(define PRECEDENCE
  #hash((+ . 0)
        (- . 0)
        (* . 1)
        (/ . 1)
        (-u . 2)))

(define (sym-operator? x)
  (hash-has-key? PRECEDENCE x))

(define (parse tl)
  (define (precedence<=? op1 op2)
    (<= (hash-ref PRECEDENCE op1)
       (hash-ref PRECEDENCE op2)))
  (let loop ([exprs '()] [ops '()] [l tl])
    (match l
      [(list) (reverse (append (reverse ops) exprs))]
      [(cons (? number? x) xs)
       (loop (cons x exprs) ops xs)]
      [(cons '-u xs)
       (loop exprs (cons '-u ops) xs)]
      [(cons 'lp xs)
       (loop exprs (cons 'lp ops) xs)]
      [(cons 'rp xs)
       (define-values (left right)
         (splitf-at ops (λ (x) (not (eq? x 'lp)))))
       (loop (append (reverse left) exprs) (cdr right) xs)]
      [(cons (? sym-operator? x) xs)
       (define-values (left right)
         (splitf-at ops (λ (y) (and (sym-operator? y)
                                    (precedence<=? x y)))))
       (loop (append (reverse left) exprs) (cons x right) xs)])))

(define (calc expr)
  (define rpn
    (parse (tokenize (filter-not char-whitespace? (string->list expr)))))
  (let loop ([l '()] [xs rpn])
    (match xs
      ['() (car l)]
      [(cons (? number? x) xs)
       (loop (cons x l) xs)]
      [(cons (? (λ (x) (eq? x '-u))) xs)
       (loop (cons (- (car l)) (cdr l)) xs)] 
      [(cons (? sym-operator? x) xs)
       (match-define (list v1 v2 ls ...) l)
       (loop (match x
               ['+ (cons (+ v2 v1) ls)]
               ['- (cons (- v2 v1) ls)]
               ['* (cons (* v2 v1) ls)]
               ['/ (cons (/ v2 v1) ls)])
             xs)])))
__________________________________________
#lang racket
(provide calc)

(define (calc exp)
  (struct op (sym arity prec assoc) #:transparent)

  (define tokens
    (map (match-lambda
           [(app string->number (? number? n)) n]
           [(? (match-lambda [(or "(" ")") #t] [_ #f]) p) p]
           [(app string->symbol (? symbol? s)) s])
         (regexp-match* #px"\\d+(?:\\.\\d+)?|\\(|\\)|\\+|-|\\*|/" exp)))

  (define parsed
    (let iter ([input tokens] [output '()])
      (if (null? input)
          (reverse output)
          (match* ((car input) output)
            [('- (or '() (cons (or "(" (? op? _)) _))) (iter (cdr input) (cons (op '- 1 2 'right) output))]
            [((? symbol? s) _) (iter (cdr input) (cons (op s 2 (if (member s '(* /)) 1 0) 'left) output))]
            [(token _) (iter (cdr input) (cons token output))]))))

  (define rpn ; shunting-yard
    (let iter ([input parsed] [output '()] [operators '()])
      (define (eat-ops out oper ops)
        (if (and (not (null? ops))
                 (not (eq? "(" (car ops)))
                 (or (> (op-prec (car ops)) (op-prec oper))
                     (and (= (op-prec (car ops)) (op-prec oper))
                          (eq? (op-assoc oper) 'left))))
            (eat-ops (cons (car ops) out) oper (cdr ops))
            (iter (cdr input) out (cons oper ops))))
      
      (define (match-paren out ops)
        (if (eq? "(" (car ops))
            (iter (cdr input) out (cdr ops))
            (match-paren (cons (car ops) out) (cdr ops))))
      
      (if (null? input)
          (append (reverse output) operators)
          (match (car input)
            [(? number? n) (iter (cdr input) (cons n output) operators)]
            [(? op? oper) (eat-ops output oper operators)]
            ["(" (iter (cdr input) output (cons "(" operators))]
            [")" (match-paren output operators)]))))
  
  (define ns (make-base-namespace))
  
  (let compute ([stack '()] [input rpn])
    (match* (stack input)
      [((list result) '()) result]
      [(_ (cons (? number? n) rest)) (compute (cons n stack) rest)]
      [((cons a st) (cons (op sym 1 _ _) rest)) (compute (cons ((eval sym ns) a) st) rest)]
      [((list b a st ...) (cons (op sym 2 _ _) rest)) (compute (cons ((eval sym ns) a b) st) rest)])))
