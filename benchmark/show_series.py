import argparse
import csv
import statistics
import subprocess
import time

from tabulate import tabulate

from commons import (LangParams, UserParams, change_work_dir, get_now,
                     now_to_str, print_total_time, read_config)


class SeriesParams(UserParams):
    def __init__(self, x0: float, r: float, languages: list[str] = [], languages_to_skip: list[str] = [], export_to_file: bool = False, iter: int = 0):
        UserParams.__init__(self, x0, r, languages,
                            languages_to_skip, export_to_file)
        self.iter = iter


class SeriesResult:
    def __init__(self, iter: int):
        self.lang_series: dict[str, list[float]] = {}
        self.iter = iter

    def calculate_average(self):
        if len(self.lang_series) == 1:
            return
        results = self.get_results()
        average: list[float] = []
        deviation: list[float] = []
        for i in range(1, self.iter + 1):
            average.append(statistics.mean(results[i]))
            deviation.append(statistics.stdev(results[i]))
        self.lang_series["AVERAGE"] = average
        self.lang_series["DEVIATION"] = deviation

    def get_results(self):
        header = []
        for name in self.lang_series.keys():
            header.append(name)

        result = [header]
        for i in range(0, self.iter):
            line = []
            for series in self.lang_series.values():
                line.append(series[i])
            result.append(line)

        return result


COL_SIZE = 24
OUTPUT_DIR = "output/series"


def parse_args() -> SeriesParams:
    parser = argparse.ArgumentParser(
        description="Creates a benchmark"
    )
    parser.add_argument("x0", help="first value of series", type=float)
    parser.add_argument("r", help="R value", type=float)
    parser.add_argument(
        "iter", help="Number of Interactions to each series. The series size.", type=int)
    parser.add_argument("-l", "--languages", nargs="*",
                        help="Codes of Languages to be executed")
    parser.add_argument("-s", "--languages-to-skip", nargs="*",
                        help="Codes of Languages to be skipped")
    parser.add_argument("-f", help="export the series to a CSV file",
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    if not 0.0 <= args.x0 <= 1.0:
        parser.error("x0 must be between 0.0 and 1.0")
    if not 0.0 <= args.r <= 4.0:
        parser.error("r must be between 0.0 and 4.0")
    if args.iter <= 0:
        parser.error("iter must be a positive number")

    return SeriesParams(x0=args.x0, r=args.r, iter=args.iter, languages=args.languages, languages_to_skip=args.languages_to_skip, export_to_file=args.f)


def run_command(param: LangParams, user_params: SeriesParams):
    print("[{0}] {1}".format(
        get_now(), param.name.rjust(COL_SIZE)), flush=True, end="")
    final_command = (param.command +
                     " s {} {} {} s").format(user_params.x0, user_params.r, user_params.iter)
    result = subprocess.run(final_command, shell=True, capture_output=True)

    lines = result.stdout.splitlines()
    for i in range(0, len(lines)):
        lines[i] = lines[i].decode("utf-8")

    limits = [i for i, line in enumerate(lines) if line == ("-" * 40)]
    series = lines[limits[0]+1:limits[1]]

    str_time = lines[limits[1] + 1]
    print(str_time.rjust(COL_SIZE))

    return list(map(lambda x: float(x), series))


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


def lines_to_console(results: SeriesResult):
    print(tabulate(results.get_results(), headers="firstrow", tablefmt="psql", floatfmt=".18f"))


def lines_to_file(user_params: SeriesParams, results: SeriesResult):
    file_name = f"{OUTPUT_DIR}/x0={user_params.x0}_r={user_params.r}_it={user_params.iter}_{now_to_str()}.csv"
    with open(file_name, 'w', newline="",  encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerows(results.get_results())
    print("-" * 80)
    print(f"[{get_now()}] Exporting to {file_name}")


def main():
    t0 = time.time()

    user_params = parse_args()

    change_work_dir()
    lang_params = read_config(user_params)

    results = SeriesResult(user_params.iter)

    for param in lang_params:
        results.lang_series[param.name] = run_command(param, user_params)

    results.calculate_average()

    if(user_params.export_to_file):
        lines_to_file(user_params, results)
    else:
        lines_to_console(results)

    print_total_time(t0)


if __name__ == '__main__':
    main()
