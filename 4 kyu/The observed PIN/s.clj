5263c6999e0f40dee200059d


(ns observedpin)

(def corrections {
  \1 "124"  \2 "1235"  \3 "236"
  \4 "1457" \5 "24568" \6 "3569"
  \7 "478"  \8 "57890" \9 "689"
            \0 "80"
})

(defn get-pins [observed]
  (if (empty? observed)
    [""]
    (let [heads (corrections (first observed)) tails (get-pins (rest observed))]
      (for [d heads ds tails] (str d ds)))))
______________________________
(ns observedpin
  (require [clojure.string]))

(defn get-adjacent [x]
  (case x
    \1 [1 2 4]   \2 [1 2 3 5]   \3 [2 3 6]
    \4 [1 4 5 7] \5 [2 4 5 6 8] \6 [3 5 6 9]
    \7 [4 7 8]   \8 [0 5 7 8 9] \9 [6 8 9]
                 \0 [0 8] ))

(defn cart-prod [colls]  
  (if (empty? colls)
    '(())
    (for [more (cart-prod (rest colls)) x (first colls)]
      (cons x more))))
  
(defn get-pins [observed]  
  (map clojure.string/join (cart-prod (map get-adjacent (seq observed)))))
______________________________
(ns observedpin
(:require [clojure.string :as str]))

(def neighbors {\1 "124"
                \2 "1235"
                \3 "236"
                \4 "1457"
                \5 "24568"
                \6 "3569"
                \7 "478"
                \8 "57890"
                \9 "689"
                \0 "80"})


(defn get-pins [input]
  (->> (reduce #(for [x %1
                      y (neighbors %2)]
                  (conj x y)) [[]] (seq input))
       (map str/join)))
