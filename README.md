# EU Debates: From Text to Network with LLMs (Simulated)

## Overview
I convert EU Parliament debates into structured data (LLM-style), explore descriptives, and build a Speaker–Keyword knowledge graph for network analysis.

## Pipeline
1. **01_load_data.py** — load Hugging Face dataset (`RJuro/eu_debates`), filter 2019–2024 English, sample 400 → `data/eu_debates_sample.csv`.
2. **02_extract_structured.py** — simulate LLM extraction to JSON-like rows → `outputs/extracted.csv`.
3. **03_descriptive_analysis.py** — top keywords/parties → `outputs/top_keywords.png`, `outputs/top_parties.png`.
4. **04_build_network.py** — Speaker–Keyword graph, colored by node type → `outputs/network.png`.
5. **05_export_triples.py** — export KG triples → `outputs/triples.csv`.
6. **06_quality_check.py** — manual spot-check sample (precision/recall, documented below).
7. **07_community_detection.py** *(optional)* — thematic communities.

## Results (examples)
- **Top keywords:** see `outputs/top_keywords.png`.
- **Network:** `outputs/network.png` (🔵 speakers, 🟠 keywords).
- **Triples:** `outputs/triples.csv` (subject, relation, object, weight).

## Quality & Limitations
- Manual spot-check (n=20): ~**[your precision]% precision**, ~**[your recall]% recall** (approx).
- Common errors: procedural phrases (e.g., “on behalf”) as keywords; single keyword per speech; English-only subset; no entity disambiguation.

## How to Run
```bash
python 01_load_data.py
python 02_extract_structured.py
python 03_descriptive_analysis.py
python 04_build_network.py
python 05_export_triples.py
python 06_quality_check.py
# optional
python 07_community_detection.py
## 🎥 Project Presentation
https://drive.google.com/file/d/17I_gegXGOHInjhHNmu8xYRNG1DEgOnfH/view?usp=sharing
