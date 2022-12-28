import sqlalchemy as sq
import logging
import os
import pathlib


class Text_db:

    def __init__(self, db_path: pathlib.Path):
        self.db_path = db_path
        self.logger = logging.getLogger('Text_db')

        # does the db exist if not create it by connecting
        if not os.path.isfile(self.db_path):
            self.engine = sq.create_engine(f'sqlite:///{self.db_path}')
            self.logger.info(f"New database {db_path} created")
            # create the table
            with self.engine.connect() as conn:
                conn.execute(
                    'CREATE TABLE articles (pageId TEXT NOT NULL UNIQUE, title TEXT NOT NULL, text TEXT NOT NULL, PRIMARY KEY("pageId"))'
                )
            self.logger.info(f"Table articles created in {db_path}")
        else:
            self.engine = sq.create_engine(f'sqlite:///{self.db_path}')
            self.logger.info(f"Database {db_path} loaded")

    # def check if the db exists
    def db_exists(self):
        return os.path.isfile(self.db_path)

    # if the db exists return the  current number of articles
    def get_num_rows(self) -> int:
        try:
            with self.engine.connect() as conn:
                self.rows = conn.execute('SELECT COUNT(*) FROM articles')
                # read the cursor result
                self.rows = self.rows.first()[0]  # type: ignore
        except Exception as e:
            self.rows = 0
            self.logger.exception(f"Exception: {e}")
        self.logger.info(f"Database {self.db_path} has {self.rows} rows")
        return self.rows

    # insert a new article into the db
    def insert_article(self, pageId, title, text):
        with self.engine.connect() as conn:
            conn.execute(
                'INSERT INTO articles (pageId, title, text) VALUES (?, ?, ?)',
                (pageId, title, text))

    # get the text of an article
    def get_article_text(self, pageId):
        with self.engine.connect() as conn:
            self.text = conn.execute(
                'SELECT text FROM articles WHERE pageId = ?', (pageId,)).first()
            return self.text

    # remove an article from the db
    def remove_article(self, pageId):
        with self.engine.connect() as conn:
            conn.execute('DELETE FROM articles WHERE pageId = ?', (pageId,))
