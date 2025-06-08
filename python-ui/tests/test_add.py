import pytest


@pytest.fixture
def name():
    name = "Emmanuel"
    return f"Name: {name}"


def test_my_name():
    assert 1 == 1


def test_another_name(name):
    assert name == "Name: Emmanuel"


def test_n():
    assert True