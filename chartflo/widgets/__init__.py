from .number import Number
from .sparkline import Sparkline
from .datatable import DataTable
from .sequence import Sequence


class Widget(Number, DataTable, Sparkline, Sequence):
    pass
