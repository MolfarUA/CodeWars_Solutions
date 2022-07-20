53ee5429ba190077850011d4


(ns double-integer)

(defn double-integer [i]
  (* 2 i)
)
__________________________
(ns double-integer)

(def double-integer (partial * 2))
__________________________
(ns double-integer)

(defn double-integer [i]
  (+ i i))
__________________________
(ns double-integer)

(defn double-integer [i]
  "doubles an integer"
  (* 2 i)
)
