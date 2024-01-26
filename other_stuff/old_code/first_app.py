import tkinter as tk
from tkinter import ttk


def greet(event=None):
    name = name_entry.get()
    if name:
        greeting_label.config(text=f"Hello, {name}!")
    else:
        greeting_label.config(text="Hello!")


def close_on_esc(event):
    app.destroy()




app = tk.Tk()
app.title("Simple Tkinter App")
app.bind('<Escape>', close_on_esc)
app.bind('<Return>', greet)
name_entry = ttk.Entry(app, width=15)
name_entry.pack(pady=20)

greet_button = ttk.Button(app, text="Greet", command=greet)
greet_button.pack(pady=20)

greeting_label = ttk.Label(app, text="")
greeting_label.pack(pady=20)

app.mainloop()
