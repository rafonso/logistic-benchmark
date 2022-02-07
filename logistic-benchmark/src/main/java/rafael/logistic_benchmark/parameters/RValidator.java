package rafael.logistic_benchmark.parameters;

import com.beust.jcommander.IParameterValidator;
import com.beust.jcommander.ParameterException;

public class RValidator implements IParameterValidator {
    @Override
    public void validate(String name, String value) throws ParameterException {
        try {
            double r = Double.parseDouble(value);

            if (r < 0.0 || r > 4.0) {
                throw new ParameterException("r should be between 0.0 and 4.0: " + value);
            }
        } catch (NumberFormatException e) {
            throw new ParameterException("r not numeric: " + value);
        }
    }
}
