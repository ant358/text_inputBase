from src import input_data
import logging
import pathlib
from src.output_data import Text_db

db = Text_db(pathlib.Path('data/text.db'))

logger = logging.getLogger('Control')


# control the max rows allowed in the db
class Max_rows:
    def __init__(self, max_rows: int):
        self.max_rows = max_rows

    def get(self):
        return self.max_rows

    def set(self, max_rows: int):
        self.max_rows = max_rows

    def __str__(self):
        return f"Max_rows: {self.max_rows}"


class DB_rows:

    def __init__(self, db_rows: int):
        self.db_rows = db_rows

    def get(self):
        return self.db_rows

    def set(self, db_rows: int):
        self.db_rows = db_rows

    def __str__(self):
        return f"DB_rows: {self.db_rows}"


# set the control status
def status(db_rows: DB_rows, db: Text_db) -> str:
    try:
        return 'filling' if db.get_num_rows() < db_rows.get() else 'ready'
    except Exception as e:
        logger.exception(f"Exception: {e}")
        return 'error'


def fill_db(db):
    try:
        # get the articles
        article = input_data.random_article()
        # insert the articles into the db
        db.insert_article(article['pageId'], article['title'], article['text'])
    except Exception as e:
        logger.exception(f"Exception: {e}")
        db.status = 'error'
