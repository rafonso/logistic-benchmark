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

######################################
# MAIN PART
######################################

x0 = float(sys.argv[1])
r  = float(sys.argv[2])
it = int(sys.argv[3])
show_output = (len(sys.argv) > 4) and (sys.argv[4] == "show")

(series, deltaT) =  calculate(x0, r, it)

if(show_output):
  for x in series:
    print(x)

print("TIME: " + str(deltaT))