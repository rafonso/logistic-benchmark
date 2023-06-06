package rafael.logistic_benchmark.benchmarks;

final class NativeDoubleArrayGenerator implements DoubleArrayGenerator {

    static final String CODE = "na";

    static {
        System.loadLibrary("GenerateSeriesNative");
    }

    private native double[] generateSeries(double x0, double r, int iter);

    @Override
    public double[] createSeries(double x0, double r, int iter) {
        return generateSeries(x0, r, iter);
    }
}
