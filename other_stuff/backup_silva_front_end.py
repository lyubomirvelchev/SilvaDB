import tkinter as tk


def method1():
    print("Method 1 called")


def method2():
    print("Method 2 called")


def method3():
    print("Method 3 called")


def method4():
    print("Method 4 called")


row_actions = {
    "Въвеждане / Актуализация на данни за семинарите (TSEM)": method1,
    "Въвеждане / Актуализация на типовете записи (NSEM)": method2,
    "Въвеждане / Актуализация на карти за записване": method3,
    "Справка за участниците в семинар": method4,
}


class ListBoxWrapper:
    def __init__(self, parent, row_actions):
        self.listbox = tk.Listbox(parent, width=100, font=("Arial", 20))
        self.rows = list(row_actions.keys())

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
        self.listbox = ListBoxWrapper(self, row_actions)
        self.listbox.setup_listbox()


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
