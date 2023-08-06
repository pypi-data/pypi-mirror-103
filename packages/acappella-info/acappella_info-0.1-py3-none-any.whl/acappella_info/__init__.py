import os as _os

from .utils import BaseDict as _dict, csv_reader as _csv_reader
from . import json_files as _files_json, csv_files as _files_csv

__all__ = []
_path_json = _files_json.__path__[0]
_path_csv = _files_csv.__path__[0]


def get_eng_fem_split():
    json = _dict().load(_os.path.join(_path_json, 'acapella_english_fem.json'))
    return json


def get_splits_by_language_gender():
    json = _dict().load(_os.path.join(_path_json, 'acapella_all.json'))
    return json


def get_splits_by_subset():
    json = _dict().load(_os.path.join(_path_json, 'splits.json'))
    return json


def get_query_by_category():
    json = _dict().load(_os.path.join(_path_json, 'acapella_info_ordered.json'))
    return json


def get_query_by_id():
    json = _dict().load(_os.path.join(_path_json, 'acapella_info_from_ids.json'))
    return json


def get_timestamps():
    json = _dict().load(_os.path.join(_path_json, 'acapella_timestamps.json'))
    return json


def csv_gen_full_dataset():
    r"Generator which yields full_dataset.csv lines as dictionaries"
    yield from _csv_reader(_os.path.join(_path_csv, 'full_dataset.csv'))


def csv_gen_test_seen():
    r"Generator which yields test_seen.csv lines as dictionaries"
    yield from _csv_reader(_os.path.join(_path_csv, 'test_seen.csv'))


def csv_gen_test_unseen():
    r"Generator which yields test_unseen.csv lines as dictionaries"
    yield from _csv_reader(_os.path.join(_path_csv, 'test_unseen.csv'))


def csv_gen_train():
    r"Generator which yields train.csv lines as dictionaries"
    yield from _csv_reader(_os.path.join(_path_csv, 'train.csv'))


def csv_gen_val_seen():
    r"Generator which yields val_seen.csv lines as dictionaries"
    yield from _csv_reader(_os.path.join(_path_csv, 'val_seen.csv'))
