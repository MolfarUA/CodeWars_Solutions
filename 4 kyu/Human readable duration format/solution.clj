52742f58faf5485cae000b9a


(ns human-readable
  (:require clojure.string))

(defn- pluralize [[unit v]]
  (when (and v (pos? v))
    (str v " " unit (when (> v 1) "s"))))

(defn formatDuration [secs]
  (if (zero? secs)
    "now"
    ; else
    (-> {"second" 60   ; seconds-in-minute
         "minute" 60   ; minutes-in-hour
         "hour"   24   ; hours-in-day
         "day"    365  ; days-in-year
         "year"   nil} ; years-in-eternity
      (->> 
        (reduce
          (fn [[C qty]
               [unit d]]
            (let [modulus (if d (mod qty d) qty)]
              [(cond-> C
                 (pos? modulus)
                 (assoc unit modulus))
               (when d
                 (quot qty d))]))
          [{} secs])
        first
        (map pluralize)
        reverse
        (clojure.string/join ", "))
      (clojure.string/replace #", ([^,]*)$" " and $1"))))

___________________________________________________
(ns human-readable)

(def units
  [{:name "year" :unit-duration 31536000}
   {:name "day" :unit-duration 86400}
   {:name "hour" :unit-duration 3600}
   {:name "minute" :unit-duration 60}
   {:name "second" :unit-duration 1}])

(defn to-units [secs]
  (loop [remaining secs
         [unit & more-units] units
         results []]
    (if unit
      (let [{name :name unit-duration :unit-duration} unit
            unit-count (quot remaining unit-duration)]
        (recur
          (mod remaining unit-duration)
          more-units
          (if (pos? unit-count)
            (conj results (str unit-count " " name (when (< 1 unit-count) "s")))
            results)))
      results)))

(defn formatDuration [secs]
  (if-not (pos? secs)
    "now"
    (let [durations (to-units secs)]
      (str (when (< 1 (count durations)) (str (clojure.string/join ", " (butlast durations)) " and ")) (last durations)))))

___________________________________________________
(ns human-readable)

(use '[clojure.string :only (join blank?)])

(defn formatDuration [secs]
  (let [units [[60 "second"] [60 "minute"] [24 "hour"] [365 "day"] [(inc secs) "year"]]
        extract-time (fn [[_ s _] [unit name]]
                       (let [time (rem s unit)
                             rem-time (quot s unit)
                             name (join [name (if (== 1 time) "" "s")])]
                         [time rem-time name]))
        time-parts (->> (reductions extract-time [0 secs ""] units)
                        (filter #(pos? (first %)))
                        (map (fn [[s _ n]] (join [s " " n])))
                        reverse)]
    (if (zero? (count time-parts))
      "now"
      (join " and " (filter #(not (blank? %)) [(join ", " (butlast time-parts)) (last time-parts)])))
    ))
