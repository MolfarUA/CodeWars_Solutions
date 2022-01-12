(ns sumofk.core)

(defn som [l] (reduce + l))

(defn comb [n items]
  (cond
    (= n 0) '(())
    (empty? items) '()
    :else (concat (map
                    #(cons (first items) %)
                    (comb (dec n) (rest items)))
                  (comb n (rest items)))))

(defn choose-best-sum [t k ls]
  (let [ a (comb k ls) mx -1 res [] 
         b (map som a)         
         c (filter (fn [x] (<= x t)) b)
         d (if (empty? c)
             nil
             (apply max c))
       ] 
    d
    ))
_______________________________________
(ns sumofk.core)

(defn perm [arr]
  (loop [acc (list nil) ls arr]
    (if (empty? ls)
      acc
      (let [hd (first ls)
            tl (rest ls)
            ys (map (fn [xs] (conj xs hd)) acc)
            acc1 (concat acc ys)]
        (recur acc1 tl)))))

(defn best-sum [t k arr]
  (->> (perm arr)
       (filter #(= k (count %)))
       (map #(reduce + %))
       (filter #(<= % t))
    ))

(defn choose-best-sum [t k arr]
  (let [ls (best-sum t k arr)]
    (if (empty? ls)
      nil
      (reduce max ls))))
_______________________________________
(ns sumofk.core)

(defn som [l] (reduce + l))

(defn comb [n items]
  (cond
    (= n 0) '(())
    (empty? items) '()
    :else (concat (map
                    #(cons (first items) %)
                    (comb (dec n) (rest items)))
                  (comb n (rest items)))))

(defn choose-best-sum [t k ls]
  (let [ a (comb k ls) mx -1 res [] 
         b (map som a)         
         c (filter (fn [x] (<= x t)) b)
         d (if (empty? c)
             nil
             (apply max c))
       ] 
    d
    ))
_______________________________________
(ns sumofk.core)

(defn select-n [n lst]
  (defn prepend-to-all [x xss]
    (map #(cons x %) xss))
  (let [len (count lst)]
    (cond 
      (zero? n) [[]]
      (< n len) (concat (prepend-to-all (first lst)
                                (select-n (dec n) 
                                          (rest lst)))
                        (select-n n (rest lst)))
      (= n len) (prepend-to-all (first lst)
                                (select-n (dec n) 
                                          (rest lst)))
      :else [])))

(defn choose-best-sum [t k ls]
  (let [sums (->> (select-n k ls)
               (map #(reduce + %))
               (filter #(<= % t)))]
    (when (not (empty? sums))
      (apply max sums))))
_______________________________________
(ns sumofk.core)

(defn combo [m n]
  (loop [x (map vector (range n))
         y 1]
    (if (= y m)
      x
      (recur (for [i x
                   j (range n)
                   :when (every? #(> j %) i)]
               (conj i j))
             (inc y)))))

(defn comb [k ls]
  (let [combos (combo k (count ls))]
    (map (fn [v]
           (map #(ls %) v)) combos)))

(defn som [l] (reduce + l))

(defn som [l] (reduce + l))

(defn choose-best-sum [t k ls]
  (let [ a (comb k ls) mx -1 res [] 
         b (map som a)         
         c (filter (fn [x] (<= x t)) b)
         d (if (empty? c)
             nil
             (apply max c))
       ] 
    d
    ))
