import argparse
from dataclasses import dataclass

from tabulate import tabulate

from commons import LangParams, change_work_dir, get_json_config_files


@dataclass
class ShowParams:
    only_codes: bool
    commands: bool
    show_all: bool


def parse_args() -> ShowParams:
    parser = argparse.ArgumentParser(
        description="Show Languages parameters"
    )
    parser.add_argument("-c", "--only-codes", help="Show just codes",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-co", "--commands", help="Show codes and their commands",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-a", "--show-all", help="Show all details (e.g. color, max interactions, command)",
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    return ShowParams(args.only_codes, args.commands, args.show_all)


def print_codes(params: list[LangParams]):
    header = ["CODE"]
    table = list(map(lambda param: [param.code], params))
    print(tabulate(table, header))


def print_commands(params: list[LangParams]):
    header = ["CODE", "COMMAND"]
    table = list(map(lambda param: [param.code, param.command], params))
    print(tabulate(table, header))


def print_all(params: list[LangParams]):
    header = ["CODE", "NAME", "DESCRIPTION",
              "MAX ITER", "COLOR", "LINE STYLE", "COMMAND"]
    table = list(map(lambda param: [param.code, param.name, param.description,
                 param.max_iter, param.color, param.linestyle, param.command], params))
    print(tabulate(table, header, tablefmt="psql"))


def print_name_description(params: list[LangParams]):
    header = ["CODE", "NAME", "DESCRIPTION"]
    table = list(
        map(lambda param: [param.code, param.name, param.description], params))
    print(tabulate(table, header, tablefmt="psql"))


def main():
    change_work_dir()

    show_params = parse_args()
    shower = print_codes if show_params.only_codes  \
        else print_commands if show_params.commands \
        else print_all if show_params.show_all      \
        else print_name_description

    params: list[LangParams] = get_json_config_files()
    shower(params)


if __name__ == '__main__':
    main()
