import tkinter as tk



class MainView(tk.Frame):
    def __init__(self, parent, controller, subviews):
        super().__init__(parent)
        self.controller = controller
        self.subviews = subviews
        self.listbox = tk.Listbox(self, width=100, font=("Arial", 20))

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for view_name in self.subviews: # Exclude the MainView itself
            self.listbox.insert(tk.END, view_name)
        self.listbox.pack(pady=20)
        self.listbox.config(height=len(self.subviews))

    def display_listbox(self):
        self.listbox.grid(row=0, column=0, padx=10, pady=10)

    def set_initial_selection(self):
        self.listbox.selection_set(0)

    def set_focus(self):
        self.listbox.focus_set()

    def bind_keys(self):
        self.listbox.bind("<Up>", self.on_up)
        self.listbox.bind("<Down>", self.on_down)
        self.listbox.bind("<Return>", self.on_select)

    def on_up(self, event):
        current_index = self.listbox.curselection()[0]
        if current_index == 0:
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(len(self.subviews) - 1)
        else:
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(current_index - 1)
        return "break"

    def on_down(self, event):
        current_index = self.listbox.curselection()[0]
        if current_index == len(self.subviews) - 1:
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(0)
        else:
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(current_index + 1)
        return "break"

    def on_select(self, event):
        selected_option = self.listbox.get(self.listbox.curselection())
        self.controller.show_frame(selected_option)

    def set_view(self):
        self.populate_listbox()
        self.display_listbox()
        self.set_initial_selection()
        self.set_focus()
        self.bind_keys()
