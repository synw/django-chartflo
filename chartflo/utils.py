# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.utils._os import safe_join
from goerr import err
from .conf import TO_HTML, TO_JSON


def _write_json(slug, json):
    """
    Writes a chart to Vega Lite json format to a file
    """
    # check paths
    folderpath = safe_join(settings.BASE_DIR, "templates/chartflo")
    if not os.path.isdir(folderpath):
        try:
            os.makedirs(folderpath)
        except Exception as e:
            err.new(e)
    folderpath = safe_join(settings.BASE_DIR, "templates/chartflo/json")
    if not os.path.isdir(folderpath):
        try:
            os.makedirs(folderpath)
        except Exception as e:
            err.new(e)
    folderpath = safe_join(settings.BASE_DIR, "templates/chartflo/json/charts")
    if not os.path.isdir(folderpath):
        try:
            os.makedirs(folderpath)
        except Exception as e:
            err.new(e)
    # gen json
    endpath = "charts"
    chartsdir_path = safe_join(
        settings.BASE_DIR, "templates/chartflo/json/" + endpath)
    filepath = chartsdir_path + "/" + slug + ".json"
    #~ write the file
    if TO_JSON is True:
        try:
            filex = open(filepath, "w")
            filex.write(json)
            filex.close()
        except Exception as e:
            err.new(e)


def _write_file(slug, html, ctype="chart"):
    """
    Writes a chart's html to a file
    """
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
