
interface ProcessResult {
  readonly series: number[];
  readonly time: number;
}

function calculate(x0: number, k: number, size: number): ProcessResult {
  const series = new Array<number>(size);

  const t0 = Date.now();
  series[0] = x0;
  for (let i = 1; i < size; i++) {
    series[i] = k * series[i - 1] * (1.0 - series[i - 1]);
  }
  const time = Date.now() - t0;

  return { series, time };
}

export function simpleAction(x0: number, r: number, interactions: number, showSeries: boolean): void {
  const result = calculate(x0, r, interactions);

  if (showSeries) {
    console.log("-".repeat(40))
    result.series.forEach((x) => console.log(x.toString()));
    console.log("-".repeat(40))
  }

  console.log(`TIME: ${result.time} ms`);
}
 
export function repeatAction(x0: number, r: number, interactions: number, repetitions: number): void {
  const times = new Array<number>(repetitions);

  const t0 = Date.now();
  for (let i = 0; i < repetitions; i++) {
    Deno.writeAllSync(Deno.stdout, new TextEncoder().encode(`\r${i + 1}\t/\t${repetitions}`));
    times[i] = calculate(x0, r, interactions).time;
  }
  const time = Date.now() - t0;
  console.log();

  const average = times.reduce((a, b) => a + b, 0) / repetitions;

  console.log(`AVERAGE ${average} ms`);
  console.log(`TOTAL_TIME ${time}`)
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
  simpleAction(x0, r, iter, showSeries);
} else if(action === "r") {
  const repetitions = parseInt(Deno.args[4]);
  repeatAction(x0, r, iter, repetitions);
}
