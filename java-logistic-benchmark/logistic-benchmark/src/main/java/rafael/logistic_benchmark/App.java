package rafael.logistic_benchmark;

import java.util.Arrays;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;
import java.util.stream.LongStream;

public class App {

    record ProcessorResult(double[] series, long time) {
    }

    ProcessorResult calculate(double x0, double r, int iter) {
        double[] x = new double[iter];

        long t0 = System.currentTimeMillis();
        x[0] = x0;
        IntStream.range(1, iter).forEach(i -> x[i] = r * x[i - 1] * (1.0 - x[i - 1]));
        long time = System.currentTimeMillis() - t0;

        return new ProcessorResult(x, time);
    }

    private void simpleAction(double x0, double r, int iter, boolean showSeries) {
        var result =  calculate(x0, r, iter);

        if(showSeries){
            DoubleStream.of(result.series()).forEach(System.out::println);
        }

        System.out.println("TIME: " + result.time());
    }

    private void repeatAction(double x0, double r, int iter, int repetitions) {
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

        var average = LongStream.of(times).average().getAsDouble();

        System.out.println("AVERAGE " + average +" ms");
        System.out.println("TOTAL_TIME " + time);
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(args));

        char action = args[0].charAt(0);
        double x0 = Double.parseDouble(args[1]);
        double r = Double.parseDouble(args[2]);
        int iter = Integer.parseInt(args[3]);

        App app = new App();
        if (action == 's') {
            boolean showSeries = (args.length > 4) && (args[4].charAt(0) == 's');
            app.simpleAction(x0, r, iter, showSeries);
        } else if (action == 'r') {
            int repetitions = Integer.parseInt(args[4]);
            app.repeatAction(x0, r, iter, repetitions);
        }

    }
}
