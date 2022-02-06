package rafael.logistic_benchmark;

import com.beust.jcommander.IParameterValidator;
import com.beust.jcommander.ParameterException;

public class X0Validator implements IParameterValidator {
    @Override
    public void validate(String name, String value) throws ParameterException {
        try {
            double x0 = Double.parseDouble(value);

            if (x0 < 0.0 || x0 > 1.0) {
                throw new ParameterException("x0 should be between 0.0 and 1.0: " + value);
            }
        } catch (NumberFormatException e) {
            throw new ParameterException("x0 not numeric: " + value);
        }
    }
}
