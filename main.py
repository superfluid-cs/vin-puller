import csv
import requests

def pull(vin="", makedict=True):    # Download the CSV data from https://vpic.nhtsa.dot.gov/decoder/
    # Check VIN
    print(len(vin))
    if len(vin) != 17:
        raise ValueError("Invalid VIN length--must be 17, alphanumeric.")
        return None

    # Query the NHTSA site for the data
    params = {"VIN": vin}
    try:
        r = requests.get("https://vpic.nhtsa.dot.gov/decoder/Decoder/ExportToExcel", params=params, timeout=6)
    except requests.exceptions.RequestException:
        return None

    # Success -------------------------------------------------
    if not makedict:
        return r.text    # Returns the unparsed CSV text output string and exits the function

    # Process the decode into a dictionary
    reader = csv.reader(r.text.splitlines(), delimiter=",")
    rdict = {}
    for row in list(reader):
        if row[2]:
            if row[2] == "Not Applicable":
                continue
            rdict[str(row[1])] = str(row[2])
        else:
            pass

    return rdict


vin = input("Enter 17 character VIN: ")

vehicle = pull(vin)
print()
print(vehicle.pop("Model Year"), end=" ")
print(vehicle.pop("Make"), end=" ")
print(vehicle.pop("Model"))
print("\n")
print("Full dictionary:")
for key in vehicle:
    print(f"{key} - {vehicle[key]}")
