(ns kata.bus)
(defn number
  [bus-stops]
  (reduce - (apply map + bus-stops))
)
_____________________________________
(ns kata.bus)
(defn number
  [bus-stops]
  (->> bus-stops
    (map #(apply - %))
    (reduce +)))
_____________________________________
(ns kata.bus)
(defn number
  [bus-stops]
  (->> bus-stops
    (apply map +)
    (reduce -)))
_____________________________________
(ns kata.bus)

(defn delta [passengers [on off]]
  (+ passengers (- on off)))

(defn number
  [bus-stops]
  (reduce delta 0 bus-stops))
_____________________________________
(ns kata.bus)

(defn number
  [bus-stops]
  (reduce + (map (fn [e] (reduce - e)) bus-stops))
)
