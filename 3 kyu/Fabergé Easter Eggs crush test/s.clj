54cb771c9b30e8b5250011d4


(ns faberge)
(defn height [n m] 
  (loop [x (bigint n)
         t (bigint 1)
         h (bigint 0)]
    (cond 
      (zero? x) h
      :else (let [e (quot (* t (+ (- m n) x)) (- (inc n) x))]
              (recur (dec x) e (+ h e))))))
_________________________
(ns faberge)
(defn height [n m] 
  (apply +' 
    (reduce 
      #(vector
        (apply +' %1)
        (/ (*' (last %1) (- m %2 -1)) %2))
      [-1 1]
      (range 1 (inc n))
  ))
)
_________________________
(ns faberge)
(defn height [n m]
  (if (>= n m)
      (- (.pow (biginteger 2) m) 1)
      (second 
        (reduce 
          (fn [[c s] i]
            (let [c-next (/ (* c (- m i)) (+ i 1N))]
              [c-next (+ s c-next)]))
          [1N 0N] (range n))))
)
_________________________
(ns faberge)
(defn height [n t]
  (loop [sum 0N fac 1N r 0N] 
    (if (>= r n) sum
      (let [bin  (/ (* fac (- t r)) (inc r))]
      (recur (+ sum bin) bin (inc r))))))
_________________________
(ns faberge)
(defn height [n m] 
  (loop [i 1 t 1N h 0N]
    (let [t (/ (* t (+ (- m i) 1)) i)]
      (if (= i n) (+ h t)
        (recur (inc i) t (+ h t))))))
