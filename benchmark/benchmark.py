import argparse
import datetime
import math
import re
import subprocess
import sys
import time

import matplotlib.pyplot as plt

from commons import (LangParams, change_work_dir, get_now, print_total_time,
                     read_config)

COL_SIZE = 10
TIME_RE = 'TOTAL_TIME (\d+)'
OUTPUT_DIR = "output/benchmark"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Creates a benchmark"
    )
    parser.add_argument("x0", help="first value of series", type=float)
    parser.add_argument("r", help="R value", type=float)
    parser.add_argument(
        "repetitions", help="Number of repetitions to each series", type=int)
    parser.add_argument("-g", help="Results will be exported to a graphic",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-mr", help="Max repetitions",
                        type=int, default=sys.maxsize)

    args = parser.parse_args()

    if not 0.0 <= args.x0 <= 1.0:
        parser.error("x0 must be between 0.0 and 1.0")
    if not 0.0 <= args.r <= 4.0:
        parser.error("r must be between 0.0 and 4.0")
    if args.repetitions <= 0:
        parser.error("repetitions must be a positive number")
    if args.mr <= 0:
        parser.error("Max repetitions must be a positive number")

    return args


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


def run_for_interations(params: list[LangParams], args: argparse.Namespace, num_interations: int) -> dict[int, dict[str, str]]:
    time_interations = {}
    print(60 * "=")
    print("[{0}] {1} {2}".format(
        get_now(), "inter".rjust(COL_SIZE), "{:,}".format(num_interations).rjust(COL_SIZE)))
    for param in params:
        time_interations.update(run_command(param, args, num_interations))

    return {num_interations: time_interations}


def run_command(param: LangParams, args: argparse.Namespace, num_interations: int) -> dict[str, str]:
    # print(60 * "-")
    print("[{0}] {1}".format(
        get_now(), param.name.rjust(COL_SIZE)), end="", flush=True)

    if num_interations > param.max_iter:
        deltaT = ""
        print()
    else:
        final_command = (param.command + " r {} {} {} {}").format(
            args.x0, args.r, num_interations, args.repetitions)
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


def plot_results(results: dict[int, dict], params: list[LangParams],  args: argparse.Namespace, interactions: list[int]):
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
        f"x0 = {args.x0}, r = {args.r}, Repetitions = {args.repetitions}")
    plt.grid(visible=True)
    plt.xscale("log")
    plt.xlabel("Interations")
    plt.yscale("log")
    plt.ylabel("Time (ms)")

    str_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{OUTPUT_DIR}/plots/x0={args.x0}_r={args.r}_rep={args.repetitions}_{str_now}.png"
    plt.savefig(file_name)
    print(f"Plot saved at {file_name}")


def main():
    t0 = time.time()

    args = parse_args()
    interactions = get_interactions(args.mr)

    change_work_dir()
    params = read_config()

    results: dict[int, dict[str, str]] = {}

    for num_interations in interactions:
        results.update(run_for_interations(params, args, num_interations))

    print_results(results, params)

    if args.g:
        plot_results(results, params, args, interactions)

    print_total_time(t0)


if __name__ == '__main__':
    main()
