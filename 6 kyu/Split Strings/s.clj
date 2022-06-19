515de9ae9dcfc28eb6000001


(ns split-str.core)


(defn solution
  [s]
(map clojure.string/join (partition 2 2 "_" s)))
________________________________
(ns split-str.core)

(defn solution
  [s]
  (map #(apply str %) (partition 2 2 "_" s)))
________________________________
(ns split-str.core)

(defn solution
  [s]
  (->> (if (-> s count even?) s (str s "_"))
    (partition-all 2)
    (mapv (partial apply str))
    )
  )
________________________________
(ns split-str.core
  (:require [clojure.string :as str]))

(defn solution
  [s]
  (map #(str/join %) (partition 2 2 "_" s)))
________________________________
(ns split-str.core)

(defn- f [s] (let [t (apply str s)] (if (< (count t) 2) (str t "_") t)))

(defn solution
  [s]
  (map (partial f) (partition-all 2 s)))
