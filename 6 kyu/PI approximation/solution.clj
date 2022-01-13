(ns piapprox.core)

(defn round [s n] 
  (.setScale (bigdec n) s java.math.RoundingMode/HALF_EVEN)) 

(defn iterPi [epsilon]
  (loop [i 1 value 4.0]
    (if (<= (Math/abs (- Math/PI value)) epsilon)
      [i, (round 10 value)]
      (do
        ;(println value)
        (recur (inc i) (+ value (* 4.0 (/ (Math/pow -1 i) (+ 1 (* 2 i))))))))))
________________________________________
(ns piapprox.core)

(defn round [s n] 
  (.setScale (bigdec n) s java.math.RoundingMode/HALF_EVEN)) 

(defn iterPi [epsilon]
  (loop [i 1 pi4 1.0 s -1.0 d 3.0]
    (if (<= (Math/abs (- (* 4 pi4) Math/PI)) epsilon)
      [i, (round 10 (* 4 pi4))]
      (recur (inc i) (+ pi4 (* s (/ 1.0 d))) (* s -1.0) (+ 2 d)))))
________________________________________
(ns piapprox.core)

(defn round [s n]
  (.setScale (bigdec n) s java.math.RoundingMode/HALF_EVEN))

(defn iterPi [epsilon]
  (let [too-inaccurate (fn [[_ x]] (> (Math/abs (- x Math/PI)) epsilon))
        series-element (fn [k] (/ (* (- 1 (* 2 (mod k 2))) 4.0) (+ (* 2 k) 1)))
        [[n s]] (take 1 (drop-while too-inaccurate
                              (reductions (fn [[_ s] [k x]] [k (+ s x)])
                                          (map (fn [k] [k (series-element k)]) (range)))))]
    [(inc n) (round 10 s)]))
________________________________________
(ns piapprox.core)

(defn round [s n] 
  (.setScale (bigdec n) s java.math.RoundingMode/HALF_EVEN)) 

(defn iterPi [epsilon]
  (loop [acc 4.0
         sgn -1
         div 3
         num 1]
    (if (< (Math/abs (- Math/PI acc)) epsilon)
      [num (round 10 acc)]
      (recur (+ acc (/ (* 4 sgn) div))
             (- sgn)
             (+ div 2)
             (inc num)))))
________________________________________
(ns piapprox.core)

(defn round [s n] 
  (.setScale (bigdec n) s java.math.RoundingMode/HALF_EVEN)) 

(defn iterPi [epsilon]
  (->> (iterate 
          #(let [[val num sig]  %
                 den            (inc (* num 2))
                 add            (* sig (/ 1 den))]
              [(+ add val) (inc num) (* sig -1)])
              [1.0 1 -1])
       (drop-while #(> (Math/abs (- (* 4 (first %)) Math/PI)) epsilon))
       (first)
       ((fn [[val num _]] [num (round 10 (* 4 val))]))
  )
)
