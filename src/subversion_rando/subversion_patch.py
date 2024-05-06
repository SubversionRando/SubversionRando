import logging
import os
from pathlib import Path
from typing import Union
from urllib.request import urlopen
from hashlib import sha256

_mem_cache: Union[bytes, None] = None

_FILE_NAME = "subversion.1.2.ips"
_PATCH_SHA256 = "0c0e0b2f8d034d44f7e2a3d7aace9f35801344a095c0b256453902d43a5a9f6f"


def _https_fetch() -> Union[bytes, None]:
    try:
        with urlopen("https://edit-sm.art/subversion/patches/subversion.1.2.ips") as response:
            if response.getcode() == 200:
                data = response.read()
                if sha256(data).hexdigest() == _PATCH_SHA256:
                    return data
                logging.warning("WARNING: https://edit-sm.art/subversion has been tampered with")
            return None
    except Exception:
        return None


def _fs_cache_get(cache_directory: Union[str, Path]) -> Union[bytes, None]:
    cache_directory = Path(cache_directory)
    if not cache_directory.exists():
        os.makedirs(cache_directory)
    if not cache_directory.is_dir():
        return None
    file_path = cache_directory / _FILE_NAME
    if not file_path.exists():
        return None
    with open(file_path, "rb") as file:
        data = file.read()
    if sha256(data).hexdigest() == _PATCH_SHA256:
        return data
    logging.warning("WARNING: file cache has been tampered with")
    return None


def _fs_store(data: bytes, cache_directory: Union[str, Path]) -> None:
    file_path = Path(cache_directory) / _FILE_NAME
    if file_path.exists():
        return
    with open(file_path, "wb") as file:
        file.write(data)


def get(cache_directory: Union[str, Path] = ".") -> Union[bytes, None]:
    """
    gets the Subversion 1.2 patch data
    from the memory cache, or from a file system cache,
    or from the Subversion website
    """
    # Note: The web interface uses a py-script directive
    # to place the patch in the file system cache location.
    # So this code will find it when it looks in the file system cache.
    global _mem_cache
    if _mem_cache:
        return _mem_cache
    data = _fs_cache_get(cache_directory)
    if data:
        _mem_cache = data
        return data
    data = _https_fetch()
    if data:
        _mem_cache = data
        _fs_store(data, cache_directory)
    return _mem_cache
