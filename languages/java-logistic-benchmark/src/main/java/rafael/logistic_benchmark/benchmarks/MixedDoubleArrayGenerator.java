package rafael.logistic_benchmark.benchmarks;

public final class MixedDoubleArrayGenerator implements DoubleArrayGenerator {

    static final String CODE = "ma";

    private static final int MAX_NATIVE = 50_000;

    private final DoubleArrayGenerator javaGenerator = new JavaDoubleArrayGenerator();
    private final DoubleArrayGenerator nativeGenerator = new NativeDoubleArrayGenerator();

    @Override
    public double[] createSeries(double x0, double r, int iter) {
        var generator = (iter < MAX_NATIVE) ? nativeGenerator : javaGenerator;

        return generator.createSeries(x0, r, iter);
    }
}
