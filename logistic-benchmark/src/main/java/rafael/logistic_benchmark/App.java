package rafael.logistic_benchmark;


import com.beust.jcommander.JCommander;
import com.beust.jcommander.ParameterException;
import rafael.logistic_benchmark.actions.Action;
import rafael.logistic_benchmark.actions.RepeatAction;
import rafael.logistic_benchmark.actions.SimpleAction;
import rafael.logistic_benchmark.parameters.Parameters;

public class App {

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
                Action action = params.getAction().equals("r") ? new RepeatAction() : new SimpleAction();

                action.run(params);
            }
        } catch (ParameterException pe) {
            pe.printStackTrace();
            System.err.println(pe.getMessage());
            jCommander.usage();
        }

    }
}
