import { parse } from "ts-command-line-args";

import { SimpleAction } from "./actions/SimpleAction";
import { IParameters } from "./parameters/IParameters";
import { RepeatAction } from './actions/RepeatAction';

export const params = parse<IParameters>(
  {
    action: {
      type: String,
      description: "Action: s = Single, r = Repeat",
    },
    x0: { type: Number, description: "Initial x value" },
    r: { type: Number, description: "r value" },
    interactions: {
      type: Number,
      alias: "i",
      description: "Interactions to generate the series",
    },
    repetitions: {
      type: Number,
      defaultValue: 1,
      optional: true,
      description:
        "How many times the series is repeated (if action if repeat)",
    },
    //  outputToFile: { type: Boolean, optional: true, alias: 'hos', description: 'Series will be hidden in a console' , },
    hiddenOutputSeries: {
      type: Boolean,
      // alias: "of",
      description: "Series will be printed in a file",
    },
    help: {
      type: Boolean,
      optional: true,
      alias: "h",
      description: "Prints this usage guide",
    },
  },
  { helpArg: "help" }
);


console.log(params);

const action = (params.action === "s")? new SimpleAction(): ((params.action === "r")? new RepeatAction(): null);

if(action) action.run(params);
