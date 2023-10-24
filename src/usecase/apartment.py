from entities.apartment import Apartment
from repositories.scraper import ScraperRepository
from repositories.apartment_firestore import ApartmentFirestoreRepository
from infrastructure.discord import DiscordInfrastructure
import re

class ApartmentUseCase:
    def __init__(self, scraper_repository: ScraperRepository, apartment_repository: ApartmentFirestoreRepository, discord_infrastructure: DiscordInfrastructure):
        self.apartment_repository = apartment_repository
        self.scraper_repository = scraper_repository
        self.discord_infrastructure = discord_infrastructure

    def get_all_apartments(self, url, filter=None):
        apartment_ids = self.get_all_apartments_id(url)
        apartments = []
        for id in apartment_ids:
            apartment = self.get_apartment_data(id)
            if filter == None or (filter != None and self.apartment_matches_filter(apartment, filter)):
                apartments.append(apartment)
        return apartments

    def get_all_apartments_id(self, url):
        apartments = []
        apartments_url = self.scraper_repository.scrape(url).find_all("a", class_="ad-list__link")
        for apartment in apartments_url:
            apartment_id = re.findall(r"\d+", apartment.get("href"))[0]
            apartments.append(apartment_id)
        return apartments

    def get_apartment_data(self, apartment_id):
        apartment_url = "https://bostad.stockholm.se/bostad/" + apartment_id
        apartment_data = self.scraper_repository.scrape(apartment_url)

        # Build apartment object
        id = apartment_id
        address = apartment_data.find("div", class_="apartment-header").find("h1").text
        location = apartment_data.find(class_="align-self-end").text

        # Dont add last_register_date if house is not available to register for
        if apartment_data.select_one("footer.house-footer.u-m-t span") is not None:
            last_register_date = apartment_data.select_one(
                "footer.house-footer.u-m-t span"
            ).text.strip()
        else:
            last_register_date = None

        # Apartment info
        apartment_info = apartment_data.find(class_="apartment-header__info").text

        level = re.compile(r"Våning:\s*(\d+|.+)").search(apartment_info).group(1)  # BV, 1
        rent = int(re.compile(r"Hyra:\s*(\d+)").search(apartment_info).group(1))
        rooms = int(re.compile(r"Antal rum:\s*(\d+)").search(apartment_info).group(1))
        square_meter = int(re.compile(r"Boyta:\s*(\d+)").search(apartment_info).group(1))

        # Youth related info
        temporary = False
        age = False
        youth = False

        age = re.search(
            r"mellan (\d+) och (\d+) år|dig som är (\d+) år",
            apartment_data.find(class_="grid-lg-8 grid-12").text,
        )
        if age and age.group(1) and age.group(2):
            age = age.group(1) + "-" + age.group(2)
        elif age and age.group(3):
            age = age.group(3)

        tag = apartment_data.find(class_="tag")
        if tag is not None and hasattr(tag, "text"):
            if tag.text == "Ungdom korttid":
                youth = True
                temporary = True
            elif tag.text == "Ungdom":
                youth = True

        apartment = Apartment(id, address, location, last_register_date, level, rent, rooms, square_meter, temporary, age, youth)
        return apartment

    def apartment_matches_filter(self, apartment: Apartment, filter_dict):
        for key, value in filter_dict.items():
            if not hasattr(apartment, key):
                # Check if the key is a valid attribute of the apartment
                return False

            if getattr(apartment, key) != value:
                return False
        return True

    def store_apartment(self, apartment: Apartment):
        return self.apartment_repository.post_apartment_listing(apartment)

    def post_to_discord(self, apartment):
        self.discord_infrastructure.send_message(str(apartment))
