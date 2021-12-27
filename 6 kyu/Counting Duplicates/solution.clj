(ns katas.counting-duplicates)

(defn duplicate-count [text]
  (->> text
       (clojure.string/lower-case)
       (frequencies)
       (vals)
       (filter #(> % 1))
       (count)))
________________
(ns katas.counting-duplicates)

(defn duplicate-count [text]
  (count (filter #(> (second %) 1) (frequencies (clojure.string/lower-case text))))
)
____________________
(ns katas.counting-duplicates)

(defn duplicate-count [text]
  "Return the count of distinct case-insensitive alphanumeric characters"
  "that occur more than once"
  (->> text
       clojure.string/lower-case
       frequencies
       vals
       (filter #(> % 1))
       count))
__________________________
(ns katas.counting-duplicates)


(defn duplicate-count [text]
   ; Happy coding!
  (count (filter #(> (count %) 1) (vals (group-by identity (clojure.string/lower-case text))))))
____________________
(ns katas.counting-duplicates)

(defn duplicate-count [text]
  (->> text clojure.string/upper-case frequencies vals (filter #(> % 1)) count))
