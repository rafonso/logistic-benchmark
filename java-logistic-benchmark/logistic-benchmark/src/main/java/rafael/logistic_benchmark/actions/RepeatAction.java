package rafael.logistic_benchmark.actions;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import rafael.logistic_benchmark.core.Processor;
import rafael.logistic_benchmark.parameters.Parameters;

import java.util.OptionalDouble;
import java.util.stream.IntStream;
import java.util.stream.LongStream;

public class RepeatAction implements Action {

    private static final Logger LOGGER = LoggerFactory.getLogger(SimpleAction.class.getName());

    Processor processor = new Processor();

    @Override
    public void run(Parameters parameters) {
        long[] times = new long[parameters.getRepititions()];

        // warming
        processor.calculate(parameters.getX0(), parameters.getR(), parameters.getInteractions());

        long t0 = System.currentTimeMillis();
        IntStream
                .rangeClosed(1, parameters.getRepititions())
                .peek(i -> System.out.printf("\r%5d / %5d", i, parameters.getRepititions()))
                .forEach(i -> times[i - 1] = processor.calculate(parameters.getX0(), parameters.getR(), parameters.getInteractions()).time());
        long time = System.currentTimeMillis() - t0;
        System.out.println();

//        LongStream.of(times).forEach(System.out::println);
        OptionalDouble average = LongStream.of(times).average();
        LOGGER.info("AVERAGE {} ms", average.getAsDouble());
        System.out.println("TOTAL_TIME " + time);
    }
}