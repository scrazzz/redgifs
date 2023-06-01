import pytest

from redgifs import Tags

@pytest.mark.parametrize(
    "test_input, expected",
    [
        ('tits', 'Tits'),
        ('ass', 'Ass'),
        #('cum', 'Cum'),
        ('americam', 'American'),
        ('japanes', 'Japanese'),
        ('hitomi tanaka', 'Hitomi Tanaka'),
        ('big dick', 'Big Dick'),
        ('hige tits', 'Huge Tits'),
        ('alexa pearl', 'Alexa Pearl'),
        ('ava adams', 'Ava Addams'),
    ]
)
def test_tags_search(test_input, expected):
    searched = Tags().search(test_input)[0]
    assert searched == expected