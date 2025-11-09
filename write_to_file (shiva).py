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
            food_available = True if line[6] == "True" else False
            water_available = True if line[7] == "True" else False
            medical_aid_available = True if line[8] == "True" else False
            pet_friendly = True if line[9] == "True" else False
            shelter_dict[shelter_name] = [shelter_type, shelter_lat, shelter_lon, shelter_capacity,
                                          shelter_occupancy, food_available, water_available,
                                          medical_aid_available, pet_friendly]
        return shelter_dict


def main():
    shelter_dict = read_csv_to_dict("shelters.csv")


main()
