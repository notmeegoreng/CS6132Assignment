import ipaddress
import tkinter as tk
from tkinter import ttk

import table_widget

root = tk.Tk()

table_widget.init(root)

window = ttk.Frame(root, padding=10)
window.pack()

ttk.Style().configure('Error.TLabel', foreground='red')
ttk.Style().configure('App.TSeparator', padding=2)

router_frame = ttk.Frame(window, borderwidth=4, relief='ridge')  # flat, groove, raised, ridge, solid, or sunken
ttk.Label(router_frame, text='Routing Table').pack()
ttk.Separator(router_frame, orient='horizontal', style='App.TSeparator').pack(fill=tk.X, pady=2)
routing_table_widget = table_widget.RoutingTableWidget(router_frame)
routing_table_widget.pack()

router_frame.pack(side=tk.LEFT, fill=tk.Y, padx=4)

packet_frame = ttk.Frame(window, borderwidth=4, relief='ridge')

ttk.Label(packet_frame, text='Packet').pack()
ttk.Separator(packet_frame, orient='horizontal', style='App.TSeparator').pack(fill=tk.X, pady=2)
ttk.Label(packet_frame, text='Destination Address').pack()
dest_entry = ttk.Entry(packet_frame)
dest_entry.pack()
route_button = ttk.Button(packet_frame, text='Route!')
route_button.pack(pady=4)
packet_error = ttk.Label(packet_frame, style='Error.TLabel')
packet_error.pack()
packet_ans = ttk.Label(packet_frame)
packet_ans.pack()

packet_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=4)


def route_packet():
    try:
        addr = ipaddress.ip_address(dest_entry.get())
    except ValueError:
        packet_error.configure(text='Error: Invalid IP address!')
        return

    out = routing_table_widget.routing_table.route(addr)
    if out is None:
        packet_error.configure(text='Error: No route found for this IP address!')
        return

    packet_error.configure(text='')

    packet_ans.configure(text=out)


route_button.configure(command=route_packet)

root.mainloop()
