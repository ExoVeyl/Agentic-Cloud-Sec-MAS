#Checks if the vector has the same num of records as the .json file.

#Technical Integrity
import json
with open("brain_metadata.json", "r") as f:
    data = json.load(f)
    print(len(data)) # Must be 324491