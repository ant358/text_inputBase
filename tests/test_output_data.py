import pathlib
import sqlalchemy as sq
import os
from src.output_data import Text_db


# check if the db exists
if pathlib.Path('data/test.db').exists():
    # remove the db
    os.remove('data/test.db')

test_db = Text_db(pathlib.Path('data/test.db'))
test_db_path = test_db.db_path

test_article = {
    'pageId': '12345',
    'title': 'Test Article',
    'text': 'This is a test article.'
}


def test_db_exists():
    assert test_db.db_exists() is True


def test_db_engine():
    assert type(test_db.engine) == sq.engine.base.Engine


def test_insert_article():
    test_db.insert_article(test_article['pageId'], test_article['title'],
                           test_article['text'])
    assert test_article['pageId'] in test_db.get_all_pageids()


def test_get_article_text():
    assert test_db.get_article_text(
        test_article['pageId']) == test_article['text']


def test_get_all_pageids():
    assert test_article['pageId'] in test_db.get_all_pageids()


def test_get_num_rows():
    assert test_db.get_num_rows() >= 0


def test_remove_article():
    before = test_db.get_num_rows()
    test_db.remove_article(test_article['pageId'])
    assert test_db.get_num_rows() == before - 1


# delete the test db
def test_clean_up():
    os.remove(test_db.db_path)
    assert os.path.isfile(test_db_path) is False
