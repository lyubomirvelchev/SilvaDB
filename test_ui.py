import unittest
import tkinter as tk
from silva_front_end import MyApp, Router


def method1():
    print("Method 1 called")


def method2():
    print("Method 2 called")


def method3():
    print("Method 3 called")


def method4():
    print("Method 4 called")


routing_map = {
    "Въвеждане / Актуализация на данни за семинарите (TSEM)": method1,
    "Въвеждане / Актуализация на типовете записи (NSEM)": method2,
    "Въвеждане / Актуализация на карти за записване": method3,
    "Справка за участниците в семинар": method4,
}


class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.app = MyApp()

    def tearDown(self):
        self.app.destroy()

    def test_when_app_created_then_title_is_correct(self):
        expected_title = "Silva DataBase"

        self.assertEqual(expected_title, self.app.title())


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.routing_map = routing_map
        self.rows = list(self.routing_map.keys())

    def tearDown(self):
        self.root.destroy()

    def test_init_when_router_created_then_width_equals_expected_value(self):
        expected_width = 100

        listbox_object = Router(self.root, self.routing_map)

        self.assertEqual(expected_width, listbox_object.listbox.cget("width"))

    def test_populate_listbox_when_called_then_rows_match_the_keys_in_router_map(self):
        expected_rows = self.rows
        listbox_object = Router(self.root, self.routing_map)

        listbox_object.populate_listbox()

        current_rows = list(listbox_object.listbox.get(0, tk.END))
        self.assertEqual(expected_rows, current_rows)

    def test_populate_listbox_when_called_then_height_equals_row_count(self):
        expected_height = len(self.rows)
        listbox_object = Router(self.root, self.routing_map)

        listbox_object.populate_listbox()

        self.assertEqual(expected_height, listbox_object.listbox.cget("height"))

    def test_display_listbox_when_called_then_grid_settings_are_as_expected(self):
        expected_row_padding = 10
        expected_column_padding = 10
        listbox_object = Router(self.root, self.routing_map)

        listbox_object.display_listbox()

        self.assertEqual(listbox_object.listbox, self.root.grid_slaves(row=0, column=0)[0])
        self.assertEqual(expected_row_padding, listbox_object.listbox.grid_info()['padx'])
        self.assertEqual(expected_column_padding, listbox_object.listbox.grid_info()['pady'])

    def test_set_initial_selection_when_called_then_first_item_selected(self):
        expected_selection = 0
        listbox_object = Router(self.root, self.routing_map)

        listbox_object.populate_listbox()  # there must be items in the listbox before selection can be set
        listbox_object.set_initial_selection()

        current_selection = listbox_object.listbox.curselection()[0]
        self.assertEqual(expected_selection, current_selection)

    def test_on_up_when_selection_is_at_first_index_then_selection_is_changed_to_last_index(self):
        expected_selection = len(self.rows) - 1
        listbox_object = Router(self.root, self.routing_map)
        listbox_object.bind_keys()
        listbox_object.populate_listbox()
        listbox_object.listbox.selection_set(0)

        listbox_object.on_up(None)

        current_selection = listbox_object.listbox.curselection()[0]
        self.assertEqual(expected_selection, current_selection)

    def test_on_up_when_selection_is_not_at_first_index_then_selection_is_changed_to_previous_index(self):
        expected_selection = 0
        listbox_object = Router(self.root, self.routing_map)
        listbox_object.bind_keys()
        listbox_object.populate_listbox()
        listbox_object.listbox.selection_set(1)

        listbox_object.on_up(None)

        current_selection = listbox_object.listbox.curselection()[0]
        self.assertEqual(expected_selection, current_selection)

    def test_on_down_when_selection_is_at_last_index_then_selection_is_changed_to_first_index(self):
        expected_selection = 0
        listbox_object = Router(self.root, self.routing_map)
        listbox_object.bind_keys()
        listbox_object.populate_listbox()
        listbox_object.listbox.selection_set(len(self.rows) - 1)

        listbox_object.on_down(None)

        current_selection = listbox_object.listbox.curselection()[0]
        self.assertEqual(expected_selection, current_selection)

    def test_on_down_when_selection_is_not_at_last_index_then_selection_is_changed_to_next_index(self):
        expected_selection = 1
        listbox_object = Router(self.root, self.routing_map)
        listbox_object.bind_keys()
        listbox_object.populate_listbox()
        listbox_object.listbox.selection_set(0)

        listbox_object.on_down(None)

        current_selection = listbox_object.listbox.curselection()[0]
        self.assertEqual(expected_selection, current_selection)

    def test_on_enter_when_called_then_returns_current_listbox_field(self):
        expected_list_box_field = "Въвеждане / Актуализация на данни за семинарите (TSEM)"
        listbox_object = Router(self.root, self.routing_map)
        listbox_object.bind_keys()
        listbox_object.populate_listbox()
        listbox_object.listbox.selection_set(0)

        current_list_box_field = listbox_object.on_enter(None)

        self.assertEqual(expected_list_box_field, current_list_box_field)

if __name__ == "__main__":
    unittest.main()
