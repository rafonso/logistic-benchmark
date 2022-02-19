import datetime
import re
import subprocess
import sys
import time

import matplotlib.pyplot as plt

from commons import (LangParams, change_work_dir, get_now, interations,
                     languages, print_total_time)

col_size = 10
time_re = 'TOTAL_TIME (\d+)'


def run_for_interations(languages: dict[str, LangParams],  x0: float, r: float, num_interations: int, repetitions: int) -> dict[int, dict[str, str]]:
    time_interations = {}
    print(60 * "=")
    print("[{0}] {1} {2}".format(
        get_now(), "inter".rjust(col_size), "{:,}".format(num_interations).rjust(col_size)))
    for language in languages.keys():
        time_interations.update(run_command(
            language, languages.get(language), x0, r, num_interations, repetitions))

    return {num_interations: time_interations}


def run_command(language: str, lang_params: LangParams, x0: float, r: float, num_interations: int, repetitions: int) -> dict[str, str]:
    # print(60 * "-")
    print("[{0}] {1}".format(
        get_now(), language.rjust(col_size)), end="", flush=True)

    if (num_interations in lang_params.interations_to_skip):
        deltaT = ""
        print()
    else:
        final_command = (lang_params.command + " r {} {} {} {}").format(
            x0, r, num_interations, repetitions)
        # print(final_command)
        result = subprocess.run(final_command, shell=True, capture_output=True)
        deltaT = re.findall(time_re, str(result.stdout))[0]
        print(deltaT.rjust(col_size))

    return {language: deltaT}


def print_results(results: dict[int, dict], lang_names: list):
    print(60 * "=")
    print("[{0}] RESULTS".format(get_now()))
    header = "inter".rjust(col_size)
    for lang_name in lang_names:
        header = header + lang_name.rjust(col_size)
    print(header)
    for interation in results.keys():
        line = str(interation).rjust(col_size)
        times = results.get(interation)
        for lang_name in lang_names:
            line = line + str(times.get(lang_name)).rjust(col_size)
        print(line)


def plot_results(results: dict[int, dict], languages: dict[str, LangParams], x0: float, r: float, repetitions: int):
    for lang_name in languages.keys():
        times = []
        for iter in interations:
            str_time = results.get(iter).get(lang_name)
            if str_time:
                times.append(int(str_time))
            else:
                times.append(None)
        plt.plot(interations, times, label=lang_name)
    plt.legend()

    plt.title(f"x0 = {x0}, r = {r}, Repetitions = {repetitions}")
    plt.grid(visible = True)
    plt.xscale("log")
    plt.xlabel("Interations")
    plt.yscale("log")
    plt.ylabel("Time (ms)")

    str_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"../x0={x0}_r={r}_rep={repetitions}_{str_now}.png"
    plt.savefig(file_name)
    print(f"Plot saved at {file_name}")


def main():
    t0 = time.time()

    x0 = float(sys.argv[1])
    r = float(sys.argv[2])
    repetitions = int(sys.argv[3])

    change_work_dir()

    results: dict[int, dict[str, str]] = {}

    for num_interations in interations:
        results.update(run_for_interations(
            languages, x0, r, num_interations, repetitions))

    print_results(results, languages.keys())

    plot_results(results, languages, x0, r, repetitions)

    print_total_time(t0)


if __name__ == '__main__':
    main()
