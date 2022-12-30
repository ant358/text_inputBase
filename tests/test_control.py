import pathlib
import os
from src.output_data import Text_db
from src.control import (Max_rows, DB_rows, status, fill_db)

# check if the db exists
if pathlib.Path('data/test.db').exists():
    # remove the db
    os.remove('data/test.db')

db = Text_db(pathlib.Path('data/test.db'))
db_rows = DB_rows(10)
max_rows = Max_rows(10)


def test_get_max_rows():
    assert max_rows.get() >= 0


def test_set_max_rows():
    max_rows.set(15)
    assert max_rows.get() == 15


def test_get_db_rows():
    assert db_rows.get() >= 0


def test_set_db_rows():
    db_rows.set(15)
    assert db_rows.get() == 15


def test_status():
    assert status(db_rows, db) in ['filling', 'ready', 'error']


def test_fill_db():
    prefill = db.get_num_rows()
    fill_db(db)
    assert db.get_num_rows() == prefill + 1
