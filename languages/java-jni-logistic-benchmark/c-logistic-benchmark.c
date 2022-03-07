// To compile : g++ -o c-logistic-benchmark.exe c-logistic-benchmark.c
#include <stdlib.h>

double *generate(const double x0, const double r, const int it)
{
	double *x = (double *)malloc(it * sizeof(double));

	x[0] = x0;
	for (int i = 1; i < it; i++)
	{
		x[i] = r * x[i - 1] * (1.0 - x[i - 1]);
	}

	return x;
}
