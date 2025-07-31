import csv
import json
import random
import re
from datetime import datetime
from pathlib import Path

def load_shown_tips(filepath="shown_tips.json"):
    if Path(filepath).exists():
        with open(filepath, "r") as f:
            return set(json.load(f))
    return set()

def save_shown_tips(tip_ids, filepath="shown_tips.json"):
    with open(filepath, "w") as f:
        json.dump(list(tip_ids), f)

def get_weeks_since(start_date, today=None):
    if not today:
        today = datetime.today()
    return (today - start_date).days // 7

def parse_send_timeline(timeline_str):
    if not timeline_str or timeline_str.strip() == "":
        return None, None
    if "Any Time" in timeline_str:
        return 0, 100  # Whole semester
    match = re.search(r"Week\s*(\d+)\s*-\s*(\d+)", timeline_str)
    if match:
        return int(match.group(1)), int(match.group(2))
    match_single = re.search(r"Week\s*(\d+)", timeline_str)
    if match_single:
        return int(match_single.group(1)), int(match_single.group(1))
    return None, None
def read_tips(csv_path):
    tips = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start_week, end_week = parse_send_timeline(row["Timeline"])
            if start_week is None:
                continue
            tips.append({
                "ID": row["ID"],  # <-- NEW: Use this for tracking
                "Category": row["Category"],
                "Title": row["Title"],
                "Description": row["Description"],
                "Link": row["Link"],
                "StartWeek": start_week,
                "EndWeek": end_week
            })
    return tips

def pick_random_tip(tips, current_week, shown_ids):
    eligible = [tip for tip in tips 
                if tip["StartWeek"] <= current_week <= tip["EndWeek"]
                and tip["ID"] not in shown_ids]  # <-- track by ID now
    if not eligible:
        return None
    return random.choice(eligible)

def build_json(tip):
    tip_text = f'{tip["Title"]}<br>{tip["Description"]}<br><a href="{tip["Link"]}">{tip["Link"]}</a>'
    return {
        "metadata": {
            "version": "2.0"
        },
        "contentContainerWidth": "wide",
     "content": [
        {
            "elementType": "blockHeading",
            "heading": tip['Title'],
            "headingFontWeight": "bold",
            "headingLevel": 2,
            "headingTextAlignment": "center",
            "headingTextColor": "#d22030"
        },
        {
            "elementType": "html",
            "html" : f'<div class="container" style="padding: 10px">{tip["Description"]}</div>'
        },
        {
            "elementType": "list",
            "backgroundColor": "theme:subfocal_background_color",
            "headingTextAlignment": "center",
            "itemSize": "large",
            "listStyle": "grouped",
            "marginBottom": "medium",
            "marginTop": "xloose",
            "textblockMargin": "xloose",
            "items": [
                {
                    "accessory": "external",
                    "backgroundColor": "#ffffff",
                    "textblockMargin": "xloose",
                    "title": "More Information",
                    "titleFontSize": "xxlarge",
                    "titleFontWeight": "medium",
                    "titleTextColor": "#d22030",
                    "url": {
                        "browserType": "appScreen",
                        "linkType": "external",
                        "external": tip["Link"],
                        "targetNewWindow": True
                    }
                }
            ]
        }
    ]
    }


def save_tip_to_json(json_data, json_path):
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

def main(start_date_str, csv_file):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    current_week = get_weeks_since(start_date)

    shown_ids = load_shown_tips()
    tips = read_tips(csv_file)

    selected_tip = pick_random_tip(tips, current_week, shown_ids)

    if selected_tip:
        shown_ids.add(selected_tip["ID"])  # <-- save ID not title
        save_shown_tips(shown_ids)

        tip_json = build_json(selected_tip)
        save_tip_to_json(tip_json, Path("public/json/tip.json"))
        print("✅ Tip JSON updated with:", selected_tip["Title"])
    else:
        print("😎 All tips for this week have already been shown. Nothing new to show today!")

if __name__ == "__main__":
    # Set your semester start date and tip CSV file here:
    main("2025-07-23", "tips.csv")
