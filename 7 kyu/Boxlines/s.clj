(ns box-lines.core)

(defn f [x y z]
  (+ (* x (inc y) (inc z))
     (* (inc x) y (inc z))
     (* (inc x) (inc y) z)))
_____________________________________
(ns box-lines.core)

(defn f [x y z]
    (+ x y z (* 2 (+ (* x y) (* x z) (* y z))) (* 3 x y z))
  )
_____________________________________
(ns box-lines.core)

(defn f [x y z]
  (let [myfloor (+ (* x (inc y)) (* y (inc x)))
        allfloors (* myfloor (inc z))
        struts (* (inc x) (inc y))
        allstruts (* struts z)
        ]
    (+ allfloors allstruts)
  )
)
_____________________________________
(ns box-lines.core)

(defn f [x y z]
  (+ (* z (+ (* 3 x y) 1 (* 2 (+ x y)))) (* 2 x y) x y)
  )
_____________________________________
(ns box-lines.core)

(defn f [x y z]
  (+ (* 3 x y z) (* 2 (+ (* x y) (* y z) (* x z))) x y z))
_____________________________________
(ns box-lines.core)

(defn f [x y z]
  (+ (* (inc x) (inc y) z) (* (inc x) y (inc z)) (* x (inc y) (inc z))))
