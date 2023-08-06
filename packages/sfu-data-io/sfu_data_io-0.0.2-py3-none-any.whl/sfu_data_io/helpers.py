import glob
import io
import os
import pickle
import re
import tempfile
from contextlib import contextmanager
from typing import Optional, List, Tuple, Union, Generator, IO, Any
from urllib.parse import urlparse

import boto3
import numpy as np
import s3fs


def get_bucket_and_key(path: str) -> Tuple[str, str]:
    url = urlparse(path)

    return url.netloc, url.path.strip('/')


def download_s3(bucket: str, key: str, destination: str) -> None:
    directory, _ = os.path.split(destination)

    os.makedirs(directory, exist_ok=True)

    boto3.client('s3').download_file(Bucket=bucket, Key=key, Filename=destination)


def put_s3(bucket: str, key: str, reader: io.BytesIO) -> None:
    boto3.client('s3').upload_fileobj(Fileobj=reader, Bucket=bucket, Key=key)


def get_s3_keys(bucket: str, prefix: str = '') -> List[str]:
    object_list = boto3.client('s3').list_objects_v2(Bucket=bucket, Prefix=prefix)

    if 'Contents' not in object_list:
        return []

    keys = [file['Key'] for file in object_list['Contents']]

    return keys


def get_local_files(path: str) -> List[str]:
    paths = [
        path
        for path in glob.glob(os.path.join(path, '**'), recursive=True)
        if os.path.isfile(path)
    ]

    return paths


def get_files(path: str) -> List[str]:
    if not path.startswith('s3'):
        return get_local_files(path)

    bucket, prefix = get_bucket_and_key(path)

    paths = [f's3://{os.path.join(bucket, key)}' for key in get_s3_keys(bucket, prefix)]

    return paths


def exists(path: str) -> bool:
    if not path.startswith('s3'):
        return os.path.exists(path)

    bucket, key = get_bucket_and_key(path)

    return len(get_s3_keys(bucket, key)) > 0


def get_relative_path(shallow_path: str, deep_path: str) -> str:
    return re.sub('^' + shallow_path, '', deep_path).lstrip('/')


def get_file_in_directory(directory: str, file: str, base: str) -> str:
    return os.path.join(directory, os.path.relpath(file, base))


def upload_s3(source: str, bucket: str, key: str) -> None:
    boto3.client('s3').upload_file(Filename=source, Bucket=bucket, Key=key)


def get_temporary_local_directory_path() -> str:
    return tempfile.mkdtemp()


def get_temporary_local_path() -> str:
    return tempfile.mkstemp()[1]


def get_relative_path_in_directory(directory: str, shallow_path: str, deep_path: str) -> str:
    return os.path.join(directory, get_relative_path(shallow_path, deep_path))


def get_local_directory_path(path: str, directory: Optional[str] = None, prefix: Optional[str] = None) -> str:
    path_prefixed = os.path.join(path, prefix) if prefix else path

    if not path.startswith('s3'):
        return path_prefixed

    directory = get_temporary_local_directory_path() if directory is None else directory
    directory_prefixed = os.path.join(directory, prefix) if prefix else directory

    bucket, key_base = get_bucket_and_key(path)
    key_base_prefixed = os.path.join(key_base, prefix) if prefix else key_base

    for key in get_s3_keys(bucket, key_base_prefixed):
        download_s3(bucket, key, get_file_in_directory(directory, key, key_base))

    return directory_prefixed


def get_local_prefix_path(path: str, directory: Optional[str] = None) -> str:
    path, prefix = os.path.split(path)

    local_path_prefixed = get_local_directory_path(path, directory, prefix)

    return local_path_prefixed


def get_local_path(path: str) -> str:
    if not path.startswith('s3'):
        return path

    bucket, key = get_bucket_and_key(path)

    local_path = get_temporary_local_path()

    download_s3(bucket, key, local_path)

    return local_path


def load_npy(path: str, mmap_mode: Optional[str] = None) -> np.ndarray:
    return np.load(get_local_path(path), mmap_mode=mmap_mode)


def load_bin(path: str, dtype=np.uint8, mode: str = 'r+', shape: List[int] = None) -> np.ndarray:
    return np.memmap(get_local_path(path), dtype, mode, shape=shape)


@contextmanager
def open(
        path: str,
        mode: str = 'rb',
        encoding: Optional[str] = None,
        newline: Optional[str] = None) -> Generator[IO, None, None]:

    open_function = s3fs.S3FileSystem.current().open if path.startswith('s3') else io.open

    with open_function(path, mode=mode, encoding=encoding, newline=newline) as file_object:
        yield file_object


@contextmanager
def with_local_path(path: str) -> Generator[str, None, None]:
    local_path = get_temporary_local_path() if path.startswith('s3') else path

    yield local_path

    if path.startswith('s3'):
        bucket, key = get_bucket_and_key(path)
        upload_s3(local_path, bucket, key)


@contextmanager
def with_local_directory_path(path: str) -> Generator[str, None, None]:
    local_path = get_temporary_local_directory_path() if path.startswith('s3') else path

    yield local_path

    if path.startswith('s3'):
        sync_remote(local_path, path)


def read(path: str, encoding: Optional[str] = None) -> Union[bytes, str]:
    if not path.startswith('s3'):
        if encoding:
            return io.open(path, mode='r', encoding=encoding).read()
        else:
            return io.open(path, mode='rb').read()

    bucket, key = get_bucket_and_key(path)

    content = boto3.client('s3').get_object(Bucket=bucket, Key=key)['Body'].read()

    if encoding:
        return content.decode(encoding)

    return content


def save_npy(path: str, data: np.ndarray) -> None:
    if not path.startswith('s3'):
        np.save(path, data)

    else:
        bucket, key = get_bucket_and_key(path)

        with io.BytesIO() as writer:
            np.save(writer, data)

            writer.seek(0)

            put_s3(bucket, key, writer)


def save_pickle(path: str, data: Any) -> None:
    if not path.startswith('s3'):
        with io.open(path, mode='wb') as file:
            pickle.dump(data, file)

    else:
        bucket, key = get_bucket_and_key(path)

        with io.BytesIO() as writer:
            pickle.dump(data, writer)

            writer.seek(0)

            put_s3(bucket, key, writer)


def sync_remote(local_path: str, remote_path: str) -> None:
    paths = (path for path in glob.glob(os.path.join(local_path, '**'), recursive=True) if os.path.isfile(path))

    for path in paths:
        path_in_remote_path = get_relative_path_in_directory(remote_path, local_path, path)

        upload(path, path_in_remote_path)


def upload(source: str, destination: str) -> None:
    if not destination.startswith('s3'):
        raise IOError(f'Destination path {destination} not supported.')

    bucket, key = get_bucket_and_key(destination)

    upload_s3(source, bucket, key)
