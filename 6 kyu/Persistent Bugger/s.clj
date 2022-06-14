(ns persistent.core)

(defn persistence [n]
  (if (< n 10)
    0
    (let [digit-list (->> (str n)
                          seq
                          (map str)
                          (map read-string))]
        (if (= 1 (count digit-list))
            digit-list
            (inc (persistence (reduce * digit-list)))))))
________________________________________
(ns persistent.core)

(defn persistence [n]
  (loop [r 0 n n]
    (if (< n 10) r
    (->> n
      str
      (map (comp read-string str))
      (reduce *)
      (recur (inc r))))))
________________________________________
(ns persistent.core)
(defn persistence-helper [n c]
    (if (< n 10) c
      (let [digs (map #(Character/digit % 10) (str n))
            mult-num (reduce * digs)]
          (recur mult-num (inc c)))))
          
          
(defn persistence [n]
    (persistence-helper n 0))
________________________________________
(ns persistent.core)

(defn multiply-digits [number]
  (->> (str number)
       (map #(Character/getNumericValue %))
       (apply *)))

(defn persistence [number]
  (loop [digits number times 0]
    (if (>= digits 10)
      (recur (multiply-digits digits) (inc times))
      times)))
