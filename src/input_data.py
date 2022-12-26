# %%
import wikipedia
import logging

wikipedia.set_lang("en")
logger = logging.getLogger("input_data")


def get_random_wiki_page() -> str:
    """Fetch a random wikipedia page title. Set to pages=1
    A single page is returnd as a string, if multiple pages
    are returned it is a list of strings. So we always return a
    str.

    Returns:
        str: The titles of the random page
    """
    try:
        # get title and force a str return
        return str(wikipedia.random(pages=1))
    except Exception as e:
        logger.exception(f"Exception: {e}")
        return "Random page title not found"


def get_wiki_pageid(title="Monty Python") -> str:
    """Fetch a specific wikipedia page id

    Args:
        title (str): The title of the page

    Returns:
        str: The page id
    """
    try:
        pageid = wikipedia.page(title).pageid
        logging.info(f"PageId {title} returned")

    except wikipedia.exceptions.DisambiguationError as e:
        pageid = wikipedia.page(e.options[0]).pageid
        logging.exception(f"DisambiguationError: {e.options}, using {e.options[0]}")

    except wikipedia.exceptions.PageError as e:
        logging.exception(f"PageError: {e}")
        pageid = f"PageId{title} not found"

    return pageid


def get_wiki_page(
    pageid="18942",
) -> dict[str, str]:
    """Fetch a specific wikipedia page content
    using the page id

    Args:
        pageid (str): The title of the page

    Returns:
        dict[str, str]: The page id, title and text
    """
    try:
        page = {'pageId': wikipedia.page(pageid=pageid).pageid,
                'title': wikipedia.page(pageid=pageid).title,
                'text': wikipedia.page(pageid=pageid).content}
        logging.info(f"Page {pageid} returned")

    except wikipedia.exceptions.PageError as e:
        logging.exception(f"PageError: {e}")
        page = {'pageId': f"{pageid}",
                'title': f"PageId {pageid} not found",
                'text': f"PageId {pageid} not found"}

    return page


def random_article() -> dict[str, str]:
    """Fetch a random wikipedia page content
    using a random page id, and format the output
    for the database.

    Returns:
        dict[str, str]: The page id, title and text
    """
    page_title = get_random_wiki_page()
    pageID = get_wiki_pageid(page_title)
    return get_wiki_page(pageid=pageID)


if __name__ == "__main__":
    print(get_wiki_page())

# %%
