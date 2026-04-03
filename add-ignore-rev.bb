#!/usr/bin/env bb

(require '[babashka.shell :refer [sh]]
         '[clojure.string :as str])

;; Helper to run a git command and return trimmed stdout.
(defn git [& args]
  (let [{:keys [out err exit]} (apply sh "git" args)]
    (when (not= exit 0)
      (throw (ex-info (str "git " (pr-str args) " failed: " err) {})))
    (str/trim out)))

;; 1. Verify we are inside a Git work‑tree.
(try
  (git "rev-parse" "--is-inside-work-tree")
  (catch Exception _
    (println "Error: not inside a Git repository.")
    (System/exit 1)))

;; 2. Get the current HEAD SHA and its one‑line summary.
(def head-sha (git "rev-parse" "HEAD"))
(def summary  (git "log" "-1" "--pretty=%s" "HEAD"))

;; 3. Build the line to add (commented for readability).
(def ignore-line (str "# " summary " " head-sha))

;; 4. Determine the repository root and the path to the ignore file.
(def repo-root (git "rev-parse" "--show-toplevel"))
(def ignore-path (str repo-root "/.git-blame-ignore-revs"))

;; 5. Read existing lines, if the file already exists.
(def existing-lines
  (if (.exists (java.io.File. ignore-path))
    (str/split-lines (slurp ignore-path))
    []))

;; 6. Append only if the SHA isn’t already present.
(if (some #(str/includes? % head-sha) existing-lines)
  (println "SHA already present in .git-blame-ignore-revs; nothing to do.")
  (do
    (spit ignore-path
          (str (when (seq existing-lines)
                 (str (str/join "\n" existing-lines) "\n"))
               ignore-line "\n")
          :append false)
    (println "Added to .git-blame-ignore-revs:" ignore-line)))
