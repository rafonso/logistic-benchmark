package rafael.logistic_benchmark;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import rafael.logistic_benchmark.code.Processor;

import java.util.stream.DoubleStream;

/**
 * Hello world!
 */
public class App {

    private static final Logger LOGGER = LoggerFactory.getLogger(App.class.getName());

    public static void main(String[] args) {

        double x0 = 0.5;
        double r = 3.9;
        int seriesSize = 1000;

        Processor processor = new Processor();

        LOGGER.info("x0 = {}, r = {}, series size = {}", x0, r, seriesSize);

        long t0 = System.currentTimeMillis();
        double[] series = processor.calculate(x0, r, seriesSize);
        long deltaT = System.currentTimeMillis() - t0;

        DoubleStream.of(series).forEach(System.out::println);
        LOGGER.info("Tempo: {} ms", deltaT);
    }
}
