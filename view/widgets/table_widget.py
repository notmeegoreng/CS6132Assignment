import ipaddress
import tkinter as tk
from tkinter import ttk, filedialog

from view import routing_table


def init(root):
    ttk.Style().configure('RouteTable.TFrame', padding=2, background='grey')
    ttk.Style().configure('RouteTable.TEntry', padding=2)
    ttk.Style().configure('RouteTable.AButton', )

    def _table_validate_number(ins: str):
        return ins.isnumeric()

    def _table_validate_interface():
        return True

    TableEntry.table_validate_number = root.register(_table_validate_number)
    TableEntry.table_validate_interface = root.register(_table_validate_interface)


class TableEntry(ttk.Entry):
    table_validate_number = None
    table_validate_interface = None

    def __init__(self, master, validate_command):
        super().__init__(master, style='RouteTable.TEntry', validate='key', validatecommand=validate_command)
        self.bindtags(self.bindtags() + ('router_table_entry',))


class RoutingTableWidget(ttk.Frame):
    def __init__(self, master, data=None, *, on_update=lambda: None):
        super().__init__(master)
        self.on_update = on_update

        self.table_with_header = ttk.Frame(self)
        self.table_with_header.grid(row=0, columnspan=2)

        self.table_header = ttk.Frame(self)
        self.table_header.grid(row=0, columnspan=2, sticky=tk.EW)
        self.table_header.grid_columnconfigure(0, weight=1)
        self.table_header.grid_columnconfigure(1, weight=1)
        ttk.Label(self.table_header, text='Interface Number').grid(row=0, column=0)
        ttk.Label(self.table_header, text='Interface Address').grid(row=0, column=1)

        self.table = ttk.Frame(self, style='RouteTable.TFrame', borderwidth=1, relief='raised')
        self.table.grid(row=1, columnspan=2)

        # populate table
        if not data:
            data = (('', ''),)
        self.entries = []
        self.grid_last_index = 0
        self.populate(data)
        self.table.bind_class('router_table_entry', '<Key>', self.on_key)
        self.table.bind_class('router_table_entry', '<Return>', self.on_return_key)

        ttk.Button(self, text='+', command=self.add_row).grid(row=2, column=0, sticky=tk.W, pady=4)
        ttk.Button(self, text='-', command=self.remove_row).grid(row=2, column=1, sticky=tk.E, pady=4)

        ttk.Button(self, text='Save', command=self.save).grid(row=4, column=0, sticky=tk.W, pady=4)
        ttk.Button(self, text='Load', command=self.load).grid(row=4, column=1, sticky=tk.E, pady=4)

        self.mode = ttk.Label(self)
        self.mode.grid(row=5, columnspan=2)
        self.error = ttk.Label(self, style='Error.TLabel')
        self.error.grid(row=6, columnspan=2, pady=4)

        self.changed = False
        self.routing_table = routing_table.RoutingTable()

    def populate(self, data):
        for e0, e1 in self.entries:
            e0.grid_forget()
            e1.grid_forget()
        self.entries.clear()
        i = 1
        for i, (a, b) in enumerate(data, 1):
            e0, e1 = self.add_table_entries(i)
            e0.insert(0, a)
            e1.insert(0, str(b))

        self.grid_last_index = i

    def add_table_entries(self, row):
        e0 = TableEntry(self.table, validate_command=(TableEntry.table_validate_number, '%P'))
        e1 = TableEntry(self.table, validate_command=TableEntry.table_validate_interface)
        e0.grid(row=row, column=0)
        e1.grid(row=row, column=1)
        self.entries.append((e0, e1))
        return e0, e1

    def add_row(self):
        self.grid_last_index += 1
        self.add_table_entries(self.grid_last_index)

    def remove_row(self):
        if self.grid_last_index == 1:
            # error: cannot remove last
            self.error.configure(text='The last row cannot be removed!')
            return
        self.error.configure(text='')
        self.grid_last_index -= 1
        entries = self.entries.pop()
        entries[0].grid_forget()
        entries[1].grid_forget()

        self.update_table()

    def save(self):
        file = filedialog.asksaveasfile(parent=self, title='Save Routing Config', defaultextension='rcf')
        if file is None:
            return
        self.routing_table.store(file)

    def load(self):
        file = filedialog.askopenfile(parent=self, title='Load Routing Config', defaultextension='rcf')
        if file is None:
            return
        self.routing_table = routing_table.RoutingTable.load(file)
        self.populate(self.routing_table.interfaces.items())
        self.on_update()

    def on_key(self, event):
        self.changed = True
        self.mode.configure(text='Editing mode. Press enter to save changes.')

    def on_return_key(self, event):
        if self.changed:
            try:
                self.update_table()
            except ValueError:
                self.error.configure(text='Invalid IP interface address! Format: <address>/<mask size>')
                return
            self.error.configure(text='')
            self.changed = False
            self.mode.configure(text='')

    def convert(self):
        d = {int(a.get()): ipaddress.ip_interface(b.get()) for a, b in self.entries if a and b}
        return d

    def update_table(self):
        self.routing_table.interfaces = self.convert()
        self.on_update()

