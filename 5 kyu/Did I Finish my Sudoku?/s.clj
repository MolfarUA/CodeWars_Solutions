53db96041f1a7d32dc0004d2


(ns sudoku)
(defn done-or-not [board]
  (if (every? #(= (sort %) (range 1 10))
    (concat board
    (partition 9 (apply interleave board))
    (map flatten (partition 3 (apply interleave (map #(partition 3 %) board)))))) "Finished!" "Try again!"))
________________________________
(ns sudoku)

(defn cell [board i j] (nth (nth board i) j))

(defn check-sum [board i]
  (loop [sum 0 j 0]
    (if (> j 8)
      sum
      (let [row (cell board i j)
            col (cell board j i)
            box (cell board (+ (* 3 (mod i 3)) (mod j 3)) (+ (* 3 (quot i 3)) (quot j 3)))
            next-sum (+' sum row col box)]
        (recur next-sum (inc j))))))

(defn done-or-not [board]
  (loop [i 0]
    (cond
      (> i 8) "Finished!"
      (not= 135 (check-sum board i)) "Try again!"
      :else (recur (inc i)))))
________________________________
(ns sudoku)

(def zip (partial map vector))

(defn done-or-not [board]
  (let [rows board
        columns (apply zip board)
        regions (->> board
                     (map (partial partition 3))
                     (apply zip)
                     (flatten)
                     (partition 9))
        allowed (set (range 1 10))]
    (if (apply = allowed (map set (concat rows columns regions)))
      "Finished!"
      "Try again!")))
