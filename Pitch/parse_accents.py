import csv
import json
import re


def parse_string(s: str):
    # Try to match labeled format like (副)0,(名)3
    matches = re.findall(r"\((.*?)\)(\d+)", s)

    if matches:
        # Convert numbers to int
        return [(char, int(num)) for char, num in matches]
    else:
        # Otherwise, it's just numbers separated by commas
        # nums = [int(x) for x in s.split(",")]
        return [(None, int(x)) for x in s.split(",")]


def parsetojson():
    data = {}

    with open("accents.txt", "r") as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            word = row[0]
            reading = row[1]
            pitch = row[2]

            reading = reading if reading else word

            if len(pitch) == 1:
                pitch_number = int(pitch)
                data[word] = [
                    {
                        "reading": reading,
                        "altReading": None,
                        "pitchNumber": pitch_number,
                    }
                ]
            else:
                # Find all (text, number) pairs
                value = []
                result = parse_string(pitch)

                for item in result:
                    (altReading, pitch_number) = item
                    value.append(
                        {
                            "reading": reading,
                            "altReading": altReading,
                            "pitchNumber": pitch_number,
                        }
                    )

                data[word] = value

    # Write data to file
    with open("accents.json", "w", encoding="utf-8") as fo:
        json.dump(data, fo, indent=4, sort_keys=False, ensure_ascii=False)


parsetojson()

# print(re.findall(r"\((.*?)\)(\d+)", "(副)0,(名)3"))
# print(parse_string("3,0"))
