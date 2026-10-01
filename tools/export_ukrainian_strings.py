"""Supplement REDkit's 17-language export with this mod's Ukrainian label.

Default: validate inputs only. Pass --write after a normal REDkit cook to add
packed/mods/modpriceweight/content/ua.w3strings. Never installs or starts a game.
Order: cook, run this helper with --write, then install/archive without re-cooking.

Targets Remastered's RTSW version 164, zero-key UTF-8 format, observed in stock
ua.w3strings and REDkit's ar.w3strings. Reuses the native key hash from the latter.
"""

import argparse
import sqlite3
import struct
import sys
from pathlib import Path


STRING_KEY = "mod_valueweight_price_weight"
KEY_HASH = 0x52450621  # Verified in REDkit's native exports of STRING_KEY.
HEADER = struct.pack("<4sIH", b"RTSW", 164, 0)


def read_zero_key_strings(data):
    if not data.startswith(HEADER) or data[-2:] != b"\0\0":
        raise ValueError("Expected a zero-key Remastered v164 strings file")
    offset = len(HEADER)

    def number():
        nonlocal offset
        first = data[offset]
        offset += 1
        if first & 0x80:
            raise ValueError("Unexpected signed compact integer")
        result, shift, more = first & 0x3F, 6, first & 0x40
        while more:
            byte = data[offset]
            offset += 1
            result |= (byte & 0x7F) << shift
            shift += 7
            more = byte & 0x80
            if shift > 34:
                raise ValueError("Invalid compact integer")
        return result

    def records(fmt):
        nonlocal offset
        count = number()
        size = struct.calcsize(fmt)
        if offset + count * size > len(data) - 2:
            raise ValueError("Truncated strings table")
        result = [struct.unpack_from(fmt, data, offset + i * size)
                  for i in range(count)]
        offset += count * size
        return result

    directory = records("<III")
    keys = records("<II")
    text_size = number()
    if offset + text_size + 2 != len(data):
        raise ValueError("UTF-8 text table size mismatch")
    text = data[offset:offset + text_size]
    entries = []
    for string_id, start, size in sorted(directory, key=lambda row: row[1]):
        if start + size >= len(text) or text[start + size] != 0:
            raise ValueError("Invalid string bounds or terminator")
        entries.append((string_id, text[start:start + size].decode("utf-8")))
    by_id = dict(entries)
    if len(by_id) != len(entries):
        raise ValueError("Duplicate string IDs")
    # Stock packs can map keys to text supplied by a different pack.
    return entries, keys


def encode_zero_key_strings(entries, keys):
    def number(value):
        result = bytearray([(value & 0x3F) | (0x40 if value >= 64 else 0)])
        value >>= 6
        while value:
            result.append((value & 0x7F) | (0x80 if value >= 128 else 0))
            value >>= 7
        return result

    text = bytearray()
    directory = []
    for string_id, value in entries:
        if "\0" in value:
            raise ValueError("Embedded NUL in translation")
        encoded = value.encode("utf-8")
        directory.append((string_id, len(text), len(encoded)))
        text.extend(encoded + b"\0")
    result = bytearray(HEADER)
    result.extend(number(len(directory)))
    for row in sorted(directory):
        result.extend(struct.pack("<III", *row))
    result.extend(number(len(keys)))
    for row in sorted(keys):
        result.extend(struct.pack("<II", *row))
    result.extend(number(len(text)))
    result.extend(text)
    result.extend(b"\0\0")
    return bytes(result)


def prepare(project):
    content = project / "packed/mods/modpriceweight/content"
    reference = content / "ar.w3strings"
    if not reference.is_file():
        raise ValueError("Cook the project in REDkit first: ar.w3strings is missing")
    native = reference.read_bytes()
    entries, keys = read_zero_key_strings(native)
    if encode_zero_key_strings(entries, keys) != native:
        raise ValueError("Reference format changed; refusing to generate a file")

    database = project / "LocalEditorStringDataBaseW3_UTF8_mod.db"
    conn = sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)
    try:
        rows = conn.execute("""
            SELECT I.STRING_ID, S.TEXT
            FROM STRING_INFO I
            JOIN LATEST_STRINGS S ON S.STRING_ID = I.STRING_ID
            JOIN LANGUAGES L ON L.ID = S.LANG
            WHERE I.STRING_KEY = ? AND L.LANG = 'UA'
        """, (STRING_KEY,)).fetchall()
    finally:
        conn.close()
    if len(rows) != 1 or not rows[0][1] or not rows[0][1].strip():
        raise ValueError("Expected exactly one nonempty Ukrainian translation")
    string_id, translation = rows[0]
    if (KEY_HASH, string_id) not in keys:
        raise ValueError("Cooked key/ID differs from the database; recook first")
    return content / "ua.w3strings", string_id, translation


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true",
                        help="write ua.w3strings into the packed mod after cooking")
    args = parser.parse_args()
    project = Path(__file__).resolve().parent.parent
    try:
        destination, string_id, translation = prepare(project)
        print(f"Database: UA, ID {string_id}, key {STRING_KEY}")
        print(f"Translation: {translation}")
        if not args.write:
            print("Validation passed. No file written. Use --write after cooking.")
            return
        if destination.exists():
            old_entries, old_keys = read_zero_key_strings(destination.read_bytes())
            if {entry[0] for entry in old_entries} != {string_id} or old_keys != [(KEY_HASH, string_id)]:
                raise ValueError("Existing ua.w3strings contains other entries; refusing to replace it")
        result = encode_zero_key_strings([(string_id, translation)], [(KEY_HASH, string_id)])
        if read_zero_key_strings(result) != ([(string_id, translation)], [(KEY_HASH, string_id)]):
            raise ValueError("Generated file failed validation")
        if destination.exists() and destination.read_bytes() == result:
            print(f"Already up to date: {destination}")
            print("Install/archive packed now. Cooking again removes ua.w3strings; rerun this helper afterward.")
            return
        if destination.exists():
            backup = destination.with_suffix(".w3strings.previous")
            if backup.exists():
                raise ValueError(f"Move the previous backup before replacing: {backup}")
            backup.write_bytes(destination.read_bytes())
        destination.write_bytes(result)
        print(f"Created {destination} ({len(result)} bytes). Install/test manually.")
        print("Install/archive packed now. Cooking again removes ua.w3strings; rerun this helper afterward.")
    except (OSError, ValueError, IndexError, struct.error, sqlite3.Error) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
