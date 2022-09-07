import numpy as np
from typing import List, Callable
import matplotlib.pyplot as pp
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import scipy.constants as const


Scale = List[float]


class GridFigure:
    figure: Figure
    axes: List[List[Axes]]

    def __init__(self,
            xscales: List[Scale], yscales: List[Scale],
            width_mm: float, height_mm: float,
            dpi: float = 100,
            left_margin_mm: float = 15,
            right_margin_mm: float = 5,
            top_margin_mm: float = 5,
            bottom_margin_mm: float = 10,
            horizontal_gap_mm: float = 5,
            vertical_gap_mm: float = 5,
            ) -> None:
        INCHES_PER_MM = const.milli / const.inch
        nrows = len(yscales)
        ncols = len(xscales)
        total_hspace_mm = \
            left_margin_mm + \
            right_margin_mm + \
            (ncols - 1) * horizontal_gap_mm
        total_wspace_mm = \
            top_margin_mm + \
            bottom_margin_mm + \
            (nrows - 1) * vertical_gap_mm
        self.figure, self.axes = pp.subplots(nrows, ncols, squeeze=False,
            figsize = (width_mm * INCHES_PER_MM, height_mm * INCHES_PER_MM),
            dpi = dpi,
            gridspec_kw = {
                "left": left_margin_mm / width_mm,
                "right": 1 - right_margin_mm / width_mm,
                "top": 1 - top_margin_mm / height_mm,
                "bottom": bottom_margin_mm / height_mm,
                "wspace": ncols * horizontal_gap_mm / (width_mm - total_hspace_mm),
                "hspace": nrows * vertical_gap_mm / (height_mm - total_wspace_mm),
            }
        )
        for row, ys in zip(self.axes, yscales):
            for ax, xs in zip(row, xscales):
                _set_scales(ax, xs, ys)
        self.__apply_to_axes(_set_ticks_in)
        self.__apply_to_axes(_remove_xticklabels, row_slice=slice(-1))
        self.__apply_to_axes(_remove_yticklabels, col_slice=slice(1, None))
        self.__apply_to_axes(_tighten_xticklabels, row_slice=-1)
        self.__apply_to_axes(_tighten_yticklabels, col_slice=0)
        self._plot()

    def _plot(self) -> None:
        pass

    def __apply_to_axes(self, func: Callable[[Axes], None],
            row_slice: slice | int = slice(None),
            col_slice: slice | int = slice(None)) -> None:
        row_slice = _ensure_slice(row_slice)
        col_slice = _ensure_slice(col_slice)
        for row in self.axes[row_slice]:
            for ax in row[col_slice]:
                func(ax)


def _remove_xticklabels(ax: Axes) -> None:
    ax.set_xticklabels([])

def _remove_yticklabels(ax: Axes) -> None:
    ax.set_yticklabels([])

def _set_ticks_in(ax: Axes) -> None:
    ax.tick_params(direction="in")

def _tighten_xticklabels(ax: Axes) -> None:
    t = ax.xaxis.get_major_ticks()
    t[0].label.set_horizontalalignment("left")
    t[-1].label.set_horizontalalignment("right")

def _tighten_yticklabels(ax: Axes) -> None:
    t = ax.yaxis.get_major_ticks()
    t[0].label.set_verticalalignment("bottom")
    t[-1].label.set_verticalalignment("top")

def _set_scales(ax: Axes, xs: Scale, ys: Scale) -> None:
    ax.set_xlim(xs[0], xs[-1])
    ax.set_xticks(xs)
    ax.set_ylim(ys[0], ys[-1])
    ax.set_yticks(ys)

def _ensure_slice(value: slice | int) -> slice:
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

tf = TrigFigure(
    [[0, 1, 2], [0, 2, 4]],
    [[-1, 0, 1], [-2, 0, 2], [-3, 0, 3]],
    width_mm=160,
    height_mm=120,
    bottom_margin_mm=20,
    horizontal_gap_mm=10,
    vertical_gap_mm=1,
    )

pp.show()
