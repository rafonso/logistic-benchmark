import datetime
import glob
import json
import sys
import time
from dataclasses import InitVar, dataclass, field
from os import chdir
from os.path import dirname, normpath

OUTPUT_DIR = "output"


def now_to_str():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


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
    log(f"TOTAL TIME: {delta_t} ms")


def log(msg: str, breakLine: bool = True):
    now_str = datetime.datetime.now().time()
    separator = "\n" if breakLine else ""
    print(f"[{now_str}] " + msg, flush=not breakLine, end=separator)


@dataclass
class LangParams:
    name: str
    code: str
    description: str
    cmd: InitVar[str] = ""
    max_iter: int = sys.maxsize
    color: str = None
    linestyle: str = "-"
    command: str = field(init=False)
    series: list[float] = field(default_factory=list)

    def __post_init__(self, cmd: str):
        self.command = normpath(cmd)


@dataclass
class UserParams:
    x0: float
    r: float
    languages: list[str] = field(default_factory=list)
    languages_to_skip: list[str] = field(default_factory=list)
    export_to_file: bool = False


def get_json_config_files():
    def load_json(file_name):
        with open(file_name, 'r') as json_file:
            json_param = json.load(json_file)
            return LangParams(json_param["name"], json_param.get("code", None), json_param.get("description", None),
                              json_param["command"],
                              json_param.get("maxIter", None),
                              json_param.get("color", None),
                              json_param.get("linestyle", "solid"))

    files = glob.glob('./languages/**/*.config.json', recursive=True)
    params = list(map(lambda file_path: load_json(file_path), files))
    params.sort(key=lambda lp: lp.code)
    return params


def read_config(user_params: UserParams) -> list[LangParams]:
    params = get_json_config_files()

    for param in params:
        if not param.max_iter:
            param.max_iter = sys.maxsize

    if user_params.languages:
        params = list(
            filter(lambda param: param.code in user_params.languages, params))
    if user_params.languages_to_skip:
        params = list(
            filter(lambda param: param.code not in user_params.languages_to_skip, params))

    assert bool(params), "Filtered params are empty"

    return params
