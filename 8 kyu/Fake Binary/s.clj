(ns kata)

(defn fake-bin [x]
  (clojure.string/replace (clojure.string/replace x #"[1234]" "0") #"[56789]" "1")
  )
__________________________________
(ns kata
  (:require [clojure.string :as string]))

(defn convert-num 
  [n]
  (if (>= (Integer/parseInt (str n)) 5)
    "1"
    "0"))

(defn fake-bin [x]
  ;; TODO
  (string/join "" (to-array (map convert-num (char-array x)))))
__________________________________
(ns kata)

(defn < [a b] (clojure.core/< (compare a b) 0))

(defn fake-bin [x]
  (->> x
    (map #(if (< % \5) 0 1))
    (apply str)))
__________________________________
(ns kata)

(def fake-binary-true "1")
(def fake-binary-false "0")
(def fake-binary-bounduary 5)

(defn char->fake-binary [c]
  (let [number (Integer/parseInt c)]
    (if (< number fake-binary-bounduary)
      fake-binary-false fake-binary-true)))

(defn fake-bin [x]
  (clojure.string/replace x #"\d" char->fake-binary))
__________________________________
(ns kata)

(defn round_5 [a]
  (if (< (int a) (int \5)) "0" "1")
  )
(defn fake-bin [x]
  (clojure.string/join "" (map round_5 x))
  )
