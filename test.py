import ipaddress
import tkinter as tk
from tkinter import ttk
ipaddress.IPv4Address('127.256.2.3')
ipaddress.ip_interface('EA::1D:04/96')
r = tk.Tk()
e = ttk.Entry(r, textvariable=tk.StringVar(r))
print(dir(e))
