561e9c843a2ef5a40c0000a4


(ns gapinprimes.core)

;; Method isProbablePrime from BigInteger  is faster that any  do-it-yourself  algorithm
;; than most people could devise. So, first rule of any sw developer: Whenever something
;; is already done, use it.
;;
;; Nevetheless isProbablePrime is not a  true primality proof,  but a stocastic one.  If
;; need to go with a true proof try this:
;;    (defn prime? [n] (nil?(first(filter #(zero? (rem n %)) (range 2 (inc (Math/sqrt n)))))))
;; This is a non stocasting proof, although it's slower.
;;
;; Also, there is a true primality proof faster that the above due to Agrawal, Kayal and
;; Saxena (See: http://annals.math.princeton.edu/2004/160-2/p12)

(defn gap [g m n]
  (defn prime? [n] (.isProbablePrime (BigInteger/valueOf n) 5))
  (let [primes (filter prime? (range m (inc n)))]
      (first (filter #(= (- (last %)(first %)) g) (map vector primes (rest primes)))))
) 
__________________________________
(ns gapinprimes.core)

(defn prime? [n]
  (.isProbablePrime (BigInteger/valueOf n) 5))

(defn gap [g m n]
  (->> (range m (inc n))
       (filter prime?)
       ((juxt identity rest))
       (apply map vector)
       (filter (fn [[a b]] (= g (- b a))))
       first)) 
__________________________________
(ns gapinprimes.core)

(defn prime? [n]
  (if (even? n) false
      (let [lim (+ 1 (int (Math/sqrt n)))]
  (loop [i 3]
    (if (> i lim) true
        (if (zero? (mod n i)) false
      (recur (+ i 2))))))))

(defn f-prime [k n]
  (if (>= k (+ n 1))
    -1
    (if (prime? k)
      k
      (f-prime (inc k) n))))

(defn search [i g n]
  (loop [k i]
    (if (>= k (+ n 1))
      nil
      (let [r (for [p (range (+ 1 k) n) :when (prime? p)] p)]
        (if (empty? r)
          nil
          (if (= g (- (first r) k))
            [k (first r)]
            (recur (first r))))))))

(defn gap [g m n]
  (let [i (f-prime m n)]
    (if (= i -1)
      nil
      (search i g n))))
