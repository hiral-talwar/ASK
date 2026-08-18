import re

MULTI_WORD_CATEGORIES = ["dining table", "side table", "coffee table"]
SINGLE_WORD_CATEGORIES = ["sofa", "chair", "bed", "wardrobe", "lamp", "rug", "storage"]
CATEGORY_SYNONYMS = {"vanity": "vanity", "vanities": "vanity", "sideboard": "storage",
                      "tv unit": "storage", "nightstand": "side table", "stool": "chair",
                      "bookcase": "storage", "almirah": "wardrobe", "loveseat": "sofa",
                      "couch": "sofa", "settee": "sofa"}
STYLES = ["scandinavian", "japandi", "contemporary", "modern", "minimalist", "bohemian", "traditional"]
MATERIALS = ["oak", "teak", "walnut", "ash", "sheesham", "mango", "steel", "brass",
             "leather", "velvet", "cane", "beech", "wool", "cotton", "linen", "stone", "jute"]
NUM_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}


def detect_category(q):
    q = q.lower()
    for cat in MULTI_WORD_CATEGORIES:
        if cat in q:
            return cat
    for word, canonical in CATEGORY_SYNONYMS.items():
        if word in q:
            return canonical
    for cat in SINGLE_WORD_CATEGORIES:
        if cat in q:
            return cat
    return None


def detect_budget(q):
    q = q.lower().replace(",", "")
    m = re.search(r"(?:under|below|nothing over|budget of)\s*(?:rs\.?|₹|inr)?\s*(\d+)", q)
    return int(m.group(1)) if m else None


def detect_capacity(q):
    m = re.search(r"seats?\s+(\w+)", q.lower())
    if not m:
        return None
    w = m.group(1)
    return int(w) if w.isdigit() else NUM_WORDS.get(w)


def detect_dimensions(q):
    m = re.search(r"(\d{2,4})\s*x\s*(\d{2,4})", q.lower())
    return (int(m.group(1)), int(m.group(2))) if m else None


def parse_dimensions(s):
    nums = re.findall(r"\d+", s)
    return (int(nums[0]), int(nums[1])) if len(nums) >= 2 else None


def classify(question, p):
    """Returns 'strong', 'similar', or 'irrelevant' + reasons (used internally only)."""
    q = question.lower()

    category = detect_category(q)
    if category and category not in p["category"].lower() and p["category"].lower() not in category:
        return "irrelevant", []

    reasons = []
    for s in STYLES:
        if s in q and s not in p["style"].lower().replace("_", " "):
            reasons.append(f"style is {p['style']}, not {s}")
    for m in MATERIALS:
        if m in q and m not in p["material"].lower():
            reasons.append(f"material is {p['material']}, not {m}")

    budget = detect_budget(q)
    if budget and int(p["price_inr"]) > budget:
        reasons.append(f"priced at ₹{int(p['price_inr']):,}, over your ₹{budget:,} budget")

    capacity = detect_capacity(q)
    if capacity:
        word = next((w for w, n in NUM_WORDS.items() if n == capacity), None)
        desc = p["description"].lower()
        if not (word and word in desc and "seat" in desc):
            reasons.append(f"seating capacity for {capacity} isn't confirmed")

    dims = detect_dimensions(q)
    if dims:
        pdims = parse_dimensions(p["dimensions_cm"])
        if pdims and not (abs(pdims[0]-dims[0]) <= dims[0]*0.15 and abs(pdims[1]-dims[1]) <= dims[1]*0.15):
            reasons.append(f"sized {pdims[0]}x{pdims[1]} cm, not {dims[0]}x{dims[1]} cm")

    return ("similar", reasons) if reasons else ("strong", [])


def rank_products(question, results):
    """Splits retrieved products into (strong, similar) — irrelevant ones are dropped entirely."""
    strong, similar = [], []
    for p in results:
        level, reasons = classify(question, p)
        if level == "strong":
            strong.append(p)
        elif level == "similar":
            similar.append({**p, "reasons": reasons})
    return strong, similar
if __name__ == "__main__":
    from retrieve import build_index

    index = build_index()
    question = "I need a two-seater sofa for a small living room, scandinavian style, nothing over 40,000 rupees."
    results = index.search(question, num_results=8)

    strong, similar = rank_products(question, results)
    shown = (strong + similar)[:3]
    shown_strong = [p for p in shown if p in strong]
    shown_similar = [p for p in shown if p not in strong]

    def details(p):
        return f"{p['style']}, {p['material']}, {p['colour']}, ₹{int(p['price_inr']):,}, {p['dimensions_cm']} cm"

    if shown_strong:
        print("Best Match:")
        for p in shown_strong:
            print(f"  {p['sku']} - {p['name']}")
            print(f"    {details(p)}")

    if shown_similar:
        print("\nSimilar to your search:")
        for p in shown_similar:
            reasons = f" ({'; '.join(p['reasons'])})" if p.get("reasons") else ""
            print(f"  {p['sku']} - {p['name']}{reasons}")
            print(f"    {details(p)}")

    if not shown:
        print("No matches found in the catalogue for this question.")