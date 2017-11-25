def number_progress(number, legend=None, unit="", thresholds={}, icon=None, color="green", progress=0):
    if icon is None:
        icon = '<span class="info-box-icon"><i class="fa fa-thumbs-o-up"></i></span>'
    else:
        icon = '<span class="info-box-icon"><i class="fa fa-' + icon + '"></i></span>'
    if unit != "":
        unit = '<span class="unit">&nbsp;' + unit + '</span>'
    css_class = ""
    if thresholds:
        color = "green"
        if progress[0] <= thresholds["low"]:
            color = "red"
        elif progress[0] < thresholds["high"] and progress[0] > thresholds["low"]:
            color = "orange"
    wrapper = '<div class="info-box bg-' + color + '">'
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