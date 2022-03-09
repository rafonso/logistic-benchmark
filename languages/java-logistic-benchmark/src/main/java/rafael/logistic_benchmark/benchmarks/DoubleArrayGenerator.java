package rafael.logistic_benchmark.benchmarks;

sealed interface DoubleArrayGenerator permits JavaDoubleArrayGenerator, MixedDoubleArrayGenerator, NativeDoubleArrayGenerator {

    double[] createSeries(double x0, double r, int iter);

}
