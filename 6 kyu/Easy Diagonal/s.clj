559b8e46fa060b2c6a0000bf


(ns choose1.core)

(defn- binomial [n k]
  "Compute the binomial coefficient n choose k with automatic promotion to BigInt"
  (let [rprod (fn [x y] (reduce *' (range x (inc y))))]
    (/ (rprod (- n k -1) n) (rprod 1 k))))

(defn diagonal [n p]
  "The sum of a diagonal in Pascal's Triangle is the value at the (inc n), (inc p) location"
  (binomial (inc n) (inc p)))
_____________________________
(ns choose1.core)

(def pascals-diags
  (iterate (partial reductions +') (repeat 1)))

(defn diagonal [n p]
  (-> pascals-diags (nth (inc p)) (nth (- n p))))
_____________________________
(ns choose1.core)

(def pascals-diags
  (iterate (partial reductions +') (repeat 1)))

(defn diagonal [n p]
  (reduce +' 0 (take (inc (- n p)) (nth pascals-diags p))))
