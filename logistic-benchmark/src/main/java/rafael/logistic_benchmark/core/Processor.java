package rafael.logistic_benchmark.core;

import java.util.stream.IntStream;

public class Processor {

    public double[] calculate(double x0, double k, int size) {
        double[] x = new double[size];
        x[0] = x0;

        IntStream.range(1, size).forEach(i -> x[i] = k * x[i - 1] * (1.0 - x[i - 1]));

        return x;
    }

}
