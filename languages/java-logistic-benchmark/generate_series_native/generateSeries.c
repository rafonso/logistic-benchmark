#include "rafael_logistic_benchmark_benchmarks_NativeDoubleArrayGenerator.h"
#include <stdlib.h>

JNIEXPORT jdoubleArray JNICALL Java_rafael_logistic_1benchmark_benchmarks_NativeDoubleArrayGenerator_generateSeries(JNIEnv* env,
	jobject thiz, jdouble x0, jdouble r, jint iter)
{
	double* x = (double*)malloc(iter * sizeof(double));
	if (x) {

		x[0] = x0;
		for (int i = 1; i < iter; i++)
		{
			x[i] = r * x[i - 1] * (1.0 - x[i - 1]);
		}

		// Source: https://groups.google.com/g/android-ndk/c/WLBFdz9I7bA
		jdoubleArray doubleArray = (*env)->NewDoubleArray(env, iter);
		(*env)->SetDoubleArrayRegion(env, doubleArray, 0, iter, (const jdouble*)x);

		return doubleArray;
	}

	return NULL;
}
