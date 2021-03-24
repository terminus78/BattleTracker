import pathlib
import json

obj = {
        "a": "1",
        "b": "2",
        "c": "3"
    }
obj2 = {
        "d": "4",
        "e": "5",
        "f": "6"
    }


jsonFile = pathlib.Path("jsonFile.json")
if jsonFile.exists() == False:
    with open("jsonFile.json", "w") as savefile:
        json.dump(obj, savefile)
else:
    with open("jsonFile.json", "r") as savefile:
        readObj = json.load(savefile)
        readObj.update(obj2)
    with open("jsonFile.json", "w") as savefile:
        json.dump(readObj, savefile)