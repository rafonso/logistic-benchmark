import datetime
import glob
import json
import sys
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
    def __init__(self, name: str, cmd: str, max_iter: int = sys.maxsize) -> None:
        self.name = name
        self.command = normpath(cmd)
        self.max_iter = max_iter

    def __repr__(self):
        return f"[{self.name}: '{self.command}', {self.max_iter}]"


def read_config() -> list[LangParams]:
    def load_json(file_name):
        with open(file_name, 'r') as json_file:
            json_param = json.load(json_file)
            return LangParams(json_param["name"], json_param["command"], json_param.get("maxIter", sys.maxsize))

    files = glob.glob('./languages/**/*.config.json', recursive=True)
    params = list(map(lambda file_path: load_json(file_path), files))
    params.sort(key=lambda lp: lp.name)

    return params
