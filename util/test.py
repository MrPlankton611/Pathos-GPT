import json

with open("util/login1.json", "r") as f:
    file_data = json.load(f)
    print(file_data)