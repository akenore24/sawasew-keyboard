import json
import os

# -----------------------------------------
# CONFIG — Edit if your file names differ
# -----------------------------------------
OLD_DICT_FILE = "mobile_dict.json"
NEW_DICT_FILE = "amharic_root_forms_dictionary.json"
OUTPUT_FILE   = "mobile_dict_merged.json"

# -----------------------------------------
# Amharic punctuation to remove
# -----------------------------------------
AMHARIC_PUNCTUATION = ["፡", "።", "፣", "፤", "፥", "፦"]


def clean_word(word):
    """Remove Amharic punctuation from a word."""
    for p in AMHARIC_PUNCTUATION:
        word = word.replace(p, "")
    return word.strip()


def load_json(filename):
    """Safely load JSON, return Python object."""
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return None

    with open(filename, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"❌ JSON decode error in {filename}")
            return None


def extract_old_words(old_data):
    """Extract words from the old dictionary (supports both formats)."""
    if isinstance(old_data, list):
        return set(old_data)

    if isinstance(old_data, dict) and "words" in old_data:
        return set(old_data["words"])

    print("⚠️ Unknown format in mobile_dict.json — expected array or {'words': [...]} ")
    return set()


def extract_new_words(new_data):
    """Extract all root + forms from new dictionary."""
    words = set()

    if "words" not in new_data:
        print("❌ NEW_DICT_FILE missing 'words' key")
        return words

    for entry in new_data["words"]:
        root = clean_word(entry.get("root", ""))
        if root:
            words.add(root)

        forms = entry.get("forms", [])
        for form in forms:
            cleaned = clean_word(form)
            if cleaned:
                words.add(cleaned)

    return words


def main():
    print("📥 Loading dictionaries...")

    old_data = load_json(OLD_DICT_FILE)
    new_data = load_json(NEW_DICT_FILE)

    if old_data is None or new_data is None:
        print("❌ Cannot proceed. Fix file paths and try again.")
        return

    print("🔍 Extracting words...")
    old_words = extract_old_words(old_data)
    new_words = extract_new_words(new_data)

    print(f"   → Old dictionary words: {len(old_words)}")
    print(f"   → New dictionary words: {len(new_words)}")

    # -----------------------------------------
    # MERGE, CLEAN AND SORT
    # -----------------------------------------
    print("🧹 Cleaning and merging...")

    merged = set()

    # Clean old words
    for w in old_words:
        cleaned = clean_word(w)
        if cleaned:
            merged.add(cleaned)

    # Clean new words
    for w in new_words:
        cleaned = clean_word(w)
        if cleaned:
            merged.add(cleaned)

    merged_list = sorted(list(merged))

    print(f"✅ Total merged words: {len(merged_list)}")

    # -----------------------------------------
    # SAVE OUTPUT FILE
    # -----------------------------------------
    print(f"💾 Saving to {OUTPUT_FILE}...")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"words": merged_list}, f, ensure_ascii=False, indent=2)

    print("🎉 Merge complete! Your dictionary is ready.")


if __name__ == "__main__":
    main()
