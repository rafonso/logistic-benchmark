import csv
import datetime
import subprocess
import sys
import time


class LangParams:
    def __init__(self, cmd, skip: list = []) -> None:
        self.command = cmd
        self.interations_to_skip = skip


col_size = 24


def get_now():
    return datetime.datetime.now().time()


def run_command(language: str, lang_params: LangParams, x0: float, r: float, interations: int):
    print("[{0}] {1}".format(
        get_now(), language.rjust(col_size)), flush=True, end="")
    final_command = lang_params.command.format(x0, r, interations)
    result = subprocess.run(final_command, shell=True, capture_output=True)

    lines = result.stdout.splitlines()
    for i in range(0, len(lines)):
        lines[i] = lines[i].decode("utf-8")

    limits = [i for i, line in enumerate(lines) if line == ("-" * 40)]
    series = lines[limits[0]+1:limits[1]]

    str_time = lines[limits[1] + 1]
    print(str_time.rjust(col_size))

    return series


def create_output(results: dict, it: int) -> list[list[str]]:
    lines = []
    languages = results.keys()
    lines.append(list(languages))

    for i in range(0, it):
        line = []
        for language in languages:
            line.append(results.get(language)[i])
        lines.append(line)

    return lines


def lines_to_console(lines: list[list[str]]):
    for line in lines:
        for item in line:
            print(item.ljust(col_size), flush=True, end="")
        print()


def lines_to_file(x0: float, r: float, interations: int, lines: list[list[str]]):
    str_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"x0={x0}_r={r}_it={interations}_{str_now}.csv"
    with open(file_name, 'w', newline="",  encoding='UTF8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(lines)
    print(f"Exporting to {file_name}")


def main():
    t0 = time.time()

    x0 = float(sys.argv[1])
    r = float(sys.argv[2])
    it = int(sys.argv[3])
    output_to_file = (len(sys.argv) > 4) and (sys.argv[4] == "f")

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

    lines = create_output(results, it)

    print()
    if(output_to_file):
        lines_to_file(x0, r, it, lines)
    else:
        lines_to_console(lines)

    delta_t = int((time.time() - t0) * 1000)
    print("=" * 60)
    print(f"TOTAL TIME: {delta_t} ms")


if __name__ == '__main__':
    main()
