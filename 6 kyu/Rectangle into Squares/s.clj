55466989aeecab5aac00003e


(ns sq-in-rect.core)

(defn sq-in-rect [lng wdth]
  (if (not= lng wdth)
    (loop [l lng w wdth sqrs [] ]
      (if (and (> l 0) (> w 0))
        (cond
          (< l w) (recur l (- w l) (conj sqrs l))
          (< w l) (recur w (- l w) (conj sqrs w))
          (= l w) (recur l (- w l) (conj sqrs l))
        )
        sqrs
      )
    )
    nil
  )
)
______________________________
(ns sq-in-rect.core)

(defn sq-in-rect [lng wdth]
  (if (= lng wdth)
    nil
    (loop [[a b] (sort [lng wdth]) sqrs []]
      (if (> a 0) (recur (sort [a (- b a)]) (conj sqrs a)) sqrs))
  )
)
______________________________
(ns sq-in-rect.core)

(defn rect [a b]
  (if (some zero? [a b]) nil
      (let [[short long] (sort [a b])]
        (cons short (rect (- long short) short)))))

;;guard for the condition that rect 5 5 = nil rather than 5

(defn sq-in-rect [a b]
  (when (not= a b)
    (rect a b)))

