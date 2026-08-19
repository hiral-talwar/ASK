# ASK — SuperBolter Furniture Assistant

A question-answering assistant over SuperBolter's 41-product furniture
catalogue. Ask in plain English, get recommendations grounded in real
products with SKUs cited - never invented.

## How to run it
git clone https://github.com/hiral-talwar/ASK 
cd ASK 
pip install -r requirements.txt

Create a `.env` file:
GEMINI_API_KEY=your-key-here
Then: streamlit run app.py


## Live URL

https://ask-lpk1.onrender.com

Hosted on a free tier - may take 30-60 seconds to load if it's been idle.

## Model used

Gemini 3.5 Flash Lite, via Google AI Studio's free tier.

## What's broken or missing

- Retrieval is keyword-based; true synonyms not present in the catalogue
  text (e.g. "settee" vs "sofa") can be missed unless explicitly mapped.
- Multi-item requests (e.g. "a bed, side table, and lamp") can sometimes
  omit a lower-frequency category if higher-frequency categories fill the
  shortlist first - documented in RESULTS.md (Q5).
- No conversation memory between questions; each is answered independently.

## Hours spent

Approximately 10-15 hours.