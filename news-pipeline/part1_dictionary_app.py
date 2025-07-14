import zipfile
import os

# File contents for part1
part1_code = '''"""part1_dictionary_app.py – English ➜ French ➜ German translator"""

a2f = {
    "cat": "chat",
    "dog": "chien",
    "car": "voiture",
    "house": "maison",
    "book": "livre",
    "black": "noir",
    "white": "blanc",
    "food": "nourriture",
}

f2g = {
    "chat": "Katze",
    "chien": "Hund",
    "voiture": "Auto",
    "maison": "Haus",
    "livre": "Buch",
    "noir": "schwarz",
    "blanc": "weiß",
    "nourriture": "Essen",
}

def translate_via_french(en_word: str):
    fr_word = a2f.get(en_word.lower())
    if fr_word is None:
        return None, None
    de_word = f2g.get(fr_word)
    return fr_word, de_word

if __name__ == "__main__":
    word = input("Enter an English word ▶ ")
    fr, de = translate_via_french(word)
    if fr:
        print(f"French : {fr}")
        if de:
            print(f"German : {de}")
    else:
        print("❌ Word not found in the mini-dictionary.")
'''

# File contents for part2
part2_code = '''"""part2_reordering_dictionary.py – English ➜ French with adjective–noun re-ordering"""

lexicon = {
    "black": "noir",
    "white": "blanc",
    "big": "grand",
    "small": "petit",
    "cat": "chat",
    "dog": "chien",
    "car": "voiture",
}

adjectives_en = {"black", "white", "big", "small"}

def translate_and_reorder(phrase: str) -> str:
    words = phrase.lower().split()
    fr_adjs, fr_nouns = [], []
    for w in words:
        fr = lexicon.get(w)
        if fr is None:
            raise ValueError(f"Unknown word: {w}")
        (fr_adjs if w in adjectives_en else fr_nouns).append(fr)
    return " ".join(fr_nouns + fr_adjs)

if __name__ == "__main__":
    s = input("Enter an English noun phrase ▶ ")
    print("French :", translate_and_reorder(s))
'''

# Write both files to a zip archive
zip_path = "/mnt/data/lab2_dictionary_app.zip"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    zipf.writestr("part1_dictionary_app.py", part1_code)
    zipf.writestr("part2_reordering_dictionary.py", part2_code)

zip_path
