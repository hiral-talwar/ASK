import os
import time
from dotenv import load_dotenv
from google import genai
from retrieve import build_index

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = """
You are a shopping assistant for SuperBolter, a furniture retailer.
Answer the customer's question using ONLY the products listed below.

Rules:
- Every product you mention must be one of the ones listed below. Cite its SKU.
- Never invent a product, price, delivery date, or detail not shown below.
- If none of the products below genuinely answer the question, say plainly
  that the catalogue does not cover this, and do not cite any SKU.
- If a product exists but part of the question (like delivery) isn't
  covered by the information given, say so explicitly instead of guessing.

PRODUCTS:
{products}

CUSTOMER QUESTION: {question}

ANSWER:
""".strip()


def format_products(results):
    lines = []
    for r in results:
        lines.append(
            f"SKU: {r['sku']} | {r['name']} | {r['category']} | {r['room']} | "
            f"{r['style']} | {r['material']} | {r['colour']} | ₹{r['price_inr']} | "
            f"{r['dimensions_cm']} | {r['description']}"
        )
    return "\n".join(lines)


def ask(question, index):
    results = index.search(question, num_results=3)
    products_text = format_products(results)
    prompt = PROMPT_TEMPLATE.format(products=products_text, question=question)

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            return {
                "answer": response.text,
                "retrieved_skus": [r["sku"] for r in results],
            }
        except Exception as e:
            print(f"--- error attempt {attempt+1}: {e}")
            if attempt < 2:
                time.sleep(2)
            else:
                return {
                    "answer": "Sorry, the assistant is temporarily unavailable.",
                    "retrieved_skus": [],
                }


if __name__ == "__main__":
    index = build_index()
    result = ask("I need a two-seater sofa for a small living room, scandinavian style, nothing over 40,000 rupees.", index)
    print(result["answer"])
    print("Retrieved SKUs:", result["retrieved_skus"])