52f677797c461daaf7000740


(ns smallest-sum.core)

(defn gcd' [a b]
  (if (zero? b) a
      (gcd' b (mod a b))))

(defn solution
  [arr]
  (let [gcd-all (reduce gcd' arr)]
    (* (count arr)
       gcd-all)))
_______________________________
(ns smallest-sum.core)

(defn gcd [a b] (if (zero? b) a (gcd b (mod a b))))
(defn solution [arr] (* (count arr) (reduce gcd arr)))
_______________________________
(ns smallest-sum.core)

(defn solution [arr]
  (let [gcd (reduce (fn [previous curr]
            (.gcd (biginteger previous) (biginteger curr)))
            (first arr)
            arr
          )
        ]
    (* gcd (count arr))))
_______________________________
(ns smallest-sum.core)

(defn- gcd [^long a ^long b]
  (if (= b 0)
    a
    (gcd b (rem a b))))

(defn solution [^clojure.lang.IPersistentVector v]
  (* (.count v)
     (reduce
       (fn [^long d ^long n] (gcd d n))
       (nth v 0)
       v)))
