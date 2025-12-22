#!/usr/bin/env bb

(require '[clojure.java.io :as io]
         '[cli-matic.core :refer [run-cmd]])

(defn rand-in-range
  [min max]
  (+ min (rand-int (- (inc max) min))))

(defn add-whitespace-to-lines
  [{:keys [file max-space-chars space-types prob-cutoff]}]
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

(def cli-options
  [{:option "file" :short "f" :type :string :default "" :desc "The input file"}
   {:option "max-space-chars" :short "m" :type :int :default 5 :desc "Maximum number of whitespace characters to add to a line"}
   {:option "space-types" :short "s" :type :string :default " " :desc "Types of whitespace to add (Unicode characters with property White_Space=yes)"}
   {:option "prob-cutoff" :short "p" :type :double :default 0.5 :desc "Probability cutoff that a line will receive whitespace"}])

(let [parsed-args (run-cmd *command-line-args* cli-options)]
  (doseq [line (add-whitespace-to-lines parsed-args)]
    (println line)))
