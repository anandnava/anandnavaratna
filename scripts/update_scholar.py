import json
import os
from datetime import datetime, timezone
from scholarly import scholarly

SCHOLAR_ID = "qd8-6ZEAAAAJ"
OUTPUT_PATH = "data/scholar.json"


def main():
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["indices"])

    data = {
        "metrics": {
            "citations": author.get("citedby", 0),
            "h_index": author.get("hindex", 0),
            "i10_index": author.get("i10index", 0),
            "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        }
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Updated {OUTPUT_PATH}: {data['metrics']}")


if __name__ == "__main__":
    main()
