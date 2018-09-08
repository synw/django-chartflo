# -*- coding: utf-8 -*-
from goerr import Err


class Sparkline(Err):
    
    def simple(self, data):
        html = """<span class="sparkline sparkline-embeded" data-type="line" 
        data-spot-Radius="3" data-highlight-Spot-Color="#f39c12" data-highlight-Line-Color="#222" 
        data-min-Spot-Color="#f56954" data-max-Spot-Color="#00a65a" data-spot-Color="#39CCCC" 
        data-offset="90" data-width="70px" data-height="15px" data-line-Width="2" 
        data-line-Color="#39CCCC" data-fill-Color="rgba(57, 204, 204, 0.08)">"""
        strdata = [str(x) for x in data]
        html += ",".join(strdata)
        html += "</span>"
        return html
