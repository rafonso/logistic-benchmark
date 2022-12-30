import datetime
import re
import subprocess

REPETITIONS = 100

COMMAND = "python .\\benchmark\\benchmark.py {0} {1} {2} -g -gs both " + \
    "-l c go rust c# java-array java-mixed kotlin scala "

X0s = [0.0, 0.1, 0.5, 0.9, 1.0]

Rs = [0.0, 0.5, 1.5, 2.5, 3.1, 3.5, 3.9, 3.99, 4.0]

TIMES: int = 3

regex_time = "^\\[.*\\] TOTAL TIME: (\\d+) ms"


def create_csv():
    file_name = "output\\benchmarks_" + \
        datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

    # header
    with open(file_name, 'a', encoding='UTF8') as f:
        f.write(" x0,   r")
        for time in range(1, TIMES + 1):
            f.write(f",{time:6d}")

    return file_name


def write_csv_content(file_name: str, begin: str, content: str):
    with open(file_name, 'a+', encoding='UTF8') as f:
        f.write(begin)
        f.write(content)


def execute_benchmark(x0: float, r: float):
    command_to_run = COMMAND.format(x0, r, REPETITIONS)

    complete_process = subprocess.run(
        command_to_run, shell=True, capture_output=True)
    last_line = complete_process.stdout.decode(
        encoding='utf-8', errors='strict').splitlines()[-1]
    time_str = re.search(regex_time, last_line).group(1)

    return int(time_str)


def main():
    csv_file_path = create_csv()

    for x0 in X0s:
        for r in Rs:
            write_csv_content(csv_file_path, "\n", f"{x0:.1f}")
            write_csv_content(csv_file_path, ",", f"{r:.2f}")
            for i in range(1, TIMES + 1):
                print(f"x0 = {x0:.1f}, r = {r:.2f}, Execution {i}",
                      flush=True, end=" ")
                time = execute_benchmark(x0, r)
                print(f"{time:,}")
                write_csv_content(csv_file_path, ",", f"{time:6d}")


if __name__ == '__main__':
    main()
