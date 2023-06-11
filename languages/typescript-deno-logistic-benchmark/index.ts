import { IConsole, repeatAction, simpleAction } from './common.ts';

const denoConsole: IConsole = {
  print: (...str: string[]) => {
    Deno.writeAllSync(Deno.stdout, new TextEncoder().encode(str.join(" ")));
  },
  println: (...str: string[]) => {
    Deno.writeAllSync(Deno.stdout, new TextEncoder().encode(str.join(" ")));
    console.log();
  }
}

/************************************
 * MAIN
 ************************************/

const action =        Deno.args[0];
const x0 = parseFloat(Deno.args[1]);
const r =  parseFloat(Deno.args[2]);
const iter = parseInt(Deno.args[3]);

if(action === "s") {
  const showSeries = (Deno.args.length === 5) && (Deno.args[4] === "s");
  simpleAction(x0, r, iter, showSeries, denoConsole);
} else if(action === "r") {
  const repetitions = parseInt(Deno.args[4]);
  repeatAction(x0, r, iter, repetitions, denoConsole);
}
