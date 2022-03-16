package rafael.logistic_benchmark

import scala.collection.mutable.ArrayBuffer

object Main {

  def generate(x0: Double, r: Double, iter: Int): (Array[Double], Long) = {
    val t0 = System.currentTimeMillis()

    val x = new Array[Double](iter)
    x(0) = x0
    Range(1, iter).foreach(i => x(i) = r * x(i - 1) * (1.0 - x(i - 1)))

    (x, System.currentTimeMillis() - t0)
  }

  def simpleAction(x0: Double, r: Double, iter: Int, showSeries: Boolean): Unit = {
    val (series, time) = generate(x0, r, iter)

    if (showSeries) {
      println("-" * 40)
      series.foreach(println)
      println("-" * 40)
    }

    println(s"TIME: $time ms")
  }

  def repeatAction(x0: Double, r: Double, iter: Int, repetitions: Int): Unit = {
    val times = new ArrayBuffer[Long](repetitions)

    // warming
    generate(x0, r, iter)

    val t0 = System.currentTimeMillis()
    Range(0, repetitions)
      .foreach(i => {
        print(s"\r${i + 1} / $repetitions")
        times += generate(x0, r, iter)._2
      })
    val deltaT = System.currentTimeMillis() - t0
    println()

    val average = times.sum.toDouble / times.size

    println(s"AVERAGE $average ms")
    println(s"TOTAL_TIME $deltaT")
  }

  def main(args: Array[String]): Unit = {
    val action = args(0)(0)
    val x0 = args(1).toDouble
    val r = args(2).toDouble
    val iter = args(3).toInt

    if (action == 's') {
      val showSeries = (args.length >= 5) && (args(4)(0) == 's')
      simpleAction(x0, r, iter, showSeries)
    } else if (action == 'r') {
      val repetitions = args(4).toInt
      repeatAction(x0, r, iter, repetitions)
    }
  }

}
