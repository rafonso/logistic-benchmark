from tabulate import tabulate

from commons import get_json_config_files, change_work_dir

change_work_dir()

params = get_json_config_files()

header = ["NAME", "MAX ITER", "COLOR", "LINE STYLE", "COMMAND"]
table = list(
    map(lambda param: [param.name, param.max_iter, param.color, param.linestyle, param.command], params))

print(tabulate(table, header, tablefmt="psql"))
