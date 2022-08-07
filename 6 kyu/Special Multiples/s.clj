55e785dfcb59864f200000d9


(ns countmultiples.core)

(defn prime? [n]
  (not-any? #(zero? (rem n %)) (range 2N n))
  )
(defn primes []
  (lazy-seq (filter prime? (drop 2N (range))))
  )
(defn count-spec-mult [n maxval]
  (let [pr (take n (primes)) minvall (reduce * pr)]
    (count (take-while #(< % maxval) (iterate (partial + minvall) minvall)))
    )
  )
_________________________________
(ns countmultiples.core)

(defn count-spec-mult [n m]
  (let [k (vec (take n (map bigint [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71]))) 
        p (apply * k)]
    (bigint (/ m p))
  ))
_________________________________
(ns countmultiples.core)

(defn primes [n]
  (take n (filter (fn [k] (every? (fn [d] (pos? (rem k d))) (range 2 (inc (quot k 2)))))
            (range 2 1000))))

(defn count-spec-mult [n maxval]
  (quot (dec maxval) (apply * (primes n))))
