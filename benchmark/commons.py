import datetime
import time
from os import chdir
from os.path import dirname, normpath


def get_now():
    return datetime.datetime.now().time()


def change_work_dir():
    ''' Change the working dir to the languages one '''
    script_dir = dirname(__file__)
    chdir(normpath(script_dir + "/.."))


def print_total_time(t0: float):
    """Print the total time of execution of program.

    Parameters:
    t0: the initial time (in milliseconds) when started the execution
    """
    delta_t = int((time.time() - t0) * 1000)
    print("=" * 60)
    print(f"[{get_now()}] TOTAL TIME: {delta_t} ms")


class LangParams:
    def __init__(self, cmd, skip: list = []) -> None:
        self.command = normpath(cmd)
        self.interations_to_skip = skip


languages = {
    "c":        LangParams("languages/c-logistic-benchmark/c-logistic-benchmark.exe"),
    "c#":       LangParams("languages/cs-logistic-beanchmark/bin/Debug/net6.0/cs-logistic-beanchmark.exe"),
    "go":       LangParams("languages/go-logistic-benchmark/go-logistic-benchmark.exe"),
    "java":     LangParams("java -jar languages/java-logistic-benchmark/target/java-logistic-benchmark-jar-with-dependencies.jar"),
    "kotlin":   LangParams("java -jar languages/kotlin-logistic-benchmark/target/kotlin-logistic-benchmark-jar-with-dependencies.jar"),
    "lua":      LangParams("lua languages/lua-logistic-benchmark/main.lua", [5_620_000, 10_000_000]),
    "node":     LangParams("npm start --prefix languages/typescript-logistic-benchmark --"),
    "python":   LangParams("python languages/python-logistic-benchmark/main.py", [10_000_000]),
}
