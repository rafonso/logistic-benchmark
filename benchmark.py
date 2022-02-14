import datetime
import re
import subprocess
import sys
from typing import Any


class LangParams:
    def __init__(self, cmd, skip: list = []) -> None:
        self.command = cmd
        self.interations_to_skip = skip


col_size = 10
time_re = 'TOTAL_TIME (\d+)'


def get_now():
    return datetime.datetime.now().time()


def run_for_interations(languages: dict[str, LangParams],  x0: float, r: float, num_interations: int, repetitions: int) -> dict[int, dict]:
    time_interations = {}
    print(60 * "=")
    print("[{0}] {1} {2}".format(
        get_now(), "inter".rjust(col_size), str(num_interations).rjust(col_size)))
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
        final_command = lang_params.command.format(
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
    x0 = float(sys.argv[1])
    r = float(sys.argv[2])
    repetitions = int(sys.argv[3])

    languages = {
        "c":        LangParams(".\\c-logistic-benchmark\\x64\\Debug\\c-logistic-benchmark.exe r {} {} {} {}",  [10_000_000]),
        "c#":       LangParams(".\\cs-logistic-beanchmark\\bin\\Debug\\net6.0\\cs-logistic-beanchmark.exe r {} {} {} {}"),
        "go":       LangParams(".\\go-logistic-benchmark\\go-logistic-benchmark.exe r {} {} {} {}"),
        "java":     LangParams("java -jar .\\java-logistic-benchmark\\logistic-benchmark\\target\\java-logistic-benchmark-jar-with-dependencies.jar r {} {} {} {}"),
        "node":     LangParams("npm start --prefix typescript-logistic-benchmark -- r {} {} {} {}"),
        "python":   LangParams("python .\\python-logistic-benchmark\\main.py r {} {} {} {}"),
    }

    interations = [100, 1_000, 10_000, 100_000,
                   1_000_000, 5_000_000, 10_000_000]

    results = {}

    for num_interations in interations:
        results.update(run_for_interations(
            languages, x0, r, num_interations, repetitions))

    print_results(results, languages.keys())


if __name__ == '__main__':
    main()
