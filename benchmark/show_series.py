import csv
import datetime
import statistics
import subprocess
import sys
import time

from commons import (LangParams, change_work_dir, get_now, print_total_time,
                     read_config)

COL_SIZE = 24
OUTPUT_DIR = "output/series"


def run_command(param: LangParams, x0: float, r: float, interations: int):
    print("[{0}] {1}".format(
        get_now(), param.name.rjust(COL_SIZE)), flush=True, end="")
    final_command = (param.command +
                     " s {} {} {} s").format(x0, r, interations)
    result = subprocess.run(final_command, shell=True, capture_output=True)

    lines = result.stdout.splitlines()
    for i in range(0, len(lines)):
        lines[i] = lines[i].decode("utf-8")

    limits = [i for i, line in enumerate(lines) if line == ("-" * 40)]
    series = lines[limits[0]+1:limits[1]]

    str_time = lines[limits[1] + 1]
    print(str_time.rjust(COL_SIZE))

    return series


def create_output(results: dict, it: int) -> list[list[str]]:
    lines = []
    languages = results.keys()
    lines.append(list(languages))
    lines[0].append("AVERAGE")
    lines[0].append("DEVIATION")

    for iteration in range(0, it):
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


def lines_to_file(x0: float, r: float, interations: int, lines: list[list[str]]):
    str_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{OUTPUT_DIR}/x0={x0}_r={r}_it={interations}_{str_now}.csv"
    with open(file_name, 'w', newline="",  encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerows(lines)
    print(f"Exporting to {file_name}")


def main():
    t0 = time.time()

    x0 = float(sys.argv[1])
    r = float(sys.argv[2])
    it = int(sys.argv[3])
    output_to_file = (len(sys.argv) > 4) and (sys.argv[4] == "f")

    change_work_dir()
    params = read_config()

    results = {}
    for param in params:
        results.update({param.name: run_command(param, x0, r, it)})

    lines = create_output(results, it)

    print()
    if(output_to_file):
        lines_to_file(x0, r, it, lines)
    else:
        lines_to_console(lines)

    print_total_time(t0)


if __name__ == '__main__':
    main()
