from pyarrow import fs

import io
from urllib.parse import urlparse
import os
from enum import Enum


class _Scheme(Enum):
    HDFS = 'hdfs'
    FILE = 'file'
    DEFAULT = ''


def read_file(path):
    scheme, host, port, path = _parse_path(path)
    if _Scheme(scheme) is _Scheme.HDFS:
        return _read_hdfs(host=host, port=port, path=path)
    else:
        return _read_local(path=path)


def write_file(buffer, path):
    scheme, host, port, path = _parse_path(path)
    if _Scheme(scheme) is _Scheme.HDFS:
        _write_hdfs(buffer=buffer, host=host, port=port, path=path)
    else:
        _write_local(buffer=buffer, path=path)


def _parse_path(path):
    p = urlparse(path)
    return p.scheme, p.hostname, p.port, os.path.abspath(p.path)


def _read_hdfs(host, port, path):
    hdfs = fs.HadoopFileSystem(host=host, port=port)
    with hdfs.open_input_stream(path) as stream:
        data = stream.read()
    return io.BytesIO(data)


def _read_local(path):
    with open(path, mode='rb') as f:
        data = f.read()
    return io.BytesIO(data)


def _write_hdfs(buffer, host, port, path):
    hdfs = fs.HadoopFileSystem(host=host, port=port)
    with hdfs.open_output_stream(path) as stream:
        stream.write(buffer.getbuffer())


def _write_local(buffer, path):
    with open(path, mode='wb') as f:
        f.write(buffer.getbuffer())
