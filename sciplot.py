import numpy as np
from typing import List, Callable, NamedTuple
import matplotlib.pyplot as pp
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import scipy.constants as const


class Scale(NamedTuple):
    label: str
    ticks: List[float]


class GridFigure:
    figure: Figure
    axes: List[List[Axes]]

    def __init__(self,
            x_scales: List[Scale], y_scales: List[Scale],
            column_titles: List[str] = [],
            width_mm: float = 80,
            height_mm: float = 80,
            dpi: float = 100,
            left_margin_mm: float = 15,
            right_margin_mm: float = 5,
            top_margin_mm: float = 5,
            bottom_margin_mm: float = 10,
            horizontal_gap_mm: float = 5,
            vertical_gap_mm: float = 5,
            ) -> None:
        INCHES_PER_MM = const.milli / const.inch
        nrows = len(y_scales)
        ncols = len(x_scales)
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
        self.__setup_titles(column_titles)
        self.__setup_labels([v.label for v in x_scales], [v.label for v in y_scales])
        self.__setup_ticks([v.ticks for v in x_scales], [v.ticks for v in y_scales])
        self._plot()

    def _plot(self) -> None:
        pass

    def __setup_titles(self, column_titles: List[str]):
        for ax, title in zip(self.axes[0], column_titles):
            ax.set_title(title)

    def __setup_labels(self, x_labels: List[str], y_labels: List[str]):
        for ax, label in zip(self.axes[-1], x_labels):
            ax.set_xlabel(label)
        for row, label in zip(self.axes, y_labels):
            row[0].set_ylabel(label)

    def __setup_ticks(self, x_ticks: List[List[float]], y_ticks: List[List[float]]):
        for row, yt in zip(self.axes, y_ticks):
            for ax, xt in zip(row, x_ticks):
                _set_ticks(ax, xt, yt)
        self.__apply_to_axes(_set_ticks_in)
        self.__apply_to_axes(_remove_xticklabels, row_slice=slice(-1))
        self.__apply_to_axes(_remove_yticklabels, col_slice=slice(1, None))
        self.__apply_to_axes(_tighten_xticklabels, row_slice=-1)
        self.__apply_to_axes(_tighten_yticklabels, col_slice=0)

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

def _set_ticks(ax: Axes, x_ticks: List[float], y_ticks: List[float]) -> None:
    ax.set_xlim(x_ticks[0], x_ticks[-1])
    ax.set_xticks(x_ticks)
    ax.set_ylim(y_ticks[0], y_ticks[-1])
    ax.set_yticks(y_ticks)

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
    [Scale("a", [0, 1, 2]), Scale("b", [0, 2, 4])],
    [Scale("c", [-1, 0, 1]), Scale("d", [-2, 0, 2]), Scale("e", [-3, 0, 3])],
    column_titles=["foo", "boo"],
    width_mm=160,
    height_mm=120,
    top_margin_mm=20,
    bottom_margin_mm=15,
    horizontal_gap_mm=2,
    vertical_gap_mm=2,
    )

pp.show()
