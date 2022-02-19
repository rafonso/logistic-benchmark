// To compile : g++ -o c-logistic-benchmark.exe c-logistic-benchmark.c
#include <chrono>
#include <stdlib.h>
#include <stdio.h>

typedef struct
{
	double *series;
	int series_size;
	long time;
} Result;

Result generate(const double x0, const double r, const int it)
{
	double *x = (double *)malloc(it * sizeof(double));

	long t0 = clock();
	if (x)
	{
		x[0] = x0;
		for (int i = 1; i < it; i++)
		{
			x[i] = r * x[i - 1] * (1.0 - x[i - 1]);
		}
	}
	long deltaT = clock() - t0;

	return {x, it, deltaT};
}

void simple_action(const double x0, const double r, const int it, int show_series)
{
	Result result = generate(x0, r, it);

	if (show_series)
	{
		printf("----------------------------------------\n");
		for (int i = 0; i < result.series_size; i++)
		{
			printf("%.17f\n", result.series[i]);
		}
		printf("----------------------------------------\n");
	}

	printf("TIME: %d ms", result.time);
}

void repeat_action(const double x0, const double r, const int it, int repetitions)
{
	long *times = (long *)malloc(it * sizeof(long));

	if (times)
	{
		long t0 = clock();
		long totalTime = 0;
		for (int i = 0; i < repetitions; i++)
		{
			printf("\r%5d / %5d", (i + 1), repetitions);
			times[i] = generate(x0, r, it).time;
			totalTime += times[i];
		}
		printf("\n");
		long deltaT = clock() - t0;
		long average = totalTime / repetitions;

		printf("AVERAGE %d ms\n", average);
		printf("TOTAL_TIME %d\n", deltaT);
	}
}

int main(int argc, char *argv[])
{
	char action = argv[1][0];
	double x0 = atof(argv[2]);
	double r = atof(argv[3]);
	int it = atoi(argv[4]);

	if (action == 's')
	{
		int show_series = (argc > 5) && (argv[5][0] == 's');
		simple_action(x0, r, it, show_series);
	}
	else if (action == 'r')
	{
		int repetitions = atoi(argv[5]);
		repeat_action(x0, r, it, repetitions);
	}
}
