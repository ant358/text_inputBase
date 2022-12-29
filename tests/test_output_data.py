from src.output_data import Text_db
import pathlib
import os

test_db = Text_db(pathlib.Path('data/test.db'))
test_db_path = test_db.db_path

test_article = {
    'pageId': '12345',
    'title': 'Test Article',
    'text': 'This is a test article.'
}


def test_db_exists():
    assert os.path.isfile(test_db_path) is True


def test_insert_article():
    test_db.insert_article(test_article['pageId'], test_article['title'],
                           test_article['text'])
    assert test_db.get_num_rows() == 1


def test_get_article_text():
    assert test_db.get_article_text(
        test_article['pageId']) == test_article['text']


def test_get_all_pageids():
    assert test_db.get_all_pageids() == [test_article['pageId']]


def test_get_num_rows():
    assert test_db.get_num_rows() == 1


def test_remove_article():
    test_db.remove_article(test_article['pageId'])
    assert test_db.get_num_rows() == 0


# delete the test db
def test_clean_up():
    os.remove(test_db.db_path)
    assert os.path.isfile(test_db_path) is False
