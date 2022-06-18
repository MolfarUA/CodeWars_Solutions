(ns digitizer.core)

(defn digitize [n]
  (->> n
       str
       reverse
       (map #(Character/digit % 10))))
________________________
(ns digitizer.core)

(defn digitize [n]
  (reverse (map #(Integer/parseInt (str %)) (str n))))
________________________
(ns digitizer.core)

(defn digitize [n]
  (->> (str n)
       (reverse)
       (map str)
       (map read-string)))
________________________
(ns digitizer.core)

(defn parse [n]
  (Integer/parseInt (str n)))

(defn digitize [n]
  (map parse (reverse (to-array(str n)))))
________________________
(ns digitizer.core)

(defn digitize
  ([n] (digitize n []))
  ([n list] (if (< n 10) (concat list [n])
                (recur (quot n 10) (concat list [(mod n 10)])))))
