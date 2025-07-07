import csv
import json
import random
from pathlib import Path

def read_tips(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def pick_random_tip(tips):
    return random.choice(tips)

def build_json(tip_text):
    return {
        "metadata": {
            "version": "2.0"
        },
        "contentContainerWidth": "wide",
        "content": [
            {
                "elementType": "blockHeading",
                "heading": "Tip of the day",
                "headingFontWeight": "bold",
                "headingLevel": 2,
                "headingTextAlignment": "center",
                "headingTextColor": "#d22030"
            },
            {
                "elementType": "html",
                "html": (
                    '<div class="container" style="text-align:center; font-weight:bold;">\r\n'
                    f'{tip_text}\r\n'
                    '</div>'
                )
            }
        ]
    }

def save_tip_to_json(json_data, json_path):
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    tips = read_tips('tips.csv')
    random_tip = pick_random_tip(tips)
    tip_text = random_tip['tips']
    final_json = build_json(tip_text)
    save_tip_to_json(final_json, Path('json/tip.json'))
    print("✅ Tip JSON updated with:", tip_text)
