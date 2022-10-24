54f8693ea58bce689100065f


(ns egypt.core)

(defn f [r]
  (cond (> r 1)             (quot r 1)
        (zero? r)           0
        (= 1 (numerator r)) r
        :else               (/ 1 (inc (quot (denominator r) (numerator r))))))

(defn g [r]
  (lazy-seq (cons (f r) (g (- r (f r))))))

(defn decompose [r]
  (->> r
       read-string
       rationalize
       g
       (take-while pos?)
       (map str)))
_________________________________
(ns egypt.core)
(defn decompose [r]
    (defn inner-decompose [r acc]
     (let [num (if (ratio? r) (numerator r) r)
           denom (if (ratio? r) (denominator r) 1)]
        (cond
          (zero? r) acc
          (> r 1) (recur (- r (int r)) (conj acc (str (int r))))
          (= 1 num) (conj acc (str r))
          :else (recur (- r (/ 1 (inc (int (/ denom num))))) (conj acc (str (/ 1 (inc (int (/ denom num))))))
   ))))
   (inner-decompose (rationalize (read-string r)) []))
_________________________________
(ns egypt.core)

(defn decompose [r]
  (let [r (read-string r)]
    (if (or (not (number? r)) (= 0 r))
      []
      (if (= r (int r))
        [(str r)]
        (let [r (rationalize r) e (rationalize (int r)) m (rationalize (- r e)) res []]
          (if (= 0 m)
            (conj res (str r))
            (loop [r m res (if (not= 0 e) (conj res (str e)) res)]
              (if (= 0 r)
                res
                (let [k (/ 1 (rationalize (Math/ceil (/ 1 r))))]
                  (recur (rationalize (- r k))
                         (conj res (str (rationalize k)))))))))))))
