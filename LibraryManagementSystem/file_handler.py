import json
class FileHandler:
    def read_file(self, filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
    def write_file(self, filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)