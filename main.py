# note does not run in jupyter notebook, run in the terminal
from fastapi import FastAPI
import uvicorn
import logging
import os
import pathlib
from datetime import datetime
from src.input_data import get_wiki_page
from src.output_data import Text_db
from src.control import (status, fill_db, Max_rows, DB_rows)

# setup logging
# get todays date
datestamp = datetime.now().strftime('%Y%m%d')
# get the container name used in the Dockerfile
container_name = os.getenv('CONTAINER_NAME')
# append date to logfile name
log_name = f'log-{container_name}-{datestamp}.txt'
path = os.path.abspath('./logs/')
# add path to log_name to create a pathlib object
# required for loggin on windows and linux
log_filename = pathlib.Path(path, log_name)

# create log file if it does not exist
if os.path.exists(log_filename) is not True:
    # create the logs folder if it does not exist
    if os.path.exists(path) is not True:
        os.mkdir(path)
    # create the log file
    open(log_filename, 'w').close()

# create logger
logger = logging.getLogger()
# set minimum output level
logger.setLevel(logging.DEBUG)
# Set up the file handler
file_logger = logging.FileHandler(log_filename)

# create console handler and set level to debug
ch = logging.StreamHandler()
# set minimum output level
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter('[%(levelname)s] -'
                              ' %(asctime)s - '
                              '%(name)s : %(message)s')
# add formatter
file_logger.setFormatter(formatter)
ch.setFormatter(formatter)
# add a handler to logger
logger.addHandler(file_logger)
logger.addHandler(ch)
# mark the run
logger.info(f'Lets get started! - logginng in "{log_filename}" today')

# create the FastAPI app
app = FastAPI()

# load the database
db_path = pathlib.Path('data/text.db')

db = Text_db(db_path)
# limit the max size that can be set
max_rows = Max_rows(10000)

# set the db rows
db_rows = DB_rows(1000)


# fill the database
def add_articles_to_db(db):
    """Fill the database to the set level"""
    if db.get_num_rows() < max_rows.get():
        while db.get_num_rows() < db_rows.get():
            # insert the articles into the db
            fill_db(db)
            # log the progress
            logger.debug(f"DB rows: {db.get_num_rows()}")
        logger.info(f"Database rows filled - now: {db.get_num_rows()}")
    else:
        logger.info(f"Database rows at maxium - now: {db.get_num_rows()}")


# fill the database to the set level
add_articles_to_db(db)


# OUTPUT- routes
@app.get("/")
async def root_infomation():
    """Get the root information"""
    logging.info("Root requested")
    return {
        "API Root": (
            f"This in the container ({os.getenv('CONTAINER_NAME')}) that manages the input text database.\
             This database acts as aource of text for the other containers.")
    }


# return the a wikipedia page object
@app.get("/return_article/{pageid}")
async def return_wiki_page_from_a_pageid(pageid: str):
    """Get the text content of a Wikipedia page from its pageid"""
    logging.info(f"Page {pageid} requested")
    return get_wiki_page(pageid)


# add a page to the database
@app.get("/add_article/{pageid}")
async def add_article_to_db_from_a_page_id(pageid: str):
    """Use a pageid to manually add a Wikipedia page to the database"""
    page = get_wiki_page(pageid)
    db.insert_article(page['pageId'], page['title'], page['text'])
    logging.info(f"Page {pageid} added")
    return {f"Page {pageid} added to the database": page}


# return the number of rows in the database
@app.get("/get_num_rows")
async def get_num_rows_in_db():
    """Get the number of rows in the database"""
    logging.info("Number of rows requested")
    return {"The number of rows in the database is: ": db.get_num_rows()}


# return the db status
@app.get("/get_db_status")
async def get_db_status():
    """Get the status of the database"""
    logging.info("Database status requested")
    return {"The database status is: ": status(db_rows=db_rows, db=db)}


# return the list of pageids in the database
@app.get("/get_pageids")
async def get_pageids():
    """Get the list of pageids in the database"""
    logging.info("Pageids requested")
    return {"pageids: ": db.get_all_pageids()}


# INPUT routes
# set the db rows
@app.post("/set_db_rows/{rows}")
async def set_the_max_db_rows(rows: int):
    """Set the number of rows in the database, and fill the database to that level"""
    db_rows.set(rows)
    add_articles_to_db(db)
    logging.info(f"Set db rows to {rows}")
    return {"The total number of db rows has been set to: ": db_rows.get()}


if __name__ == "__main__":
    # goto localhost:8080/
    # or localhost:8080/docs for the interactive docs
    uvicorn.run(app, port=8080, host="0.0.0.0")
