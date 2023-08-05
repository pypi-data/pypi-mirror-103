import json
import requests

from datetime import date

from ssam.classes import *


class WasteScheduler(object):
	""" Class definition of the SSAM Schedule Checker. """

	def __init__(self):
		""" Initiate SSAM API. """
		self.__search_url = 'https://edpfuture.ssam.se/FutureWeb/SimpleWastePickup/SearchAdress'
		self.__schedule_url = 'https://edpfuture.ssam.se/FutureWeb/SimpleWastePickup/GetWastePickupSchedule?address='

	def get_waste_bins(self, building_id):
		"""
		Fetch waste bin schedule from the SSAM API.
		"""
		result = requests.get(self.__schedule_url + f'({building_id})')
		data = json.loads(result.text)

		waste_bins = []

		for bin_data in data['RhServices']:
			next_waste_pickup = bin_data['NextWastePickup']
			waste_pickups_per_year = bin_data['WastePickupsPerYear']
			waste_type = bin_data['WasteType']
			waste_pickup_frequency = bin_data['WastePickupFrequency']
			bin_code = bin_data['BinType']['Code']
			bin_size = bin_data['BinType']['Size']
			bin_unit = bin_data['BinType']['Unit']
			bin_container_type = bin_data['BinType']['ContainerType']
			number_of_bins = bin_data['NumberOfBins']
			is_active = bin_data['IsActive']
			id = bin_data['ID']
			description = bin_data['Fee']['Description']

			waste_bin = WasteBin(next_waste_pickup, waste_pickups_per_year, waste_type, waste_pickup_frequency, bin_code, bin_size, bin_unit, bin_container_type, number_of_bins, is_active, id, description, building_id)
			waste_bins.append(waste_bin)

		return waste_bins

	def search_building(self, address):
		""" 
		Search for an address in order to find your Building ID. 
		The Building ID is a unique identifier we must use when fetching
		the Waste Pickup Schedule for a customer.
		Partial address strings are allowed. The API will return the 
		first 10 (or less) matching addresses.
		"""
		result = requests.post(self.__search_url, json={'searchText': address})

		# The API may return up to 10 matching addresses so we
		# need to save the returned addresses in a list.
		address_list = []

		# Check the search result and parse if successful.
		if result.status_code == 200:
			search_result = result.json()
			if search_result['Succeeded']:
				for building_str in search_result['Buildings']:
					# The API return a string in the format:
					# 'Storgatan 1, Storstaden (71337)'
					# We need to parse it into address, city and ID
					building_list = re.split('[,()]', building_str)
					address = building_list[0].strip()
					city = building_list[1].strip()
					id = building_list[2].strip()

					# Create a new Building and append it to the list
					building = Building(address, city, id)
					address_list.append(building)

		return address_list
