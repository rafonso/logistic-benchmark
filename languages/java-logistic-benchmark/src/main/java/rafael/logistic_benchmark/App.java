package rafael.logistic_benchmark;

public class App {

    private static Benchmark getBenchmark(String benchmarkOption) {
        switch (benchmarkOption) {
            case "ar":
                return new ArrayBenchmark();
            case "al":
                return new ArrayListBenchmark();
            case "ll":
                return new LinkedListBenchmark();
            case "pa":
                return new PreallocArrayListBenchmark();
            default:
                throw new IllegalArgumentException("Invalid benchmark option: " + benchmarkOption);
        }
    }

    public static void main(String[] args) {
        String benchmarkOption = args[0];
        char action = args[1].charAt(0);
        double x0 = Double.parseDouble(args[2]);
        double r = Double.parseDouble(args[3]);
        int iter = Integer.parseInt(args[4]);

        Benchmark benchmark = getBenchmark(benchmarkOption);
        if (action == 's') {
            boolean showSeries = (args.length > 5) && (args[5].charAt(0) == 's');
            benchmark.simpleAction(x0, r, iter, showSeries);
        } else if (action == 'r') {
            int repetitions = Integer.parseInt(args[5]);
            benchmark.repeatAction(x0, r, iter, repetitions);
        }

    }
}
