import builtins
from pathlib import Path

import requests

real_open = builtins.open


def fake_open(*args, **kwargs):
    if _is_need_url_open(*args, **kwargs):
        return UrlOpen(*args, **kwargs)
    else:
        return real_open(*args, **kwargs)


def _is_need_url_open(file, *args, **kwargs):
    from settings import config
    # /share_data/
    target_path = config.DP_SHARE_DATA_DIR
    flag = isinstance(file, str) and file.startswith(target_path)
    return flag


class UrlOpen(object):
    BASE_URL = ''

    def __init__(self, file, mode='r', *args, **kwargs):
        self.file = file
        self.filename = Path(file).name
        self.url = self.BASE_URL + self.filename
        self.mode = mode
        self.args = args
        self.kwargs = kwargs

    def read(self) -> bytes:
        print(f'read file from {self.url}')
        return requests.get(self.url).content

    def write(self, _bytes: bytes):
        print(f'write file to {self.url}')
        # 发送文件
        requests.post(self.url, data=_bytes)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def patch_open(host='http://host.docker.internal:5088/'):
    builtins.open = fake_open
    UrlOpen.BASE_URL = host
    print(f'替换open, host={host}')


def reset_open():
    builtins.open = real_open
    print('重置open')
