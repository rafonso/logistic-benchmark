package rafael.logistic_benchmark.benchmarks;

sealed interface DoubleArrayGenerator permits JavaDoubleArrayGenerator, NativeDoubleArrayGenerator {

    double[] createSeries(double x0, double r, int iter);

}
