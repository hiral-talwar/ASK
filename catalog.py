import csv


def load_catalogue(path="catalogue.csv"):
    products = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            searchable_text = " ".join([
                row["name"], row["category"], row["room"], row["style"],
                row["material"], row["colour"], row["description"]
            ])
            row["searchable_text"] = searchable_text
            products.append(row)
    return products