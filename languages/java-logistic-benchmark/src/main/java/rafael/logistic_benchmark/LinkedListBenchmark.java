package rafael.logistic_benchmark;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class LinkedListBenchmark extends Benchmark {
    @Override
    protected ProcessorResult calculate(double x0, double r, int iter) {
        List<Double> series = new LinkedList<>();

        long t0 = System.currentTimeMillis();
        double x = x0;
        for (int i = 0; i < iter; i++) {
            series.add(x);
            x = r * x * (1.0 - x);
        }
        long time = System.currentTimeMillis() - t0;

        return new ProcessorResult(null, series, time);
    }
}
