(defproject clojure-logistic-benchmark "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.10.3"]]
  :repl-options {:init-ns clojure-logistic-benchmark.core}
  :main clojure-logistic-benchmark.core
  :aot [clojure-logistic-benchmark.core]
  :jar-name "clojure-logistic-benchmark-simple.jar"
  :uberjar-name "clojure-logistic-benchmark.jar")
