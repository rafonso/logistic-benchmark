# To compile native: pyinstaller -F main.py  
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


def simple_action(calculate, x0, r, it, show_output):
    (series, deltaT) = calculate(x0, r, it)

    if(show_output):
        print("-" * 40)
        for x in series:
            print(x)
        print("-" * 40)

    print("TIME: " + str(deltaT) + " ms")


def repeat_action(x0, r, it, repetitions):
    times = [0.0] * repetitions

    t0 = time.time()
    for i in range(0, repetitions):
        print("\r{0}\t/\t{1}".format((i + 1), repetitions))
        times[i] = calculate(x0, r, it)[1]
    deltaT = int((time.time() - t0) * 1000)
    print()

    average = sum(times) / len(times)

    print("AVERAGE: {0} ms".format(average))
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
