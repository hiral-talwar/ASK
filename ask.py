import os
import time
from dotenv import load_dotenv
from google import genai
from retrieve import build_index
from match import rank_products

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = """
You are a shopping assistant for SuperBolter, a furniture retailer.
Answer using ONLY the products listed below. Never invent a product, price,
dimension, or delivery information.

Format your answer like this:
- If BEST MATCHES has products, start with a "Best Match:" section listing them
  (SKU, name, key details).
- If SIMILAR RECOMMENDATIONS also has products, add a "Similar to your search:"
  section below it, briefly explaining how each differs, using the note given.
- Only include a section if it actually has products — don't show an empty one.
- If both lists are empty, say something like: "We don't currently have that in
  our collection." Do not use the word "catalogue" or sound robotic — write it
  the way a helpful salesperson would.

Every product you mention must include its SKU.
If the customer asks about something the product data does not cover — such as
delivery, timelines, stock availability, or location — say so explicitly, for
example: "Please note that delivery details are not covered in our current
information." Do this only when they actually asked about it; never volunteer
unrelated caveats the customer didn't ask about.

BEST MATCHES:
{strong}

SIMILAR RECOMMENDATIONS:
{similar}

CUSTOMER QUESTION: {question}

ANSWER:
""".strip()


def format_line(p):
    note = f" | NOTE: {'; '.join(p['reasons'])}" if p.get("reasons") else ""
    return (f"SKU: {p['sku']} | {p['name']} | {p['category']} | {p['style']} | "
            f"{p['material']} | {p['colour']} | ₹{p['price_inr']} | "
            f"{p['dimensions_cm']} | {p['description']}{note}")


def ask(question, index):
    raw_results = index.search(question, num_results=41)
    raw_skus = [r["sku"] for r in raw_results]

    strong, similar = rank_products(question, raw_results)

    from match import detect_categories
    num_categories = len(detect_categories(question))
    cap = max(3, num_categories * 2) if num_categories > 1 else 3
    shown = (strong + similar)[:3]
    shown_skus = [p["sku"] for p in shown]

    strong_text = "\n".join(format_line(p) for p in strong[:3]) or "(none)"
    similar_text = "\n".join(format_line(p) for p in similar[:3]) or "(none)"

    prompt = PROMPT_TEMPLATE.format(strong=strong_text, similar=similar_text, question=question)

    for attempt in range(3):
        try:
            response = client.models.generate_content(model="gemini-3.5-flash-lite", contents=prompt)
            return {"answer": response.text, "raw_retrieved_skus": raw_skus, "shown_skus": shown_skus}
        except Exception as e:
            print(f"--- error attempt {attempt+1}: {e}")
            if attempt < 2:
                time.sleep(2)
            else:
                return {"answer": "Sorry, the assistant is temporarily unavailable.",
                         "raw_retrieved_skus": raw_skus, "shown_skus": []}


if __name__ == "__main__":
    index = build_index()
    for q in [
        "I need a two-seater sofa for a small living room, scandinavian style, nothing over 40,000 rupees.",
        "Do you sell bathroom vanities?",
        "Can I get the walnut wardrobe delivered to Coimbatore by Friday?",
    ]:
        print(f"\n{'='*60}\nQ: {q}")
        r = ask(q, index)
        print(r["answer"])
        print("Shown:", r["shown_skus"])