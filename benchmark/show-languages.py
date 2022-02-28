import datetime
import glob
import json
import sys
import time
from os import chdir
from os.path import dirname, normpath

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

max_len_name = max(map(lambda cmd: len(cmd), map(lambda param: param.name   , params)))
max_len_cmd  = max(map(lambda cmd: len(cmd), map(lambda param: param.command, params)))

header_format = "│ " +"{:^" + str(max_len_name) + "} │ {:^10} │ {:^" + str(max_len_cmd) + "} │"
str_format    = "│ " +"{:<" + str(max_len_name) + "} │ {:>10} │ {:<" + str(max_len_cmd) + "} │"

print("┌─" +("─" * max_len_name) + "─┬─" + ("─" * 10) + "─┬─" + ("─" * max_len_cmd)  + "─┐")
print(header_format.format("NAME", "MAX ITER", "COMMAND"))
print("├─" +("─" * max_len_name) + "─┼─" + ("─" * 10) + "─┼─" + ("─" * max_len_cmd)  + "─┤")
for param in params:
  str_max_iter = "{:,}".format(param.max_iter) if param.max_iter else ""
  print(str_format.format(param.name, str_max_iter, param.command))
print("└─" +("─" * max_len_name)  + "─┴─" + ("─" * 10)+ "─┴─" + ("─" * max_len_cmd) + "─┘")
