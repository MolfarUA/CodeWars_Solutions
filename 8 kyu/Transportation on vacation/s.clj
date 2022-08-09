568d0dd208ee69389d000016


(ns rentalcarcost.core)

(defn rental-car-cost [d]
  (def cost (* d 40) )
  (cond 
    (>= d 7) (- cost 50)
    (>= d 3) (- cost 20)
    :else cost
  )
)
__________________________
(ns rentalcarcost.core)

(defn rental-car-cost [d]
  (let [init (* d 40)]
    (cond
      (>= d 7) (- init 50)
      (>= d 3) (- init 20)
      :else init)))
__________________________
(ns rentalcarcost.core)

;; Discounts and thresholds
(def discount-base 0)
(def discount-tier-one-threshold 3)
(def discount-tier-one-value 20)

(def discount-tier-two-threshold 7)
(def discount-tier-two-value 50)

;; Base cost to rent car for one day.
(def daily-cost 40)

(defn discount [days]
"Calculate discount to apply based on days."
  (cond (>= days discount-tier-two-threshold) discount-tier-two-value
        (>= days discount-tier-one-threshold) discount-tier-one-value
        :else discount-base))

(defn base [days]
  "Calculates base cost of rental for number of days."
  (* daily-cost days))


(defn rental-car-cost [days]
  "Returns car rental cost after applying discounts."
  (- (base days) (discount days)))
 
