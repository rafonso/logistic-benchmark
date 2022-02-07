package rafael.logistic_benchmark;

import com.beust.jcommander.Parameter;
import com.beust.jcommander.validators.PositiveInteger;

public class Parameters {
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

    public Double getX0() {
        return x0;
    }

    public Double getR() {
        return r;
    }

    public Integer getInteractions() {
        return interactions;
    }

    public boolean isOutputToFile() {
        return outputToFile;
    }

    public boolean isHelp() {
        return help;
    }
}
