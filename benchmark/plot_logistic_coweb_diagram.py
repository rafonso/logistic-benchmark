# Original Source: https://scipython.com/blog/cobweb-plots/
import sys
from dataclasses import dataclass
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

# Use LaTeX throughout the figure for consistency
# rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 16})
# rc('text', usetex=True)# Figure dpi
dpi = 72


@dataclass
class AnnotatedFunction:
    """A small class representing a mathematical function.

    This class is callable so it acts like a Python function, but it also
    defines a string giving its latex representation.

    """
    func: Any
    latex_label: str

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def plot_cobweb(f: AnnotatedFunction, r: float, x0: float, it: int = 40):
    """Make a cobweb plot.

    Plot y = f(x; r) and y = x for 0 <= x <= 1, and illustrate the behaviour of
    iterating x = f(x) starting at x = x0. r is a parameter to the function.

    """
    x = np.linspace(0, 1, 500)
    fig: Figure = plt.figure(figsize=(600/dpi, 450/dpi), dpi=dpi)
    ax = fig.add_subplot(111)

    # Plot y = f(x) and y = x
    ax.plot(x, f(x, r), c='#444444', lw=2)
    ax.plot(x, x, c='#444444', lw=2)

    # Iterate x = f(x) for it steps, starting at (x0, 0).
    px, py = np.empty((2, it+1, 2))
    px[0], py[0] = x0, 0
    for n in range(1, it, 2):
        px[n  ] =   px[n-1]
        py[n  ] = f(px[n-1], r)
        px[n+1] =   py[n  ]
        py[n+1] =   py[n  ]

    # Plot the path traced out by the iteration.
    ax.plot(px, py, c='b', alpha=0.7)

    # Annotate and tidy the plot.
    ax.minorticks_on()
    ax.grid(which='minor', alpha=0.5)
    ax.grid(which='major', alpha=0.5)
    ax.set_aspect('equal')
    ax.set_xlabel('$x$')
    ax.set_ylabel(f.latex_label)
    ax.set_title(f'$x_0 = {x0}, r = {r}$')

    plt.get_current_fig_manager()\
        .set_window_title(f'x0 = {x0}, r = {r}, interactions = {it}')
    plt.show()


def main():
    x0  = float (sys.argv[1])
    r   = float (sys.argv[2])
    it  = int   (sys.argv[3])

    # The logistic map, f(x) = rx(1-x).
    func = AnnotatedFunction(lambda x, r: r*x*(1-x), r'$rx(1-x)$')

    plot_cobweb(func, r, x0, it)


if __name__ == '__main__':
    main()
