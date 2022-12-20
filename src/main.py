"""
This module is used to scrape apartment data from https://bostad.stockholm.se
It uses the Selenium and BeautifulSoup to navigate the website and extract relevant information.
The apartment data is stored in a Firebase database using the firebase_admin library.
The module also has a function for sending a notification to a Discord webhook
when a new apartment matching specified filters is found.
"""

import time
import re
import os
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import firebase_admin
from firebase_admin import credentials, firestore
from google.api_core import exceptions
import requests

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("--no-sandbox")


def get_website(url, sleep=1):
    """
    Retrieve the HTML content of a website.

    This function uses the Chrome webdriver to fetch the HTML content of a website.
    The function can optionally pause for a specified number of seconds before fetching the content,
    which can be useful for allowing JavaScript on the website to fully load.

    Parameters:
    url (str): The URL of the website to retrieve.
    sleep (int, optional): The number of seconds to pause before returning the website content.

    Returns:
    BeautifulSoup: An object containing the parsed HTML content of the website.
    """

    with webdriver.Chrome(options=options) as driver:
        driver.get(url)  # Fetch url
        time.sleep(sleep)  # Wait for JS to load
        soup = BeautifulSoup(driver.page_source, "lxml")
    return soup


def get_apartment_info(apartment_id):
    """
    Retrieve detailed information about an apartment.

    This function retrieves detailed information about an apartment with the given ID from a website
    and returns the data in a dictionary.

    Parameters:
    apartment_id (str): The ID of the apartment for which to retrieve information.

    Returns:
    dict: A dictionary containing detailed information about the apartment.
    """

    apartment = {}
    url = "https://bostad.stockholm.se/bostad/" + apartment_id
    soup = get_website(url, sleep=0)

    # General info
    apartment["address"] = soup.find("div", class_="apartment-header").find("h1").text
    apartment["location"] = soup.find(class_="align-self-end").text
    apartment["last_register_date"] = soup.select_one("footer.house-footer.u-m-t span").text.strip()

    # Apartment info
    apartment_info = soup.find(class_="apartment-header__info").text
    apartment["rent"] = int(re.compile(r"Hyra:\s*(\d+)").search(apartment_info).group(1))
    apartment["level"] = re.compile(r"Våning:\s*(\d+|.+)").search(apartment_info).group(1)  # BV, 1
    apartment["rooms"] = int(re.compile(r"Antal rum:\s*(\d+)").search(apartment_info).group(1))
    apartment["square_meter"] = int(re.compile(r"Boyta:\s*(\d+)").search(apartment_info).group(1))

    # Youth related info
    age = re.search(
        r"mellan (\d+) och (\d+) år|dig som är (\d+) år",
        soup.find(class_="grid-lg-8 grid-12").text,
    )
    if age and age.group(1) and age.group(2):
        apartment["age"] = age.group(1) + "-" + age.group(2)
    elif age and age.group(3):
        apartment["age"] = age.group(3)

    tag = soup.find(class_="tag")
    if tag is not None and hasattr(tag, "text"):
        if tag.text == "Ungdom korttid":
            apartment["youth"] = True
            apartment["youth_temporary"] = True
        elif tag.text == "Ungdom":
            apartment["youth"] = True

    # Other
    apartment["link"] = url
    return apartment


def get_all_apartments(url, filters=None):
    """
    Retrieve apartment data from a website and filter it based on specified criteria.

    Parameters:
    url (str): The URL of the website from which to retrieve the data.
    filters (dict, optional): Criteria to filter the retrieved data by. Defaults to None.

    Returns:
    dict: Data for each apartment, with apartment IDs as keys.
    """
    apartments = {}
    apartments_url = get_website(url).find_all("a", class_="ad-list__link")
    for apartment in apartments_url:
        apartment_id = re.findall(r"\d+", apartment.get("href"))[0]
        apartment_data = get_apartment_info(apartment_id)
        # Check if the apartment matches the specified filters
        if not filters or all(apartment_data.get(f) == v for f, v in filters.items()):
            apartments[apartment_id] = apartment_data
    return apartments


def store_data_in_firestore(firestore_db, collection_name, doc_name, data):
    """
    Store data in a Firestore database.

    This function stores the given data in a document in the specified collection of a Firestore db.
    If a document with the same name already exists in the collection,
    the data will not be stored and the function will return False.
    Otherwise, the function will return True.

    Parameters:
    firestore_db (firestore.client): A Firestore client instance.
    collection_name (str): The name of the collection in which the data should be stored.
    doc_name (str): The name of the document in which the data should be stored.
    data (dict): The data to be stored in the document.

    Returns:
    bool: True if the data was successfully stored in the Firestore database, False otherwise.
    """

    doc_ref = firestore_db.collection(collection_name).document(doc_name)
    try:
        doc_ref.create(data)
        return True
    except exceptions.AlreadyExists:
        return False


def post_to_discord(apartment, webhook_url):
    """
    Post a message to Discord via a webhook.

    Parameters:
    apartment (dict): A dictionary containing information about an apartment.
    webhook_url (str): The URL of the Discord webhook to which the message should be posted.
    """

    message = {"content": ""}

    for key, value in apartment.items():
        # Prettify the key by capitalizing each word and replacing underscore with space
        prettified_key = " ".join([word.capitalize() for word in key.split("_")])
        message["content"] += f"{prettified_key}: {value} \n"

    requests.post(webhook_url, json=message, timeout=5)


def main():
    """
    Main function for the apartment listing program.

    This function retrieves all apartment listings from a given URL,
    stores them in a Firestore database,
    and posts a message to Discord for each apartment listing.
    """

    all_apartments = get_all_apartments(INPUT_APARTMENTS_URL, INPUT_APARTMENTS_FILTER)
    for apartment_id, apartment_data in all_apartments.items():
        if store_data_in_firestore(db, "apartment_listings", apartment_id, apartment_data):
            print(apartment_data)
            post_to_discord(apartment_data, INPUT_DISCORD_WEBHOOK_URL)


if __name__ == "__main__":
    INPUT_DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
    INPUT_APARTMENTS_URL = (
        os.environ.get("APARTMENTS_URL")
        or "https://bostad.stockholm.se/bostad/?sort=annonserad-fran-desc&ungdom=1"
    )
    INPUT_APARTMENTS_FILTER = os.environ.get("APARTMENTS_FILTER")  # Defaults to None if env not set

    if INPUT_APARTMENTS_FILTER:
        try:
            INPUT_APARTMENTS_FILTER = json.loads(INPUT_APARTMENTS_FILTER)
        except (TypeError, json.JSONDecodeError):
            raise ValueError("APARTMENTS_FILTER must be a valid JSON object")

    CRED = credentials.Certificate(json.loads(os.environ["FIREBASE_ACCOUNT"]))
    firebase_admin.initialize_app(CRED)
    db = firestore.client()

    main()
