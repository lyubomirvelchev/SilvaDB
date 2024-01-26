import tkinter as tk
from views.main_view import MainView
from views.nsem_view import NsemView
from views.tsem_view import TsemView


class NavController(tk.Tk):
    def __init__(self, views_dict):
        super().__init__()
        self.frames = {}
        self.views_dict = views_dict
        self.show_frame("MainView")

    def show_frame(self, page_name):
        self.current_frame.destroy() if hasattr(self, "current_frame") else None
        if page_name == "MainView":
            subviews_list = [keys for keys in self.views_dict.keys() if keys != "MainView"]
            self.current_frame = self.views_dict[page_name](self, self, subviews_list)
        else:
            self.current_frame = self.views_dict[page_name](self)
        self.current_frame.set_view()
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame.tkraise()


if __name__ == "__main__":
    VIEWS = {
        "MainView": MainView,
        "Въвеждане / Актуализация на данни за семинарите (TSEM)": TsemView,
        "Въвеждане / Актуализация на типовете записи (NSEM)": NsemView,
    }
    app = NavController(VIEWS)
    app.mainloop()
