import json
import os

OLD_DICT_FILE = "mobile_dict.json"
NEW_DICT_FILE = "amharic_root_forms_dictionary.json"
OUTPUT_FILE   = "root_forms_map.json"

AMHARIC_PUNCTUATION = ["፡", "።", "፣", "፤", "፥", "፦"]

def clean_word(word):
    """Remove Amharic punctuation and whitespace."""
    for p in AMHARIC_PUNCTUATION:
        word = word.replace(p, "")
    return word.strip()

def load_json(path):
    if not os.path.exists(path):
        print(f"❌ Missing file: {path}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    print("📥 Loading dictionaries...")
    new_dict = load_json(NEW_DICT_FILE)
    old_dict = load_json(OLD_DICT_FILE)

    if new_dict is None or old_dict is None:
        print("❌ Cannot process root → forms map.")
        return

    print("🔧 Building root → forms mapping...")

    root_map = {}

    # -----------------------------
    # 1️⃣ Extract root → forms from new dictionary
    # -----------------------------
    for entry in new_dict["words"]:
        root = clean_word(entry["root"])
        forms = [clean_word(f) for f in entry.get("forms", [])]

        # ensure root included in forms
        if root not in forms:
            forms.append(root)

        # remove empty strings
        forms = sorted(set([f for f in forms if f]))

        root_map[root] = forms


    # -----------------------------
    # 2️⃣ Add old dictionary words (if not present)
    # -----------------------------
    print("🔄 Merging old dictionary words...")

    if isinstance(old_dict, dict) and "words" in old_dict:
        old_words = old_dict["words"]
    else:
        old_words = old_dict if isinstance(old_dict, list) else []

    for w in old_words:
        cleaned = clean_word(w)
        if not cleaned:
            continue

        # Try assigning unknown old words as "their own root"
        if cleaned not in root_map:
            root_map[cleaned] = [cleaned]

        # Otherwise add to its root forms if possible
        else:
            if cleaned not in root_map[cleaned]:
                root_map[cleaned].append(cleaned)


    # -----------------------------
    # 3️⃣ Save output file
    # -----------------------------
    print(f"💾 Saving root → forms map to: {OUTPUT_FILE}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(root_map, f, ensure_ascii=False, indent=2)

    print("🎉 Done! The file is ready for autocomplete use.")
    print(f"🔢 Total roots: {len(root_map)}")

if __name__ == "__main__":
    main()
