import sys
import time
from numba import jit


@jit(cache=True)
def calculate(x0: float, r: float, it: int):
    series = [0.0] * it

    series[0] = x0
    for i in range(1, it):
        series[i] = r * series[i - 1] * (1 - series[i - 1])

    return series


@jit(forceobj=True)
def simple_action(calculate, x0, r, it, show_output):
    t0 = time.time()
    series = calculate(x0, r, it)
    deltaT = int((time.time() - t0) * 1000)

    if(show_output):
        print("-" * 40)
        for x in series:
            print(x)
        print("-" * 40)

    print("TIME: " + str(deltaT) + " ms")


@jit(cache=True)
def repeat_action(x0, r, it, repetitions):
    times = [0.0] * repetitions

    t0 = time.time()
    i = 0
    while i < repetitions:
        print(f'\r{i + 1}\t/\t{repetitions}', end="", flush=True)
        times[i] = calculate(x0, r, it)[1]
        i = i + 1
    deltaT = int((time.time() - t0) * 1000)
    print()

    average = sum(times) / len(times)

    print(f'AVERAGE: {average} ms')
    print("TOTAL_TIME " + str(deltaT))


def main():
    action = sys.argv[1]
    x0 = float(sys.argv[2])
    r = float(sys.argv[3])
    it = int(sys.argv[4])

    if action == "s":
        show_output = (len(sys.argv) > 5) and (sys.argv[5] == "s")
        simple_action(calculate, x0, r, it, show_output)
    elif action == "r":
        repetitions = int(sys.argv[5])
        repeat_action(x0, r, it, repetitions)


if __name__ == '__main__':
    main()
