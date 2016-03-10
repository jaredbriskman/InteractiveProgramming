import tkSimpleDialog
from Tkinter import *

import tkSimpleDialog

class MyDialog(tkSimpleDialog.Dialog):

    def body(self, other):
        Label(other, text="BPM:").grid(row=0)
        Label(other, text="Bars:").grid(row=1)
        self.e1 = Entry(other)
        self.e2 = Entry(other)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        try:
            first = int(self.e1.get())
            second = int(self.e2.get())
        except:
            first, second = 120, 8
        self.result = first, second

    def values(self):
        return self.result
