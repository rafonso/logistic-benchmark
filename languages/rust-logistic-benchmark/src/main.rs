use instant::Instant;
use std::env;

fn calculate(x0: f64, r: f64, it: i32) -> (std::vec::Vec<f64>, u128) {
    let mut x: Vec<f64> = Vec::with_capacity(it as usize);
    let mut last_x = x0;
    let t0 = Instant::now();
    x.push(x0);
    for _i in 1..it {
        last_x = r * last_x * (1.0 - last_x);
        x.push(last_x);
    }
    let delta_t = t0.elapsed().as_millis();

    return (x, delta_t);
}

fn simple_action(x0: f64, r: f64, it: i32, show_output: bool) {
    let (series, delta_t) = calculate(x0, r, it);

    if show_output {
        let break_line: String = "-".repeat(40);
        println!("{}", break_line);
        series.into_iter().for_each(|x| println!("{}", x));
        println!("{}", break_line);
    }

    println!("TIME: {} ms", delta_t);
}

fn repeat_action(x0: f64, r: f64, it: i32, rep: i32) {
    let mut times: Vec<u128> = Vec::with_capacity(rep as usize);
    let t0 = Instant::now();
    for i in 0..rep {
        print!("\r{:04}/{:04}", (i + 1), rep);
        times.push(calculate(x0, r, it).1);
    }
    let delta_t = t0.elapsed().as_millis();
    println!();

    let average = times
        .into_iter()
        .reduce(|a, b| a + b)
        .map(|sum| sum / rep as u128);

    println!("AVERAGE: {:?} ms", average);
    println!("TOTAL_TIME {:?}", delta_t);
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let action: char = args[1].chars().nth(0).unwrap();
    let x0: f64 = args[2].parse::<f64>().unwrap();
    let r: f64 = args[3].parse::<f64>().unwrap();
    let it: i32 = args[4].parse::<i32>().unwrap();

    if action == 's' {
        let show_output = (args.len() == 6) && (args[5].chars().nth(0).unwrap() == 's');
        simple_action(x0, r, it, show_output);
    } else if action == 'r' {
        let repetitions = args[5].parse::<i32>().unwrap();
        repeat_action(x0, r, it, repetitions);
    }
}
