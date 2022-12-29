from src.input_data import (get_random_wiki_page, get_wiki_page,
                            get_wiki_pageid, random_article)


def test_get_random_wiki_page():
    result = get_random_wiki_page()
    assert len(result) > 3
    assert type(result) == str


def test_get_wiki_pageid():
    result = get_wiki_pageid('Monty Python')
    assert result == '18942'


def test_get_wiki_page():
    result = get_wiki_page('18942')
    assert result['title'] == 'Monty Python'


def test_random_article():
    result = random_article()
    assert result.keys() == {'pageId', 'title', 'text'}
