import tkinter as tk
from tkinter import ttk
import csv


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Rows App")
        self.rows = ['a', 'b', 'c', 'd', 'e']
        self.methods = [self.method_a, self.method_b, self.method_c, self.method_d, self.method_e]
        self.setup_ui()

    def setup_ui(self):
        self.setup_listbox()
        self.setup_buttons()
        self.bind_keys()

    def setup_buttons(self):
        for i, method in enumerate(self.methods):
            button = ttk.Button(self, text=f"Call {self.rows[i]}", command=method)
            button.grid(row=i, column=1, padx=10, pady=2)

    def setup_listbox(self):
        self.listbox = tk.Listbox(self, height=len(self.rows), width=20)
        for row in self.rows:
            self.listbox.insert(tk.END, row)
        self.listbox.grid(row=0, column=0, padx=10, pady=10)
        self.listbox.selection_set(0)  # Select the first row initially

    def bind_keys(self):
        self.bind("<Up>", self.on_up)
        self.bind("<Down>", self.on_down)
        self.bind("<Return>", self.on_enter)

    def on_up(self, event):
        current_index = self.listbox.curselection()[0]
        if current_index == 0:  # If at the first item, loop to the end
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(len(self.rows) - 1)
        else:
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(current_index - 1)
        return "break"

    def on_down(self, event):
        current_index = self.listbox.curselection()[0]
        if current_index == len(self.rows) - 1:  # If at the last item, loop to the start
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(0)
        else:
            self.listbox.selection_clear(current_index)
            self.listbox.selection_set(current_index + 1)
        return "break"

    def on_enter(self, event):
        current_index = self.listbox.curselection()[0]
        method_to_call = self.methods[current_index]
        method_to_call()

    def method_a(self):
        print("Method A called!")

    def method_b(self):
        print("Method B called!")

    def method_c(self):
        for widget in self.winfo_children():
            widget.grid_forget()
        self.show_csv_view("official_data/tsem.csv")

    def method_d(self):
        for widget in self.winfo_children():
            widget.grid_forget()
        self.show_csv_view("official_data/nsem.csv")

    def load_csv(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return list(reader)

    def show_csv_view(self, filepath):
        data = self.load_csv(filepath)


        # Setting up the Treeview
        tree = ttk.Treeview(self, columns=[f"#{i}" for i in range(len(data[0]))], show="headings")
        for i, column in enumerate(data[0]):
            tree.heading(f"#{i}", text=column)
            tree.column(f"#{i}", width=100)

        for row in data[1:]:
            tree.insert("", "end", values=row)

        tree.grid(row=0, column=0, padx=10, pady=10)

        back_button = ttk.Button(self, text="Back to Main", command=self.show_main_view)
        back_button.grid(row=1, column=0, padx=10, pady=10)

    def method_e(self):
        self.listbox.grid_forget()
        for widget in self.winfo_children():
            widget.grid_forget()

        self.show_greeting_view()

    def show_greeting_view(self):
        greeting_label = ttk.Label(self, text="Hello! Welcome to the Greeting View!")
        greeting_label.grid(row=0, column=0, padx=10, pady=10)

        back_button = ttk.Button(self, text="Back to Main", command=self.show_main_view)
        back_button.grid(row=1, column=0, padx=10, pady=10)

    def show_main_view(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.setup_listbox()
        self.setup_buttons()
        self.bind_keys()


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
