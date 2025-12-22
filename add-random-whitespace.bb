#!/usr/bin/env bb

(require '[clojure.java.io :as io]
         '[clojure.string :as str])

(defn rand-in-range
  [min max]
  (+ min (rand-int (- (inc max) min))))

(defn add-whitespace-to-lines
  [file max-space-chars space-types prob-cutoff]
  (with-open [rdr (io/reader file)]
    (let [lines (line-seq rdr)
          updated-lines (mapv (fn [line]
                                (if (< (rand) prob-cutoff)
                                  (str (nth space-types (rand-int (count space-types)))
                                       (apply str (repeat (rand-in-range 1 max-space-chars) " "))
                                       line
                                       (apply str (repeat (rand-in-range 1 max-space-chars) " "))
                                       (nth space-types (rand-int (count space-types))))
                                  line))
                              lines)]
      updated-lines)))

(let [[file & args] *command-line-args*
      max-space-chars (Integer/parseInt (or (first args) "5"))
      space-types (str/split (or (second args) " ") #"")
      prob-cutoff (Double/parseDouble (or (nth args 2) "0.5"))]
  (doseq [line (add-whitespace-to-lines file max-space-chars space-types prob-cutoff)]
    (println line)))
