import os

from google.api_core import exceptions

from src.entities.apartment import Apartment

class ApartmentFirestoreRepository:
    def __init__(self, db):
        self.db = db
        self.collection_name = "apartment_listings"

    def post_apartment_listing(self, apartment: Apartment):
        document_id = apartment.get_string_id()
        doc = self.db.collection(self.collection_name).document(document_id)
        try:
            doc.create({}) # Empty document as we only use the document_id
        except exceptions.AlreadyExists:
            return False
        return True
