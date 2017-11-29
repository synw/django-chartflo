

def number(number, legend=None, unit=None, icon=None, color="green"):
    if unit is None:
        unit = ""
    ibg = " bg-" + color
    if icon is None:
        icon = '<span class="info-box-icon' + ibg + \
            '"><i class="fa fa-thumbs-o-up"></i></span>'
    else:
        icon = '<span class="info-box-icon' + ibg + \
            '"><i class="fa fa-' + icon + '"></i></span>'
    if unit != "":
        unit = '<span class="unit">&nbsp;' + unit + '</span>'
    wrapper = '<div class="info-box">'
    res = wrapper + icon + '\n<div class="info-box-content">'
    css_class = ""
    if legend is not None:
        res = res + '\n<span class="info-box-text ' + \
            css_class + '">' + legend + '</span>'
    res = res + '\n<span class="info-box-number">' + \
        str(number) + ' ' + unit + '</span>'
    res = res + "</div></div>"
    return res