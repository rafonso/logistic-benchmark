
export interface IConsole {
  println(...str: string[]): void;
  print(...str: string[]): void;
}

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

export function simpleAction(x0: number, r: number, interactions: number, showSeries: boolean, console: IConsole): void {
  const result = calculate(x0, r, interactions);

  if (showSeries) {
    console.println("-".repeat(40))
    result.series.forEach((x) => console.println(x.toString()));
    console.println("-".repeat(40))
  }

  console.println(`TIME: ${result.time} ms`);
}
 
export function repeatAction(x0: number, r: number, interactions: number, repetitions: number, console: IConsole): void {
  const times = new Array<number>(repetitions);

  const t0 = Date.now();
  for (let i = 0; i < repetitions; i++) {
    console.print(`\r${i + 1}\t/\t${repetitions}`);
    times[i] = calculate(x0, r, interactions).time;
  }
  const time = Date.now() - t0;
  console.println();

  const average = times.reduce((a, b) => a + b, 0) / repetitions;

  console.println(`AVERAGE ${average} ms`);
  console.println(`TOTAL_TIME ${time}`)
}