from retrieve import build_index
from ask import ask

with open("questions.txt", "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f if l.strip().startswith("Q")]

questions = [l.split(".", 1)[1].strip() for l in lines]

index = build_index()

for i, q in enumerate(questions, 1):
    print(f"\n{'='*70}")
    print(f"Q{i}: {q}")
    print('='*70)
    result = ask(q, index)
    print(result["answer"])
    print(f"\nRaw retrieved SKUs: {result['raw_retrieved_skus']}")
    print(f"Shown to model: {result['shown_skus']}")