export function calculate(x0: number, k: number, size: number): ProcessResult {
  const series = new Array<number>(size);

  const t0 = Date.now();
  series[0] = x0;
  for (let i = 1; i < size; i++) {
    series[i] = k * series[i - 1] * (1.0 - series[i - 1]);
  }
  const time = Date.now() - t0;

  return { series, time };
}

export interface ProcessResult {
  readonly series: number[];
  readonly time: number;
}
