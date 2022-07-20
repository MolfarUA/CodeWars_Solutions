54d496788776e49e6b00052f


(ns sumbyfactors.core)

;prime calculation found here: https://stackoverflow.com/questions/960980/fast-prime-number-generation-in-clojure
(defn prime? [n]
      (.isProbablePrime (BigInteger/valueOf n) 5))
(def primes (concat [2] (filter prime? 
        (take-nth 2 (range 1 Integer/MAX_VALUE)))))

;my code
(defn sum-of-divided [lst] 
  (let [maxi (apply max (map #(Math/abs %) lst))]
    (for [p primes
          :while (<= p maxi)
          :let [hits (filter #(zero? (mod % p)) lst)]
          :when (not-empty hits)]
      [p (reduce + hits)])))
________________________________________________
(ns sumbyfactors.core)

(defn prime-factors [n]
  (loop [n (Math/abs n) divisor 2 factors []]
    (if (< n 2)
      (distinct factors)
      (if (= 0 (rem n divisor))
        (recur (/ n divisor) divisor (conj factors divisor))
        (recur n (inc divisor) factors)))))       

(defn list-prime-factors [l]
  (distinct (flatten (map (fn [x] (prime-factors x)) l))))

(defn sum-for-one [n lst]
  (reduce (fn [s x] (if (= 0 (mod x n)) (+ x s) s)) 0 lst))

(defn sum-of-divided [lst]
  (sort-by first(map (fn [x] (list x (sum-for-one x lst))) (list-prime-factors lst))))
________________________________________________
(ns sumbyfactors.core)

(defn- prime-factors [n]
  (loop [n (Math/abs n) divisor 2 factors []]
    (if (< n 2)
      (distinct factors)
      (if (= 0 (rem n divisor))
        (recur (/ n divisor) divisor (conj factors divisor))
        (recur n (inc divisor) factors)))))       

(defn- list-prime-factors [l]
  (distinct (flatten (map (fn [x] (prime-factors x)) l))))

(defn- sum-for-one [n lst]
  (reduce (fn [s x] (if (= 0 (mod x n)) (+ x s) s)) 0 lst))

(defn sum-of-divided [lst]
  (sort-by first(map (fn [x] (list x (sum-for-one x lst))) (list-prime-factors lst))))
