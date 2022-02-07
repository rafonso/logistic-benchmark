package rafael.logistic_benchmark;


import com.beust.jcommander.JCommander;
import com.beust.jcommander.ParameterException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import rafael.logistic_benchmark.actions.Action;
import rafael.logistic_benchmark.actions.RepeatAction;
import rafael.logistic_benchmark.core.Processor;
import rafael.logistic_benchmark.parameters.Parameters;

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


    public static void main(String[] args) {
        Parameters params = new Parameters();


        var jCommander = JCommander
                .newBuilder()
                .addObject(params)
                .build();
        try {
            jCommander.parse(args);
            if (params.isHelp()) {
                jCommander.usage();
            } else {
                Action action = new RepeatAction();

                action.run(params);

//                App app = new App();
//                app.run(params);
            }
        } catch (ParameterException pe) {
            pe.printStackTrace();
            System.err.println(pe.getMessage());
            jCommander.usage();
        }

    }

    public void run(Parameters params) {
        Processor processor = new Processor();

        LOGGER.info("x0 = {}, r = {}, series size = {}", params.getX0(), params.getR(), params.getInteractions());



        long t0 = System.currentTimeMillis();
        double[] series = processor.calculate(params.getX0(), params.getR(), params.getInteractions());
        long deltaT = System.currentTimeMillis() - t0;

        if (params.isOutputToFile()) {
            exportToFile(params, series, deltaT);
        } else {
            DoubleStream.of(series).forEach(System.out::println);
        }

        LOGGER.info("Tempo: {} ms", deltaT);
    }

    private void exportToFile(Parameters params, double[] series, long deltaT) {
        String fileName = String.format("x0=%f_r=%f_it=%d_time=%d.%tF_%<tH-%<tM-%<tS-%<tL.txt", params.getX0(), params.getR(), params.getInteractions(), deltaT, LocalDateTime.now());

        Path path = Paths.get(fileName);
        try {
            Files.write(path, DoubleStream.of(series).mapToObj(Double::toString).toList());
        } catch (IOException e) {
            e.printStackTrace();
        }

        LOGGER.info("Saving to {}", fileName);
    }

}
