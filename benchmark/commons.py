import datetime
import time
from os import chdir
from os.path import dirname, normpath


def get_now():
    return datetime.datetime.now().time()


def change_work_dir():
    ''' Change the working dir to the languages one '''
    script_dir = dirname(__file__)
    chdir(normpath(script_dir + "/../languages"))


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
    "c":        LangParams("c-logistic-benchmark/c-logistic-benchmark.exe"),
    "c#":       LangParams("cs-logistic-beanchmark/bin/Debug/net6.0/cs-logistic-beanchmark.exe"),
    "go":       LangParams("go-logistic-benchmark/go-logistic-benchmark.exe"),
    "java":     LangParams("java -jar java-logistic-benchmark/target/java-logistic-benchmark-jar-with-dependencies.jar"),
    "kotlin":   LangParams("java -jar kotlin-logistic-benchmark/target/kotlin-logistic-benchmark-jar-with-dependencies.jar"),
    "lua":      LangParams("lua lua-logistic-benchmark/main.lua", [10_000_000]),
    "node":     LangParams("npm start --prefix typescript-logistic-benchmark --"),
    "python":   LangParams("python python-logistic-benchmark/main.py", [10_000_000]),
}


interations = [100, 300, 1_000, 3_000, 10_000, 30_000, 100_000, 300_000, 1_000_000, 3_000_000, 10_000_000]
