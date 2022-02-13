import datetime
import re
import subprocess
import sys

col_size = 10
time_re = 'TOTAL_TIME (\d+)'


def run_for_interations(languages,  x0, r, num_interations, repetitions):
    time_interations = {}
    print(60 * "=")
    print("[{0}] {1} {2}".format(
        datetime.datetime.now().time(), "inter".rjust(col_size), str(num_interations).rjust(col_size)))
    for language in languages.keys():
        time_interations.update(run_command(
            language, languages.get(language), x0, r, num_interations, repetitions))
    return {num_interations: time_interations}


def run_command(description, command_pattern, x0, r, num_interations, repetitions):
    print(60 * "-")
    print("[{0}] {1}".format(datetime.datetime.now().time(),
          description.rjust(col_size)), end="", flush=True)
    final_command = command_pattern.format(x0, r, num_interations, repetitions)
    # print(final_command)
    result = subprocess.run(final_command, shell=True, capture_output=True)
    deltaT = re.findall(time_re, str(result.stdout))[0]
    print(deltaT.rjust(col_size))
    return {description: deltaT}


def print_results(results, languages):
    print(60 * "=")
    print("[{0}] RESULTS".format(datetime.datetime.now().time()))
    header = "inter".rjust(col_size)
    for language in languages.keys():
        header = header + language.rjust(col_size)
    print(header)
    for interation in results.keys():
        line = str(interation).rjust(col_size)
        times = results.get(interation)
        for language in languages.keys():
            line = line + str(times.get(language)).rjust(col_size)
        print(line)


def main():
    x0 = float(sys.argv[1])
    r = float(sys.argv[2])
    repetitions = int(sys.argv[3])

    languages = {
        "c": ".\\c-logistic-benchmark\\x64\\Debug\\c-logistic-benchmark.exe r {} {} {} {}",
        "c#": ".\\cs-logistic-beanchmark\\bin\\Debug\\net6.0\\cs-logistic-beanchmark.exe r {} {} {} {}",
        "java": "java -jar .\\java-logistic-benchmark\\logistic-benchmark\\target\\java-logistic-benchmark-jar-with-dependencies.jar r {} {} {} {}",
        "node": "npm start --prefix typescript-logistic-benchmark -- r {} {} {} {}",
        "python": "python .\\python-logistic-benchmark\\main.py r {} {} {} {}"
    }

    interations = [100, 1_000, 10_000, 100_000, 1_000_000, 5_000_000]

    results = {}

    for num_interations in interations:
        results.update(run_for_interations(
            languages, x0, r, num_interations, repetitions))

    print_results(results, languages)


if __name__ == '__main__':
    main()
