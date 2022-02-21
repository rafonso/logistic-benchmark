import argparse
import csv
import math
import re
import subprocess
import sys
import time

import matplotlib.pyplot as plt

from commons import (LangParams, UserParams, change_work_dir, get_now,
                     print_total_time, read_config, now_to_str)

# class BenchmarkResults: 
#     def __init__(self, interactions: list[int], lang_params: list[LangParams]):
#         self.interactions = interactions
#         self.lang_times: dict[str, list[int]] = {}
#         for lang_param in lang_params:
#             self.lang_times[lang_param.name] = []

COL_SIZE = 10
TIME_RE = 'TOTAL_TIME (\d+)'
OUTPUT_DIR = "output/benchmark"


def parse_args() -> UserParams:
    parser = argparse.ArgumentParser(description="Creates a benchmark")
    parser.add_argument("x0", help="first value of series", type=float)
    parser.add_argument("r", help="R value", type=float)
    parser.add_argument(
        "repetitions", help="Number of repetitions to each series", type=int)
    parser.add_argument("-f", help="export the results to a CSV file",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-g", help="Results will be exported to a graphic",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-mi", help="Max Iteractions",
                        type=int, default=sys.maxsize)
    parser.add_argument("-l", "--languages", nargs="*",
                        help="Languages to be executed")
    parser.add_argument("-s", "--languages-to-skip", nargs="*",
                        help="Languages to be skipped")

    args = parser.parse_args()

    if not 0.0 <= args.x0 <= 1.0:
        parser.error("x0 must be between 0.0 and 1.0")
    if not 0.0 <= args.r <= 4.0:
        parser.error("r must be between 0.0 and 4.0")
    if args.repetitions <= 0:
        parser.error("repetitions must be a positive number")
    if args.mi <= 0:
        parser.error("Max repetitions must be a positive number")

    return UserParams(x0=args.x0, r=args.r, repetitions=args.repetitions, max_iterations=args.mi,
                      languages=args.languages, languages_to_skip=args.languages_to_skip, export_to_plot=args.g, export_to_file=args.f)


def get_interactions(max_interactions: int) -> list[int]:
    qdrt_10 = math.sqrt(math.sqrt(10))
    roots_10 = [1 / (qdrt_10*qdrt_10*qdrt_10), 1 /
                (qdrt_10*qdrt_10), 1 / (qdrt_10), 1.0]
    powers_10 = [100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]

    interations = [10]
    for pow_10 in powers_10:
        for root_10 in roots_10:
            interation = int(root_10 * pow_10)
            if interation > max_interactions:
                return interations
            interations.append(interation)

    return interations


def run_for_interations(params: list[LangParams], user_params: UserParams, num_interations: int) -> dict[int, dict[str, str]]:
    time_interations = {}
    print(60 * "=")
    print("[{0}] {1} {2}".format(
        get_now(), "inter".rjust(COL_SIZE), "{:,}".format(num_interations).rjust(COL_SIZE)))
    for param in params:
        time_interations.update(run_command(
            param, user_params, num_interations))

    return {num_interations: time_interations}


def run_command(param: LangParams, user_params: UserParams, num_interations: int) -> dict[str, str]:
    print("[{0}] {1}".format(
        get_now(), param.name.rjust(COL_SIZE)), end="", flush=True)

    if num_interations > param.max_iter:
        deltaT = ""
        print()
    else:
        final_command = (param.command + " r {} {} {} {}").format(
            user_params.x0, user_params.r, num_interations, user_params.repetitions)
        result = subprocess.run(final_command, shell=True, capture_output=True)
        deltaT = re.findall(TIME_RE, str(result.stdout))[0]
        print(deltaT.rjust(COL_SIZE))

    return {param.name: deltaT}


def print_results(results: dict[int, dict], params: list[LangParams]):
    print(60 * "=")
    print("[{0}] RESULTS".format(get_now()))
    header = "inter".rjust(COL_SIZE)
    for param in params:
        header = header + param.name.rjust(COL_SIZE)
    print(header)
    for interation in results.keys():
        line = str(interation).rjust(COL_SIZE)
        times = results.get(interation)
        for param in params:
            line = line + str(times.get(param.name)).rjust(COL_SIZE)
        print(line)

def export_results_to_csv(results: dict[int, dict], params: list[LangParams],  user_params: UserParams):
    lines: list[list[str]] = []
    
    header = ["iter"]
    for param in params:
        header.append(param.name)
    lines.append(header)

    for interation in results.keys():
        line = [interation]
        times = results.get(interation)
        for param in params:
            line.append(str(times.get(param.name)))
        lines.append(line)

    file_name = f"{OUTPUT_DIR}/x0={user_params.x0}_r={user_params.r}_it={user_params.iter}_{now_to_str()}.csv"
    with open(file_name, 'w', newline="",  encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerows(lines)
    print(f"Exporting to {file_name}")


def plot_results(results: dict[int, dict], params: list[LangParams],  user_params: UserParams, interactions: list[int]):
    for param in params:
        times = []
        for iter in interactions:
            str_time = results.get(iter).get(param.name)
            if str_time:
                times.append(int(str_time))
            else:
                times.append(None)
        plt.plot(interactions, times, label=param.name)
    plt.legend()

    plt.title(
        f"x0 = { user_params.x0}, r = { user_params.r}, Repetitions = { user_params.repetitions}")
    plt.grid(visible=True)
    plt.xscale("log")
    plt.xlabel("Interations")
    plt.yscale("log")
    plt.ylabel("Time (ms)")

    file_name = f"{OUTPUT_DIR}/plots/x0={user_params.x0}_r={user_params.r}_rep={user_params.repetitions}_{now_to_str()}.png"
    plt.savefig(file_name)
    print(f"Plot saved at {file_name}")


def main():
    t0 = time.time()

    user_params = parse_args()
    interactions = get_interactions(user_params.max_iterations)

    change_work_dir()
    params = read_config(user_params)

    results: dict[int, dict[str, str]] = {}

    for num_interations in interactions:
        results.update(run_for_interations(
            params, user_params, num_interations))

    if user_params.export_to_file:
        export_results_to_csv(results, params, user_params)
    else:
        print_results(results, params)

    if user_params.export_to_plot:
        plot_results(results, params, user_params, interactions)

    print_total_time(t0)


if __name__ == '__main__':
    main()
