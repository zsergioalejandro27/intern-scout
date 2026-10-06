import pytest

from src.processing.geo import PRIORITY_COUNTRIES, TARGET_COUNTRIES, detect_country


@pytest.mark.parametrize(
    "location, expected",
    [
        ("Berlin", "Germany"),
        ("Parsdorf, Bavaria", "Germany"),
        ("München", "Germany"),
        ("Munich", "Germany"),
        ("Zürich", "Switzerland"),
        ("Genève", "Switzerland"),
        ("Wien, Österreich", "Austria"),
        ("Linz", "Austria"),
        ("Stockholm", "Sweden"),
        ("Malmö", "Sweden"),
        ("Oslo, Norway", "Norway"),
        ("København", "Denmark"),
        ("Helsinki", "Finland"),
        ("Remote, Germany", "Germany"),
    ],
)
def test_detects_target_countries(location, expected):
    assert detect_country(location) == expected


@pytest.mark.parametrize("location", ["Paris, France", "London", "Remote", "", None])
def test_unknown_or_out_of_scope_locations_return_none(location):
    assert detect_country(location) is None


def test_priority_countries_are_all_targets_except_germany():
    assert PRIORITY_COUNTRIES == TARGET_COUNTRIES - {"Germany"}
