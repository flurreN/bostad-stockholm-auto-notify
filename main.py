from src.repositories.apartment_firestore import ApartmentFirestoreRepository
from src.usecase.apartment import ApartmentUseCase
from src.infrastructure.discord import DiscordInfrastructure
from src.repositories.scraper import ScraperRepository
from firebase_admin import firestore, initialize_app, credentials

import os
import json

def main():
    scraper_repository = ScraperRepository()
    apartment_repository = ApartmentFirestoreRepository(db)
    discord_infra = DiscordInfrastructure(INPUT_DISCORD_WEBHOOK_URL)
    apartment_usecase = ApartmentUseCase(scraper_repository, apartment_repository, discord_infra)

    apartments = apartment_usecase.get_all_apartments(INPUT_APARTMENTS_URL, INPUT_APARTMENTS_FILTER)
    for apartment in apartments:
       if apartment_usecase.store_apartment(apartment) == True:
           apartment_usecase.post_to_discord(apartment)

if __name__ == "__main__":
    INPUT_DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
    INPUT_APARTMENTS_URL = (
        os.environ.get("APARTMENTS_URL")
        #or "https://bostad.stockholm.se/bostad/?sort=annonserad-fran-desc&ungdom=1"
        or "https://bostad.stockholm.se/bostad/?sort=annonserad-fran-desc&ungdom=1&s=59.33489&n=59.34250&w=18.04110&e=18.05474&hide-filter=true"
    )
    INPUT_APARTMENTS_FILTER = os.environ.get("APARTMENTS_FILTER")  # Defaults to None if env not set
    if INPUT_APARTMENTS_FILTER:
        try:
            INPUT_APARTMENTS_FILTER = json.loads(INPUT_APARTMENTS_FILTER)
        except (TypeError, json.JSONDecodeError):
            raise ValueError("APARTMENTS_FILTER must be a valid JSON object")

    FIRESTORE_CRED = credentials.Certificate(json.loads(os.environ["FIREBASE_ACCOUNT"]))
    initialize_app(FIRESTORE_CRED)
    db = firestore.client()

    main()
