#include "rafael_logistic_benchmark_benchmarks_NativeDoubleArrayGenerator.h"
#include <stdlib.h>

JNIEXPORT jdoubleArray JNICALL Java_rafael_logistic_1benchmark_benchmarks_NativeDoubleArrayGenerator_generateSeries(JNIEnv *env,
                                                                                                                    jobject thiz, jdouble x0, jdouble r, jint it)
{
  double *x = (double *)malloc(it * sizeof(double));

  x[0] = x0;
  for (int i = 1; i < it; i++)
  {
    x[i] = r * x[i - 1] * (1.0 - x[i - 1]);
  }

  // Source: https://groups.google.com/g/android-ndk/c/WLBFdz9I7bA
  jdoubleArray doubleArray = (*env)->NewDoubleArray(env, it);
  (*env)->SetDoubleArrayRegion(env, doubleArray, 0, it, (const jdouble *)x);

  return doubleArray;
}
