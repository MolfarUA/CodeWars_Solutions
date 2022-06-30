(ns banjo)

(defn plays-banjo? [name]
  (str name
    (if (#{\r \R} (first name))
      " plays banjo"
      " does not play banjo")))
________________________________
(ns banjo)

(defn plays-banjo?
  [name]
  (str name
       (if (#{\R \r} (first name))
           " plays"
           " does not play")
       " banjo"))
________________________________
(ns banjo)

(defn plays-banjo?
  [name]
  (if (or (= (first name) \r) (= (first name) \R))
  (str name " plays banjo")
  (str name " does not play banjo"))
)
