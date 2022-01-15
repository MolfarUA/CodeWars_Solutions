(ns code-decode.core)

(defn digits [s]
  (->> (map str s)
       (map read-string)))

(defn count-bits [n]
  (count (Integer/toBinaryString n)))

(defn code-digit [d]
  (str (apply str (repeat (dec (count-bits d)) "0"))
       "1"
       (Integer/toBinaryString d)))

(defn code [n]
  (->> (digits n)
       (map code-digit)
       (reduce str)))

(defn parse-next [n]
  (let [bits (inc (count (take-while (partial not= \1) n)))]
    (list (Integer/parseInt (apply str (take bits (drop bits n))) 2)
          (apply str (drop (* 2 bits) n)))))

(defn decode-digits [n]
  (if (empty? n)
    nil
    (let [[a b] (parse-next n)]
      (lazy-seq (cons a (decode-digits b))))))

(defn decode [n]
  (apply str  (map str (decode-digits n))))
__________________________
(ns code-decode.core)

(defn encode-digit [n]
    (let [bits (Integer/toBinaryString n)
          prefix (repeat (dec (count bits)) "0")]
        (str (apply str prefix) "1" bits)))

(defn code [s]
  (apply str (map encode-digit (map #(- (int %) 48) s))))

(defn decode [xs]
  (loop [xs xs 
         acc []]
    (if (empty? xs) (apply str acc)
      (let [bits (take-while #(= % \0) xs)
            nbits (inc (count bits))
            digits (apply str (take nbits (drop nbits xs)))
            val (Integer/parseUnsignedInt digits 2)]
        (recur (drop (* 2 nbits) xs) (conj acc (str val)))
      ))))
__________________________
(ns code-decode.core
  (:require [clojure.string :as string]))

(defn code-number [n]
  (let [s (Integer/toString n 2)]
    (str (string/join (repeat (dec (count s)) "0")) "1" s)))

(defn code [s]
  (string/join (map (comp code-number #(- (int %) 48)) s)))

(defn decode [s] 
  (loop [buf []
         s s]
    (if (seq s)
      (let [c (inc (count (take-while #(= % \0) s)))
            n-end (+ c c)]
        (recur (conj buf (str (Integer/parseInt (subs s c n-end) 2)))
               (subs s n-end (count s))))
      (string/join buf))))
__________________________
(ns code-decode.core)
(use '[clojure.string :only (split)])
(use '[clojure.set :only (map-invert)])

(def dictionary {"0" "10"
                 "1" "11"
                 "2" "0110"
                 "3" "0111"
                 "4" "001100"
                 "5" "001101"
                 "6" "001110"
                 "7" "001111"
                 "8" "00011000"
                 "9" "00011001"})
(def dictionary-inverted (map-invert dictionary))

(defn chunks [strng]
  (->> (map #(take % strng) [8 6 4 2])
       (map (partial apply str))
       (distinct)))

(defn code [strng]
  (apply str (map dictionary (split strng #""))))

(defn decode [strng]
  (if (empty? strng) ""
    (let [[s] (filter dictionary-inverted (chunks strng))]
      (str (dictionary-inverted s) (decode (subs strng (count s)))))))
__________________________
(ns code-decode.core
  (:require [clojure.string :as str]))

(defn code [num]
  (let [digits (->> num str (map (comp read-string str)))]
    (reduce (fn [acc i]
              (str acc (let [bin (Integer/toBinaryString i)]
                          (str (apply str (repeat (dec (count bin)) "0")) "1" bin)))) "" digits )))

(defn decode [b]
  (loop [bin b res ""]
    (if (str/blank? bin)
      res
      (let [bits (inc (count (take-while #(not= \1 %) bin)))]
        (recur (subs bin (* 2 bits)) (str res (Integer/parseInt (subs bin bits (* 2 bits)) 2)))))))
__________________________
(ns code-decode.core
  (:require [clojure.string :as str]))

(defn digit->coding
  [s]
  (let [d (Integer/toString (Integer. s) 2)
        k (count d)]
    (str (str/join (repeat (dec k) "0"))
         "1"
         d)))

(defn code
  [s]
  (let [digits (re-seq #"\d" s)]
    (str/join
     (map digit->coding digits))))

(defn decode
  [s]
  (str/replace s
               ; between "|" are the digits from 9 to 0, coded with code fn.
               #"00011001|00011000|001111|001110|001101|001100|0111|0110|11|10"
               {"10" "0"
                "11" "1"
                "0110" "2"
                "0111" "3"
                "001100" "4"
                "001101" "5"
                "001110" "6"
                "001111" "7"
                "00011000" "8"
                "00011001" "9"
                }))

