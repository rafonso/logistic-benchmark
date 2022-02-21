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
    def __init__(self, name: str, cmd: str = "", max_iter: int = sys.maxsize) -> None:
        self.name = name
        self.command = normpath(cmd)
        self.max_iter = max_iter
        self.series: list[float] = []

    def __repr__(self):
        return f"[{self.name}: '{self.command}', {self.max_iter}]"


class UserParams:
    def __init__(self, x0: float, r: float, iter: int = 0, repetitions: int = 0,  languages: list[str] = [],
                 languages_to_skip: list[str] = [], export_to_file: bool = False, export_to_plot: bool = False, max_iterations: int = sys.maxsize):
        self.x0 = x0
        self.r = r
        self.iter = iter
        self.repetitions = repetitions
        self.languages = languages
        self.languages_to_skip = languages_to_skip
        self.export_to_file = export_to_file
        self.max_iterations = max_iterations
        self.export_to_plot = export_to_plot


def read_config(user_params: UserParams) -> list[LangParams]:
    def load_json(file_name):
        with open(file_name, 'r') as json_file:
            json_param = json.load(json_file)
            return LangParams(json_param["name"], json_param["command"], json_param.get("maxIter", sys.maxsize))

    files = glob.glob('./languages/**/*.config.json', recursive=True)
    params = list(map(lambda file_path: load_json(file_path), files))
    params.sort(key=lambda lp: lp.name)

    if user_params.languages:
        params = list(
            filter(lambda param: param.name in user_params.languages, params))
    if user_params.languages_to_skip:
        params = list(
            filter(lambda param: param.name not in user_params.languages_to_skip, params))

    assert bool(params), "Filtered params are empty"

    return params
