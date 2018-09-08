# -*- coding: utf-8 -*-
from goerr import Err
from .sparkline import Sparkline
from ..utils import _write_file


class Number(Err):
    
    def simple(self, number, title, icon="chart-bar", spdata=None):
        sparkline = ""
        if spdata is not None:
            sp = Sparkline()
            sparkline = sp.simple(spdata)
        html = '<div class="number"><div class="number-icon has-background-link">'
        html += '<i class="fas fa-' + icon + '"></i></div><div class="number-content">'
        html += '<div class="number-content-title">' + title + '</div>'
        html += '<div class="number-content-num">' + str(number) + '</div>'
        html += sparkline + '</div></div>'
        return html
    
    def write(self, slug, dashboard, html):
        try:
            _write_file(slug, html, "number", dashboard)
        except Exception as e:
            self.err(e)
            return
        print("[x] Generated number " + slug)
    
