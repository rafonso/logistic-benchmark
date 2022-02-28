package rafael.logistic_benchmark;

public class App {

    private static Benchmark getBenchmark(char option) {
        switch (option) {
            case 'a':
                return new ArrayBenchmark();
            case 'l':
                return new ListBenchmark();
            default:
                throw new IllegalArgumentException("Invalid benchmark option: " + option);
        }
    }

    public static void main(String[] args) {
        char option = args[0].charAt(0);
        char action = args[1].charAt(0);
        double x0 = Double.parseDouble(args[2]);
        double r = Double.parseDouble(args[3]);
        int iter = Integer.parseInt(args[4]);

        Benchmark benchmark = getBenchmark(option);
        if (action == 's') {
            boolean showSeries = (args.length > 5) && (args[5].charAt(0) == 's');
            benchmark.simpleAction(x0, r, iter, showSeries);
        } else if (action == 'r') {
            int repetitions = Integer.parseInt(args[5]);
            benchmark.repeatAction(x0, r, iter, repetitions);
        }

    }
}
