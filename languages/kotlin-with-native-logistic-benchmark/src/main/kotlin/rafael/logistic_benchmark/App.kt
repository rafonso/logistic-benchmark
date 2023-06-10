package rafael.logistic_benchmark

import kotlin.system.measureTimeMillis

private val nativeArrayGenerator = NativeDoubleArrayGenerator()

private fun calculate(x0: Double, r: Double, iter: Int): Pair<DoubleArray, Long> {
    var x: DoubleArray

    val deltaT = measureTimeMillis {
        x = nativeArrayGenerator.generateSeries(x0, r, iter)
    }

    return Pair(x, deltaT)
}

private fun simpleAction(x0: Double, r: Double, iter: Int, showSeries: Boolean) {
    val (series, deltaT) = calculate(x0, r, iter)

    if (showSeries) {
        println("-".repeat(40))
        series.forEach(::println)
        println("-".repeat(40))
    }

    println("TIME: $deltaT ms")
}

private fun repeatAction(x0: Double, r: Double, iter: Int, repetitions: Int) {
    val times = LongArray(repetitions)

    // warming
    calculate(x0, r, iter)

    val deltaT = measureTimeMillis {
        IntRange(1, repetitions).forEach {
            print("\r$it / $repetitions")
            times[it - 1] = calculate(x0, r, iter).second
        }
    }
    println()

    val average = times.average()

    println("AVERAGE $average ms")
    println("TOTAL_TIME $deltaT")
}


fun main(args: Array<String>) {
    val action = args[0][0]
    val x0 = args[1].toDouble()
    val r = args[2].toDouble()
    val iter = args[3].toInt()

    if (action == 's') {
        val showSeries = (args.size > 4) && (args[4][0] == 's')
        simpleAction(x0, r, iter, showSeries)
    } else if (action == 'r') {
        val repetitions = args[4].toInt()
        repeatAction(x0, r, iter, repetitions)
    }
}

