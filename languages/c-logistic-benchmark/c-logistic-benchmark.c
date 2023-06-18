// To compile : g++ -o c-logistic-benchmark-1.exe c-logistic-benchmark-1.c
#include <stdlib.h>
#include <stdio.h>

#ifdef _WIN32
#include <Windows.h>
#else
#include <sys/time.h>
#endif

// Code created by ChatGPT
long long getMilliseconds()
{
#ifdef _WIN32
	FILETIME ft;
	GetSystemTimeAsFileTime(&ft);
	long long ms = ft.dwHighDateTime;
	ms <<= 32;
	ms |= ft.dwLowDateTime;
	ms /= 10000;
	return ms;
#else
	struct timeval tv;
	gettimeofday(&tv, NULL);
	long long ms = tv.tv_sec * 1000LL + tv.tv_usec / 1000;
	return ms;
#endif
}

struct Result
{
	double *series;
	int series_size;
	long long time;
};

struct Result generate(const double x0, const double r, const int it)
{
	double *x = (double *)malloc(it * sizeof(double));

	long long t0 = getMilliseconds();
	if (x)
	{
		x[0] = x0;
		for (int i = 1; i < it; i++)
		{
			x[i] = r * x[i - 1] * (1.0 - x[i - 1]);
		}
	}
	long long deltaT = getMilliseconds() - t0;

	return (struct Result){x, it, deltaT};
}

void simple_action(const double x0, const double r, const int it, int show_series)
{
	struct Result result = generate(x0, r, it);

	if (show_series)
	{
		printf("----------------------------------------\n");
		for (int i = 0; i < result.series_size; i++)
		{
			printf("%.17f\n", result.series[i]);
		}
		printf("----------------------------------------\n");
	}

	printf("TIME: %lld ms", result.time);
	free(result.series);
}

void repeat_action(const double x0, const double r, const int it, int repetitions)
{
	long long *times = (long long *)malloc(it * sizeof(long long) + 1);
	if (!times)
	{
		fprintf(stderr, "It was not possible allocate array!");
		return;
	}

	long long t0 = getMilliseconds();
	long long totalTime = 0;
	for (int i = 0; i < repetitions; i++)
	{
		printf("\r%5d / %5d", (i + 1), repetitions);
		struct Result result = generate(x0, r, it);
		times[i] = result.time;
		totalTime += times[i];
		free(result.series);
	}
	printf("\n");
	long long deltaT = getMilliseconds() - t0;
	time_t average = totalTime / repetitions;

	printf("AVERAGE %d ms\n", average);
	printf("TOTAL_TIME %lld\n", deltaT);

	// free(times);
}

int main(int argc, char *argv[])
{

	if (argc < 4)
	{
		fprintf(stderr, "You need 4 arguments to run");
		exit(1);
	}

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
