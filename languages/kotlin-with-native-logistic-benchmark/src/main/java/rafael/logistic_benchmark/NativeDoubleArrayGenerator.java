package rafael.logistic_benchmark;

import java.io.File;

final class NativeDoubleArrayGenerator {

    static {
        File currentDir = new File(".");
        System.out.println(currentDir.getAbsolutePath());
        System.loadLibrary("GenerateSeriesNative");
    }

    native double[] generateSeries(double x0, double r, int iter);

}
