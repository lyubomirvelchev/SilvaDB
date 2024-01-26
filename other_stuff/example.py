import tkinter as tk


# Model
class Model:
    @staticmethod
    def square(num):
        return num ** 2


# View
class View:
    def __init__(self, master):
        self.entry = tk.Entry(master)
        self.entry.pack(pady=20)

        self.button = tk.Button(master, text="Square", command=self.on_button_click)
        self.button.pack()

        self.label = tk.Label(master, text="")
        self.label.pack(pady=20)

    def on_button_click(self):
        # Delegating the event handling to the controller
        self.controller.handle_click()


# Controller
class Controller:
    def __init__(self, root):
        self.view = View(root)
        # Setting up a reference to the controller in the view
        self.view.controller = self

    def handle_click(self):
        # Retrieving the number from the view
        number = float(self.view.entry.get())

        # Using the model to square the number
        squared_value = Model.square(number)

        # Updating the view with the result
        self.view.label.config(text=squared_value)


root = tk.Tk()
app = Controller(root)
root.mainloop()
