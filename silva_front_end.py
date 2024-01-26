import tkinter as tk


def method1():
    print("Method 1 called")


def method2():
    print("Method 2 called")


def method3():
    print("Method 3 called")


def method4():
    print("Method 4 called")


class Router:
    def __init__(self, parent, rows):
        self.listbox = tk.Listbox(parent, width=100, font=("Arial", 20))
        self.rows = rows
        self.parent = parent

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for row in self.rows:
            self.listbox.insert(tk.END, row)
        self.listbox.config(height=len(self.rows))

    def display_listbox(self):
        self.listbox.grid(row=0, column=0, padx=10, pady=10)

    def set_initial_selection(self):
        self.listbox.selection_set(0)

    def set_focus(self):
        self.listbox.focus_set()

    def bind_keys(self):
        self.listbox.bind("<Up>", self.on_up)
        self.listbox.bind("<Down>", self.on_down)
        self.listbox.bind("<Return>", self.on_enter)

    def on_up(self, event):
        current_index = self.listbox.curselection()[0]
        if current_index == 0:
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(len(self.rows) - 1)
        else:
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(current_index - 1)
        return "break"

    def on_down(self, event):
        current_index = self.listbox.curselection()[0]
        if current_index == len(self.rows) - 1:
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(0)
        else:
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(current_index + 1)
        return "break"

    def on_enter(self, event):
        current_selection = self.listbox.curselection()[0]
        return self.parent.router_navigation(current_selection)

    def setup_listbox(self):
        self.populate_listbox()
        self.display_listbox()
        self.set_initial_selection()
        self.set_focus()
        self.bind_keys()


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Silva DataBase")
        self.row_actions = {
            "Въвеждане / Актуализация на данни за семинарите (TSEM)": self.tsem_view,
            "Въвеждане / Актуализация на типовете записи (NSEM)": method2,
            "Въвеждане / Актуализация на карти за записване": method3,
            "Справка за участниците в семинар": method4,
        }
        self.current_view = Router(self, list(self.row_actions.keys()))
        self.current_view.setup_listbox()

    def router_navigation(self, current_selection):
        self.row_actions[self.current_view.rows[current_selection]]()

    def back_to_router(self):
        self.current_view = Router(self, list(self.row_actions.keys()))
        self.current_view.setup_listbox()

    def tsem_view(self):
        self.current_view = TsemView(self)


class TsemView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="TSEM view")
        self.label.pack()

        self.button = tk.Button(self.frame, text="Back", command=self.parent.back_to_router)
        self.button.pack()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
