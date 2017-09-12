# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.utils._os import safe_join
from goerr import err
from .conf import TO_HTML


def _write_file(slug, html, ctype="chart"):
    """
    Writes a chart's html to a file
    """
    global TO_HTML
    # check directories
    folderpath = safe_join(settings.BASE_DIR, "templates/chartflo")
    if not os.path.isdir(folderpath):
        try:
            os.makedirs(folderpath)
        except Exception as e:
            err.new(e)
    endpath = "charts"
    if ctype == "number":
        endpath = "numbers"
    chartsdir_path = safe_join(
        settings.BASE_DIR, "templates/chartflo/" + endpath)
    if not os.path.isdir(chartsdir_path):
        try:
            os.makedirs(chartsdir_path)
        except Exception as e:
            err.new(e)
    # check file
    filepath = chartsdir_path + "/" + slug + ".html"
    #~ write the file
    if TO_HTML is True:
        try:
            filex = open(filepath, "w")
            filex.write(html)
            filex.close()
        except Exception as e:
            err.new(e)
