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

        self.router_img = tk.PhotoImage(file='view/router.ppm')

    def draw_graph(self, event=None):
        print('drawing graph')
        w, h = self.winfo_width(), self.winfo_height()
        print(w, h)
        if abs(w - h) > 10:
            print('config')
            self.configure(height=w)
            return
        if self.image_id is not None:
            self.delete(self.image_id)
            for line_id, label in self.lines.values():
                self.delete(line_id)
                label.place_forget()
            self.lines.clear()
        print(self.winfo_width(), self.winfo_height())

        interfaces = self.routing_widget.routing_table.interfaces
        n = len(interfaces)
        line_dist = (w ** 2 + h ** 2) ** 0.5 // 4
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
        # draw router
        self.image_id = self.create_image(w // 2, h // 2, anchor=tk.CENTER, image=self.router_img)

    def highlight_line(self, address):
        if self.highlighted is not None:
            self.itemconfig(self.highlighted, state=tk.NORMAL)
        self.highlighted = self.lines[address][0]
        self.itemconfig(self.highlighted, state=tk.DISABLED)
