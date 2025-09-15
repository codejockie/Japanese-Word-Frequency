import json
import os

# A modified version of the code from: https://github.com/Bluskyo/JLPT_Vocabulary


def makeCSV():
    directory = os.getcwd()
    filepath = os.path.join(directory, "JLPT Vocabulary")
    with open(f"{filepath}/jlpt_vocabulary.csv", "w") as writeFile:
        writeFile.write(f"Vocabulary,JLPT Level\n")
        for level in range(1, 6):
            with open(f"{filepath}/N{level}.txt") as file:
                for line in file:
                    writeFile.write(f"{line.strip()},N{level}\n")


def makeJSON():
    dictonary = {}
    directory = os.getcwd()
    filepath = os.path.join(directory, "JLPT Vocabulary")

    for level in range(1, 6):
        with open(f"{filepath}/N{level}.txt") as file:
            for line in file:
                dictonary[line.strip()] = f"N{level}"

    dictonaryJson = json.dumps(dictonary, indent=4, ensure_ascii=False)

    with open(f"{filepath}/jlpt_vocabulary.json", "w", encoding="utf-8") as writeFile:
        writeFile.write(dictonaryJson)


makeCSV()
makeJSON()
