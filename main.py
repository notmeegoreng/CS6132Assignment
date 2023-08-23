import ipaddress
import tkinter as tk
from tkinter import ttk

from view import widgets

root = tk.Tk()

widgets.init(root)

window = ttk.Frame(root, padding=10)
window.pack()

ttk.Style().configure('Error.TLabel', foreground='red')
ttk.Style().configure('App.TSeparator', padding=2)


router_frame = ttk.Frame(window, borderwidth=4, relief='ridge')  # flat, groove, raised, ridge, solid, or sunken
ttk.Label(router_frame, text='Routing Table').pack()
ttk.Separator(router_frame, orient='horizontal', style='App.TSeparator').pack(fill=tk.X, pady=2, expand=tk.TRUE)
routing_table_widget = widgets.RoutingTableWidget(router_frame)
routing_table_widget.pack(expand=True)

router_frame.pack(side=tk.LEFT, fill=tk.Y, padx=4, expand=True)

graph_frame = ttk.Frame(window, borderwidth=4, relief='ridge')
graph_widget = widgets.GraphWidget(graph_frame, routing_widget=routing_table_widget)
graph_widget.pack(fill=tk.BOTH)

graph_frame.pack(side=tk.BOTTOM, before=router_frame, fill=tk.X, padx=4, pady=8, expand=True)
image_id = None


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

packet_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=4, expand=True)


def route_packet():
    try:
        addr = ipaddress.ip_address(dest_entry.get())
    except ValueError:
        packet_error.configure(text='Error: Invalid IP address!')
        return

    ident, addr = routing_table_widget.routing_table.route(addr)
    if ident is None:
        packet_error.configure(text='Error: No route found for this IP address!')
        return

    packet_error.configure(text='')

    packet_ans.configure(text=ident)
    graph_widget.highlight_line(addr)


route_button.configure(command=route_packet)

root.mainloop()
