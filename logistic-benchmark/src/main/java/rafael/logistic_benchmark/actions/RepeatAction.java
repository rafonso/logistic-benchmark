package rafael.logistic_benchmark.actions;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import rafael.logistic_benchmark.core.Processor;
import rafael.logistic_benchmark.parameters.Parameters;

import java.util.stream.IntStream;
import java.util.stream.LongStream;

public class RepeatAction implements Action {

    private static final Logger LOGGER = LoggerFactory.getLogger(SimpleAction.class.getName());

    Processor processor = new Processor();

    private long calculateSeries(Parameters params) {
        long t0 = System.currentTimeMillis();
        double[] series = processor.calculate(params.getX0(), params.getR(), params.getInteractions());

        return System.currentTimeMillis() - t0;
    }

    @Override
    public void run(Parameters parameters) {
        long[] times = new long[parameters.getRepititions()];

        // warming
        calculateSeries(parameters);

        IntStream
                .rangeClosed(1, parameters.getRepititions())
                .peek(i -> System.out.print('.'))
                .forEach(i -> times[i - 1] = calculateSeries(parameters));
        System.out.println();

        LongStream.of(times).forEach(System.out::println);
        System.out.println(LongStream.of(times).average());
    }
}
