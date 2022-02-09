import { calculate } from "./core/index";
import { parse } from "ts-command-line-args";
import { IParameters } from "./parameters/IParameters";

export const params = parse<IParameters>(
  {
    // action: {type: String, alias: "ac", description: "Action: s = Single, r = Repeat"},
    x0: { type: Number, description: "Initial x value" },
    r: { type: Number, description: "r value" },
    interactions: {
      type: Number,
      alias: "i",
      description: "Interactions to generate the series",
    },
    // repititions: {type: Number, alias: "re", description : "How many times the series is repeated (if action if repeat)"},
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

const result = calculate(params.x0, params.r, params.interactions);

if (!params.hiddenOutputSeries) {
  result.series.forEach((x) => console.log(x));
}
console.log("----------------");
console.log("TIME: ", result.time, "ms");

console.log(params);
