import argparse
from dataclasses import dataclass

from tabulate import tabulate

from commons import LangParams, change_work_dir, get_json_config_files


@dataclass
class ShowParams:
    only_codes: bool
    show_all: bool


def parse_args() -> ShowParams:
    parser = argparse.ArgumentParser(
        description="Show Languages parameters"
    )
    parser.add_argument("-c", "--only-codes", help="Show just codes",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-a", "--show-all", help="Show all details (e.g. color, max interactions, command)",
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    return ShowParams(args.only_codes, args.show_all)


def print_codes(params):
    print()
    for param in params:
        print(param.code)
    print()


def get_header(show_params: ShowParams) -> list[str]:
    header = ["CODE", "NAME", "DESCRIPTION"]
    if(show_params.show_all):
        header.extend(("MAX ITER", "COLOR", "LINE STYLE", "COMMAND"))

    return header


def get_table(params: list[LangParams], show_params: ShowParams) -> list[list[str]]:
    if show_params.show_all:
        return list(map(lambda param: [param.code, param.name, param.description, param.max_iter, param.color, param.linestyle, param.command], params))
    else:
        return list(map(lambda param: [param.code, param.name, param.description], params))


def main():
    change_work_dir()

    show_params = parse_args()
    params = get_json_config_files()

    if show_params.only_codes:
        print_codes(params)
    else:
        header = get_header(show_params)
        table = get_table(params, show_params)
        print(tabulate(table, header, tablefmt="psql"))


if __name__ == '__main__':
    main()
