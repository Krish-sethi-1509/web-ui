# SpecFinder India

A laptop finder and comparison project for Indian listings. Its browser catalogue uses jQuery and Ajax to load and filter the cleaned CSV without reloading the page. A separate Python and Streamlit prototype provides additional specification search and analysis.

## Run the browser catalogue

From the repository root:

\`\`\`bash
python -m http.server 8000
\`\`\`

Open http://localhost:8000/web/. The page loads the cleaned CSV using Ajax. Internet access is needed for the jQuery and Papa Parse CDN scripts.

## Run the Streamlit prototype

\`\`\`bash
python -m pip install -r requirements-project.txt
streamlit run app.py
\`\`\`

See README-project.md for project objectives, syllabus concepts, features, dataset attribution, limitations and future scope.