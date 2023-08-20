import tkinter as tk
from tkinter import ttk

r = tk.Tk()
e = ttk.Entry(r, textvariable=tk.StringVar(r))
print(dir(e))
