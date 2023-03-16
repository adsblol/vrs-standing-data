import csv
import json
import os



class CSVToJson:
    # This class is used to convert a csv file to a json file
    # The csv file must have a header row
    # The output will be a list of dictionaries
    def __init__(self, csv_file, translate_keys=None):
        self.csv_file = csv_file
        self.translate_keys = translate_keys
        self.dicts = None

    def read_csv(self):
        # Read the csv file and return a list of dictionaries
        with open(self.csv_file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            self.dicts = [row for row in reader]

    def filterby(self, key, value):
        # Filter the list of dictionaries by a key and value
        return [row for row in self.dicts if row[key] == value]


def run():
    this_path = os.path.dirname(os.path.abspath(__file__))
    Airports = CSVToJson("airports.csv")
    Airports.read_csv()
    Routes = CSVToJson("routes.csv")
    Routes.read_csv()

    for route in Routes.dicts:
        # Header:
        # Callsign,Code,Number,AirlineCode,AirportCodes
        # write this file to
        # data/routes/XX/XXXX.json
        # where XX is the first two letters of the Callsign
        # and XXXX is the Callsign
        callsign = route["Callsign"]
        path = os.path.join(this_path, "data", "routes", callsign[:2])
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        filename = os.path.join(path, callsign + ".json")
        file_contents = {
            "callsign": route["Callsign"],
            "number": route["Number"],
            "airline_code": route["AirlineCode"],
            "airport_codes": route["AirportCodes"],
            "_airport_codes_iata": route["AirportCodes"],
            "_airports": [],
        }
        for airport in file_contents["airport_codes"].split("-"):
            # Get the airport data
            airport_data = Airports.filterby("Code", airport)
            if len(airport_data) == 0:
                print("No airport data for", airport)
                continue
            airport_data = airport_data[0]
            file_contents["_airports"].append(airport_data)
            if len(airport_data["IATA"]) == 3:
                file_contents["_airport_codes_iata"] = file_contents[
                    "_airport_codes_iata"
                ].replace(airport, airport_data["IATA"])
        # Write the file
        with open(filename, "w") as f:
            json.dump(file_contents, f, indent=4)

if __name__ == "__main__":
    run()
