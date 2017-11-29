from .number import Number


number = Number()

"""
def number_progress(number, legend=None, unit="", thresholds={}, icon=None, color="green", progress=None):
    ibg = ""
    if progress is None:
        ibg = " bg-" + color
    if icon is None:
        icon = '<span class="info-box-icon' + ibg + \
            '"><i class="fa fa-thumbs-o-up"></i></span>'
    else:
        icon = '<span class="info-box-icon' + ibg + \
            '"><i class="fa fa-' + icon + '"></i></span>'
    if unit != "":
        unit = '<span class="unit">&nbsp;' + unit + '</span>'
    css_class = ""
    if thresholds:
        if progress is None:
            err.new(number_progress,
                    "Please provide a progress number to use thresholds")
            err.throw()
        color = "green"
        if progress[0] <= thresholds["low"]:
            color = "red"
        elif progress[0] < thresholds["high"] and progress[0] > thresholds["low"]:
            color = "orange"
    if progress is not None:
        wrapper = '<div class="info-box bg-' + color + '">'
    else:
        wrapper = '<div class="info-box">'
    res = wrapper + icon + '\n<div class="info-box-content">'
    if legend is not None:
        res = res + '\n<span class="info-box-text ' + \
            css_class + '">' + legend + '</span>'
    res = res + '\n<span class="info-box-number">' + \
        str(number) + ' ' + unit + '</span>'
    if progress is not None:
        res += '<div class="progress">'
        res += '<div class="progress-bar" style="width:' + \
            str(progress[0]) + '%"></div>'
        res += '</div>'
        res += '<span class="progress-description">' + progress[1] + '</span>'
    res = res + "</div></div>"
    return res
"""


def sparkline(data):
    w = """<span class="sparkline" data-type="line" 
       data-spot-Radius="3" data-highlight-Spot-Color="#f39c12" data-highlight-Line-Color="#222" 
       data-min-Spot-Color="#f56954" data-max-Spot-Color="#00a65a" data-spot-Color="#39CCCC" 
       data-offset="90" data-width="50px" data-height="15px" data-line-Width="2" 
       data-line-Color="#39CCCC" data-fill-Color="rgba(57, 204, 204, 0.08)">"""
    w += data
    w += "</span>"
    return w
