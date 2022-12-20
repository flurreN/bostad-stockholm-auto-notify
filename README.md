# bostad-stockholm-auto-notify

## What is this project doing?

This project is a web scraper that extracts information about apartments from https://bostad.stockholm.se and sends notifications to a Discord webhook when a new apartment matching specified filters is found. The code uses the Selenium and BeautifulSoup libraries to navigate the website and extract relevant information. The apartment data is then stored in a free Firestore database to keep track of what has been posted to Discord.

![image](https://user-images.githubusercontent.com/4808216/208787085-6135fa42-1f6a-4e84-98d0-168d36fb35e5.png)

## Prerequisites

To use this code, you will need the following:

- A Discord webhook URL. You can create a webhook in your Discord server settings.
- A Firebase Firestore database with credentials stored as a joined line json string.

If you are running this code in a GitHub Action, you will need to set `FIREBASE_ACCOUNT` and `DISCORD_WEBHOOK_URL` as GitHub secrets.

## Inputs

- `FIREBASE_ACCOUNT`: JSON String of Firebase account credentials
- `DISCORD_WEBHOOK_URL`: Discord webhook url
- `INPUT_APARTMENTS_URL` (OPTIONAL): The URL of the apartment listing website to scrape.Defaults to `https://bostad.stockholm.se/bostad/?sort=annonserad-fran-desc&ungdom=1` if the `APARTMENTS_URL` environment variable is not set.
- `INPUT_APARTMENTS_FILTER` (OPTIONAL): A dictionary of filters to apply to the apartment listings. Defaults to `None` if the `APARTMENTS_FILTER` environment variable is not set or is not a valid JSON object.
  Example value: `{"youth": true, "age": "23"}`. Full list of available filter values.
  ```
  {
    "address": "Kristinehovsgatan 23",
    "location": "Stockholm, Södermalm",
    "last_register_date": "2022-12-20",
    "rent": 5114,
    "level": "6",
    "rooms": 1,
    "square_meter": 26,
    "age": "23",
    "youth": true,
    "youth_temporary": True,
    "link": "https://bostad.stockholm.se/bostad/202222315",
  }
  ```

## How to use

1. Clone this repository or use it as a template.
2. Set the `DISCORD_WEBHOOK_URL` and `FIREBASE_ACCOUNT` environment variables with your Discord webhook URL and Firebase credentials, respectively as Github Secrets
3. Update the `APARTMENTS_URL` and `APARTMENTS_FILTER` environment variables in the workflow if you want to override the default values for `INPUT_APARTMENTS_URL` and `INPUT_APARTMENTS_FILTER`. These has to be removed to get use the default value
4. Pipeline will trigger the script on push and on cronjob trigger

test
