from zipfile import ZipFile
import json

'''
with ZipFile("H:\\Projects\\Programs\\Calculator\\First Battle.brpg", "w") as savefile:
    testObj = {
        "TestDog": {
            "name": "TestDog",
            "hP": "5",
            "type": "ally",
            "height": "1",
            "size": "small",
            "coordinate": [
                "1",
                "1",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "\n"
        },
        "TestBird": {
            "name": "TestBird",
            "hP": "1",
            "type": "enemy",
            "height": "1",
            "size": "tiny",
            "coordinate": [
                "",
                "",
                ""
            ],
            "condition": [
                "normal"
            ],
            "notes": "Skwauk\n"
        },
        "TestCat": {
            "name": "TestCat",
            "hP": "6",
            "type": "dead",
            "height": "1",
            "size": "small",
            "coordinate": [
                "20",
                "32",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "Aww sad kitty\n"
        },
        "TestChicken": {
            "name": "TestChicken",
            "hP": "1",
            "type": "bystander",
            "height": "1",
            "size": "tiny",
            "coordinate": [
                "5",
                "16",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "He never wanted this\n"
        },
        "TestPig": {
            "name": "TestPig",
            "hP": "10",
            "type": "ally",
            "height": "1",
            "size": "medium",
            "coordinate": [
                "19",
                "7",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "An unlikely but hardy friend\n"
        },
        "TestShark": {
            "name": "TestShark",
            "hP": "15",
            "type": "enemy",
            "height": "1",
            "size": "medium",
            "coordinate": [
                "29",
                "29",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "What the hell is a shark doing here?\n"
        },
        "TestLemming": {
            "name": "TestLemming",
            "hP": "0",
            "type": "dead",
            "height": "1",
            "size": "tiny",
            "coordinate": [
                "",
                "",
                ""
            ],
            "condition": [
                "normal"
            ],
            "notes": "Well, we saw that coming\n"
        },
        "TestBigBad": {
            "name": "TestBigBad",
            "hP": "50",
            "type": "enemy",
            "height": "3",
            "size": "huge",
            "coordinate": [
                "16",
                "23",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "Oof\n"
        },
        "TestFox": {
            "name": "TestFox",
            "hP": "5",
            "type": "bystander",
            "height": "1",
            "size": "small",
            "coordinate": [
                "",
                "",
                ""
            ],
            "condition": [
                "normal"
            ],
            "notes": "Foxy\n"
        },
        "TestApe": {
            "name": "TestApe",
            "hP": "10",
            "type": "enemy",
            "height": "1",
            "size": "medium",
            "coordinate": [
                "1",
                "1",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "\n"
        },
        "TestBiggerGooder": {
            "name": "TestBiggerGooder",
            "hP": "400",
            "type": "ally",
            "height": "4",
            "size": "gargantuan",
            "coordinate": [
                "7",
                "5",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "When godzilla decides to help...\n"
        }
    }
    testJSON = json.dumps(testObj, indent=4)
    prefDict = {
        "mapSize": [32, 46]
    }
    prefJSON = json.dumps(prefDict, indent=4)
    savefile.writestr('preferences.json', prefJSON)
    savefile.writestr('creatures.json', testJSON)

var1, var2, var3 = [1, 2, 3]
print("{0} {1} {2}".format(var1, var2, var3))
'''