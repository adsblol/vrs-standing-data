import csv
import json
import os


class CSVToJson:
    # This class is used to convert a csv file to a json file
    # The csv file must have a header row
    # The output will be a list of dictionaries
    def __init__(self, csv_file, translate_keys=None, dicts_by_key=None):
        self.csv_file = csv_file
        self.translate_keys = translate_keys
        self.dicts = []
        self.dicts_by_key_filter = dicts_by_key
        self.dicts_by_key = {}

    def read_csv(self):
        # Read the csv file and return a list of dictionaries
        with open(self.csv_file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.dicts.append(row)
                if self.dicts_by_key_filter:
                    self.dicts_by_key[row[self.dicts_by_key_filter]] = row


def run():
    this_path = os.path.dirname(os.path.abspath(__file__))
    Airports = CSVToJson(os.path.join(this_path, "airports.csv"), dicts_by_key="ICAO")
    Airports.read_csv()
    Routes = CSVToJson(os.path.join(this_path, "routes.csv"), dicts_by_key="Callsign")
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
            airport_data = Airports.dicts_by_key.get(airport, [])
            if len(airport_data) == 0:
                print("No airport data for", airport)
                continue
            # Code,Name,ICAO,IATA,Location,CountryISO2,Latitude,Longitude,AltitudeFeet
            fmt_airport = {
                "name": airport_data["Name"],
                "icao": airport_data["ICAO"],
                "iata": airport_data["IATA"],
                "location": airport_data["Location"],
                "countryiso2": airport_data["CountryISO2"],
                "lat": float(airport_data["Latitude"]),
                "lon": float(airport_data["Longitude"]),
                "alt_feet": float(airport_data["AltitudeFeet"]),
                "alt_meters": float(
                    round(int(airport_data["AltitudeFeet"]) * 0.3048, 2)
                ),
            }

            file_contents["_airports"].append(fmt_airport)
            if len(fmt_airport["iata"]) == 3:
                file_contents["_airport_codes_iata"] = file_contents[
                    "_airport_codes_iata"
                ].replace(airport, fmt_airport["iata"])
        # Write the file
        with open(filename, "w") as f:
            json.dump(file_contents, f, indent=4)


if __name__ == "__main__":
    run()
