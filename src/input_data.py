# %%
import wikipedia
import logging

wikipedia.set_lang("en")


def get_random_wiki_page(pages=2) -> list[str]:
    """Fetch a random wikipedia page title. Defaults to 2 pages
    If a single page is returnd it is a string, if multiple pages
    are returned it is a list of strings. So we always return a
    list with 2. And return the first element.

    Args:
        pages (int, optional): The number of pages titles.
        Defaults to 2.

        Returns:
            list[str]: The titles of the random pages
    """
    return wikipedia.random(pages=pages)[0]


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
        page = {'pageId': f"PageId{pageid} not found",
                'title': f"PageId{pageid} not found",
                'text': f"PageId{pageid} not found"}

    return page


if __name__ == "__main__":
    print(get_wiki_page())

# %%
