import sqlite3
import json
import os
import re
import statistics
import unicodedata


def convert(filepath: str):
    # Load JSON data
    with open(file=filepath, mode="r") as file:
        data = json.load(file)

    filename = os.path.splitext(os.path.basename(filepath))[0]
    print(f"Processing {filename}.json...")

    # Connect to SQLite database (or create one if it doesn't exist)
    with sqlite3.connect(f"databases/{filename}.db") as conn:
        cursor = conn.cursor()

        # Create a table
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS word_frequency (
                word TEXT NOT NULL,
                frequency INTEGER
            );
            """
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_word_frequency_word ON word_frequency(word);"
        )

        # Insert JSON data into the table
        for word, freq in zip(data.keys(), data.values()):
            try:
                # Convert the string to a list of integers
                frequencies = [int(num) for num in freq.split(",")]
                frequency = max(frequencies)
                cursor.execute(
                    f"INSERT INTO word_frequency (word, frequency) VALUES (?, ?)",
                    (word, frequency),
                )
            except ValueError:
                frequencies = re.findall(r"\d+", freq)
                frequencies = list(map(int, frequencies))
                frequency = max(frequencies)
                cursor.execute(
                    f"INSERT INTO word_frequency (word, frequency) VALUES (?, ?)",
                    (word, frequency),
                )


def create_dbs():
    directory = "vocabulary"
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):  # Ensure it's a file
            convert(filepath)


def get_frequencies(key: str, directory: str) -> list[str]:
    """Gets all frequency data available in all JSON files for a given word (key).
    This is used in situations where the frequency is a word like 'Very rare' instead a numeric value.
    """
    frequencies = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):  # Ensure it's a file
            with open(filepath, "r") as file:
                data = json.load(file)
                try:
                    frequency = data[key]
                    if frequency and frequency.isdigit():
                        frequencies.append(frequency)
                except KeyError:
                    print(f"Key ({key}) not found")
    return frequencies


def combine_sources(directory: str):
    """Creates a DB of word frequency by parsing the JSON frequency files and inserting the data into a table in the DB."""
    # Connect to SQLite database (or create one if it doesn't exist)
    with sqlite3.connect(f"databases/{directory}_frequency.db") as conn:
        cursor = conn.cursor()

        # Create a table
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS word_frequency (
                word TEXT NOT NULL,
                source TEXT NOT NULL,
                frequency INTEGER,
                PRIMARY KEY(word, source)
            );
            """
        )

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):  # Ensure it's a file
                print(f"Processing {filename}...")
                source = os.path.splitext(os.path.basename(filepath))[0]
                # Load JSON data
                with open(file=filepath, mode="r") as file:
                    data = json.load(file)
                    if type(data) is list:
                        process_list(data=data, source=source, cursor=cursor)
                    elif type(data) is dict:
                        process_dicts(
                            data=data, source=source, cursor=cursor, directory=directory
                        )

                print(f"Processed {filename}!")


# data will have a structure like: ["二","freq",1] OR ["の","freq",{"value":1,"displayValue":"1"}]
def process_list(data, source: str, cursor: sqlite3.Cursor):
    """Processes list based JSON files such that the content is a list of lists."""
    for array in data:
        word, _, value = array
        pattern = r"<[^>]+>"
        if bool(re.search(pattern, word)):
            continue
        if not contains_full_width_alphanumeric(word):
            continue
        if contains_full_width_numbers(word):
            continue

        if type(value) is int:
            cursor.execute(
                f"INSERT OR IGNORE INTO word_frequency (word, source, frequency) VALUES (?, ?, ?)",
                (word, source, value),
            )
        elif type(value) is dict:
            frequency = value["value"]
            cursor.execute(
                f"INSERT OR IGNORE INTO word_frequency (word, source, frequency) VALUES (?, ?, ?)",
                (word, source, frequency),
            )


def process_dicts(data, source: str, cursor: sqlite3.Cursor, directory: str):
    """Processes dictionary based JSON files such that the content is made of up keys and values."""
    for word, freq in zip(data.keys(), data.values()):
        try:
            # Is freq equals "Very rare"
            if freq == "Very rare":
                frequencies = get_frequencies(word, directory)
                if len(frequencies) > 0:
                    frequencies = list(map(int, frequencies))
                    frequency = statistics.mean(frequencies)
                    cursor.execute(
                        f"INSERT OR IGNORE INTO word_frequency (word, source, frequency) VALUES (?, ?, ?)",
                        (word, source, frequency),
                    )
            else:
                # Convert the string to a list of integers
                frequencies = [int(num) for num in freq.split(",")]
                frequency = max(frequencies)
                cursor.execute(
                    f"INSERT OR IGNORE INTO word_frequency (word, source, frequency) VALUES (?, ?, ?)",
                    (word, source, frequency),
                )
        except (
            ValueError
        ):  # catches integer conversion error where frequency contains '㋕'
            frequencies = re.findall(r"\d+", freq)
            frequencies = list(map(int, frequencies))
            frequency = max(frequencies)
            cursor.execute(
                f"INSERT OR IGNORE INTO word_frequency (word, source, frequency) VALUES (?, ?, ?)",
                (word, source, frequency),
            )


def is_full_width(char):
    return unicodedata.east_asian_width(char) in ["W", "F"]


def is_fullwidth_number(char):
    """Check if a character is a full-width (Zenkaku) number."""
    return char.isdigit() and unicodedata.east_asian_width(char) == "F"


def contains_full_width_alphanumeric(text):
    return any(is_full_width(char) and char.isalnum() for char in text)


def contains_full_width_numbers(text):
    pattern = r"[\uFF10-\uFF19]"
    return any(is_fullwidth_number(char) for char in text)


def process_jmdict():
    directory = os.getcwd()

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                source = os.path.splitext(os.path.basename(filepath))[0]

                with open(file=filepath, mode="r") as file:
                    data = json.load(file)

                    # Connect to SQLite database (or create one if it doesn't exist)
                    with sqlite3.connect(f"databases/{source}.db") as conn:
                        cursor = conn.cursor()

                        # Create a table
                        cursor.execute(
                            f"""
                            CREATE TABLE IF NOT EXISTS word_frequency (
                                word TEXT NOT NULL,
                                frequency INTEGER
                            );
                            """
                        )
                        cursor.execute(
                            "CREATE INDEX IF NOT EXISTS idx_word_frequency_word ON word_frequency(word);"
                        )

                        for array in data:
                            word, _, value = array
                            pattern = r"<[^>]+>"
                            if bool(re.search(pattern, word)):
                                continue
                            # Skip non-alphanumeric
                            if not contains_full_width_alphanumeric(word):
                                continue
                            # Skip zenkaku numeric
                            if contains_full_width_numbers(word):
                                continue

                            if type(value) is int:
                                cursor.execute(
                                    f"INSERT INTO word_frequency (word, frequency) VALUES (?, ?)",
                                    (word, value),
                                )
                            elif type(value) is dict:
                                frequency = value["value"]
                                cursor.execute(
                                    f"INSERT INTO word_frequency (word, frequency) VALUES (?, ?)",
                                    (word, frequency),
                                )


# process_jmdict()
combine_sources(directory="kanji")
combine_sources(directory="vocabulary")
