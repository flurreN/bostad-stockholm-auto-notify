from bs4 import BeautifulSoup
import pytest
from src.main import get_website, get_apartment_info, get_all_apartments


@pytest.mark.parametrize(
    "url,sleep",
    [
        ("https://bostad.stockholm.se/bostad/?sort=annonserad-fran-desc&ungdom=1", 1),
        ("https://bostad.stockholm.se/bostad/202222315", 0),
    ],
)
def test_get_website(url, sleep):
    soup = get_website(url, sleep)
    assert isinstance(soup, BeautifulSoup)


@pytest.mark.parametrize(
    "apartment_id,apartment",
    [
        (
            "202222315",
            {
                "address": "Kristinehovsgatan 23",
                "location": "Stockholm, Södermalm",
                # "last_register_date": "2022-12-20",
                "rent": 5114,
                "level": "6",
                "rooms": 1,
                "square_meter": 26,
                "age": "23",
                "youth": True,
                "youth_temporary": True,
                "link": "https://bostad.stockholm.se/bostad/202222315",
            },
        ),
        (
            "202217391",
            {
                "address": "Mässvägen 10",
                "location": "Botkyrka, Tullinge",
                # "last_register_date": "2022-12-21",
                "rent": 4868,
                "level": "1",
                "rooms": 1,
                "square_meter": 20,
                "link": "https://bostad.stockholm.se/bostad/202217391",
            },
        ),
    ],
)
def test_get_apartment_info(apartment_id, apartment):
    assert get_apartment_info(apartment_id) == apartment


def test_get_all_apartments_with_filter():
    apartments = get_all_apartments(
        "https://bostad.stockholm.se/bostad?s=59.19477&n=59.40266&w=17.84077&e=18.19782&sort=annonserad-fran-desc&vanlig=1&ungdom=1",
        {"youth": True},
    )
    assert all(apartment_info["youth"] for apartment_info in apartments.values())


def test_get_all_apartments_with_filter_no_result():
    assert not get_all_apartments(
        "https://bostad.stockholm.se/bostad/?sort=annonserad-fran-desc&ungdom=1", {"age": "99"}
    )
