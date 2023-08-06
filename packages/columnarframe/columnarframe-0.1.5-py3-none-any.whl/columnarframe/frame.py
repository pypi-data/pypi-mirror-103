import csv

from .column import Column


class ColumnarFrame:
    def __init__(self, data=None):
        self.rows = -1
        self.data = {}
        if data is not None:
            for k, v in data.items():
                self._check_length(v)
                self.data[k] = Column(v, self.rows)

    def _check_length(self, v):
        if self.rows == -1:
            self.rows = len(v)
        elif self.rows != len(v):
            raise RuntimeError('different row count.')

    @property
    def columns(self):
        return list(self.data.keys())

    def __getitem__(self, name):
        if isinstance(name, list):
            return ColumnarFrame({k: Column(self.data[k]) for k in name})
        return self.data[name]

    def __setitem__(self, name, value):
        if isinstance(value, list):
            self._check_length(value)
        self.data[name] = Column(value, self.rows)

    def __repr__(self):
        return self.data.__repr__()

    def __len__(self):
        return self.rows

    def rename(self, columns):
        ncf = ColumnarFrame(self.data)
        for f, t in columns.items():
            ncf.data[t] = ncf.data.pop(f)
        return ncf

    def to_csv(
            self, name, *, encoding='utf-8',
            sep=',', na_rep='', index=False, header=True):
        if isinstance(name, str):
            with open(name, 'w', encoding=encoding) as f:
                self._write_csv(f, sep, na_rep, index, header)
        else:
            self._write_csv(name, sep, na_rep, index, header)

    def _write_csv(self, stream, sep, na_rep, _, header):
        w = csv.writer(stream, delimiter=sep)
        if na_rep != '':
            iters = [
                map(
                    lambda x: x if x is not None else na_rep,
                    val.to_list()
                ) for val in self.data.values()]
        else:
            iters = [self.data[k] for k in self.data.keys()]

        if header:
            w.writerow(list(self.data.keys()))
        w.writerows(zip(*iters))
