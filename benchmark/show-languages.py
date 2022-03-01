import glob
import json
from os import chdir
from os.path import dirname, normpath

from tabulate import tabulate

from commons import LangParams


def load_json(file_name):
    with open(file_name, 'r') as json_file:
        json_param = json.load(json_file)
        return LangParams(json_param["name"], json_param["command"], json_param.get("maxIter", None))


script_dir = dirname(__file__)
chdir(normpath(script_dir + "/.."))

files = glob.glob('./languages/**/*.config.json', recursive=True)
params = list(map(lambda file_path: load_json(file_path), files))
params.sort(key=lambda lp: lp.name)

header = ["NAME", "MAX ITER", "COMMAND"]
table = list(
    map(lambda param: [param.name, param.max_iter, param.command], params))

print(tabulate(table, header, tablefmt="psql"))
