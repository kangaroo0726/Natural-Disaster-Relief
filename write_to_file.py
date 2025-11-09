import csv

def read_csv_to_dict(filename):
    with open(filename) as file_in:
        shelter_dict = {}
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
            food_available = True if line[7] == "True" else False
            water_available = True if line[8] == "True" else False
            medical_aid_available = True if line[9] == "True" else False
            pet_friendly = True if line[10] == "True" else False
            if "pet_friendly" not in shelter_dict:
                shelter_dict["pet_friendly"] = []
            if "medical" not in shelter_dict:
                shelter_dict["medical"] = []
            if "general" not in shelter_dict:
                shelter_dict["general"] = []
            if pet_friendly and medical_aid_available:
                shelter_dict["pet_friendly"].append([shelter_name, shelter_type, shelter_address, shelter_lat,
                                                     shelter_lon, shelter_capacity, shelter_occupancy, food_available,
                                                     water_available])
                shelter_dict["medical"].append([shelter_name, shelter_type, shelter_address, shelter_lat,
                                                     shelter_lon, shelter_capacity, shelter_occupancy, food_available,
                                                     water_available])
            elif pet_friendly:
                shelter_dict["pet_friendly"].append([shelter_name, shelter_type, shelter_address, shelter_lat,
                                                     shelter_lon, shelter_capacity, shelter_occupancy, food_available,
                                                     water_available])
            elif medical_aid_available:
                shelter_dict["medical"].append([shelter_name, shelter_type, shelter_address, shelter_lat,
                                                shelter_lon, shelter_capacity, shelter_occupancy, food_available,
                                                water_available])
            else:
                shelter_dict["general"].append([shelter_name, shelter_type, shelter_address, shelter_lat,
                                                shelter_lon, shelter_capacity, shelter_occupancy, food_available,
                                                water_available])

        return shelter_dict
