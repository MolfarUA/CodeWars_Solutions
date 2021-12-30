(ns digital-root)

(defn digital-root [n]
  (if (> n 0) (+ 1 (mod (- n 1) 9)) 0)
)

________________________________
(ns digital-root)

(defn digital-root [n]
  (if (< n 10) 
    n
    (recur (apply + (map #(Character/digit % 10) (str n))))))

________________________________
(ns digital-root)

(defn sum-digit [x] (reduce + (map #(Integer. (str %)) (str x))))

(defn digital-root [n]
  (if (< n 10) n
    (digital-root (sum-digit n))))

________________________________
(ns digital-root)

(defn digitize [n]
  (map (comp read-string str) (str n)))

(defn digital-root [n]
  (if (< n 10) n (digital-root (apply + (digitize n)))))

________________________________
(ns digital-root)

(defn sum-of-digits
  [n]
  (->> n
       (iterate #(quot % 10))
       (take-while pos?)
       (map #(rem % 10))
       (reduce +)))

(defn digital-root
  [n]
  (->> n
       (iterate sum-of-digits)
       (drop-while (partial <= 10))
       (first)))
