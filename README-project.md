# SpecFinder India

A student web application for searching and comparing laptop listings in India. The project combines a browser-based catalogue that demonstrates jQuery and Ajax with a Python and Streamlit prototype for specification search and analysis.

## Problem and objective

Laptop specifications can be difficult to compare across processor, graphics, memory, storage, screen size and price. SpecFinder India helps a student shortlist laptops by budget and requirements, then compare the specifications in one place.

## Main features

- Search by laptop brand or model.
- Filter by brand, laptop category, maximum budget and minimum RAM.
- Sort matches by price or dataset rating.
- Expand a listing to view more specifications.
- Select up to three laptops and compare them side by side.
- Use a beginner-friendly profile and deeper specification filters in the Streamlit prototype.

## Syllabus concepts demonstrated

The browser catalogue uses **jQuery**, **Ajax (XMLHttpRequest)**, JavaScript DOM updates, HTML and CSS. On page load, the Ajax request loads the cleaned CSV, Papa Parse reads its rows, and jQuery renders and filters the catalogue without a full page reload.

The separate Streamlit prototype uses Python, Pandas and Plotly for data-driven search and analysis.

## Run the browser catalogue

From the repository root, start a local static web server:

\`\`\`bash
python -m http.server 8000
\`\`\`

Open http://localhost:8000/web/. The browser catalogue loads the cleaned CSV through Ajax. Internet access is needed for the jQuery and Papa Parse CDN scripts.

## Run the Streamlit prototype

\`\`\`bash
python -m pip install -r requirements-project.txt
streamlit run app.py
\`\`\`

## Dataset and limitations

The cleaned laptop dataset is included at data/processed/laptops_cleaned.csv. It is copied from the [Indian laptop specifications dataset](https://github.com/abhinavflac/laptops-specs-dataset); the source repository's MIT license is included in this project. The cleaning and exploratory analysis notebooks are included.

The app can also load a supplemental Smartprix CSV from data/raw/smartprix_laptop.csv when that file is supplied. That supplemental file is not currently included. Listings are dataset snapshots, not live offers; retailer names, product-page URLs and current availability are not provided. Similar models from different data sources may appear more than once. Preserve the source attribution when using or redistributing the data.

## Future scope

Add current retailer links and availability, refresh data on a schedule, connect a database, add user saved lists, and extend the catalogue to PC components.