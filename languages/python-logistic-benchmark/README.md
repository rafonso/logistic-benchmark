# Python

## Development Environment
  - [Python](https://www.python.org/) [3.10.1](https://www.python.org/downloads/release/python-3101/)
  - [PyPy](https://www.pypy.org/) [3.9](https://www.pypy.org/download.html)
  - VS Code

## Highlights

### [Basic script](./main.py)
It was possible to use a list with predetermined size. However at the end it was the slowest to execute.

### [Basic script with Pypy](./main.py)
Instead using basic CPython, it was running with [Pypy](https://www.pypy.org/index.html). This time, for it executed much faster thanks to JIT compiler.

### [Native Executable](./setup.py)
Creates a native executable from Basic Script. The time as practically the same as basic script.

### [Cuda integration](./main_cuda.py)
Basically equals to Basic Script, but using [numba decorators](https://numba.pydata.org/numba-doc/latest/user/jit.html). Until interactions 500 interactions its time is greater than basic script. After this, the execution time was basically 20% faster than basic script.

## Graphics
### General execution
![](./assets/python_linear.png)
![](./assets/python_log.png)

