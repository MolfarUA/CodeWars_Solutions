51c8e37cee245da6b40000bd


(ns strip-comments)

(def rep clojure.string/replace)

(defn strip-comments [t s]
  (-> t
      (rep (re-pattern (str "[" (apply str s) "].*")) "")
      (rep #"\h+\n" "\n")
      (rep #"\h+$" "")
) )
__________________________________
(ns strip-comments
  (:require [clojure.string :as s]))

(defn strip-comments [text syms]
  (s/join "\n"
          (map (fn [line]
                 (->> line
                      (take-while #(not (contains? (set syms) (str %))))
                      (s/join "")
                      (s/trimr)
                      ))
               (s/split text #"\n"))))
__________________________________
(ns strip-comments)

(defn strip-comments [text comment-symbols]
  (clojure.string/join "\n"
    (map 
        #(if (nil? %)
           ""
           (clojure.string/trimr %))
        (map
          #(first (clojure.string/split % (re-pattern (str "[" (apply str comment-symbols) "]"))))
          (clojure.string/split 
            text
            #"\n")))))
__________________________________
(ns strip-comments)
(def not-empty? (comp not empty?))
(def into-lines! (fn [t] (clojure.string/split-lines t)))

(defn line-has-comment-symb?
  [line cmark]
  (->> cmark
       (map #(clojure.string/includes? line %))
       (filter true?)
       not-empty?))

(defn symbols->regex-pattern [symbs]
  (re-pattern (str "[" (clojure.string/join "" symbs) "]")))

(defn before-comment-only! [text pattern]
  (-> text (clojure.string/split pattern) first))

(defn with-pattern-remove-comments! [text symb]
  (let [pattern (symbols->regex-pattern symb)]
    (-> text (before-comment-only! pattern))))

(defn remove-comment! [text symb]
  (if (line-has-comment-symb? text symb)
    (with-pattern-remove-comments! text symb)
    text))

(defn only-til-comment-or-empty-str
  [comment-symbols lines]
  (->> lines
       (map #(remove-comment! % comment-symbols))
       (map #(if (nil? %) "" %))))

(defn strip-comments [text comment-symbols]
  (->> text
       into-lines!
       (only-til-comment-or-empty-str comment-symbols)
       (map #(clojure.string/trimr %))
       (reduce (fn [acc cur] (str acc "\n" cur)))))
