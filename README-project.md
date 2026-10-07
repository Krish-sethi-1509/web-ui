# SpecFinder India

A student prototype for finding and comparing laptops by budget and hardware requirements.

## Features

- Start with a simple profile for gaming at college, study and everyday use, or a custom specification search.
- Choose a budget, graphics level, processor tier, and minimum RAM using beginner-friendly descriptions.
- Open **Know more** to filter by brand, exact GPU and processor family, storage, screen size, laptop category, and model name.
- View laptop matches as image-ready cards, open **View details** for a closer look, or use the full comparison table and price chart.
- Smartprix product photos load from image URLs when available; add local product photos under `assets/laptops/` using the filename guidance in `assets/laptops/README.md`.

## Run on macOS

From this project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-project.txt
streamlit run app.py
```

## Dataset

Both CSVs are included in this repository at `data/processed/laptops_cleaned.csv` and `data/raw/smartprix_laptop.csv`. The app loads and normalizes the Smartprix rows automatically. The Smartprix dataset adds image URLs alongside more specs, prices and Apple/RTX listings.

The combined list has 1,939 rows (992 original plus 947 Smartprix). Preserve source attribution. The first source README describes its dataset as CC0, while that repository’s `LICENSE` says MIT; check with the author if you need to redistribute that dataset. The supplemental CSV is from Kaggle’s Smartprix laptop specs and prices dataset.

## Known limitations

- This is not a complete catalogue of every laptop. Similar model listings from the two sources are retained.
- The CSVs do not include retailer names or product-page URLs. Prices are dataset snapshots, not live cross-store offers or current availability.
- RTX 3050 is present in both sources. The gaming preset starts at the entry gaming GPU tier; use the study or custom profile for MacBooks.
- Ratings use the original dataset’s 0–100 score scale.

## Project area for evaluation

Web Scraping / data analysis. The dataset sources report collecting laptop product listings from Indian e-commerce websites. This prototype focuses on normalizing structured fields and building a detailed specification search interface.
