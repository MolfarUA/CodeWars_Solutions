(ns findeven.core)

(defn find-even-index [xs]
  (let [
      left-sums (reductions + xs)
      right-sums (reverse (reductions + (rseq xs)))
    ] (.indexOf (map = left-sums right-sums) true)))
________________________
(ns findeven.core)

(defn find-even-index [arr]
  (let [diffs (map-indexed (fn [i v] 
    (- (reduce + (take (inc i) arr))
       (reduce + (nthrest arr i)))) arr)]
   (.indexOf diffs 0)))
________________________
(ns findeven.core)

(defn find-even-index [arr]
  (let [left (conj (reductions + arr) 0)
        right (rest (reverse (conj (reductions + (reverse arr)) 0)))]
    (.indexOf (map = left right) true)))
________________________
(ns findeven.core)

(defn default [default val] (if (not= val nil) val default))

(defn find-even-index [arr]
  (->> (count arr)
       (range)
       (filter #(= (reduce + (subvec arr 0 %)) (reduce + (subvec arr (inc %)))))
       (first)
       (default -1))
  )
________________________
(ns findeven.core)

(defn find-even-index [arr]
  (let [c (count arr)]
    (loop [i 0]
     (let [ls (if (zero? i) 0 (reduce + (subvec arr 0 i)))
           rs (reduce + (subvec arr (inc i) c))]
       (cond (= ls rs) i
             (>= i (dec c)) -1
             :else (recur (inc i)))))))
