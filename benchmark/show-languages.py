import argparse

from tabulate import tabulate

from commons import LangParams, change_work_dir, get_json_config_files


class ShowParams:
    def __init__(self, show_all: bool):
        self.show_all = show_all


def parse_args() -> ShowParams:
    parser = argparse.ArgumentParser(
        description="Show Languages parameters"
    )
    parser.add_argument("-a", "--show-all", help="Show all details (e.g. color, max iteractions, command)",
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    return ShowParams(args.show_all)


def get_header(show_params: ShowParams) -> list[str]:
    header = ["NAME"]
    if(show_params.show_all):
        header.extend(("MAX ITER", "COLOR", "LINE STYLE", "COMMAND"))

    return header


def get_table(params: list[LangParams], show_params: ShowParams) -> list[list[str]]:
    if show_params.show_all:
        return list(map(lambda param: [param.name, param.max_iter, param.color, param.linestyle, param.command], params))
    else:
        return list(map(lambda param: [param.name], params))


def main():
    change_work_dir()
    
    show_params = parse_args()
    header = get_header(show_params)
    params = get_json_config_files()
    table = get_table(params, show_params)
    
    print(tabulate(table, header, tablefmt="psql"))


if __name__ == '__main__':
    main()
