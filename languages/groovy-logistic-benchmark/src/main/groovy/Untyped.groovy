static def calculate(x0, r, it) {
    def series = new double[it]

    def t0 = System.currentTimeMillis()
    series[0] = x0
    for (def i = 1; i < it; i++) {
        series[i] = r * series[i - 1] * (1 - series[i - 1])
    }
    def deltaT = (System.currentTimeMillis() - t0)

    return [series, deltaT]
}

def simpleAction(x0, r, it, showOutput) {
    def (series, deltaT) = calculate(x0, r, it)

    if (showOutput) {
        println('-' * 40)
        series.each { x -> println(x) }
        println("-" * 40)
    }

    println("TIME: ${deltaT} ms")
}

def repeatAction(x0, r, it, repetitions) {
    def times = new double[repetitions]

    def t0 = System.currentTimeMillis()
    (1..repetitions).each { i ->
        print("\r${i}\t/\t${repetitions}")
        times[i - 1] = calculate(x0, r, it)[1]
    }
    def deltaT = (System.currentTimeMillis() - t0)
    println()

    def average = (times.sum() / times.size()) as long

    println("AVERAGE: ${average} ms")
    println("TOTAL_TIME ${deltaT}")
}

def action = args[0]
def x0 = args[1] as double
def r = args[2] as double
def it = args[3] as int

if (action == 's') {
    def showOutput = args.size() > 4 && args[4] == 's'
    simpleAction(x0, r, it, showOutput)
} else if (action == 'r') {
    def repetitions = args[4] as int
    repeatAction(x0, r, it, repetitions)
}
