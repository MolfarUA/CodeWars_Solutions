55c6126177c9441a570000cc


(ns weightsort.core
  (:require [clojure.string :as str]))

(defn- sum-of-digits [s]
  (->> s
       (map (comp read-string str))
       (apply +)))

(defn order-weight [strng]
  (->> 
    (str/split strng #"\s+")
    (sort-by #(vector (sum-of-digits %) %))
    (str/join " ")))
_____________________________
(ns weightsort.core
  (:require [clojure.string :as str]))

(defn weight-comp [s1 s2]
  (let [digit-weight (fn [s] (reduce + (map #(Character/getNumericValue %) s)))

        digits-s1 (digit-weight s1)
        digits-s2 (digit-weight s2)]
    (if (not= digits-s1 digits-s2)
      (compare digits-s1 digits-s2)
      (compare s1 s2)
      )))

(defn order-weight [s]
  (->> (str/split s #" ")
       (sort weight-comp)
       (str/join " ")))
_____________________________
(ns weightsort.core)
(use '[clojure.string :only (join split)])

(defn f [x y] (+ x (- (int y) (int \0))))

(def ob (partial reduce f 0))

(defn order-weight [s]
  (->> (split s #"\s")
       sort
       (sort-by ob)
       (join " ")))
