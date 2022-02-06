package rafael.logistic_benchmark;


import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
import com.beust.jcommander.ParameterException;
import com.beust.jcommander.validators.PositiveInteger;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import rafael.logistic_benchmark.code.Processor;

import java.util.stream.DoubleStream;

/**
 * Hello world!
 */
public class App {
    private static final Logger LOGGER = LoggerFactory.getLogger(App.class.getName());

    @Parameter(names = {"-x0"}, description = "Initial x value", required = true, validateWith = X0Validator.class)
    private Double x0;

    @Parameter(names = {"-r"}, description = "r value", required = true, validateWith = RValidator.class)
    private Double r;

    @Parameter(names = {"-it"}, description = "Interactions to generate the series", required = true, validateWith = PositiveInteger.class)
    private Integer interactions;

    @Parameter(names = {"-h", "--help"}, description = "Show usage", help = true)
    private boolean help;

    public static void main(String[] args) {
        App app = new App();

        var jCommander = JCommander
                .newBuilder()
                .addObject(app)
                .build();
        try {
            jCommander.parse(args);
            if (app.help) {
                jCommander.usage();
            } else {
                app.run();
            }
        } catch (ParameterException pe) {
            System.err.println(pe.getMessage());
            jCommander.usage();
        }

    }

    public void run() {
        Processor processor = new Processor();

        LOGGER.info("x0 = {}, r = {}, series size = {}", x0, r, interactions);

        long t0 = System.currentTimeMillis();
        double[] series = processor.calculate(x0, r, interactions);
        long deltaT = System.currentTimeMillis() - t0;

        LOGGER.info("Tempo: {} ms", deltaT);
    }

}
