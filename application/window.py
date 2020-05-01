from tkinter import *    # Carga módulo tk (widgets estándar)
from tkinter import ttk  # Carga ttk (para widgets nuevos 8.5+)


class Window:
    BOTTOM_SIDE = BOTTOM
    window = None

    def __init__(self, title, width=350, height=150):
        self.base = Tk()
        self.base.geometry('{0}x{1}'.format(width, height))
        self.base.configure(bg='beige')
        self.base.title(title)
        self.component = {}
        self.nextId = 0
        self.base.withdraw()
        self.inputVar = {}

    def add_component(self, component, side=None, px=0, py=0, is_expandable=True, column=-1, row=-1, columnspan=1,
                      sticky=""):
        self.component[self.nextId] = component
        if column >= 0 and row >= 0:
            component.grid(column=column, row=row, columnspan=columnspan, padx=px, pady=py, sticky=sticky)
        else:
            component.pack(side=side, expand=is_expandable, fill=BOTH, padx=px, pady=py)
        self.nextId += 1
        return self.nextId - 1

    def add_button(self, text, command, side=BOTTOM, px=0, py=0, column=-1, row=-1, columnspan=1):
        return self.add_component(ttk.Button(self.base, text=text, command=command), side, is_expandable=False,
                                  px=px, py=py, column=column, row=row, columnspan=columnspan)

    def add_text(self, text, width=400, height=300, side=TOP, px=0, py=0, column=-1, row=-1, columnspan=1):
        id = self.add_component(Text(self.base, width=width, height=height), side, px=px, py=py, column=column, row=row,
                                columnspan=columnspan, is_expandable=False)
        self.component[id].insert("1.0", text)
        return id

    def add_label(self, text="", side=TOP, font=None, anchor="e", px=0, py=0, column=-1, row=-1, columnspan=1):
        return self.add_component(Label(self.base, text=text, font=font, anchor=anchor), side=side, px=px, py=py, column=column,
                                  row=row, columnspan=columnspan, is_expandable=False)

    def add_linear_separator(self, side=TOP, px=0, py=0, column=-1, row=-1, columnspan=1):
        return self.add_component(ttk.Separator(self.base, orient=HORIZONTAL), side=side, px=px, py=py, column=column,
                                  row=row, columnspan=columnspan, is_expandable=True, sticky="ew")

    def change_label_properties(self, id, text=None):
        c = self.component[id]
        if text is not None:
            c['text'] = text

    def get_text_component(self, id):
        return self.component[id]['text']

    def add_input(self, width=40, side=TOP, px=0, py=0, column=-1, row=-1, columnspan=1):
        self.inputVar[self.nextId] = StringVar()
        return self.add_component(Entry(self.base, textvariable=self.inputVar[self.nextId], width=width),
                                  side=side, px=px, py=py, column=column, row=row, columnspan=columnspan,
                                  is_expandable=False)

    def delete_text(self, id):
        self.component[id].delete(0,END)

    def get_input(self, id):
        return self.component[id].get()

    def open_window(self, window):
        self.base.destroy()
        window.show()

    def hide(self):
        self.base.withdraw()

    def close(self):
        self.base.destroy()

    def show(self):
        self.base.update()
        self.base.deiconify()
        self.base.mainloop()
