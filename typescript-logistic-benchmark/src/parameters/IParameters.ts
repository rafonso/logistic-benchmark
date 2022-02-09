export interface IParameters {
  // readonly action: "r" | "s";
  readonly x0: number;
  readonly r: number;
  readonly interactions: number;
  // readonly repetitions: number;
  // readonly outputToFile: boolean;
  readonly hiddenOutputSeries: boolean;
  readonly help?: boolean;
}
