#!/usr/bin/env bb

;; https://stackoverflow.com/a/68411760
(require '[clojure.java.io :as io])

(let [archive (first *command-line-args*)
      pattern (second *command-line-args*)]
  (cond
    (or (nil? archive) (nil? pattern))
    (do
      (println "Usage: findclass.bb <zip-or-jar> <regex>")
      (System/exit 1))

    :else
    (try
      (with-open [zf (java.util.zip.ZipFile. (io/file archive))]
        (let [entries (enumeration-seq (.entries zf))
              match? (some #(re-find (re-pattern pattern) (.getName ^java.util.zip.ZipEntry %))
                           entries)]
          (when match?
            (println archive))))
      (catch Exception e
        (binding [*out* *err*]
          (println "Error reading archive:" (.getMessage e)))
        (System/exit 1)))))
