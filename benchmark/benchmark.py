import argparse
import csv
import math
import os
import random
import re
import subprocess
import sys
import time
from dataclasses import InitVar, dataclass, field

import matplotlib.pyplot as plt
from tabulate import tabulate

from commons import (OUTPUT_DIR, LangParams, UserParams, change_work_dir, log,
                     now_to_str, print_total_time, read_config)


@dataclass
class BenchmarkParams(UserParams):
    repetitions: int = 0
    export_to_plot: bool = False
    min_iterations: int = 0
    max_iterations: int = sys.maxsize
    graphic_scale_type: str = "log"
    graphic_file_extension: str = "png"
    show_command: bool = False,
    show_code: bool = False

    def is_linear_plotting(self):
        return (self.graphic_scale_type == "both") or (self.graphic_scale_type == "linear")

    def is_log_plotting(self):
        return (self.graphic_scale_type == "both") or (self.graphic_scale_type == "log")


@dataclass
class LangResults:
    color: str
    line_style: str
    times: list[int] = field(default_factory=list)


@dataclass
class BenchmarkResults:
    lang_params: InitVar[list[LangParams]]
    interactions: list[int]
    results: dict[str, LangResults] = field(init=False)

    def __post_init__(self, lang_params: list[LangParams]):
        self.results = {}
        for lang_param in lang_params:
            self.results[lang_param.name] = LangResults(
                lang_param.color, lang_param.linestyle)

    def get_results(self):
        header = ["Iter"]
        for name in self.results.keys():
            header.append(name)

        result = [header]
        for i, iter in enumerate(self.interactions):
            line = [str(iter)]
            for lang_result in self.results.values():
                line.append(str(lang_result.times[i]))
            result.append(line)

        return result


COL_SIZE = 11
CODE_COL_SIZE = 20
COMMAND_COL_SIZE = 240
TIME_RE = 'TOTAL_TIME (\d+)'
BENCHMARK_DIR = f"{OUTPUT_DIR}/benchmark"
PLOTS_DIR = f"{BENCHMARK_DIR}/plots"
REPORTS_DIR = f"{BENCHMARK_DIR}/reports"

NAME_WIDTH = 3*COL_SIZE
SEPARATOR_SIZE = (17 + 1 + NAME_WIDTH + COL_SIZE)
SEPARATOR = SEPARATOR_SIZE * "="


