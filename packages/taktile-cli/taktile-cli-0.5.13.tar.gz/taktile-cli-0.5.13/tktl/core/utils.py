import functools
import itertools
import os
import time
from typing import List, Sequence

import pyarrow.parquet as pq  # type: ignore
from cached_property import cached_property  # type: ignore

from tktl.core.exceptions import WrongPathError


def concatenate_urls(fst_part, snd_part):
    fst_part = fst_part if not fst_part.endswith("/") else fst_part[:-1]
    template = "{}{}" if snd_part.startswith("/") else "{}/{}"
    concatenated = template.format(fst_part, snd_part)
    return concatenated


class PathParser(object):
    LOCAL_DIR = 0
    LOCAL_FILE = 1
    GIT_URL = 2
    S3_URL = 3

    @classmethod
    def parse_path(cls, path):
        if cls.is_local_dir(path):
            return cls.LOCAL_DIR

        if cls.is_local_zip_file(path):
            return cls.LOCAL_FILE

        if cls.is_git_url(path):
            return cls.GIT_URL

        if cls.is_s3_url(path):
            return cls.S3_URL

        raise WrongPathError("Given path is neither local path, nor valid URL")

    @staticmethod
    def is_local_dir(path):
        return os.path.exists(path) and os.path.isdir(path)

    @staticmethod
    def is_local_zip_file(path):
        return os.path.exists(path) and os.path.isfile(path) and path.endswith(".zip")

    @staticmethod
    def is_git_url(path):
        return (
            not os.path.exists(path)
            and path.endswith(".git")
            or path.lower().startswith("git:")
        )

    @staticmethod
    def is_s3_url(path):
        return not os.path.exists(path) and path.lower().startswith("s3:")


def lru_cache(timeout: int, maxsize: int = 128, typed: bool = False):
    def wrapper_cache(func):
        func = functools.lru_cache(maxsize=maxsize, typed=typed)(func)
        func.delta = timeout * 10 ** 9
        func.expiration = time.monotonic_ns() + func.delta

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if time.monotonic_ns() >= func.expiration:
                func.cache_clear()
                func.expiration = time.monotonic_ns() + func.delta
            return func(*args, **kwargs)

        wrapped_func.cache_info = func.cache_info
        wrapped_func.cache_clear = func.cache_clear
        return wrapped_func

    return wrapper_cache


def flatten(x: Sequence) -> List:
    return list(itertools.chain.from_iterable(x))


class DelayedLoadingFrame(object):
    def __init__(
        self,
        path: str,
        label_name: str,
        is_label: bool = False,
        profile_columns: List[str] = None,
        load_for_profiling: bool = False,
    ):
        self.path = path
        self.label_name = label_name
        self.is_label = is_label
        self.load_for_profiling = load_for_profiling
        self._reset_index = False
        self._profile_columns = profile_columns

    @property
    def profile_columns(self):
        return (
            self._profile_columns if self._profile_columns is not None else self.columns
        )

    @property
    def reset_index(self):
        return self._reset_index

    @reset_index.setter
    def reset_index(self, val):
        self._reset_index = val

    @cached_property
    def columns(self):
        return [
            c
            for c in pq.read_table(self.path, memory_map=True).column_names
            if not c.startswith("__index_level_") and c != self.label_name
        ]

    @cached_property
    def _parquet_file(self):
        return pq.ParquetFile(self.path, memory_map=True)

    @cached_property
    def schema(self):
        return next(self.to_batches()).schema

    def to_batches(self):
        if self.is_label:
            return self._parquet_file.iter_batches(columns=[self.label_name])
        return self._parquet_file.iter_batches(columns=self.columns)

    def load(self):
        if self.load_for_profiling:
            return self._load_profiling()

        if self.is_label:
            frame = pq.read_table(
                self.path, memory_map=True, columns=[self.label_name]
            ).to_pandas()
            return frame[self.label_name]
        else:
            frame = pq.read_table(self.path, memory_map=True)
            return frame.drop([self.label_name]).to_pandas()

    def _load_profiling(self):
        df = pq.read_table(
            self.path, columns=self.profile_columns, memory_map=True
        ).to_pandas()
        df.columns = [str(c) for c in df.columns]
        if self.reset_index:
            df = df.reset_index(drop=True)
        return df


def check_and_get_value(value):
    if isinstance(value, DelayedLoadingFrame):
        if value.load_for_profiling:
            return value.load()[value.profile_columns]
        return value.load()
    else:
        return value
