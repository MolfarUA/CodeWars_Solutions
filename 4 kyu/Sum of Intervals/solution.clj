(ns sum-intervals.core)

(defn sum-intervals
  [intervals]
  (->> intervals
       (mapcat #(apply range %))
       set
       count))

________________
(ns sum-intervals.core)

(defn overlap? [[x y] [i j]] (not (or (> i y) (< j x))))
   
(defn merge-interval
  "Merge interval to the end of a sorted vector of intervals"
  [intervals [x y :as interval]]
  (let [[i j :as last-int] (last intervals)]
    (if (overlap? interval last-int)
      (conj (vec (butlast intervals)) [(min x i) (max y j)])
      (conj intervals interval)
    )
  )
)

(defn interval-length [[a b]] (- b a))

(defn sum-intervals
  [intervals]
  (->> intervals
       (sort)
       (reduce merge-interval [[0 0]])
       (map interval-length)
       (reduce +)
  )
)

_________________________
(ns sum-intervals.core)

(defn sum-intervals [intervals]
  (->> intervals
    sort
    (reductions (fn [[_b' e'] [b e]] [(max b e') (max e e')]))
    (map (fn [[b e]] (- e b)))
    (reduce +)))

___________________
(ns sum-intervals.core)

(defn sum-intervals [intervals]
  (count (set (flatten (for [interval intervals]
    (for [i (range (first interval) (second interval))]
      i))))))

______________________
(ns sum-intervals.core)

;; Maps intervals onto a number line, tracking changes in the number of open intervals
(defn to-numline [intervals]
  (-> (fn [numline intv] 
        (-> numline 
          (assoc (first intv) (+ 1 (numline (first intv) 0))) 
          (assoc (last intv) (- (numline (last intv) 0) 1)))) 
    (reduce {} intervals)))

;; Loops over numline keys, summing when all intervals have closed
(defn sum-intervals [intervals]
  (let [numline (to-numline intervals)]
    (loop [ks (sort (keys numline))
           opener nil
           score 0
           sum 0]
      (let [k (first ks)
            d (numline k)]
        (cond
          (nil? k) sum
          (= 0 score) (recur (rest ks) k (+ score d) sum)
          (= 0 (+ score d)) (recur (rest ks) nil 0 (+ sum (- k opener)))
          :else (recur (rest ks) opener (+ score d) sum))))))

____________________________
(ns sum-intervals.core)

(defn sum-intervals [intervals]
  (->> intervals
       (sort)
       (reductions (fn  [[a b] [c d]] [(max b c) (max b d)]))
       (map (fn [[x y]] (- y x)))
       (reduce +)))

_______________
(ns sum-intervals.core)

(defn r
  [[a b]]
  (range a b))

(defn sum-intervals
  [intervals]
  (count (reduce #(apply conj %1 (r %2)) #{} intervals)))

_____________________
(ns sum-intervals.core)

(defn sum-intervals
  [intervals]
  (loop [sl intervals
         all-ranges []]
    (if (zero? (count sl)) (count (set (flatten all-ranges)))
        (recur (next sl) (conj all-ranges (range (first (first sl)), (second (first sl))))))))
