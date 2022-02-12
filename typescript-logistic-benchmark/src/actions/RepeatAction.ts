import { calculate } from '../core';
import { IParameters } from '../parameters/IParameters';
import { Action } from './IAction';

export class RepeatAction implements Action {
  run(params: IParameters): void {
    if (params.repetitions) {
      const times = new Array<number>(params.repetitions);

      for (let i = 0; i < params.repetitions; i++) {
        process.stdout.write(`\r${i + 1}\t/\t${params.repetitions}`);
        times[i] = calculate(params.x0, params.r, params.interactions).time;
      }
      process.stdout.write("\n");

      const average = times.reduce((a, b) => a + b, 0) / params.repetitions;

      console.log("AVERAGE", average, "ms");
    } else {
      throw new Error("Repetitions not defined!");
    }
  }
}
