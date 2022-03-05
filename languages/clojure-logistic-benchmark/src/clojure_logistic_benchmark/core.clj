(ns clojure-logistic-benchmark.core
  (:gen-class))

(defn average [lst] (/ (reduce + lst) (count lst)))

(defn calculate1
  [r iter t0 series i x]
  (if (= i iter)
    [series (- (System/currentTimeMillis) t0)]
    (recur r iter t0 (conj series x) (+ i 1) (* (* r x) (- 1.0 x)))))

(defn calculate
  [x0 r iter]
  (calculate1 r iter (System/currentTimeMillis) [] 0 x0))

(defn simple-action
  [x0 r iter show-series]
  (let [[series delta-t] (calculate x0 r iter)]
    (if show-series
      (do
        (println (apply str (repeat 40 "-")))
        (run! println series)
        (println (apply str (repeat 40 "-")))))
    (println "TIME:" delta-t "ms")))

(defn repeat-action
  [x0 r iter repetitions]
  (let [times (long-array repetitions) t0 (System/currentTimeMillis)]
    (doall
      (for [i (range repetitions)]
        (aset-long times i ((calculate x0 r iter) 1)))
      )
    (let [delta-t (- (System/currentTimeMillis) t0) avg (average times)]
      (println)
      (println "AVERAGE" (double avg) "ms")
      (println "TOTAL_TIME" delta-t))))

(defn -main [& args]
  (def cli-args (vec args))
  (def action (get cli-args 0))
  (def x0 (Double/parseDouble (get cli-args 1)))
  (def r (Double/parseDouble (get cli-args 2)))
  (def iter (Integer/parseInt (get cli-args 3)))

  (cond
    (= action "s") (do
                     (def show-series (and (= (count cli-args) 5) (= (get cli-args 4) "s")))
                     (simple-action x0 r iter show-series))
    (= action "r") (do
                     (def repetitions (Integer/parseInt (get cli-args 4)))
                     (repeat-action x0 r iter repetitions))
    :default (println "No defined action defined. Arguments: " cli-args)))

