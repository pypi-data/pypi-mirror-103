import re


class Building(object):
    """ Class definition of a building as returned by the API server. """

    def __init__(self, address, city, id):
        """ Class constructor """
        self.__address = address
        self.__city = city
        self.__id = id

    def __str(self):
        """ Define how the print method should print the object. """

        return 'TODO_PRINT_STR()'

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name = type(self).__name__
        address = f"address = '{self.address}'"
        city = f"city = '{self.city}'"
        id = f"id = {self.id}"

        return f"{class_name}({address}, {city}, {id})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'address': self.address,
            'city': self.city,
            'id': self.id
        }

    # Building properties
    @property
    def address(self):
        return self.__address

    @property
    def city(self):
        return self.__city

    @property
    def id(self):
        return self.__id


class WasteBin(object):
    """ Class definition of a waste bin returned by the API server. """

    def __init__(self, next_waste_pickup, waste_pickups_per_year, waste_type, 
        waste_pickup_frequency, bin_code, bin_size, bin_unit, 
        bin_container_type, number_of_bins, is_active, id, description, 
        building_id):
        """ Class constructor """
        self.__next_waste_pickup = next_waste_pickup
        self.__waste_pickups_per_year = waste_pickups_per_year
        self.__waste_type = waste_type
        self.__waste_pickup_frequency = waste_pickup_frequency
        self.__bin_code = bin_code
        self.__bin_size = bin_size
        self.__bin_unit = bin_unit
        self.__bin_container_type = bin_container_type
        self.__number_of_bins = number_of_bins
        self.__is_active = is_active
        self.__id = id
        self.__description = description
        self.__building_id = building_id

    def __str(self):
        """ Define how the print method should print the object. """

        return 'TODO_PRINT_STR()'

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name = type(self).__name__
        next_waste_pickup = f"next_waste_pickup = '{self.next_waste_pickup}'"
        waste_pickups_per_year = f"waste_pickups_per_year = {self.waste_pickups_per_year}"
        waste_type = f"waste_type = '{self.waste_type}'"
        waste_pickup_frequency = f"waste_pickup_frequency = '{self.waste_pickup_frequency}'"
        bin_code = f"bin_code = '{self.bin_code}'"
        bin_size = f"bin_size = {self.bin_size}"
        bin_unit = f"bin_unit = '{self.bin_unit}'"
        bin_container_type = f"bin_container_type = '{self.bin_container_type}'"
        number_of_bins = f"number_of_bins = {self.number_of_bins}"
        is_active = f"is_active = {self.is_active}"
        id = f"id = {self.id}"
        description = f"description = '{self.description}'"
        building_id = f"building_id = {self.building_id}"

        return f"{class_name}({next_waste_pickup}, {waste_pickups_per_year}, {waste_type}, {waste_pickup_frequency}, {bin_code}, {bin_size}, {bin_unit}, {bin_container_type}, {number_of_bins}, {is_active}, {id}, {description}, {building_id})"

    @property
    def next_waste_pickup(self):
        return self.__next_waste_pickup

    @property
    def waste_pickups_per_year(self):
        return self.__waste_pickups_per_year
    
    @property
    def waste_type(self):
        return self.__waste_type
    
    @property
    def waste_pickup_frequency(self):
        return self.__waste_pickup_frequency

    @property
    def bin_code(self):
        return self.__bin_code
    
    @property
    def bin_size(self):
        return self.__bin_size

    @property
    def bin_unit(self):
        return self.__bin_unit

    @property
    def bin_container_type(self):
        return self.__bin_container_type

    @property
    def number_of_bins(self):
        return self.__number_of_bins

    @property
    def is_active(self):
        return self.__is_active

    @property
    def id(self):
        return self.__id

    @property
    def description(self):
        return self.__description
    
    @property
    def building_id(self):
        return self.__building_id
