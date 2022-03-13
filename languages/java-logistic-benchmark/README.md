# Java

## Development Environment
  - Java 17
  - IntelliJ 2021.3.2
  - For Native DLL:
    - C++ 20
    - Visual Studio Community 2022

## Highlights

### [Java Double Array](./src/main/java/rafael/logistic_benchmark/benchmarks/JavaDoubleArrayGenerator.java )
Create a double array with size equals to number of interactions
#### Graphics
![Double Array - Linear](./assets/java-array-double-linear.svg "Double Array - Linear")
![Double Array - Log](./assets/java-array-double-log.svg "Double Array - Log")

### [Java Native Array](./src/main/java/rafael/logistic_benchmark/benchmarks/NativeDoubleArrayGenerator.java )
Calls a Native DLL to create a double array with size equals to number of interactions
#### Graphics
![Native Array - Linear](./assets/java-array-native-linear.svg "Native Array - Linear")
![Native Array - Log](./assets/java-array-native-log.svg "Native Array - Log")

### [Java Mixed Array](./src/main/java/rafael/logistic_benchmark/benchmarks/MixedDoubleArrayGenerator.java )
Calls the Native DLL until 50,000 interactions and uses JAva Double array after this.
#### Graphics
![Native Mixed - Linear](./assets/java-array-mixed-linear.svg "Mixed Array - Linear")
![Native Mixed - Log](./assets/java-array-mixed-log.svg "Mixed Array - Log")

### [Array List](./src/main/java/rafael/logistic_benchmark/benchmarks/ArrayListBenchmark.java)
Uses a new [ArrayList](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/ArrayList.html#%3Cinit%3E())
without initial size.
#### Graphics
![ArrayList - Linear](./assets/java-array-list-linear.svg "ArrayList - Linear")
![ArrayList - Log](./assets/java-array-list-log.svg "ArrayList - Log")

### [Array List with prealloced size](./src/main/java/rafael/logistic_benchmark/benchmarks/ArrayListBenchmark.java)
Uses a new [ArrayList](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/ArrayList.html#%3Cinit%3E())
without initial size.
#### Graphics
![ArrayList - Linear](./assets/java-array-list-prealloc-linear.svg "ArrayList Prealloc - Linear")
![ArrayList - Log](./assets/java-array-list-prealloc-log.svg "ArrayList Prealloc - Log")

### [Java Linked List](./src/main/java/rafael/logistic_benchmark/benchmarks/LinkedListBenchmark.java )
 Create a new [Linked List](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/LinkedList.html) 
 with initial size 0. It was the slowest execution among Java implementations. 
#### Graphics
![Linked List - Linear](./assets/java-linked-list-linear.svg "Linked List - Linear")
![Linked List - Log](./assets/java-linked-list-log.svg "Linked List - Log")


## Graphics
### General execution
![Java and C and Clojure Kotlin - Log](./assets/java_c_clojure_kotlin-log.svg)
![Java and C and Clojure Kotlin - Linear](./assets/java_c_clojure_kotlin-linear.svg)
### Until 100,000 interactions
![Java and C and Clojure Kotlin Until 100,000 - Log](./assets/java_c_clojure_kotlin-until_100,000-log.svg)
![Java and C and Clojure and Kotlin Until 100,000 - Linear](./assets/java_c_clojure_kotlin-until_100,000-linear.svg)
### Until 10,000 interactions
![Java and C and Clojure Kotlin Until 100,00 - Log](./assets/java_c_clojure_kotlin-until_10,000-log.svg)
![Java and C and Kotlin Until 10,000 - Linear](./assets/java_c_clojure_kotlin-until_10,000-linear.svg)


