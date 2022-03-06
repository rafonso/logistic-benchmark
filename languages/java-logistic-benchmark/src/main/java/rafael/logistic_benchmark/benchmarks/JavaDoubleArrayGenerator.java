package rafael.logistic_benchmark.benchmarks;

import java.util.stream.IntStream;

final public class JavaDoubleArrayGenerator implements DoubleArrayGenerator {

    static final String CODE = "ar";

    @Override
    public double[] createSeries(double x0, double r, int iter) {
        double[] series = new double[iter];

        series[0] = x0;
        IntStream.range(1, iter)
                .forEach(i -> series[i] = r * series[i - 1] * (1.0 - series[i - 1]));

        return series;
    }
}
