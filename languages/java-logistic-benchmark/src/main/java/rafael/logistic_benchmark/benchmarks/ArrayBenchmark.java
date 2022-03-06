package rafael.logistic_benchmark.benchmarks;

class ArrayBenchmark extends Benchmark {

    private final DoubleArrayGenerator generator;

    public ArrayBenchmark(DoubleArrayGenerator generator) {
        this.generator = generator;
    }

    @Override
    protected ProcessorResult calculate(double x0, double r, int iter) {
        long t0 = System.currentTimeMillis();
        double[] series = this.generator.createSeries(x0, r, iter);

        return new ProcessorResult(series, null, (System.currentTimeMillis() - t0));
    }
}
