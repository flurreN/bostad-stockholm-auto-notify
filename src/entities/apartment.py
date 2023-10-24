class Apartment:
    def __init__(self, id, address, location, last_register_date, level, rent, rooms, square_meter, temporary=False, age=None, youth=False):
        self.id = id
        self.address = address
        self.location = location
        self.last_register_date = last_register_date
        self.level = level
        self.link = "https://bostad.stockholm.se/bostad/" + str(id)
        self.rent = rent
        self.rooms = rooms
        self.square_meter = square_meter
        self.temporary = temporary
        self.age = age
        self.youth = youth

        if (youth == False and age) or (age == None and youth):
            raise ValueError("Both youth and age need to be set if its a youth apartment")

    def get_string_id(self):
        return str(self.id)

    def __str__(self):
        apartment = f"Address: {self.address}\n" \
               f"Last Register Date: {self.last_register_date}\n" \
               f"Level: {self.level}\n" \
               f"Link: {self.link}\n" \
               f"Location: {self.location}\n" \
               f"Rent: {self.rent}\n" \
               f"Rooms: {self.rooms}\n" \
               f"Square Meter: {self.square_meter}\n"

        if self.temporary:
            apartment += f"Temporary: {self.temporary}\n"

        if self.age is not None:
            apartment += f"Age: {self.age}\n"

        if self.youth:
            apartment += f"Youth: {self.youth}\n"

        return apartment
