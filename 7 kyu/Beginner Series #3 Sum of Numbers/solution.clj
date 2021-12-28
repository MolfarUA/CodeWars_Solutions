(ns clojure.numbers-sum)

(defn get-sum [a b]
   (apply + (range (min a b) (inc (max a b)))))

__________________________________
(ns clojure.numbers-sum)

(defn get-sum
  "Int Int -> Int
  Return the sum of all integers between and including `a` and `b`.
  If a = b, count only once."
  [a b]
  (let [start (min a b)
        end (max a b)]
    (* (/ (inc (- end start )) 2) ;; pairs
       (+ a b))))                 ;; each

__________________________________
(ns clojure.numbers-sum)

(defn get-sum [a b]
  (def limits (sort [a b]))
  (reduce + (range (first limits) (inc (last limits))))
)

__________________________________
(ns clojure.numbers-sum)

(defn get-sum [a b]
  (reduce + 0 (range (min a b) (inc (max a b))))
)

__________________________________
(ns clojure.numbers-sum)

(defn get-sum [a b]
  (cond
    (= a b) a
    (< b a)
    (->>
     (range b (inc a))
     (reduce +))
    :else
    (->>
     (range a (inc b))
     (reduce +))))

__________________________________
(ns clojure.numbers-sum)

(defn get-inner-sum [a b]
  ( if (== a b)
    a
    (reduce + (range a (+ 1 b)))
  ))

(defn get-sum [a b]
  ( if (> a b)
    (get-inner-sum b a)
    (get-inner-sum a b)
  ))

__________________________________
(ns clojure.numbers-sum)

(defn get-sum [a b]
;  (apply + (range (min a b) (inc (max a b))))
;  (def l (sort [a b])) 
;  (reduce + 0 (range (first l) (inc (last l))))
  (let [l (sort [a b])] 
  (reduce + 0 (range (first l) (inc (last l)))))
)
