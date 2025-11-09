import json
import csv

with open("shelterData.csv") as f:
    data = json.load(f)

with open("shelters.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

with open("shelters.csv") as file_in:
    header = file_in.readline()
    reader_in = csv.reader(file_in)
    for line in reader_in:
        shelter_name = line[0]
        shelter_address = line[1]
        shelter_type = line[2]
        shelter_lat = float(line[3])
        shelter_lon = float(line[4])
        shelter_capacity = int(line[5])
        shelter_occupancy = int(line[6])
        food_available = True if line[6] == "True" else False
        water_available = True if line[7] == "True" else False
        medical_aid_available = True if line[8] == "True" else False
        pet_friendly = True if line[9] == "True" else False



