544675c6f971f7399a000e79


(ns string-to-number-kata)

(defn string-to-number [str]
  (Integer/parseInt str))
_______________________
(ns string-to-number-kata)

(defn string-to-number [str]
  (read-string str)
)
_______________________
(ns string-to-number-kata)

(defn string-to-number [str]
  (Long/valueOf str))
_______________________
(ns string-to-number-kata)

(defn string-to-number [str]
  (def i (Integer/parseInt str))
)
_______________________
(ns string-to-number-kata
  [:require [clojure.core :as core]])

(defn string-to-number [str]
  (Integer/parseInt str))
_______________________
(ns string-to-number-kata)

(defn string-to-number [str]
  "Use Java interop"
  (Integer/parseInt str)
)
