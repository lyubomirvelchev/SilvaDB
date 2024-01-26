import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pandas as pd


class TsemView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.df = pd.read_csv('official_data/tsem.csv')  # Load data when the class is instantiated
        self.df = self.df.sort_values(by=['ZAPT'])

    def go_back(self):
        self.parent.show_frame("MainView")

    def load_csv_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, row in self.df.iterrows():
            self.tree.insert('', 'end', values=list(row))

    def add_new_record(self):
        new_data = simpledialog.askstring("New Record", "Enter new record (comma separated): Код,Наименование")
        if new_data:
            try:
                kod, name = new_data.split(',')
                if kod in self.df['ZAPT'].values:
                    messagebox.showerror("Error", "Този код вече съществува!\nНе са направени промени!")
                    return
                self.df.loc[len(self.df.index)] = [kod, name]
                self.df.to_csv('official_data/tsem.csv', index=False)
                self.load_csv_data()
                messagebox.showinfo("Success", "Успешно добавен запис!")
            except ValueError:
                messagebox.showerror("Error", "Невалидни данни!")

    def delete_record(self):
        delete_id = simpledialog.askstring("Delete Record", "Enter ID to delete:")
        if delete_id:
            if delete_id in self.df['ZAPT'].values:
                self.df = self.df[self.df['ZAPT'] != delete_id]
                self.df.to_csv('official_data/tsem.csv', index=False)
                self.load_csv_data()
                messagebox.showinfo("Success", "Успешно изтрит запис!")
            else:
                messagebox.showerror("Error", "Несъществуващ код!")

    def search_data(self):
        search_term = self.search_entry.get()
        for item in self.tree.get_children():
            if search_term in self.tree.item(item, "values")[0] or search_term in self.tree.item(item, "values")[1]:
                self.tree.selection_add(item)
            else:
                self.tree.selection_remove(item)

    def set_view(self):
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.title_label = tk.Label(self, text="Въвеждане / Актуализация на данни за семинарите (TSEM)",
                                    font=("Arial", 16))
        self.title_label.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W, columnspan=2)

        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.search_button = tk.Button(self, text="Search", command=self.search_data)
        self.search_button.grid(row=1, column=1, padx=10, pady=10)

        self.tree = ttk.Treeview(self, columns=('Код', 'Наименование'), height=20, show='headings')
        self.load_csv_data()
        self.tree.grid(row=2, column=0, padx=20, pady=20, columnspan=2)
        self.tree.column('Код', width=50, anchor='center')
        self.tree.column('Наименование', width=350, anchor='w')

        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=2, column=2, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        self.add_button = tk.Button(self, text="Add New Record", command=self.add_new_record)
        self.add_button.grid(row=1, column=3, padx=10, pady=10, sticky='w')

        self.delete_button = tk.Button(self, text="Delete", command=self.delete_record)
        self.delete_button.grid(row=1, column=4, padx=10, pady=10, sticky='w')

        self.tree.focus_set()
