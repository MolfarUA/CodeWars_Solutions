57cfdf34902f6ba3d300001e


(ns clojure.star-sort)
(require '[clojure.string :as string])

(defn star-sort [arr]
	(->> (sort arr)
    	 (first)
    	 (string/join "***")))
___________________________
(ns clojure.star-sort)

(defn star-sort [arr]
 (clojure.string/join "***" (first (sort arr))))
___________________________
(ns clojure.star-sort
  (:require [clojure.string :as string]))

(defn star-sort
  [arr]
  (->> arr
       sort
       first
       (string/join "***")))
