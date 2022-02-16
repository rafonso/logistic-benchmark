use instant::Instant;
use std::env;

fn calculate<const IT: usize>(x0: f64, r: f64) -> ([f64; IT], u128){
    let mut x: [f64; IT] = [0.0; IT];
    let t0 = Instant::now();
    x[0] = x0;
    for i in 1..IT {
        x[i] = r * x[i - 1] * (1.0 - x[i - 1]);
    }
    let delta_t = t0.elapsed().as_millis();

    return (x, delta_t);
}

fn simple_action<const IT: usize>(x0: f64, r: f64, show_output: bool) {
    let (series, delta_t) = calculate::<IT>(x0, r);

    if show_output {
        let break_line: String = "-".repeat(40);
        println!("{}", break_line);
        for x in series {
            println!("{}", x);
        }
        println!("{}", break_line);
    }

    println!("TIME: {} ms", delta_t);
}

fn repeat_action<const IT: usize, const REP: usize>(x0: f64, r: f64) {
    let mut times : [u128; REP] = [0; REP];

    let t0 = Instant::now();
    for i in 0..REP {
        print!("\r{:?} / {:?}", (i + 1), REP);
        times[i] = calculate::<IT>(x0, r).1;
    }
    let delta_t = t0.elapsed().as_millis();
    println!();

    let mut sum = 0;
    for time in times {
        sum += time;
    }
    let average = sum / (REP as u128);

    println!("AVERAGE: {:?} ms", average);
    println!("TOTAL_TIME {:?}", delta_t);
}

fn main() {
    let args: Vec<String> = env::args().collect();

    println!("ARGS {:?}", args);

    let action: char = args[1].chars().nth(0).unwrap();
    let x0: f64 = args[2].parse::<f64>().unwrap();
    let r: f64 = args[3].parse::<f64>().unwrap();
    const IT: usize = 100; //args[4].parse::<usize>().unwrap();

    println!("MAX {:?}", usize::MAX);

    if action == 's' {
        let show_output = true;
        simple_action::<IT>(x0, r, show_output);
    } else if action == 'r' {
        const REP: usize = 100;
        repeat_action::<IT, REP>(x0, r);
    }
}
