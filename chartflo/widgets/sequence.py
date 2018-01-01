# -*- coding: utf-8 -*-
from dataswim import ds
from ..utils import _write_file


class Sequence():

    def sequence(self, slug, dashboard, key, value, data=None, style=None,
                 trs=None, verbose=True):
        """
        Draw sequence boxes
        """
        df = self.df.filter([key, value], axis=1)
        if style is None:
            style = "width:46px;padding:0.2em 0.6em 0.6em 0.2em"
        html = '<div class="sequence">\n'
        for row in df.itertuples():
            value = row[2]
            if str(value).endswith(".0"):
                value = int(value)
            klass = ""
            st = ""
            if trs is not None:
                if value <= trs["low"]:
                    klass = " text-success"
                    st = "font-weight:bold"
                elif value > trs["high"]:
                    klass = " text-danger"
                    st = "font-weight:bold"
            box = '<div class="sequence-box" style="' \
                + style + '">'
            box += '<div class="sequence-key" style="font-size:85%">' \
                + str(row[1]) + '</div><div class="sequence-value'+klass \
                + '" style="'+st+';">'
            box += str(value) + '</div>'
            box += '</div>\n'
            html += box
        html += '</div>'
        _write_file(slug, html, "sequence", dashboard)
        if verbose is True:
            ds.ok("Generated sequence " + slug)


seq = Sequence()
