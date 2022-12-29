# %%
from fastapi.testclient import TestClient
from src.control import add_articles_to_db, db_rows
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_read_root():
    response = client.get("/")
    assert type(response.json()) == dict


def test_return_article():
    response = client.get("/return_article/18942")
    assert response.json()['title'] == 'Monty Python'


def test_get_num_rows_in_db(db):
    response = client.get("/get_num_rows")
    assert response.json()['The number of rows in the database is: '] == db.get_num_rows()


def test_add_article_to_db_from_a_page_id():
    pass


def test_add_article_to_db_from_a_page_id(pageid: str):
    pass
    

def test_get_db_status():
    pass


def set_the_max_db_rows(rows: int):
    pass
