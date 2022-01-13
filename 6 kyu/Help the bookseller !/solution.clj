(ns bookseller.core
  (:require [clojure.string :as string] ))

(defn get-books-for-category
  [list-of-books category]
  (filter (fn [book]
      (string/starts-with? book category))
    list-of-books))

(defn get-book-quantities
  [list-of-books]
  (for [book list-of-books]
    (Integer/parseInt (nth (string/split book #" ") 1))
  )
)

(defn coll-is-empty
  [coll]
  (= (count coll) 0))

(defn stock-list [list-of-books list-of-cat]
  (if (or
       (coll-is-empty list-of-books)
       (coll-is-empty list-of-cat))
    []
    (for [category list-of-cat]
      [category (reduce + (get-book-quantities (get-books-for-category list-of-books category)))]
    ))
)
________________________________________
(ns bookseller.core
  (:require [clojure.string :as str]))

(defn books-by-category [list-of-books category]
  "Filter a list of books in a certain category"
  (->> list-of-books
       (filter #(= (first %) (char category)))))

(defn category-char-from [str]
  "Extract the category of a book from the String into a Character"
  (.charAt str 0))

(defn str-to-int [str]
  "Convert a number in string form to an int"
  (Integer/parseInt str))

(defn get-number-in-stock [book]
  "Extract the number of books in stock(same title) from book string"
  (str-to-int (nth (str/split book #" ") 1)))

(defn extract-sum-from-books [list-of-books]
  "Calculate the sum of all books in stock from a books list"
  (->> list-of-books
       (map get-number-in-stock)
       (reduce +)))

(defn print-stock [cat-num-list]
  (map #(format "(%s : %s)" (first %) (second %)) cat-num-list))

(defn stock-list [list-of-books list-of-cat]
  (print list-of-books)
  (print list-of-cat)
  (if (or (empty? list-of-books) (empty? list-of-cat))
    []
  (->> list-of-cat
       (map #(books-by-category list-of-books (category-char-from %)))
       (map #(extract-sum-from-books %))
       (interleave list-of-cat)
       (partition 2))))
________________________________________
(ns bookseller.core)

(defn split-spaces
  "Split a coll of items on spaces."
  [coll]
  (map #(clojure.string/split % #" ") coll))

(defn category-stock
  "Create a seq of maps corresponding to categories and the stock for
   each item."
  [coll]
  (map (fn [item]
         (assoc {} (str (ffirst item)) (Integer/parseInt (second item))))
       coll))

(defn stock-list [list-of-books list-of-cat]
  (if (empty? list-of-books)
    []
  (as-> (split-spaces list-of-books) m
        (category-stock m)
        (apply merge-with + m)
        (map m list-of-cat)
        (replace {nil 0} m)
        (map vector list-of-cat m))))
________________________________________
(ns bookseller.core)

(defn split-info [val]
  (let [split-info (clojure.string/split val #" ")]
    {(str (first (first split-info))) (Integer/parseInt (second split-info))}))

(defn sum-up 
  ([]
   [])
  ([current-val new-val]
              (let [splited (split-info new-val)]
                (if (map? current-val)
                  (merge-with #(+ %1 %2) current-val splited)
                  (merge-with #(+ %1 %2) (split-info current-val) splited)))))

(defn stock-list [list-of-books list-of-cat]
  (let [counted (reduce sum-up list-of-books)]
    (if-not (empty? counted)
      (vec (for [cat list-of-cat]
             (if (contains? counted cat)
               [cat (get counted cat)]
               [cat 0])))
      [])))
________________________________________
(ns bookseller.core)

(defn stock-list [list-of-books list-of-cat]
  (if (or (empty? list-of-books) (empty? list-of-cat))
    []
    (let [stock
          (reduce (fn [acc entry]
                    (update acc
                            (-> entry first str)
                            (fnil + 0) (-> entry
                                           (clojure.string/split #" ")
                                           last
                                           Integer/parseInt))) 
                  {} list-of-books)]
      (map #(vector %1 (get stock %1 0)) list-of-cat))))
