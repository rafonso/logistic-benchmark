#include <chrono>
#include <stdlib.h>
#include <stdio.h>

typedef struct
{
	double* series;
	int series_size;
	long time;
} Result;

Result generate(const double x0, const double r, const int it)
{
	double* x = (double*)malloc(it * sizeof(double));

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

	return { x, it, deltaT };
}

int main(int argc, char* argv[])
{
	double x0 = 0.1;
	double r = 3.91;
	int it = 100;

	Result result = generate(x0, r, it);

	for (int i = 0; i < result.series_size; i++)
	{
		printf("%.17f\n", result.series[i]);
	}
	printf("%d", result.time);
}
