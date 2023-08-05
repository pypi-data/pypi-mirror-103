import csv
from .frame import ColumnarFrame


def make_key(idx, key):
    if key is None or key == '':
        return str(idx)
    return key


def read_csv(
        filename,
        encoding='utf-8',
        delimiter=',',
        skiprows=0,
        skipfooter=0,
        header=True,
        quotechar='"',
        doublequote=True,
        escapechar=None,
        ):

    with open(filename, 'r', encoding=encoding) as f:
        csvdata = csv.reader(
            f,
            delimiter=delimiter,
            quotechar=quotechar,
            doublequote=doublequote,
            escapechar=escapechar)

        rit = iter(csvdata)
        if skiprows > 0:
            for _ in range(skiprows):
                next(rit)

        data = None
        if header:
            row = next(rit)
            head = [make_key(idx, key) for idx, key in enumerate(row)]
            data = {key: [] for key in head}

        for row in rit:
            if data is None:
                head = [str(i) for i in range(len(row))]
                data = {key: [] for key in head}

            for key, value in zip(head, row):
                if len(value) == 0:
                    value = None
                data[key].append(value)

        if skipfooter > 0:
            data = {k: v[:-skipfooter] for k, v in data.items()}

    return ColumnarFrame(data)
