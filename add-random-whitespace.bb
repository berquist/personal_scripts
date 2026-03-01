#!/usr/bin/env bb

(require '[clojure.java.io :as io]
         '[lambdaisland.cli :as cli])

(defn rand-in-range
  "Return a random integer in the inclusive range [min, max]."
  [min max]
  (+ min (rand-int (- (inc max) min))))

(defn add-random-whitespace
  "Read *file* line‑by‑line and, with probability *prob-cutoff*, prepend and
   append a random whitespace character (chosen from *space-types*) surrounded
   by a random number (1‑*max-space-chars*) of ordinary spaces."
  [{:keys [file max-space-chars space-types prob-cutoff]}]
  (with-open [rdr (io/reader file)]
    (let [lines (line-seq rdr)
          space-chars (seq space-types)
          updated-lines
          (mapv (fn [line]
                  (if (< (rand) prob-cutoff)
                    (let [lead  (nth space-chars (rand-int (count space-chars)))
                          trail (nth space-chars (rand-int (count space-chars)))
                          left  (apply str (repeat (rand-in-range 1 max-space-chars) " "))
                          right (apply str (repeat (rand-in-range 1 max-space-chars) " "))]
                      (str lead left line right trail))
                    line))
                lines)]
      updated-lines)))

(cli/dispatch
 {:command #'add-random-whitespace
  :flags ["--file, -f" {:doc "The input file"}
          "--max-space-chars, -m" {:doc "Maximum number of whitespace characters to add to a line"
                                   :default 5}
          "--space-types, -s" {:doc "Types of whitespace to add (Unicode characters with property White_Space=yes)"
                               :default " "}
          "--prob-cutoff, -p" {:doc "Probability cutoff that a line will receive whitespace"
                               :default 0.5}]})
