import pathlib
import json
import os
import math
import copy
from tkinter.constants import S
from typing import Sized
from zipfile import ZipFile

import tkinter as tk
from tkinter import Text, ttk,font,messagebox
from ttkthemes import ThemedStyle
import PIL.Image
from PIL import ImageTk


class BuildClass():
    def __init__(self, root):
        self.root = root