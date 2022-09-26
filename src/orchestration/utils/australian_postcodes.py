import csv

def australian_postcodes():
    with open("./australian_postcodes.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row