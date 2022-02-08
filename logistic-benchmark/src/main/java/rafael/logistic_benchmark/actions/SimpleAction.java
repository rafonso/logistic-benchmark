package rafael.logistic_benchmark.actions;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import rafael.logistic_benchmark.core.Processor;
import rafael.logistic_benchmark.core.ProcessorResult;
import rafael.logistic_benchmark.parameters.Parameters;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.stream.DoubleStream;

public class SimpleAction implements Action {
    private static final Logger LOGGER = LoggerFactory.getLogger(SimpleAction.class.getName());

    Processor processor = new Processor();

    private void exportToFile(Parameters params, ProcessorResult result) {
        String fileName = String.format("x0=%f_r=%f_it=%d_time=%d.%tF_%<tH-%<tM-%<tS-%<tL.txt", params.getX0(), params.getR(), params.getInteractions(), result.time(), LocalDateTime.now());

        Path path = Paths.get(fileName);
        try {
            Files.write(path, DoubleStream.of(result.series()).mapToObj(Double::toString).toList());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        LOGGER.info("Saving to {}", fileName);
    }


    @Override
    public void run(Parameters params) {
        var result =  processor.calculate(params.getX0(), params.getR(), params.getInteractions());

        if (params.isOutputToFile()) {
            exportToFile(params, result);
        }

        if(!params.isHiddenOutputSeries()){
            DoubleStream.of(result.series()).forEach(System.out::println);
        }

        LOGGER.info("Tempo: {} ms", result.time());
    }
}
