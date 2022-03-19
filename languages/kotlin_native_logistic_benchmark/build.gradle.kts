plugins {
    kotlin("multiplatform") version "1.6.10"
}

group = "rafael.logistic_benchmark"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

kotlin {
    val hostOs = System.getProperty("os.name")
    val isMingwX64 = hostOs.startsWith("Windows")
    val logisticBenchmarkTarget = when {
        hostOs == "Mac OS X" -> macosX64("logistic_benchmark")
        hostOs == "Linux" -> linuxX64("logistic_benchmark")
        isMingwX64 -> mingwX64("logistic_benchmark")
        else -> throw GradleException("Host OS is not supported in Kotlin/Native.")
    }

    logisticBenchmarkTarget.apply {
        binaries {
            executable {
                entryPoint = "main"
            }
        }
    }
//    sourceSets {
//        val logistic_benchmarkMain by getting
//        val logistic_benchmarkTest by getting
//    }
}
