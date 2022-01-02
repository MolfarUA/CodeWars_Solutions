(ns katas.unique-in-order)

(defn unique-in-order [input]
  (dedupe input))
_____________________________________________
(ns katas.unique-in-order)

(defn unique-in-order
  [input]
  (reduce 
    #(if (= (peek %1) %2)
         %1
         (conj %1 %2))
    []
    input))
_____________________________________________
(ns katas.unique-in-order)


(defn unique-in-order [input]
  (mapcat set (partition-by identity input))
)
_____________________________________________
(ns katas.unique-in-order)

(defn unique-in-order [input]
  (map first (partition-by identity input)))
_____________________________________________
(ns katas.unique-in-order)

(defn add-if-dif
  [acc it]
  (if (= (last acc) it) acc (conj acc it))
)

(defn unique-in-order
  [input]
  (reduce add-if-dif [] input)
)
_____________________________________________
(ns katas.unique-in-order)

(defn add-if-dif
  [acc it]
  (if (= (last acc) (last it)) acc (conj acc (last it)))
)

(defn unique-in-order
  [input]
  (reduce add-if-dif [] (mapv #(into [%1] [%2]) (iterate inc 0) input))
)
