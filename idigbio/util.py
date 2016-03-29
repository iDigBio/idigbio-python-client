from __future__ import absolute_import
import hashlib


def calcFileHash(f, op=True, return_size=False):
    md5 = hashlib.md5()
    size = 0
    if op:
        with open(f, "rb") as fd:
            buf = fd.read(128)
            while len(buf) > 0:
                size += len(buf)
                md5.update(buf)
                buf = fd.read(128)
    else:
        buf = f.read(128)
        while len(buf) > 0:
            size += len(buf)
            md5.update(buf)
            buf = f.read(128)
    if return_size:
        return (md5.hexdigest(), size)
    else:
        return md5.hexdigest()
