import math
import tkinter as tk


class GraphWidget(tk.Canvas):
    def __init__(self, master, *, routing_widget):
        super().__init__(master)
        self.image_id = None
        self.lines = {}
        self.highlighted = None

        self.routing_widget = routing_widget
        routing_widget.on_update = self.draw_graph
        self.bind('<Configure>', self.draw_graph)

        self.router_img = tk.PhotoImage(file='view/assets/router.ppm')
        self.packet_img = tk.PhotoImage(file='view/assets/frame.ppm')

    def draw_graph(self, event=None):
        w, h = self.winfo_width(), self.winfo_height()
        if self.image_id is not None:
            self.delete(self.image_id)
            for line_id, label in self.lines.values():
                self.delete(line_id)
                label.place_forget()
            self.lines.clear()

        interfaces = self.routing_widget.routing_table.interfaces
        n = len(interfaces)
        s = min(w, h)
        line_dist = 2 ** 0.5 * s // 3.5
        for i, interface in enumerate(interfaces.values()):
            # draw lines
            angle = 2 * math.pi * i / n
            x = w // 2 + line_dist * math.cos(angle)
            y = h // 2 + line_dist * math.sin(angle)
            line_id = self.create_line(
                w // 2, h // 2,
                x, y,
                disabledwidth=5
            )
            # draw labels
            label = tk.Label(self, text=interface)
            label.place(x=x, y=y, anchor=tk.CENTER)
            self.lines[interface] = (line_id, label)
        if self.highlighted is not None:
            # highlight line
            self.itemconfig(self.lines[self.highlighted][0], state=tk.DISABLED)
        # draw router
        self.image_id = self.create_image(w // 2, h // 2, anchor=tk.CENTER, image=self.router_img)

    def highlight_line(self, interface=None):
        if self.highlighted is not None:
            self.itemconfig(self.lines[self.highlighted][0], state=tk.NORMAL)
        self.highlighted = interface
        if interface is not None:
            self.itemconfig(self.lines[interface][0], state=tk.DISABLED)

    def animate_packet(self, interface):
        w, h = self.winfo_width(), self.winfo_height()
        packet = self.create_image(w // 2, h // 2, anchor=tk.CENTER, image=self.packet_img)
        s = min(w, h)
        i = tuple(self.lines).index(interface)
        angle = 2 * math.pi * i / len(self.lines)
        line_dist = 2 ** 0.5 * s // 3
        x = line_dist * math.cos(angle)
        y = line_dist * math.sin(angle)
        self.after(100, self.packet_moving, packet, x, y, w // 2, h // 2)

    def packet_moving(self, packet, x, y, x_i, y_i):
        x_m = x / 100
        y_m = y / 100

        def move_packet(times=0):
            self.move(packet, x_m, y_m)
            c_x, c_y = self.coords(packet)
            if abs(c_x - x_i - x) <= 25 and abs(c_y - y_i - y) <= 25:
                self.delete(packet)
            else:
                self.after(10, move_packet, times + 1)

        move_packet()
