import json
import os
from datetime import datetime, timezone
from scholarly import scholarly

SCHOLAR_ID = "qd8-6ZEAAAAJ"
OUTPUT_PATH = "data/scholar.json"

def categorize(title: str, venue: str) -> str:
    text = f"{title} {venue}".lower()
    if any(k in text for k in ["war", "warfare", "defence", "defense", "digital twin", "deepfake", "synergy", "electronic"]):
        return "defence"
    if any(k in text for k in ["digital governance", "e-governance", "chatbot", "citizen", "jedem"]):
        return "digital-gov"
    return "ai-policy"

def main():
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["basics", "indices", "publications"])

    metrics = {
        "citations": author.get("citedby", 0),
        "h_index": author.get("hindex", 0),
        "i10_index": author.get("i10index", 0),
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d")
    }

    publications = []
    for pub in author.get("publications", []):
        filled = scholarly.fill(pub)
        bib = filled.get("bib", {})
        title = bib.get("title", "Untitled")
        venue = bib.get("citation") or bib.get("journal") or bib.get("booktitle") or bib.get("venue") or ""
        year = int(bib.get("pub_year", 0)) if str(bib.get("pub_year", "")).isdigit() else 0

        publications.append({
            "title": title,
            "authors": bib.get("author", "A. R. Navaratna"),
            "venue": venue,
            "year": year,
            "type": "Publication",
            "category": categorize(title, venue),
            "citations": filled.get("num_citations", 0),
            "doi": filled.get("pub_url", "")
        })

    # Sort newest first, then by citations
    publications.sort(key=lambda x: (x["year"], x["citations"]), reverse=True)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"metrics": metrics, "publications": publications}, f, indent=2, ensure_ascii=False)

    print(f"Updated {OUTPUT_PATH} with {len(publications)} publications.")

if __name__ == "__main__":
    main()