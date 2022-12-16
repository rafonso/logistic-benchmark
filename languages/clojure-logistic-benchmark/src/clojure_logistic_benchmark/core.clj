(ns clojure-logistic-benchmark.core
  (:gen-class))

(defn average [lst] (/ (reduce + lst) (count lst)))

(defn calculate1
  [r iter t0 series i x]
  (if (= i iter)
    [series (- (System/currentTimeMillis) t0)]
    (do
      (aset-double series i x)
      (recur r iter t0 series (+ i 1) (* (* r x) (- 1.0 x))))))

(defn calculate
  [x0 r iter]
  (calculate1 r iter (System/currentTimeMillis) (double-array iter) 0 x0))

(defn simple-action
  [x0 r iter show-series]
  (let [[series delta-t] (calculate x0 r iter)]
    (when show-series
      (println (apply str (repeat 40 "-")))
      (run! println series)
      (println (apply str (repeat 40 "-"))))
    (println "TIME:" delta-t "ms")))

(defn repeat-action
  [x0 r iter repetitions]
  (let [times (long-array repetitions) t0 (System/currentTimeMillis)]
    (doall
     (for [i (range repetitions)]
       (aset-long times i ((calculate x0 r iter) 1))))
    (let [delta-t (- (System/currentTimeMillis) t0) avg (average times)]
      (println)
      (println "AVERAGE" (double avg) "ms")
      (println "TOTAL_TIME" delta-t))))

(defn -main [& args]
  (let [cli-args                     (vec args)
        action                       (get cli-args 0)
        x0       (Double/parseDouble (get cli-args 1))
        r        (Double/parseDouble (get cli-args 2))
        iter     (Integer/parseInt   (get cli-args 3))]
    (cond
      (= action "s") ((let [show-series (and (= (count cli-args) 5) (= (get cli-args 4) "s"))]
                        (simple-action x0 r iter show-series)))
      (= action "r") ((let [repetitions (Integer/parseInt (get cli-args 4))]
                        (repeat-action x0 r iter repetitions)))
      :else          (println "No defined action defined. Arguments: " cli-args))))
