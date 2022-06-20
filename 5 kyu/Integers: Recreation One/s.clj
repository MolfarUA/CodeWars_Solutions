55aa075506463dac6600010d


(ns sumdivsq.core)

(defn square?
  [x]
  (zero? (rem (Math/sqrt x) 1)))
    
(defn divisors
  [n]
  (filter #(zero? (rem n %)) (range 1 (inc n))))
    
(defn list-squared [m n]
  (keep
    (fn [x]
      (let [divs (divisors x)
            divs-squared (map #(* % %) divs)
            divs-squared-sum (reduce + divs-squared)]
          (when (square? divs-squared-sum)
            [x divs-squared-sum])))
    (range m n)))
________________________________
(ns sumdivsq.core)

(defn factors [n]
  (into (sorted-set)
    (reduce concat
      (for [x (range 1 (inc (Math/sqrt n))) :when (zero? (rem n x))]
        [(* x x) (* (/ n x) (/ n x))]))))

(defn sum-sq-factors [n]
  (let [s (reduce + (vec (factors n))) r (int(Math/sqrt s))]
    (if (= s (* r r))
      [n s]
      nil)))

(defn list-squared [m n]
  (vec (remove nil? (map sum-sq-factors (range m n)))))
________________________________
(ns sumdivsq.core)

(defn factors [n]
  (into (sorted-set)
    (reduce concat
      (for [x (range 1 (inc (Math/sqrt n))) :when (zero? (rem n x))]
        [(* x x) (* (/ n x) (/ n x))]))))

(defn sum-sq-factors [n]
  (let [s (reduce + (vec (factors n))) r (int(Math/sqrt s))]
    (if (= s (* r r))
      [n s]
      nil)))

(defn list-squared [m n]
  (vec (remove nil? (map sum-sq-factors (range m n)))))
