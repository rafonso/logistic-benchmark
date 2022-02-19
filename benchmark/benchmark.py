import re
import subprocess
import sys
import time
from typing import Any

from commons import (LangParams, change_work_dir, get_now, interations,
                     languages, print_total_time)

col_size = 10
time_re = 'TOTAL_TIME (\d+)'


def run_for_interations(languages: dict[str, LangParams],  x0: float, r: float, num_interations: int, repetitions: int) -> dict[int, dict]:
    time_interations = {}
    print(60 * "=")
    print("[{0}] {1} {2}".format(
        get_now(), "inter".rjust(col_size), "{:,}".format(num_interations).rjust(col_size)))
    for language in languages.keys():
        time_interations.update(run_command(
            language, languages.get(language), x0, r, num_interations, repetitions))

    return {num_interations: time_interations}


def run_command(language: str, lang_params: LangParams, x0: float, r: float, num_interations: int, repetitions: int) -> dict[str, Any]:
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


def print_results(results: dict, lang_names: list):
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


def main():
    t0 = time.time()

    x0 = float(sys.argv[1])
    r = float(sys.argv[2])
    repetitions = int(sys.argv[3])

    change_work_dir()

    results = {}

    for num_interations in interations:
        results.update(run_for_interations(
            languages, x0, r, num_interations, repetitions))

    print_results(results, languages.keys())

    print_total_time(t0)


if __name__ == '__main__':
    main()
