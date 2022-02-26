import { IConsole, repeatAction, simpleAction } from "./common";

const nodeConsole: IConsole = {
  print: (...str: string[]) => {
    process.stdout.write(str.join(" "));
  },
  println: (...str: string[]) => {
    console.log(str.join(" "));
  }
}


/************************************
 * MAIN
 ************************************/

const action = process.argv[2];
const x0 = parseFloat(process.argv[3]);
const r =  parseFloat(process.argv[4]);
const iter = parseInt(process.argv[5]);

if(action === "s") {
  const showSeries = (process.argv.length === 7) && (process.argv[6] === "s");
  simpleAction(x0, r, iter, showSeries, nodeConsole);
} else if(action === "r") {
  const repetitions = parseInt(process.argv[6]);
  repeatAction(x0, r, iter, repetitions, nodeConsole);
}
