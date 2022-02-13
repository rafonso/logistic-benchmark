package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func calculate(x0 float64, r float64, interactions int) ([]float64, int64) {
	series := make([]float64, interactions)

	var t0 = time.Now().UnixMilli()
	series[0] = x0
	for i := 1; i < interactions; i++ {
		series[i] = r * series[i-1] * (1.0 - series[i-1])
	}
	var deltaT = time.Now().UnixMilli() - t0

	return series, deltaT
}

func simple_action(x0 float64, r float64, interactions int, showSeries bool) {
	series, deltaT := calculate(x0, r, interactions)

	if showSeries {
		for i := 0; i < len(series); i++ {
			fmt.Println(series[i])
		}
	}

	fmt.Println("TIME: ", deltaT, " ms")
}

func repeat_action(x0 float64, r float64, interactions int, repetitions int) {
	times := make([]int64, repetitions)

	var t0 = time.Now().UnixMilli()
	for i := 1; i < repetitions; i++ {
		fmt.Printf("\r%4d/%4d", (i + 1), repetitions)
		_, times[i] = calculate(x0, r, interactions)
	}
	var deltaT = time.Now().UnixMilli() - t0
	fmt.Println()

	var sum int64 = 0
	for i := 0; i < repetitions; i++ {
		sum += (times[i])
	}
	average := sum / int64(repetitions)

	fmt.Printf("AVERAGE %d ms\n", average)
	fmt.Printf("TOTAL_TIME %d", deltaT)
}

func main() {
	action := os.Args[1] // strings.Split(os.Args[0], "")[0]
	x0, _ := strconv.ParseFloat(os.Args[2], 64)
	r, _ := strconv.ParseFloat(os.Args[3], 64)
	interactions, _ := strconv.Atoi(os.Args[4])

	if action == "s" {
		showSeries := (len(os.Args) >= 6) && (os.Args[5] == "s")
		simple_action(x0, r, interactions, showSeries)
	} else if action == "r" {
		repetitions, _ := strconv.Atoi(os.Args[5])
		repeat_action(x0, r, interactions, repetitions)
	}
}
