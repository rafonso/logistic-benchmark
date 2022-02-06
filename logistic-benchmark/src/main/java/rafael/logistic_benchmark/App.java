package rafael.logistic_benchmark;


import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
import com.beust.jcommander.ParameterException;
import com.beust.jcommander.validators.PositiveInteger;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import rafael.logistic_benchmark.core.Processor;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
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

    @Parameter(names = {"-of"}, description = "Serie will be printed in a file")
    private boolean outputToFile = false;

    @Parameter(names = {"-h", "--help"}, description = "Show usage", help = true)
    private boolean help;

    public static void main(String[] args) {
        App app = new App();

        var jCommander = JCommander
                .newBuilder()
//                .verbose(1)
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

        if(outputToFile) {
            exportToFile(series, deltaT);
        } else {
            DoubleStream.of(series).forEach(System.out::println);
        }

        LOGGER.info("Tempo: {} ms", deltaT);
    }

    private void exportToFile(double[] series, long deltaT) {
//        LocalDateTime now = LocalDateTime.now();
        String fileName = String.format("x0=%f_r=%f_it=%d_time=%d.%tF_%<tH-%<tM-%<tS-%<tL.txt", x0, r, interactions, deltaT, LocalDateTime.now());

        Path path = Paths.get(fileName);
        try {
            Files.write(path, DoubleStream.of(series).mapToObj(Double::toString).toList());
        } catch (IOException e) {
            e.printStackTrace();
        }

        LOGGER.info("Saving to {}", fileName);
    }

}
