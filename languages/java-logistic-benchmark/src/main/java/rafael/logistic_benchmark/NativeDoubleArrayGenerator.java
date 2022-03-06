package rafael.logistic_benchmark;

final class NativeDoubleArrayGenerator implements DoubleArrayGenerator {

    private native double[] generateSeries(double x0, double r, int iter);

    @Override
    public double[] createSeries(double x0, double r, int iter) {
        return generateSeries(x0, r, iter);
    }
}
