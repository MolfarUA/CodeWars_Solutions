(ns mixin.core
  (:require [clojure.string :as s]))

(defn mix [s t]
  (let [[fs ft] (map #(frequencies (s/replace % #"[^a-z]" "")) [s t])]
    (->> (concat (keys fs) (keys ft))
         (distinct)
         (map
           (fn [c]
             (let [x (fs c 0)
                   y (ft c 0)]
               [(cond
                  (= x y) \=
                  (> x y) \1
                  :else \2)
                (apply str (repeat (max x y) c))])))
         (filter #(> (count (second %)) 1))
         (sort-by #(-> [(- (count (second %))) (first %) (first (second %))]))
         (map #(str (first %) ":" (second %)))
         (s/join \/ ))))

__________________________________________________
(ns mixin.core)
(require '[clojure.string :as str])
(defn mix [s1 s2]
    (->> (for [c "abcdefghijklmnopqrstuvwxyz" 
                  :let [x1 (str/join (filter #{c} s1))
                        n1 (count x1)        
                        x2 (str/join (filter #{c} s2))
                        n2 (count x2)]
                  :when (< 1 (max n1 n2))]
                (cond (< n1 n2) {:src \2 :chs x2 :len n2}
                      (< n2 n1) {:src \1 :chs x1 :len n1}
                      :else     {:src \= :chs x1 :len n1}))
        (sort-by (juxt (comp - :len) :src :chs))
        (map  #(format "%c:%s" (:src %) (:chs %)))
        (str/join \/)))

__________________________________________________
(ns mixin.core)
(require '[clojure.string :as str])

(defn mix [s1 s2]
  (let [f  (fn [idx]
             (fn [m] (->> m
                         (frequencies)
                         (filter (fn [[k v]] (and (> v 1) (Character/isLowerCase k))))
                         (into {})
                         (map (fn [[k v]] [k [idx v]]))
                         (into {}))))]
    (->> (merge-with (fn [itm1 itm2]
                       (let [[idx1 v1] itm1
                             [idx2 v2] itm2]
                         (cond (> v1 v2) itm1
                               (= v1 v2) ["=" v1]
                               :else itm2)))
                     ((f 1) s1)
                     ((f 2) s2))

         (sort (fn [[k1 [idx1 v1]] [k2 [idx2 v2]]]
                 (let [idx1 (if (= "=" idx1) 3 idx1)
                       idx2 (if (= "=" idx2) 3 idx2)
                       v-compare (compare v2 v1)
                       i-compare (compare idx1 idx2)
                       k-compare (compare k1 k2)]
                   (cond
                     (not (= 0 v-compare)) v-compare
                     (not (= 0 i-compare)) i-compare
                     :else k-compare))))
         (map (fn [[k [idx v]]] (->> (repeat v k) (apply str idx ":"))))
         (str/join "/"))))

__________________________________________________
(ns mixin.core)
(require '[clojure.string :as str])

(defn mk-tab [s]
  (for [x (map char (range 97 123)) 
      :let [c (count (filter (fn [v] (= x v)) s)) ]
     ]
  (list x c)))

(defn mk-pair [sndx sndy]
  (let [m (max sndx sndy)
        p (cond
            (and (> m 1) (> m sndx)) 2
            (and (> m 1) (> m sndy)) 1
            :else 0)
       ]
    (list p m)))

(defn mk-str [x y]
  (cond 
    (= 1 (first y)) (str "1:" (apply str (repeat (second y) x)))
    (= 2 (first y)) (str "2:" (apply str (repeat (second y) x)))
    :else (str "=:" (apply str (repeat (second y) x)))))
    
(defn compsort [a b]
  (let [x (- (count b) (count a))]
    (if (= 0 x)
      (compare a b)
      x)))

(defn mix [s1 s2]
  (let [a1 (map vector (mk-tab s1) (mk-tab s2))
        a2 (map (fn [ [x y] ] [(first x) (mk-pair (second x) (second y))]) a1)
        a3 (filter (fn [ [x y] ] (> (second y) 1)) a2)
        a4 (str/join "/" (sort compsort (map (fn [ [x y] ] (mk-str x y)) a3)))
       ]
    a4))

__________________________________________________
(ns mixin.core)

(defn mix [s1 s2]
  (let [stat (fn [s] (frequencies (filter #(<= 97 (int %) 122) s)))
        fs1 (stat s1) fs2 (stat s2)
        mark (fn [c] ([\1 \= \2] (inc (compare (fs2 c) (fs1 c))))) ]
    (->> (merge-with max fs1 fs2)
      (filter #(< 1 (% 1)))
      (map (fn [[c n]] (apply str (mark c) \: (repeat n c))))
      sort
      (sort-by count >)
      (interpose \/)
      flatten
      (apply str) )))
