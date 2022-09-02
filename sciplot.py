import numpy as np
from typing import List, Callable
import matplotlib.pyplot as pp
from matplotlib.figure import Figure
from matplotlib.axes import Axes


Scale = List[float]


class GridFigure:
    figure: Figure
    axes: List[List[Axes]]

    def __init__(self, xscales: List[Scale], yscales: List[Scale]) -> None:
        nrows = len(yscales)
        ncols = len(xscales)
        self.figure, self.axes = pp.subplots(nrows, ncols, squeeze=False)
        self._plot()
        for row, ys in zip(self.axes, yscales):
            for ax, xs in zip(row, xscales):
                set_scales(ax, xs, ys)
        self.__apply_to_axes(set_ticks_in)
        self.__apply_to_axes(remove_xticklabels, row_slice=slice(-1))
        self.__apply_to_axes(remove_yticklabels, col_slice=slice(1, None))
        self.__apply_to_axes(tighten_xticklabels, row_slice=-1)
        self.__apply_to_axes(tighten_yticklabels, col_slice=0)

    def _plot(self) -> None:
        pass

    def __apply_to_axes(self, func: Callable[[Axes], None],
            row_slice: slice | int = slice(None),
            col_slice: slice | int = slice(None)) -> None:
        row_slice = ensure_slice(row_slice)
        col_slice = ensure_slice(col_slice)
        for row in self.axes[row_slice]:
            for ax in row[col_slice]:
                func(ax)


def remove_xticklabels(ax: Axes) -> None:
    ax.set_xticklabels([])

def remove_yticklabels(ax: Axes) -> None:
    ax.set_yticklabels([])

def set_ticks_in(ax: Axes) -> None:
    ax.tick_params(direction="in")

def tighten_xticklabels(ax: Axes) -> None:
    t = ax.xaxis.get_major_ticks()
    t[0].label.set_horizontalalignment("left")
    t[-1].label.set_horizontalalignment("right")

def tighten_yticklabels(ax: Axes) -> None:
    t = ax.yaxis.get_major_ticks()
    t[0].label.set_verticalalignment("bottom")
    t[-1].label.set_verticalalignment("top")

def set_scales(ax: Axes, xs: Scale, ys: Scale) -> None:
    ax.set_xlim(xs[0], xs[-1])
    ax.set_xticks(xs)
    ax.set_ylim(ys[0], ys[-1])
    ax.set_yticks(ys)

def ensure_slice(value: slice | int) -> slice:
    if type(value) is slice:
        return value
    if value >= 0:
        return slice(value, value + 1)
    if value == -1:
        return slice(-1, None)
    return slice(value, value + 1)



class TrigFigure(GridFigure):
    
    def _plot(self) -> None:
        x = np.linspace(0, 2)
        for row in range(len(self.axes)):
            self.axes[row][0].plot(x, np.sin((1 + row) * x * np.pi) * (1 + row))
            self.axes[row][1].plot(x * 2, np.cos((1 + row) * x * np.pi * 2) * (1 + row))

tf = TrigFigure([[0, 1, 2], [0, 2, 4]], [[-1, 0, 1], [-2, 0, 2], [-3, 0, 3]])

pp.show()
