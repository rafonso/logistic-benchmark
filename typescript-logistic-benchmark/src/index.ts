import { calculate } from './core/index';


const x0 = 0.1;
const r = 3.91;
const iterations = 200000;

const result = calculate(x0, r, iterations);

//result.series.forEach(x => console.log(x));
console.log("----------------")
console.log("TIME: ", result.time, "ms");


