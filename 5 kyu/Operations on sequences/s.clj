(ns prodseq.core)

(defn- abs [n] (max n (- n)))
(defn- h[arr]
  (let [x (bigint (arr 0)) y (bigint (arr 1)) z (bigint (arr 2)) t (bigint (arr 3))
        a (- (* x z) (* y t))
        b (+ (* x t) (* y z))     
       ]
    [(abs a) (abs b)])
)
(defn solve[arr]
  (if (= (count arr) 4) 
    (h arr)
    (let [a1 (h (subvec arr 0 4)) a2 (subvec arr 4 (count arr))]
     (solve (vec (concat a1 a2)))))
)
_____________________________________
(ns prodseq.core)

(defn two-squares [k x y z]
  (let [[a b c d] (if (>= (* k z) (* x y)) [k x y z] [x k z y])
        l1        (+ (* a c) (* b d))
        r1        (- (* a d) (* b c))]
    [l1 r1]))

(defn reduce-product [[a b c d & rest]]
  (let [[left right] (two-squares a b c d)]
    (if (empty? rest)
      [left right]
      (reduce-product (concat [left right] rest)))))

(defn solve [arr]
  (reduce-product (map bigint arr)))
_____________________________________
(ns prodseq.core)

(defn solve [arr]
  (loop [a_ (bigint (peek arr)) b_ (bigint (peek (pop arr))) rst (pop (pop arr))]
    (cond
      (empty? rst) [a_ b_]
      :else (let
             [m_ (bigint (peek rst))
              n_ (bigint (peek (pop rst)))
              nrst (pop (pop rst))
              a (min a_ b_)
              b (max a_ b_)
              m (min m_ n_)
              n (max m_ n_)
              ]
              (recur (-' (*' n b) (*' m a)) (+' (*' n a) (*' m b))  nrst)))))
_____________________________________
(ns prodseq.core)

(defn solve [[a b c d & arr]]
  (let [next-a (biginteger (- (* a c) (* b d)))
        next-b (biginteger (+ (* a d) (* b c)))]
    (if (empty? arr)
      [(.abs next-a) (.abs next-b)]
      (recur (concat [next-a next-b] arr)))))
_____________________________________
(ns prodseq.core)

(defn- abs [x]
  (if (neg? x) (- x) x))

(defn solve [xs]
  (transduce
   (partition-all 2)
   (completing (fn [[a b] [c d]] [(+ (* a c) (* b d))
                                  (abs (- (* a d) (* b c)))]))
   [1N 0N]
   xs))