def parse_args() -> BenchmarkParams:
    parser = argparse.ArgumentParser(description="Creates a benchmark")
    parser.add_argument("x0", help="first value of series", type=float)
    parser.add_argument("r", help="R value", type=float)
    parser.add_argument(
        "repetitions", help="Number of repetitions to each series", type=int)
    parser.add_argument("-f", help="export the results to a CSV file",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-g", help="Results will be exported to a graphic",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-gf", help="graphic file extension",
                        choices=["png", "svg"], default="png")
    parser.add_argument("-gs", help="Graphic scale type",
                        choices=["linear", "log", "both"], default="log")
    parser.add_argument("-ni", help="Min Interactions",
                        type=int, default=0)
    parser.add_argument("-mi", help="Max Interactions",
                        type=int, default=sys.maxsize)
    parser.add_argument("-l", "--languages",
                        help="Codes of Languages to be executed", nargs="*")
    parser.add_argument("-s", "--languages-to-skip",
                        help="Codes of Languages to be skipped", nargs="*")
    parser.add_argument("-comm", help="Show commands (just to debug)",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-code", help="Show language codes (just to debug)",
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    if not 0.0 <= args.x0 <= 1.0:
        parser.error("x0 must be between 0.0 and 1.0")
    if not 0.0 <= args.r <= 4.0:
        parser.error("r must be between 0.0 and 4.0")
    if args.repetitions <= 0:
        parser.error("repetitions must be a positive number")
    if not 0 <= args.ni < args.mi:
        parser.error(
            "Min repetitions should be lesser than Max repetitions and greater then 0.")

    return BenchmarkParams(x0=args.x0, r=args.r, repetitions=args.repetitions, min_iterations=args.ni, max_iterations=args.mi,
                           languages=args.languages, languages_to_skip=args.languages_to_skip, export_to_plot=args.g, export_to_file=args.f,
                           graphic_scale_type=args.gs, graphic_file_extension=args.gf, show_command=args.comm, show_code=args.code)


def get_interactions(min_interactions: int, max_interactions: int) -> list[int]:
    qdrt_10 = math.sqrt(math.sqrt(10))
    roots_10 = [1 / (qdrt_10*qdrt_10*qdrt_10), 1 /
                (qdrt_10*qdrt_10), 1 / (qdrt_10), 1.0]
    powers_10 = [100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]

    if 10 >= min_interactions:
        interactions = [10]
    else:
        interactions = []

    for pow_10 in powers_10:
        for root_10 in roots_10:
            interaction = int(root_10 * pow_10)
            if interaction > max_interactions:
                return interactions
            if interaction >= min_interactions:
                interactions.append(interaction)

    return interactions


def run_for_interactions(user_params: BenchmarkParams, results: BenchmarkResults, lang_params: list[LangParams], num_interactions: int):

    def run_command(lang_param: LangParams) -> int:
        log(lang_param.name.replace("\n", " ").rjust(NAME_WIDTH), False)

        if num_interactions > lang_param.max_iter:
            delta_t = ""
            print()
        else:
            final_command = f"{lang_param.command} r {user_params.x0} {user_params.r} {num_interactions} {user_params.repetitions}"

            if user_params.show_code:
                print((f"\t{lang_param.code}").ljust(
                    CODE_COL_SIZE), flush=True, end="")
            if user_params.show_command:
                print((f"\t'{final_command}'").ljust(
                    COMMAND_COL_SIZE), flush=True, end="")

            result = subprocess.run(
                final_command, shell=True, capture_output=True, check=True)
            delta_t = int(re.findall(TIME_RE, str(result.stdout))[0])
            print("{:,}".format(delta_t).rjust(COL_SIZE))

        return delta_t

    print(SEPARATOR)
    log("{0} {1}".format(
        "INTERACTIONS".rjust(NAME_WIDTH), "{:,}".format(num_interactions).rjust(COL_SIZE - 1)))
    # Source: https://stackoverflow.com/questions/9770668/scramble-python-list
    indexes = sorted(range(len(lang_params)), key=lambda x: random.random())
    for index in indexes:
        lang_param = lang_params[index]
        delta_t = run_command(lang_param)
        results.results[lang_param.name].times.append(delta_t)


def print_results(results: BenchmarkResults):
    log("RESULTS")
    print(tabulate(results.get_results(), headers="firstrow", tablefmt="psql"))


def export_results_to_csv(user_params: BenchmarkParams, results: BenchmarkResults):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR, True)

    file_name = f"{REPORTS_DIR}/x0={user_params.x0}_r={user_params.r}_it={user_params.repetitions}_{now_to_str()}.csv"
    with open(file_name, 'w', newline="",  encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerows(results.get_results())
    log(f"Exporting to {file_name}")


def plot_results(user_params: BenchmarkParams, results: BenchmarkResults):

    def fill_series():
        for lang, result in results.results.items():
            times_series = []
            for str_time in result.times:
                if str_time:
                    times_series.append(int(str_time))
                else:
                    times_series.append(None)
            plt.plot(results.interactions, times_series, label=lang,
                     color=result.color, linestyle=result.line_style)

    def basic_config():
        plt.legend()
        plt.title(
            f"x0 = { user_params.x0}, r = { user_params.r}, Repetitions = { user_params.repetitions}")
        plt.grid(visible=True, which="both")
        plt.xlabel("Interactions")
        plt.ylabel("Time (ms)")
        if not os.path.exists(PLOTS_DIR):
            os.makedirs(PLOTS_DIR, True)

        return f"{PLOTS_DIR}/x0={user_params.x0}_r={user_params.r}_rep={user_params.repetitions}_{now_to_str()}_TYPE.{user_params.graphic_file_extension}"

    def save_plot(file_name_base: str, scale_type: str):
        plt.xscale(scale_type)
        plt.yscale(scale_type)
        file_name = file_name_base.replace("TYPE", scale_type)
        plt.savefig(file_name, format=user_params.graphic_file_extension)
        log(f"{scale_type.capitalize()} plot saved at {file_name}")

    fill_series()
    file_name_base = basic_config()
    if user_params.is_linear_plotting():
        save_plot(file_name_base, "linear")
    if user_params.is_log_plotting():
        save_plot(file_name_base, "log")


def process_error(e: subprocess.CalledProcessError):
    print(f"""
---------------------- EXECUTION ERROR ----------------------
- COMMAND:
{e.cmd}
- MESSAGE:
{e.stderr.decode()}""")


def main():
    t0 = time.time()

    user_params = parse_args()

    change_work_dir()
    lang_params = read_config(user_params)

    try:
        results = BenchmarkResults(
            lang_params, get_interactions(user_params.min_iterations, user_params.max_iterations))

        for num_interactions in results.interactions:
            run_for_interactions(user_params, results,
                                 lang_params, num_interactions)
        print(SEPARATOR)

        if user_params.export_to_file:
            export_results_to_csv(user_params, results)
        else:
            print_results(results)

        if user_params.export_to_plot:
            plot_results(user_params, results)
    except subprocess.CalledProcessError as e:
        process_error(e)

    print_total_time(t0)


if __name__ == '__main__':
    main()
