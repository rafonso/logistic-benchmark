package rafael.logistic_benchmark.benchmarks;

import java.util.Collection;
import java.util.Objects;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;
import java.util.stream.LongStream;

public abstract class Benchmark {

    public static Benchmark getBenchmark(String benchmarkOption) {
        return switch (benchmarkOption) {
            case JavaDoubleArrayGenerator.CODE -> new ArrayBenchmark(new JavaDoubleArrayGenerator());
            case ArrayListBenchmark.CODE -> new ArrayListBenchmark();
            case LinkedListBenchmark.CODE -> new LinkedListBenchmark();
            case PreallocArrayListBenchmark.CODE -> new PreallocArrayListBenchmark();
            default -> throw new IllegalArgumentException("Invalid benchmark option: " + benchmarkOption);
        };
    }

    protected record ProcessorResult(double[] seriesArray, Collection<Double> seriesCollection, long time) {
        double[] toArray() {
            return Objects.isNull(seriesArray)?
                    seriesCollection.stream().mapToDouble(Double::doubleValue).toArray():
                    seriesArray;
        }
    }

    protected abstract ProcessorResult calculate(double x0, double r, int iter);

    public void simpleAction(double x0, double r, int iter, boolean showSeries) {
        var result =  calculate(x0, r, iter);

        if(showSeries){
            System.out.println("-".repeat(40));
            DoubleStream.of(result.toArray()).forEach(System.out::println);
            System.out.println("-".repeat(40));
        }

        System.out.println("TIME: " + result.time() +" ms");
    }

    public void repeatAction(double x0, double r, int iter, int repetitions) {
        long[] times = new long[repetitions];

        // warming
        calculate(x0, r, iter);

        long t0 = System.currentTimeMillis();
        IntStream
                .rangeClosed(1, repetitions)
                .peek(i -> System.out.printf("\r%5d / %5d", i, repetitions))
                .forEach(i -> times[i - 1] = calculate(x0, r, iter).time());
        long time = System.currentTimeMillis() - t0;
        System.out.println();

        @SuppressWarnings("OptionalGetWithoutIsPresent")
        var average = LongStream.of(times).average().getAsDouble();

        System.out.println("AVERAGE " + average +" ms");
        System.out.println("TOTAL_TIME " + time);
    }
}
