import { calculate } from "../core";
import { IParameters } from "../parameters/IParameters";
import { Action } from "./IAction";

export class SimpleAction implements Action {

  run(params: IParameters): void {
    const result = calculate(params.x0, params.r, params.interactions);

    if (!params.hiddenOutputSeries) {
      result.series.forEach((x) => console.log(x));
    }

    console.log("TIME: ", result.time, "ms");
  }
}
