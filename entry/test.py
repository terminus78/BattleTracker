'''
from zipfile import ZipFile
import json


with ZipFile("H:\\Projects\\Programs\\Calculator\\First Battle.brpg", "w") as savefile:
    test_obj = {
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
    testJSON = json.dumps(test_obj, indent=4)
    pref_dict = {
        "mapSize": [32, 46]
    }
    prefJSON = json.dumps(pref_dict, indent=4)
    savefile.writestr('preferences.json', prefJSON)
    savefile.writestr('creatures.json', testJSON)

var1, var2, var3 = [1, 2, 3]
print("{0} {1} {2}".format(var1, var2, var3))
'''

import tkinter as tk
import tkinter.ttk as ttk

def iter_layout(layout, tab_amnt=0, elements=[]):
    """Recursively prints the layout children."""
    el_tabs = '  '*tab_amnt
    val_tabs = '  '*(tab_amnt + 1)

    for element, child in layout:
        elements.append(element)
        print(el_tabs+ '\'{}\': {}'.format(element, '{'))
        for key, value in child.items():
            if type(value) == str:
                print(val_tabs + '\'{}\' : \'{}\','.format(key, value))
            else:
                print(val_tabs + '\'{}\' : [('.format(key))
                iter_layout(value, tab_amnt=tab_amnt+3)
                print(val_tabs + ')]')

        print(el_tabs + '{}{}'.format('} // ', element))

    return elements

def stylename_elements_options(stylename, widget):
    """Function to expose the options of every element associated to a widget stylename."""

    try:
        # Get widget elements
        style = ttk.Style()
        layout = style.layout(stylename)
        config = widget.configure()

        print('{:*^50}\n'.format(f'Style = {stylename}'))

        print('{:*^50}'.format('Config'))
        for key, value in config.items():
            print('{:<15}{:^10}{}'.format(key, '=>', value))

        print('\n{:*^50}'.format('Layout'))
        elements = iter_layout(layout)

        # Get options of widget elements
        print('\n{:*^50}'.format('element options'))
        for element in elements:
            print('{0:30} options: {1}'.format(
                element, style.element_options(element)))

    except tk.TclError:
        print('_tkinter.TclError: "{0}" in function'
                'widget_elements_options({0}) is not a regonised stylename.'
                .format(stylename))

widget = ttk.Button(None)
class_ = widget.winfo_class()
stylename_elements_options(class_, widget)