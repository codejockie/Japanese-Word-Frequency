import csv
import json

# ACCDB_unicode source: https://github.com/javdejong/nhk-pronunciation


keys = [
    "NID",  # 0
    "ID",  # 1
    "WAVname",  # 2
    "K_FLD",  # 3
    "ACT",  # 4
    "midashigo",  # 5
    "nhk",  # 6
    "kanjiexpr",  # 7
    "NHKexpr",  # 8
    "numberchars",  # 9
    "nopronouncepos",  # 10
    "nasalsoundpos",  # 11
    "majiri",  # 12
    "kaisi",  # 13
    "KWAV",  # 14
    "midashigo1",  # 15
    "akusentosuu",  # 16
    "bunshou",  # 17
    "ac",  # 18
]

reading_key_idx = 5
alt_reading_key_idx = 15
pitch_number_idx = 16
number_chars_idx = 9
ac_idx = 18


def parse_accdb():

    data = {}

    with open("ACCDB_unicode.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            # print(row)  # Each row is a list of values
            key = row[7]
            value = dict(zip(keys, row))
            data[key] = value

    # Write data to file
    with open("nhk_pronunciations.json", "w", encoding="utf-8") as fo:
        json.dump(data, fo, indent=4, sort_keys=False, ensure_ascii=False)


def convert_to_pitch_data():
    data = {}

    with open("ACCDB_unicode.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            key = row[7]
            reading = row[reading_key_idx]
            # altReading = row[alt_reading_key_idx]
            # pitchNumber = row[pitch_number_idx]
            # mora_count = row[number_chars_idx]
            ac = row[ac_idx]

            data[key] = [
                {"reading": reading, "altReading": None, "pitchNumber": parse_accent(ac=ac)}
            ]

    # Write data to file
    with open("nhk_pitch_info.json", "w", encoding="utf-8") as fo:
        json.dump(data, fo, indent=4, sort_keys=False, ensure_ascii=False)


def parse_accent(ac: str):
    trimmed = ac.rstrip("0")
    if not trimmed: return None

    last = int(trimmed[-1])

    if last == 1:
        accent_type = 0 # heiban
    else:
        accent_type = last - 1 # drop after this mora

    return accent_type

# parse_accdb()

convert_to_pitch_data()
