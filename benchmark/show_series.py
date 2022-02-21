import argparse
import csv
import datetime
import statistics
import subprocess
import time

from commons import (LangParams, change_work_dir, get_now, print_total_time,
                     read_config)

COL_SIZE = 24
OUTPUT_DIR = "output/series"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Creates a benchmark"
    )
    parser.add_argument("x0", help="first value of series", type=float)
    parser.add_argument("r", help="R value", type=float)
    parser.add_argument(
        "iter", help="Number of Interactions to each series. The series size.", type=int)
    parser.add_argument("-f", help="export the series to a CSV file",
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    if not 0.0 <= args.x0 <= 1.0:
        parser.error("x0 must be between 0.0 and 1.0")
    if not 0.0 <= args.r <= 4.0:
        parser.error("r must be between 0.0 and 4.0")
    if args.iter <= 0:
        parser.error("iter must be a positive number")

    return args

def run_command(param: LangParams, args: argparse.Namespace):
    print("[{0}] {1}".format(
        get_now(), param.name.rjust(COL_SIZE)), flush=True, end="")
    final_command = (param.command +
                     " s {} {} {} s").format(args.x0, args.r, args.iter)
    result = subprocess.run(final_command, shell=True, capture_output=True)

    lines = result.stdout.splitlines()
    for i in range(0, len(lines)):
        lines[i] = lines[i].decode("utf-8")

    limits = [i for i, line in enumerate(lines) if line == ("-" * 40)]
    series = lines[limits[0]+1:limits[1]]

    str_time = lines[limits[1] + 1]
    print(str_time.rjust(COL_SIZE))

    return series


def create_output(results: dict, iter: int) -> list[list[str]]:
    lines = []
    languages = results.keys()
    lines.append(list(languages))
    lines[0].append("AVERAGE")
    lines[0].append("DEVIATION")

    for iteration in range(0, iter):
        iteration_values = []
        for language in languages:
            iteration_values.append(float(results.get(language)[iteration]))
        iteration_values.append(statistics.mean(iteration_values))
        iteration_values.append(statistics.stdev(iteration_values))
        lines.append(iteration_values)

    return lines


def lines_to_console(lines: list[list[str]]):
    for line in lines:
        for item in line:
            print(str(item).ljust(COL_SIZE), flush=True, end="")
        print()


def lines_to_file(args: argparse.Namespace, lines: list[list[str]]):
    str_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{OUTPUT_DIR}/x0={args.x0}_r={args.r}_it={args.iter}_{str_now}.csv"
    with open(file_name, 'w', newline="",  encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerows(lines)
    print(f"Exporting to {file_name}")


def main():
    t0 = time.time()

    args = parse_args()

    change_work_dir()
    params = read_config()

    results = {}
    for param in params:
        results.update({param.name: run_command(param, args)})

    lines = create_output(results, args.iter)

    print()
    if(args.f):
        lines_to_file(args, lines)
    else:
        lines_to_console(lines)

    print_total_time(t0)


if __name__ == '__main__':
    main()
