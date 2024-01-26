import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pandas as pd


class NsemView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.df = pd.read_csv('official_data/nsem.csv')

    def go_back(self):
        self.parent.show_frame("MainView")

    def set_view(self):
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.title_label = tk.Label(self, text="Въвеждане / Актуализация на типовете записи (NSEM)", font=("Arial", 16))
        self.title_label.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W, columnspan=2)

        self.left_tree = ttk.Treeview(self, columns=('id', 'name'), show='headings', height=20)
        self.left_tree.heading('id', text=self.df.columns[1])
        self.left_tree.heading('name', text=self.df.columns[2])
        for index, row in self.df.iterrows():
            self.left_tree.insert("", "end", values=(row.iloc[1], row.iloc[2]))
        self.left_tree.grid(row=1, column=0, sticky=tk.W)

        self.right_frame = tk.Frame(self, bg="white", width=300, height=400)
        self.right_frame.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W + tk.E)
        self.right_frame.grid_propagate(0)  # prevents resizing of frame due to widgets
        self.left_tree.selection_set(self.left_tree.get_children()[0])
        self.left_tree.focus_set()
        self.left_tree.focus(self.left_tree.get_children()[0])
        self.left_tree.bind("<Return>", self.display_data_on_right)
        #
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.left_tree.yview)
        self.tree_scroll.grid(row=1, column=1, sticky='ns')
        self.left_tree.configure(yscrollcommand=self.tree_scroll.set)

        self.register_button = tk.Button(self, text="Register", command=self.register_new_row)
        self.register_button.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.search_button = tk.Button(self, text="Search", command=self.open_search_window)
        self.search_button.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        self.delete_button = tk.Button(self, text="Delete", command=self.open_delete_window)
        self.delete_button.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

    def display_data_on_right(self, event):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        selected_item = self.left_tree.selection()
        item_values = self.left_tree.item(selected_item, "values")
        if not item_values:
            return

        # Get the unique id from the left treeview
        unique_id = item_values[0]

        # Get the row data from the dataframe
        row_data = self.df.loc[self.df[self.df.columns[1]] == unique_id].values[0]
        self.right_frame = tk.Frame(self, bg="white", width=300, height=400)
        self.right_frame.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W + tk.E)
        self.right_frame.grid_propagate(0)
        # Display the data on the right frame
        for col_index, col_name in enumerate(self.df.columns[3:], start=3):
            label = tk.Label(self.right_frame, text=f"{col_name}: {row_data[col_index]}", bg="white", wraplength=280)
            label.pack(pady=10)

    def register_new_row(self):
        def submit_data():
            new_data = [entry.get() for entry in entries]
            new_series = pd.Series(new_data, index=self.df.columns)
            if new_series.iloc[1] in self.df[self.df.columns[1]].values:
                messagebox.showerror("Error", "Този код вече съществува!\nНе са направени промени!")
                return
            self.df.loc[len(self.df.index)] = new_series
            self.df.to_csv('official_data/nsem.csv', index=False)
            reg_window.destroy()
            self.left_tree.insert("", "end", values=(new_series.iloc[1], new_series.iloc[2]))
            messagebox.showinfo("Success", "Успешно добавен запис!")

        reg_window = tk.Toplevel(self)
        reg_window.title("Register New Row")
        entries = []
        for idx, col in enumerate(self.df.columns):
            label = tk.Label(reg_window, text=col)
            label.grid(row=idx, column=0)
            entry = tk.Entry(reg_window)
            entry.grid(row=idx, column=1)
            entries.append(entry)
        submit_button = tk.Button(reg_window, text="Submit", command=submit_data)
        submit_button.grid(row=len(self.df.columns), column=0, columnspan=2)

    def open_search_window(self):
        search_window = tk.Toplevel(self)
        search_window.title("Search by ID")
        tk.Label(search_window, text="Enter ID:").pack(padx=10, pady=5)
        id_entry = tk.Entry(search_window)
        id_entry.pack(padx=10, pady=5)
        tk.Button(search_window, text="Search", command=lambda: self.search_by_id(id_entry.get(), search_window)).pack(
            pady=10)

    def open_delete_window(self):
        delete_id = simpledialog.askstring("Delete Record", "Enter ID to delete:")
        if delete_id:
            index_to_delete = self.df[self.df[self.df.columns[1]] == delete_id].index
            if not index_to_delete.empty:
                self.df.drop(index_to_delete, inplace=True)
                self.df.to_csv('official_data/nsem.csv', index=False)
                messagebox.showinfo("Success", "Успешно изтрит запис!")
                for row in self.left_tree.get_children():
                    self.left_tree.delete(row)
                for index, row in self.df.iterrows():
                    self.left_tree.insert("", "end", values=(row.iloc[1], row.iloc[2]))
            else:
                messagebox.showerror("Error", "Несъществуващ код!")

    def search_by_id(self, unique_id, search_window):
        if not unique_id:
            return

        row_data = self.df.loc[self.df[self.df.columns[1]] == unique_id]
        if row_data.empty:
            tk.Label(search_window, text="No matching data found!").pack(pady=5)
        else:
            # Displaying the data using the display_data_on_right function
            selected_item = self.left_tree.selection()
            self.left_tree.item(selected_item,
                                values=(row_data[self.df.columns[1]].values[0], row_data[self.df.columns[2]].values[0]))
            self.display_data_on_right(None)

    def delete_by_id(self, unique_id, delete_window):
        if not unique_id:
            return

        index_to_delete = self.df[self.df[self.df.columns[1]] == unique_id].index
        if not index_to_delete.empty:
            self.df.drop(index_to_delete, inplace=True)
            self.df.to_csv('official_data/nsem.csv', index=False)
            tk.Label(delete_window, text="Record deleted!").pack(pady=5)
            # Refresh the treeview to reflect the deletion
            for row in self.left_tree.get_children():
                self.left_tree.delete(row)
            for index, row in self.df.iterrows():
                self.left_tree.insert("", "end", values=(row.iloc[1], row.iloc[2]))
        else:
            tk.Label(delete_window, text="No matching data found!").pack(pady=5)
