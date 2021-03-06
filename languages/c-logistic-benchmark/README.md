# C Language

## Development Environment
  - g++ (GCC) 11.2.0

## Highlights
To create the array I had to use `malloc` function from `stdlib.h`. When we create a array in C such as `double[] series = double[size];` this size must be a constant, not coming from a variable (such as `int size = 1000;`). Therefore I had to appeal to `malloc` to create a `double` pointer with requested size.

Its execution time is one of fastest, mainly when series size is lesser than 10,000. 

Initially it was developed with Visual Studio 2022. However I changed to GCC because its generated executable is faster than the one created by Visual Studio.

## Graphics
### General execution
![](./assets/x0=0.1_r=3.91_rep=100_2022-03-11_19-04-30_log.svg)
### Detail for less than 10,000 executions
![](./assets/x0=0.1_r=3.91_rep=100_2022-03-11_19-05-26_linear.svg)