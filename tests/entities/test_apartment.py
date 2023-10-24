from src.entities.apartment import Apartment
import unittest

class TestApartment(unittest.TestCase):

    def test_initialization(self):
        # Test the initialization of the Apartment instance
        apartment = Apartment(
            id=1,
            address="123 Main St",
            location="City",
            last_register_date="2023-01-01",
            level=2,
            rent=1000,
            rooms=3,
            square_meter=75,
            temporary=True,
            age=20,
            youth=True
        )

        self.assertEqual(apartment.id, 1)
        self.assertEqual(apartment.address, "123 Main St")
        self.assertEqual(apartment.location, "City")
        self.assertEqual(apartment.last_register_date, "2023-01-01")
        self.assertEqual(apartment.level, 2)
        self.assertEqual(apartment.rent, 1000)
        self.assertEqual(apartment.rooms, 3)
        self.assertEqual(apartment.square_meter, 75)
        self.assertTrue(apartment.temporary)
        self.assertEqual(apartment.age, 20)
        self.assertTrue(apartment.youth)

    def test_string_representation(self):
        # Test the __str__ method of the Apartment class
        apartment = Apartment(
            id=1,
            address="123 Main St",
            location="City",
            last_register_date="2023-01-01",
            level=2,
            rent=1000,
            rooms=3,
            square_meter=75,
            temporary=True,
            age=20,
            youth=True
        )

        expected_str = "Address: 123 Main St\nLast Register Date: 2023-01-01\nLevel: 2\nLink: https://bostad.stockholm.se/bostad/1\nLocation: City\nRent: 1000\nRooms: 3\nSquare Meter: 75\nTemporary: True\nAge: 20\nYouth: True\n"
        self.assertEqual(str(apartment), expected_str)

    def test_youth_set_but_not_age(self):
        # Test that an exception is raised when youth and age are not set correctly
        with self.assertRaises(ValueError):
            Apartment(
                id=1,
                address="123 Main St",
                location="City",
                last_register_date="2023-01-01",
                level=2,
                rent=1000,
                rooms=3,
                square_meter=75,
                youth=True # Age is missing
            )

    def test_age_set_but_not_youth(self):
        # Test that an exception is raised when youth and age are not set correctly
        with self.assertRaises(ValueError):
            Apartment(
                id=1,
                address="123 Main St",
                location="City",
                last_register_date="2023-01-01",
                level=2,
                rent=1000,
                rooms=3,
                square_meter=75,
                age=23 # Youth is missing
            )

if __name__ == '__main__':
    unittest.main()
