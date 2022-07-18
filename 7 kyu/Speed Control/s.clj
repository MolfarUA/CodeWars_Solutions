56484848ba95170a8000004d


(ns gps.core)

(defn gps [s x]
  (->> (partition 2 1 x)
    (map (fn [[p c]] (- c p)))
    (map #(* % 3600.0))
    (map #(/ % s))
    (reduce max 0)
    long))
_____________________________
(ns gps.core)

(defn gps [s x]
  (if (<= (count x) 1)
    0
    (int (apply max (map #(/ (* % 3600) (float s)) (map - (rest x) x))))
  )
)
_____________________________
(ns gps.core)

(defn gps [s x]
  (if (< 1 (count x))
    (let [hourly-speed #(/ (* 3600 %) s)
          distances (map - (rest x) x)
          speeds (map hourly-speed distances)
          max-speed (apply max speeds)]
      (int max-speed))
    0))
_____________________________
(ns gps.core)

(defn gps [time-interval distances]
 (if (< (count distances) 2)
   0
   (let [distance-pairs (partition 2 (interleave (rest distances) (butlast distances)))
         pairwise-difference (fn [[a b]] (- a b))
         distances-per-interval (map pairwise-difference distance-pairs)
         seconds-in-an-hour 3600
         distance->velocity (fn [d] (/ (* seconds-in-an-hour d) time-interval))
         avg-velocities (map distance->velocity distances-per-interval)
         largest-avg-velocity (apply max avg-velocities)]
     (int largest-avg-velocity))))
