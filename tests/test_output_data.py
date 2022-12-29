from src.output_data import Text_db
import pathlib
import os

test_db = Text_db(pathlib.Path('data/test.db'))
test_db_path = test_db.db_path


def test_db_exists():
    assert os.path.isfile(test_db_path) is True


# delete the test db
def test_clean_up():
    os.remove(test_db.db_path)
    assert os.path.isfile(test_db_path) is False
