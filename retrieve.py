from minsearch import Index
from catalog import load_catalogue


def build_index():
    products = load_catalogue()
    index = Index(
        text_fields=["searchable_text"],
        keyword_fields=["sku"]
    )
    index.fit(products)
    return index


if __name__ == "__main__":
    index = build_index()
    results = index.search("two-seater sofa scandinavian under 40000", num_results=3)
    for r in results:
        print(r["sku"], "-", r["name"], "-", r["price_inr"])