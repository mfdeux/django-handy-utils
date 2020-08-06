import datetime
import decimal
import json
import typing
import uuid
from json import JSONEncoder

import numpy
import pandas as pd


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        if isinstance(obj, decimal.Decimal):
            return float(obj)

        if isinstance(obj, pd.Interval):
            if obj.left == float("-inf"):
                return f"-{obj.right}"
            if obj.right == float("inf"):
                return f"{obj.left}+"
            return f"{obj.left}-{obj.right}"

        if isinstance(obj, uuid.UUID):
            return str(obj)

        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()

        if isinstance(obj, numpy.generic):
            return numpy.asscalar(obj)

        if isinstance(obj, numpy.ndarray):
            return obj.to_list()

        if isinstance(obj, float) and numpy.isnan(obj):
            return "null"

        if isinstance(obj, numpy.integer):
            return int(obj)

        elif isinstance(obj, numpy.floating):
            return float(obj)

        return super().default(obj)


def remap_keys(mapping, value_name="value"):
    return [{"group": k, value_name: v} for k, v in mapping.items()]


def remap_timeseries(mapping, value_name="value"):
    return [{"date": k, value_name: v} for k, v in mapping.items()]


def convert_numpy_objects(dict_to_convert: typing.Dict) -> typing.Dict:
    new = {}
    for k, v in dict_to_convert.items():
        if isinstance(v, dict):
            new[k] = convert_numpy_objects(v)
        else:
            if isinstance(v, float) and (numpy.isnan(v) or numpy.isinf(v)):
                new[k] = None
            else:
                new[k] = v
    return new


def json_dumps(rmd):
    if isinstance(rmd, dict):
        rmd_new = convert_numpy_objects(rmd)
    elif isinstance(rmd, list):
        rmd_new = [convert_numpy_objects(item) for item in rmd]
    else:
        rmd_new = rmd
    return json.dumps(rmd_new, cls=CustomJSONEncoder, allow_nan=False)


def json_loads(rmd):
    return json.loads(json_dumps(rmd))
