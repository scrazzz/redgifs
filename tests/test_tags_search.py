from redgifs import Tags

import pytest

@pytest.mark.parametrize(
    "test_input, expected",
    [
        ('tits', 'Tits'),
        ('ass', 'Ass'),
        ('cum', 'Cum'),
        ('americam', 'American'), # on-purpose
        ('japanes', 'Japanese'),  # on-purpose
        ('hitomi tanaka', 'Hitomi Tanaka'),
        ('big dick', 'Big Dick'),
        ('hige tits', 'Huge Tits'), # on-purpose
        ('alexa pearl', 'Alexa Pearl'),
        ('ava adams', 'Ava Addams'), #on-purpose
    ]
)
def test_tags_search(test_input, expected):
    searched = Tags.search(test_input)
    assert searched == expected
