(ns kata)

(defn flip [d a]
  (sort (case d \R < \L >) a))

_____________________________________________
(ns kata)

(defn flip [d a]
  (case d
    \R (sort < a)
    \L (sort > a)))

_____________________________________________
(ns kata)

(defn flip [gravity boxes]
  (def gravity-side (case gravity \R < \L >))
  (sort gravity-side boxes)
)

_____________________________________________
(ns kata)

(defn flip [d a]
  (if (= d \L) (sort > a) (sort a)))
