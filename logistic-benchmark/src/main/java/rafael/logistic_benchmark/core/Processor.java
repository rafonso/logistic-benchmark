package rafael.logistic_benchmark.core;

import java.util.stream.IntStream;

public class Processor {

    public ProcessorResult calculate(double x0, double k, int size) {
        double[] x = new double[size];

        long t0 = System.currentTimeMillis();
        x[0] = x0;
        IntStream.range(1, size).forEach(i -> x[i] = k * x[i - 1] * (1.0 - x[i - 1]));
        long time = System.currentTimeMillis() - t0;

        return new ProcessorResult(x, time);
    }

}
