(ns math-parser)

; utility methods
  
(defn remove-space [word]
  (->> (clojure.string/split word #"")
   (filter #(not (clojure.string/blank? %)))
   (clojure.string/join "")))

; expr methods

(declare expression-expr)
(declare term-expr)
(declare factor-expr)
(declare number-expr)

(defn norm-expr [exp]
  (seq (char-array (remove-space exp))))

(defn number-expr [exp]
  (let [pre (take-while #(or (= % \.) (Character/isDigit %)) exp)
        pre_num (Double/parseDouble (apply str pre))
        post (drop (count pre) exp)]
    (list pre_num post)))
   
(defn expression-expr-walk [n xs]
  (cond 
    (empty? xs) (list n xs)
    (= (first xs) \+) (let [nxt (term-expr (drop 1 xs))]
        (expression-expr-walk (+ n (first nxt)) (second nxt)))
    (= (first xs) \-) (let [nxt (term-expr (drop 1 xs))]
        (expression-expr-walk (- n (first nxt)) (second nxt)))
    :else (list n xs)))
  
(defn expression-expr [exp]
  (let [num (term-expr exp)]
    (expression-expr-walk (first num) (second num))))
    
(defn term-expr-walk [n xs]
  (cond 
    (empty? xs) (list n xs)
    (= (first xs) \*) (let [nxt (factor-expr (drop 1 xs))]
        (term-expr-walk (* n (first nxt)) (second nxt)))
    (= (first xs) \/) (let [nxt (factor-expr (drop 1 xs))]
        (term-expr-walk (/ n (first nxt)) (second nxt)))
    :else (list n xs)))
    
(defn term-expr [exp]
  (let [num (factor-expr exp)]
    (term-expr-walk (first num) (second num))))
  
(defn factor-expr [exp]
  (cond 
    (Character/isDigit (first exp)) (number-expr exp)
    (= (first exp) \() (let [num (expression-expr (drop 1 exp))]
        (list (first num) (drop 1 (second num))))
    (= (first exp) \-) (let [num (factor-expr (drop 1 exp))]
        (list (- (first num)) (second num)))
    :else (list 0 exp)))

(defn calc [exp] 
  (first (expression-expr (norm-expr exp))))
_______________________________________________
(ns math-parser)

(defn is-char [element]
  (= (type element) java.lang.Character)
  )

(defn to-token [char]
  (case char \( :lparen
             \) :rparen
             \+ :op-plus
             \* :op-multiply
             \- :op-minus
             \/ :op-divide
             char ))

(defn merge-digits [token-group]
  (if (is-char (first token-group))
    (Double. (apply str token-group))
    token-group
    )
  )

;; Turns the input string into a sequence of numbers, operations
;; and parentheses
(defn tokenize [expression]
  (->> (clojure.string/replace expression #" " "")
       (seq)
       (map to-token)
       (partition-by is-char)
       (map merge-digits)
       (flatten))
  )

;; Checks if the input sequence is enclosed by parentheses
(defn is-fully-enclosed [token-seq]
  (let [first-element (first token-seq)
        last-element (last token-seq)]
    (and (= first-element :lparen) (= last-element :rparen))
    )
  )

(defn is-number-or-paren [element]
  (or (= (type element) Double) (= element :lparen) (= element :rparen))
  )

;; Get the index (if existing) of the last operation, that is
;; on level 0
;; A levels increase with each left paren and decrease with each
;; right paren, so that an operation on level 0 is not enclosed by
;; parentheses
(defn index-unenclosed-op [op token-seq]
  (
    (loop [index (dec (count token-seq)) level 0]
      (cond
            (= index -1) (constantly nil)
            (= :lparen (nth token-seq index)) (recur (dec index) (dec level))
            (= :rparen (nth token-seq index)) (recur (dec index) (inc level))
            (and (= level 0) (= op (nth token-seq index))
                 (or (< index 1) (is-number-or-paren (nth token-seq (dec index))))) (constantly index)
            :else (recur (dec index) level)
            )
      )
    )
  )

(defn trim-first-and-last [token-seq]
  (drop-last (rest token-seq))
  )

;; Recursive function that creates a call tree following the rules
;; of this kata. E.g. and * and / must be parsed before + and -
(defn parse [token-seq]
  (cond
    (some? (index-unenclosed-op :op-plus token-seq)) (let [[left right]
                                                               (split-at (index-unenclosed-op :op-plus token-seq) token-seq)]
                                                           (+ (parse left) (parse (rest right))))
    (some? (index-unenclosed-op :op-minus token-seq)) (let [[left right]
                                                           (split-at (index-unenclosed-op :op-minus token-seq) token-seq)]
                                                       (- (if (= left '()) 0.0 (parse left) ) (parse (rest right))))
    (some? (index-unenclosed-op :op-multiply token-seq)) (let [[left right]
                                                               (split-at (index-unenclosed-op :op-multiply token-seq) token-seq)]
                                                           (* (parse left) (parse (rest right))))
    (some? (index-unenclosed-op :op-divide token-seq)) (let [[left right]
                                                             (split-at (index-unenclosed-op :op-divide token-seq) token-seq)]
                                                         (/ (parse left) (parse (rest right))))
    (is-fully-enclosed token-seq) (parse (trim-first-and-last token-seq))
    (= 1 (count token-seq)) (first token-seq)
    :else token-seq
    )
  )

(defn calc [expression] (parse (tokenize expression)))
___________________________________________________________
(ns math-parser
  (:require [clojure.string :as str]))

;; [helper]
(def empty-summary {:ops [] :open-braces [] :close-braces [] :negatives [] :digits [] })

(defn- remove-ws [expr-raw]
  (str/replace expr-raw #" " ""))

;; [helper] to calc
(defn- scan-expr
  "CAUTION: expr should be removed of ws's
  produces a map of :ops :open-braces :close-braces :negatives and digits"
  [expr]
  (reduce (fn [summary [idx c]]
            (cond
              (#{\+ \* \/} c) (update summary :ops #(conj % {:value c :pos idx}))
              (= c \-) (cond
                         ;; - appear first => it is a neg sign
                         (= 0 idx)
                         (update summary :negatives #(conj % {:value c :pos idx}))
                         ;; two ops appear consecutively => - is a negative sign
                         (= (dec idx) (:pos (last (:ops summary))))
                         (update summary :negatives #(conj % {:value c :pos idx}))
                         ;; form: (- ...)
                         (= (dec idx) (:pos (last (:open-braces summary))))
                         (update summary :negatives #(conj % {:value c :pos idx}))
                         ;; otherwise it is an operator
                         :else
                         (update summary :ops #(conj % {:value c :pos idx})))

              (= c \() (update summary :open-braces #(conj % {:value c :pos idx}))
              (= c \)) (update summary :close-braces #(conj % {:value c :pos idx}))
              ;; digit
              :else (update summary :digits #(conj % {:value c :pos idx}))))
          ;; init val
          empty-summary
          ;; coll
          (map-indexed vector expr)
    ))

;; [helper]. to calc-expr
(defn- digits-and-sign-only? [expr]
  (and (empty? (:ops expr))
       (empty? (:open-braces expr))
       (empty? (:close-braces expr))
       (seq (:digits expr))))


;; [helper]. to calc-expr
(defn- parse-double
  "only called when there are only digits in the expr"
  [expr]
  (->> (concat (:negatives expr) (:digits expr))
    (map #(:value %))
    (reduce str "")
    Double/parseDouble))

;; [helper]. to divide-expr-by-symbol-pos
(defn- divide-summary-vec-by-pos [sum-vec pos]
  (reduce (fn [res item]
             (cond
               (= pos (:pos item)) res
               (> (:pos item) pos) { :after (conj (:after res) { :value (:value item) :pos (- (:pos item) 1 pos)})
                                     :before (:before res)}
               :else               { :after (:after res)
                                     :before (conj (:before res) item)}))
           {:before [] :after []}
           sum-vec))

;; [helper]. to calc-expr
(defn- divide-expr-by-symbol-pos [expr symbol-pos]
  (reduce (fn [divided-summaries key]
            (let [ vec (key expr)
                   { before-vec :before after-vec :after} (divide-summary-vec-by-pos vec symbol-pos)]
              { :before (update (:before divided-summaries) key (constantly before-vec))
                :after  (update (:after divided-summaries) key (constantly after-vec))}))
          { :before empty-summary
            :after empty-summary}
          (keys expr)))

;; (defn- get-last-plus-or-minus-from-expr [expr]
;;   (when-let [the-last (last (filter #(or (= \+ (:value %)) (= \- (:value %))) (:ops expr)))]
;;     the-last))

;; [helper] to braces-balanced?, remove-braces
(defn- combine-lst-of-braces [expr]
  (sort #(< (:pos %1) (:pos %2))(concat (:open-braces  expr)
                                         (:close-braces expr))))

;; [helper] to find-the-least-favorable-op
(defn- remove-braces
  "this function is only called when there are braces in the expr.
  A new expr w/o braces (and stuff in braces is returned)"
  [expr]

  (let [ first-open-brace-pos (:pos (first (:open-braces expr)))
         last-close-brace-pos (:pos (last (:close-braces expr)))
         ;; edit: not only just pos anymore.
         pos-lst-of-braces    (combine-lst-of-braces expr)
         room-out-of-1st-lvl-braces (reduce (fn [accu curr]
                                              (cond
                                                (= (:value curr) \()
                                                { :res (if (and (= (:lvl accu) 0)
                                                                (seq (:res accu)))
                                                           (update (:res accu)
                                                                   (dec (count (:res accu)))
                                                                   #(conj % (:pos curr)))
                                                           ;; (conj (:res accu) [(:pos curr)])
                                                           (:res accu))
                                                  :lvl (inc (:lvl accu))}

                                                :else
                                                { :res (if (= (:lvl accu) 1)
                                                           (conj (:res accu) [(:pos curr)])
                                                           (:res accu))
                                                  :lvl (dec (:lvl accu))}))
                                            { :res []
                                              :lvl 0}
                                            pos-lst-of-braces)

         update-strategy (fn [vec]
                           (into [] (filter (fn [{pos :pos}]
                                              (or (< pos first-open-brace-pos)
                                                  (> pos last-close-brace-pos)
                                                  (and (< 1 (count (:res room-out-of-1st-lvl-braces)))
                                                       (some #(< (first %) pos (second %))
                                                             (subvec (:res room-out-of-1st-lvl-braces) 0 (dec (count (:res room-out-of-1st-lvl-braces))))))))
                                      ;; coll for filter
                                      vec)))]

    (-> expr
      (update :open-braces (constantly []))
      (update :close-braces (constantly []))
      ;; filter out stuff in the boundaries of braces
      (update :ops update-strategy)
      (update :negatives update-strategy)
      (update :digits update-strategy))))

;; [helper] to get-least-favorable-operator-from-expr
(defn- find-the-least-favorable-op
  "only be call when the least favorable symbol is an op"
  [expr]
  (let [
         open-braces (:open-braces expr)
         ;; expr* is expr w/o braces
         expr* (if (empty? open-braces)
                   expr
                   (remove-braces expr))
         ops (:ops expr*)
         only-plus-minus-ops (filter #(or (= (:value %) \+) (= (:value %) \-)) ops)
         target-ops (if (empty? only-plus-minus-ops)
                        ops
                        only-plus-minus-ops)]
    (last target-ops)))

;; [helper] to calc-expr
;; edit: alias for find-the-least-favorable-op
(def get-least-favorable-operator-from-expr find-the-least-favorable-op)

;; [utility] for neg-sign-and-braces?
(defn- count-expr
  "count the length of an expr"
  [expr]
  (reduce (fn [accu key]
            (+ accu (count (key expr))))
          0
          (keys expr)))

;; [helper] to neg-sign-and-braces?
(defn braces-balanced? [expr]
  (let [combined-lst-of-braces (combine-lst-of-braces expr)]
    (reduce (fn [lvl {value :value}]
              (let [lvl* (if (= value \()
                             (inc lvl)
                             (dec lvl))]
                (if (< lvl* 0)
                    (reduced false)
                    lvl*)))
            ;; init value
            0
            combined-lst-of-braces)))


;; [helper] to neg-sign-and-all-in-braces?, calc-expr
(defn- all-in-braces?
  ([expr] (all-in-braces? expr 0))
  ([expr start]
    (-> expr
         ;; removing the outer most two braces
         (update :open-braces #(subvec % (inc start) (count %)))
         (update :close-braces #(subvec % 0 (dec (count %))))
         (braces-balanced?))))

;; [helper] to neg-sign-and-braces?
(defn- neg-sign-and-all-in-braces? [expr]
  (and (= 0 (:pos (first (:negatives expr))))
       (= 1 (:pos (first (:open-braces expr))))
       ;; last close-brace is at the end
       (= (dec (count-expr expr)) (:pos (last (:close-braces expr))))
       ;; are braces balances after remove the outer most two
       (all-in-braces? expr)))


;; TODO: in progress (Status: refer to comments)
(defn calc-expr
  "expr here is a map of :ops :open-braces :close-braces :negatives and :digits"
  [expr]
  ;; (println "\n calcing:")
  ;; (println expr)

  ;; (println "parsable?")
  ;; (println (digits-and-sign-only? expr))
  ;; (println "neg-and-braces?")
  ;; (println (neg-sign-and-all-in-braces? expr))

  ;; (println "all-in-braces?")
  ;; (println (and (= 0 (:pos (first (:open-braces expr))))
  ;;            (= (dec (count-expr expr))
  ;;              (:pos (last (:close-braces expr))))
  ;;            (all-in-braces? expr)))

  (cond

    ;; only digits left
    (digits-and-sign-only? expr)
    (parse-double expr)

    ;; form: -(......)
    (neg-sign-and-all-in-braces? expr)
    (let [{_before :before after :after}
          (divide-expr-by-symbol-pos expr 0)]
      (- (calc-expr after)))

    ;; form: (......)
    (and (= 0 (:pos (first (:open-braces expr))))
         (= (dec (count-expr expr))
            (:pos (last (:close-braces expr))))
         (all-in-braces? expr))
    (let [{_before :before after :after}
          (divide-expr-by-symbol-pos expr 0)]
      (calc-expr (update after :close-braces #(subvec % 0 (dec (count %))))))

    :else
    (let [ least-favorable-operator (get-least-favorable-operator-from-expr expr)
           {before :before after :after} (divide-expr-by-symbol-pos
                                           expr
                                           (:pos least-favorable-operator))
           func (resolve (symbol (str (:value least-favorable-operator))))]

      ;; (println "\n least fav op:")
      ;; (println least-favorable-operator)

      ;; (println "\nbefore")
      ;; (println before)
      ;; (println "\nafter")
      ;; (println after)

      (func (calc-expr before) (calc-expr after))
      )))


(defn calc [expr]
  (calc-expr (scan-expr (remove-ws expr))))

___________________________________________________________________
(ns math-parser)

;;; operators

(def operators
  [{:id :add, :fn +, :preced 2, :arity :bin, :assoc :left}
   {:id :sub, :fn -, :preced 2, :arity :bin, :assoc :left}
   {:id :mul, :fn *, :preced 3, :arity :bin, :assoc :left}
   {:id :div, :fn /, :preced 3, :arity :bin, :assoc :left}
   {:id :unary-, :fn -, :preced 4, :arity :un}])

(def operator-map (zipmap (map :id operators) operators))

;;; parsing functions

(defn separate-tokens [strng]
  (map first (re-seq #"(\d+\.?\d*)|[+*/()-]" strng)))

(defn parse-number [strng]
  (if (re-matches #"\d+\.\d+" strng)
    (Double/parseDouble strng)
    (Integer/parseInt strng 10)))

(defn parse [expr]
  (->> (separate-tokens expr)
       (reduce
        (fn [sq tok]
          (let [prev (last sq)]
            (conj sq
                  (case tok
                    "+" :add, "-" (if (or (number? prev) (= :r-paren prev))
                                    :sub
                                    :unary-)
                    "*" :mul, "/" :div, "^" :pow, "(" :l-paren, ")" :r-paren
                    (parse-number tok))))) [])))

;;; ev*laution functions

; compares two operators
(defn operator> [id1 id2]
  (let [op1 (operator-map id1)
        op1-arity (:arity op1)
        op1-preced (:preced op1)
        op2 (operator-map id2)
        op2-arity (:arity op2)
        op2-preced (:preced op2)]
    (or
     ; unary minus
     (= op1-arity :un)
     ; binary x > binary y: if x has higher precedence than y, or x is left associative and x and y have equal precedence.
     (and (= op1-arity :bin) (= op2-arity :bin)
          (or (> op1-preced op2-preced)
              (and (= op1-preced op2-preced)
                   (= (:assoc op1) :left)))))))

(defn shunting-yard [tokens]
  (loop [tokens tokens
         op-stack '()
         output []]
    (if (empty? tokens)
      (concat output op-stack)
      (let [tok (first tokens)]
        (cond
          (number? tok) (recur (rest tokens) op-stack (conj output tok))
          (= :l-paren tok) (recur (rest tokens) (conj op-stack tok) output)
          (= :r-paren tok) (recur (rest tokens)
                                  (rest (drop-while #(not= :l-paren %) op-stack))
                                  (vec (concat output (take-while #(not= :l-paren %) op-stack))))
          (operator-map tok) (let [pop-ops (take-while #(and (not= :l-paren %)
                                                             (operator> % tok))
                                                       op-stack)]
                               (recur (rest tokens)
                                      (conj (drop (count pop-ops) op-stack) tok)
                                      (vec (concat output pop-ops)))))))))

(defn calc-rpn [tokens]
  (first
   (reduce (fn [out tok]
             (if (number? tok)
               (conj out tok)
               (let [op (operator-map tok)
                     n-args (case (:arity op) :un 1, :bin 2)]
                 (conj (drop n-args out)
                       (apply (:fn op) (reverse (take n-args out)))))))
           '() tokens)))

;;; main function

(defn calc [expr]
  (->> (parse expr)
       (shunting-yard)
       (calc-rpn)
       (double)))
