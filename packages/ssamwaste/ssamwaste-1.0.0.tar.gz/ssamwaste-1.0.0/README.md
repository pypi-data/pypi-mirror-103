# SSAM Waste Schedule Library
A simple library for the SSAM Waste Schedule API written in Python 3.

SSAM (Södra Smålands Avfall & Miljö) is a Swedish Waste Management company.
They empty their customers trash bins on a pre-defined schedule. This library
will fetch the schedule from their API and present it to the user through a few simple classes and properties, wrapped inside a Python package.

## Installation
Install the latest version with pip3:
```
$ pip3 install ssamwaste
```

## Basics
### Building ID
Every household has a building ID attached to it. This ID is what's used to query the API for the schedule associated with an address.

If it's the first time you are using this library and you don't know the building ID of your address you must start by finding out your building ID:
```python
from ssam import ssam

ssam = ssam.WasteScheduler()

buildings = ssam.search_building('Storgatan 5')

# The search results are returned in a list
for building in buildings:
    print(building)
```

You can access the address, city and building ID as properties on a building object, like this:
```python
>>> building.address
'Storgatan 1'
>>> building.city
'Växjö'
>>> building.id
'71337'
```

### Schedule
```python
from ssam import ssam

ssam = ssam.WasteScheduler()

# The get_waste_bins() method require a Building ID. It returns a list of WasteBin objects.
for waste_bin in ssam.get_waste_bins(12345):
    print(waste_bin)
```

You can access the properties of the ```WasteBin``` object, like this:
```python
>>> bin.next_waste_pickup
'2021-04-23'
>>> bin.waste_pickups_per_year
26
>>> bin.waste_type
'Hushållsavfall'
>>> bin.waste_pickup_frequency
'Tömning varannan vecka fredag jämn vecka helår'
>>> bin.bin_code
'K180'
>>> bin.bin_size
180.0
>>> bin.bin_unit
'l'
>>> bin.bin_container_type
'Kärl'
>>> bin.number_of_bins
1.0
>>> bin.is_active
True
>>> bin.id
123456
>>> bin.description
'Kärl 180 l 14-dagarstömning'
>>> bin.building_id
12345
```