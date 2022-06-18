(ns haskell-array-operations)
(def head first)
(def tail rest)
(def init drop-last)
(def last_ last)
_____________________________
(ns haskell-array-operations)

(def head first)
(def tail rest)
(def init #(-> % reverse rest reverse))
(def last_ #(-> % reverse first))
_____________________________
(ns haskell-array-operations)

(defn head [[x & xs]]
  x)
  
  
(defn tail [[x & xs]]
  xs)
  
  
(defn init [xs]
  (loop [acc []
        [x & xs] xs]
        (if(empty? xs)
          acc
          (recur (conj acc x) xs))))
  
(defn last_ [xs]
  (reduce (fn [x y] y) xs))
_____________________________
(ns haskell-array-operations)

(def head first)
(def tail rest)
(def last_ last)
(def init #(-> % reverse rest reverse))
