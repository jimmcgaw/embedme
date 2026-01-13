#!/usr/bin/env python
import json
import os
import re
import unicodedata

from html.parser import HTMLParser
from html import unescape


class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__(
            convert_charrefs=False
        )  # we’ll handle entity decoding ourselves
        self._chunks = []

    def handle_data(self, data):
        self._chunks.append(data)

    def handle_entityref(self, name):
        self._chunks.append(f"&{name};")

    def handle_charref(self, name):
        self._chunks.append(f"&#{name};")

    def get_text(self):
        return unescape("".join(self._chunks))


def strip_html(text: str) -> str:
    """
    Remove HTML tags from `text` and return plain text.
    Also decodes HTML entities like &amp; -> &.
    """
    if not text:
        return ""
    stripper = _HTMLStripper()
    stripper.feed(text)
    stripper.close()
    return stripper.get_text()


# Matches ASCII control characters except valid JSON whitespace
# JSON allows: \t (0x09), \n (0x0A), \r (0x0D)
_JSON_UNSAFE_CTRL = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")


def json_safe_string(
    value: str, *, normalize: bool = True, replace_with: str = ""
) -> str:
    """
    Strip characters that are unsafe for JSON serialization.

    - Removes ASCII control chars forbidden by JSON
    - Removes invalid Unicode (unpaired surrogates)
    - Optionally normalizes Unicode (NFC)

    Args:
        value: Input string
        normalize: Apply Unicode NFC normalization
        replace_with: Replacement for removed characters

    Returns:
        JSON-safe string
    """
    if not isinstance(value, str):
        value = str(value)

    # Normalize Unicode (recommended for storage/search consistency)
    if normalize:
        value = unicodedata.normalize("NFC", value)

    # Remove invalid UTF-16 surrogate code points
    value = value.encode("utf-8", "surrogatepass").decode("utf-8", "ignore")

    # Remove disallowed JSON control characters
    value = _JSON_UNSAFE_CTRL.sub(replace_with, value)

    return value


BOOKS_IN_ORDER = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalms",
    "Proverbs",
    "Ecclesiastes",
    "Song of Solomon",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation",
]

bible = []

for book_number, book_name in enumerate(BOOKS_IN_ORDER, start=1):
    dir_name = f"./BibleJSON/JSON/{book_name}"
    print(book_name)
    chapters = os.listdir(dir_name)
    chapter_numbers = sorted([int(x.replace(".json", "")) for x in chapters])
    for chapter_number in chapter_numbers:
        chapter_file = f"{chapter_number}.json"
        file_path = f"{dir_name}/{chapter_file}"
        with open(file_path, "r") as f:
            verses = json.load(f)["verses"]
            for verse_json in verses:
                text = strip_html(verse_json["text"])
                text = text.replace("¶", "")
                text = text.replace("Jud\u00e6a", "Judea")
                text = text.replace("G\u1d0f\u1d05", "God")
                text = text.replace("\u00c6non", "Aenon")
                text = text.replace("\u00c6neas", "Aeneas")
                text = text.strip()

                bible.append(
                    {
                        "text": text,
                        "verse": verse_json["verse"],
                        "chapter": verse_json["chapter"],
                        "book": book_name,
                        "book_number": book_number,
                    }
                )

with open("bible.json", "w+") as f:
    json.dump(bible, f)
