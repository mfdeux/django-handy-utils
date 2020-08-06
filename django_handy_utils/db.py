import functools

from django.contrib.postgres.indexes import GinIndex


class UpperGinIndex(GinIndex):
    def create_sql(self, model, schema_editor, using=""):
        statement = super().create_sql(model, schema_editor, using=using)
        quote_name = statement.parts["columns"].quote_name

        def upper_quoted(column):
            return f"UPPER({quote_name(column)})"

        statement.parts["columns"].quote_name = upper_quoted
        return statement


def nest_statement(item):
    output = {}
    for key, value in item.items():
        path = key.split(".")
        target = functools.reduce(lambda d, k: d.setdefault(k, {}), path[:-1], output)
        target[path[-1]] = value
    return output


def dictfetchall(cursor, nest_dict: bool = False):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    dict_cursor = [dict(zip(columns, row)) for row in cursor.fetchall()]

    if nest_dict:
        nested_dict_cursor = []
        for item in dict_cursor:
            nested_item = nest_statement(item)
            nested_dict_cursor.append(nested_item)
        return nested_dict_cursor
    else:
        return dict_cursor
