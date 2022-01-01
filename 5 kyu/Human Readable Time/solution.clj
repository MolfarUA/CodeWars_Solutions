(ns HumanTime)  

(defn human-readable
  [x]
  (let [s (mod x 60)
        m (mod (quot x 60) 60)
        h (quot x 3600)]
    (format "%02d:%02d:%02d" h m s)))

_____________________________________
(ns HumanTime)  

(defn human-readable
  [x]
  (let [h (quot x 3600)
        m (quot (mod x 3600) 60)
        s (mod x 60)]
    (format "%02d:%02d:%02d" h m s)))

_____________________________________
(ns HumanTime)  

(defn get-seconds [totalSeconds]
   (int (mod totalSeconds 60)))

(defn get-minutes [totalSeconds]
  (int (/ (mod totalSeconds  3600) 60)))

(defn get-hours [totalSeconds]
  (int (/ totalSeconds 3600)))

(defn human-readable [x]
  (format "%02d:%02d:%02d" (get-hours x) (get-minutes x) (get-seconds x)))

_____________________________________
(ns HumanTime)  

(defn human-readable [seconds]
  (let [h (quot seconds 3600)
        m (-> (rem seconds 3600) (quot 60))
        s (rem seconds 60)]
    (format "%02d:%02d:%02d" h m s)))

_____________________________________
(ns HumanTime)  

(defn human-readable
  [x]
  (format "%02d:%02d:%02d" (quot x 3600) (quot (mod x 3600) 60) (mod x 60))
  )
