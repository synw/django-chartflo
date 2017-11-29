import pandas as pd
from goerr import err
from dataswim import ds
from django.db.models.query import QuerySet


def _check_fields(x, y):
    """
    Check if X and Y field are set
    """
    if x is None:
        if ds.x is None:
            err.new(_check_fields,
                    "No X field set: please pass one as parameter")
            return
        ds.x = x
    if y is None:
        if ds.y is None:
            err.new(_check_fields,
                    "No Y field set: please pass one as parameter")
        ds.y = y


def _dict_to_df(dictobj, xfield, yfield):
    """
    Converts a dictionnary to a pandas dataframe
    """
    x = []
    y = []
    for datapoint in dictobj:
        x.append(datapoint)
        y.append(dictobj[datapoint])
    if type(xfield) == tuple:
        xfield = xfield[0]
    if type(yfield) == tuple:
        yfield = yfield[0]
    df = pd.DataFrame({xfield: x, yfield: y})
    return df


def convert_dataset(dataset, x=None, y=None):
    """
    Convert the input data to pandas dataframe
    """
    if type(x) == tuple:
        x = x[0]
    if type(y) == tuple:
        y = y[0]
    try:
        _check_fields(x, y)
    except Exception as e:
        err.new(e, convert_dataset, "Can not find fields", x, y)
        err.throw()
    try:
        if isinstance(dataset, pd.DataFrame):
            return dataset
        elif isinstance(dataset, QuerySet):
            x_vals = []
            y_vals = []
            for row in list(dataset.values()):
                try:
                    y_vals.append(row[y])
                except:
                    y_vals.append(1)
                x_vals.append(row[x])
            dataset = pd.DataFrame({x: x_vals, y: y_vals})
        elif isinstance(dataset, dict):
            dataset = _dict_to_df(dataset, x, y)
        elif isinstance(dataset, list):
            return pd.DataFrame(dataset)
        else:
            err.new(convert_dataset,
                    "Data format unknown: "
                    + str(type(dataset)) +
                    " please provide a dictionnary, a Django Queryset or a Pandas DataFrame")
            err.throw()
    except Exception as e:
        err.new(e, convert_dataset, "Can not convert dataset")
        err.throw()
    return dataset
