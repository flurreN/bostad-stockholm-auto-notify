import unittest
from unittest.mock import Mock, patch
from src.repositories.apartment_firestore import ApartmentFirestoreRepository
from src.entities.apartment import Apartment
from google.api_core.exceptions import AlreadyExists

class TestApartmentFirestoreRepository(unittest.TestCase):

    def setUp(self):
        # Mock Firebase Admin initialize_app method
        self.mock_firebase_admin = Mock()
        self.mock_firestore = Mock()
        self.mock_collection = Mock()
        self.mock_document = Mock()
        self.mock_firestore.client.return_value = self.mock_collection
        self.mock_collection.document.return_value = self.mock_document
        self.patcher = patch('src.repositories.apartment_firestore.firebase_admin', self.mock_firebase_admin)
        self.patcher.start()

        # Initialize the repository with a dummy credentials path
        self.repo = ApartmentFirestoreRepository('dummy_credentials.json')

    def tearDown(self):
        self.patcher.stop()

    def test_post_apartment_listing_successful(self):
        # Create a sample Apartment object
        apartment = Apartment("1", "Sample Apartment", 1000)

        # Mock Firestore create method to simulate successful creation
        self.mock_document.create.return_value = None

        # Attempt to post the apartment listing
        result = self.repo.post_apartment_listing(apartment)

        # Verify that the method returned True, indicating success
        self.assertTrue(result)

    def test_post_apartment_listing_already_exists(self):
        # Create a sample Apartment object
        apartment = Apartment("1", "Sample Apartment", 1000)

        # Mock Firestore create method to simulate AlreadyExists exception
        self.mock_document.create.side_effect = AlreadyExists("Document already exists")

        # Attempt to post the apartment listing
        result = self.repo.post_apartment_listing(apartment)

        # Verify that the method returned False, indicating that the document already exists
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
