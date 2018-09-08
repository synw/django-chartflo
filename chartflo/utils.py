# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.utils._os import safe_join
from goerr import Err

tr = Err()


def _write_file(slug, html, ctype="chart", dashboard=None):
    """
    Writes html to a file
    """
    # check directories
    folderpath = safe_join(settings.BASE_DIR, "templates/")
    if not os.path.isdir(folderpath):
        try:
            os.makedirs(folderpath)
        except Exception as e:
            tr.err(e)
            return
    endpath = "charts"
    if ctype == "number":
        endpath = "numbers"
    elif ctype == "sparkline":
        endpath = "sparklines"
    elif ctype == "datatable":
        endpath = "datatables"
    elif ctype == "sequence":
        endpath = "sequences"
    if dashboard is not None:
        midpath = "dashboards/" + dashboard + "/"
    else:
        midpath = "/"
    chartsdir_path = safe_join(
        settings.BASE_DIR, "templates/" + midpath + endpath)
    if not os.path.isdir(chartsdir_path):
        try:
            os.makedirs(chartsdir_path)
        except Exception as e:
            tr.err(e)
            return
    # check file
    filepath = chartsdir_path + "/" + slug + ".html"
    # write the file
    try:
        filex = open(filepath, "w")
        filex.write(html)
        filex.close()
    except Exception as e:
        tr.err(e)
