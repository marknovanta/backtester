import csv

def extract_years(file):
    dates = []

    with open(file, mode='r') as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                dates.append(row[0])

    start = dates[0][:4]
    end = dates[-1][:4]

    years = int(end) - int(start)
    return years