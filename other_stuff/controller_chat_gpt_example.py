import tkinter as tk


# def method1():
#     print("Method 1 called")


def method2():
    print("Method 2 called")


def method3():
    print("Method 3 called")


def method4():
    print("Method 4 called")


class ListBoxWrapper:
    def __init__(self, parent, row_actions):
        self.listbox = tk.Listbox(parent, width=100, font=("Arial", 18))
        self.row_actions = row_actions
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
        # TODO: Not tested
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
        selected_row = self.listbox.get(self.listbox.curselection())
        action = self.row_actions.get(selected_row)
        if action:
            action()

    def setup_listbox(self):
        self.populate_listbox()
        self.display_listbox()
        self.set_initial_selection()
        self.set_focus()
        self.bind_keys()


def method1():
    app.show_frame(ViewForMethod1)


row_actions = {
    "Въвеждане / Актуализация на данни за семинарите (TSEM)": method1,
    "Въвеждане / Актуализация на типовете записи (NSEM)": method2,
    "Въвеждане / Актуализация на карти за записване": method3,
    "Справка за участниците в семинар": method4,
}


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.listbox = ListBoxWrapper(self, row_actions)
        self.listbox.setup_listbox()


class ViewForMethod1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="This is the view for Method 1").pack(pady=20)
        tk.Button(self, text="Back", command=lambda: controller.show_frame(MainMenu)).pack()


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Silva DataBase")
        self.frames = {}
        for F in (MainMenu, ViewForMethod1):  # Add other views to this tuple
            frame = F(self, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, frame_class):
        """Raise the frame of the given class to the top"""
        frame = self.frames[frame_class]
        frame.tkraise()


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
