import sys
import subprocess
import datetime
import re

col_size = 10
time_re = 'TOTAL_TIME (\d+)'

def run_for_interations(commands,  x0, r, num_interations, repetitions):
    time_interations = {}
    print(60 * "=")
    print("[{0}] Interations: {1}".format(
        datetime.datetime.now().time(), str(num_interations).rjust(col_size)))
    for description in commands.keys():
        time_interations.update(run_command(
            description, commands.get(description), x0, r, num_interations, repetitions))
    return {num_interations: time_interations}


def run_command(description, command_pattern, x0, r, num_interations, repetitions):
    print(60 * "-")
    print("[{0}] {1}".format(datetime.datetime.now().time(), description))
    final_command = command_pattern.format(x0, r, num_interations, repetitions)
    # print(final_command)
    result = subprocess.run(final_command, shell=True, capture_output=True)
    deltaT = re.findall(time_re, str(result.stdout))[0]
    return {description: deltaT}


def print_results(results):
    print("[{0}] RESULTS".format(datetime.datetime.now().time()))
    header = "inter".rjust(col_size)
    for command in commands.keys():
        header = header + command.rjust(col_size)
    print(header)
    for interation in results.keys():
        line = str(interation).rjust(col_size)
        times = results.get(interation)
        for command in commands.keys():
            line = line + str(times.get(command)).rjust(col_size)
        print(line)


########################################
# 	  MAIN
########################################

x0 = float(sys.argv[1])
r = float(sys.argv[2])
repetitions = int(sys.argv[3])

commands = {
    "java": "java -jar .\\java-logistic-benchmark\\logistic-benchmark\\target\\java-logistic-benchmark-jar-with-dependencies.jar -ac r -x0 {} -r {} -it {} -re {}",
    "node": "npm start --prefix typescript-logistic-benchmark -- --action=r --x0={} --r={} -i {} --repetitions={}",
    "python": "python .\\python-logistic-benchmark\\main.py r {} {} {} {}"
}

interations = [100, 1000, 10000, 100000, 1000000, 10000000]

results = {}

for num_interations in interations:
    results.update(run_for_interations(
        commands, x0, r, num_interations, repetitions))
print(60 * "=")

print_results(results)
