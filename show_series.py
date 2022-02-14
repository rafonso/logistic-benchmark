import datetime
import re
import subprocess
import sys


class LangParams:
    def __init__(self, cmd, skip: list = []) -> None:
        self.command = cmd
        self.interations_to_skip = skip


def get_now():
    return datetime.datetime.now().time()


col_size = 24


def run_command(language: str, lang_params: LangParams, x0: float, r: float, interations: int):
    print("[{0}] {1}".format(
        get_now(), language.rjust(col_size)), flush=True, end="")
    final_command = lang_params.command.format(x0, r, interations)
    result = subprocess.run(final_command, shell=True, capture_output=True)

    lines = result.stdout.splitlines()
    for i in range(0, len(lines)):
        lines[i] = lines[i].decode("utf-8")

    limits = [i for i, e in enumerate(lines) if e == ("-" * 40)]
    series = lines[limits[0]+1:limits[1]]

    str_time = lines[limits[1] + 1]
    print(str_time.rjust(col_size))

    return series


def create_output(results: dict, it: int):
    output = ""
    languages = results.keys()

    for language in languages:
        output += language.ljust(col_size)
    output += "\n"

    for i in range(0, it):
        for language in languages:
            output += results.get(language)[i].ljust(col_size)
        output += "\n"

    return output


def main():
    x0 = float(sys.argv[1])
    r = float(sys.argv[2])
    it = int(sys.argv[3])

    languages = {
        "c":        LangParams(".\\c-logistic-benchmark\\x64\\Debug\\c-logistic-benchmark.exe s {} {} {} s"),
        "c#":       LangParams(".\\cs-logistic-beanchmark\\bin\\Debug\\net6.0\\cs-logistic-beanchmark.exe s {} {} {} s"),
        "go":       LangParams(".\\go-logistic-benchmark\\go-logistic-benchmark.exe s {} {} {} s"),
        "java":     LangParams("java -jar .\\java-logistic-benchmark\\logistic-benchmark\\target\\java-logistic-benchmark-jar-with-dependencies.jar s {} {} {} s"),
        "node":     LangParams("npm start --prefix typescript-logistic-benchmark -- s {} {} {} s"),
        "python":   LangParams("python .\\python-logistic-benchmark\\main.py s {} {} {} s"),
    }

    results = {}
    for language, lang_params in languages.items():
        results.update({language: run_command(
            language, lang_params, x0, r, it)})

    output = create_output(results, it)

    print()
    print(output)


if __name__ == '__main__':
    main()
