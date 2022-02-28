package rafael.logistic_benchmark;

import java.util.stream.IntStream;

public class ArrayBenchmark extends Benchmark {
    @Override
    protected ProcessorResult calculate(double x0, double r, int iter) {
        double[] series = new double[iter];

        long t0 = System.currentTimeMillis();
        series[0] = x0;
        IntStream.range(1, iter).forEach(i -> series[i] = r * series[i - 1] * (1.0 - series[i - 1]));
        long time = System.currentTimeMillis() - t0;

        return new ProcessorResult(series, null, time);
    }
}
