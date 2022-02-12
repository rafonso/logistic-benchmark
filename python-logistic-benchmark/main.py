import sys
import time


def calculate(x0, r, it):
    series = [0] * it

    t0 = time.time()
    series[0] = x0
    for i in range(1, it):
        series[i] = r * series[i - 1] * (1 - series[i - 1])
    deltaT = int((time.time() - t0) * 1000)

    return (series, deltaT)


def repeat(x0, r, it, rep):
    times = [0.0] * rep

    for i in range(0, rep):
        print(".", end="", flush=True)
        times[i] = calculate(x0, r, it)[1]
    print("\n")

    average = sum(times) / len(times)
    print(f'AVERAGE: {average}')


######################################
# MAIN PART
######################################

action = sys.argv[1]
x0 = float(sys.argv[2])
r = float(sys.argv[3])
it = int(sys.argv[4])

if action == "s":
    (series, deltaT) = calculate(x0, r, it)

    show_output = (len(sys.argv) > 5) and (sys.argv[5] == "show")
    if(show_output):
        for x in series:
            print(x)

    print("TIME: " + str(deltaT))
elif action == "r":
    repetitions = int(sys.argv[5])
    repeat(x0, r, it, repetitions)
