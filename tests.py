import unittest
from unittest import mock
from unittest.mock import patch
import datetime

from peewee import *
from worklog_db import *
from menus.screen import Screen
from menus.add_menu import Add_Menu
from menus.main_menu import Main_Menu
from menus.search_menu import Search_Menu
from models.time_entry import Time_Entry
from models.employee import Employee
from models.time_entriesdb import *

initialize()


class MenuTests(unittest.TestCase):

    def test_main_menu(self):
        main_menu = Main_Menu()
        correct_title = "Work Log Program - Main Menu"
        correct_options = ["Add New Entry", "Search Existing", "Quit Program"]
        self.assertEqual(correct_title, main_menu.title)
        self.assertEqual(correct_options, main_menu.options)

    def test_search_menu(self):
        search_menu = Search_Menu()
        correct_title = "Work Log Program - Search Menu"
        correct_options = ["a) Browse by Employee Name",
                           "b) Search by Employee Name",
                           "c) Exact Date",
                           "d) Date Range",
                           "e) Time Spent",
                           "f) Keyword Search",
                           "g) Return to Main Menu"]
        self.assertEqual(correct_title, search_menu.title)
        self.assertEqual(correct_options, search_menu.options)

    def test_add_menu(self):
        add_menu = Add_Menu()
        correct_title = "Work Log Program - Add Time Entry"
        self.assertEqual(add_menu.title, correct_title)

    def test_run_main_menu_process(self):
        with patch('builtins.input', side_effect=["1"]):
            expected_choice = "1"
            result = run_main_menu_process()
            self.assertEqual(expected_choice, result)

    def test_search_show(self):
        expected_result = 0
        search_menu = Search_Menu()
        result = search_menu.show()
        self.assertEqual(expected_result, result)

    def test_screen_class(self):
        screen = Screen()
        correct_title = "Work Log Program - {Title}"
        result = screen.title
        self.assertEqual(correct_title, result)


class HelperFunctionTests(unittest.TestCase):

    def test_get_employee(self):
        with patch('builtins.input', side_effect=["Test Employee"]):
            Employee.create(name="Test Employee")
            expected_name = "Test Employee"
            result = get_employee()
            self.assertEqual(expected_name, result.name)

    def test_get_date(self):
        with patch('builtins.input', side_effect=["21/07/2018"]):
            date = "21/07/2018"
            expected_date = datetime.datetime.strptime(date, '%d/%m/%Y')
            result = get_date()
            self.assertEqual(expected_date, result)

    def test_validate_date(self):
        with patch('builtins.input', side_effect=["21/07/2018"]):
            valid_date = "21/07/2018"
            invalid_date = "Bob"
            date = validate_date(invalid_date)
            self.assertEqual(valid_date, date)

    def test_get_title(self):
        with patch('builtins.input', side_effect=["Title"]):
            expected_title = "Title"
            result = get_title()
            self.assertEqual(expected_title, result)

    def test_get_time_spent(self):
        with patch('builtins.input', side_effect=["30"]):
            expected_time_spent = "30"
            result = get_time_spent()
            self.assertEqual(expected_time_spent, result)

    def test_validate_time_spent(self):
        with patch('builtins.input', side_effect=["Bob", "30"]):
            expected_time_spent = "30"
            result = get_time_spent()
            self.assertEqual(expected_time_spent, result)

    def test_get_notes(self):
        with patch('builtins.input', side_effect=["Test Notes", "", "Notes"]):
            expected_notes1 = "Test Notes"
            expected_notes2 = "Notes"
            result1 = get_notes()
            result2 = get_notes()
            self.assertEqual(expected_notes1, result1)
            self.assertEqual(expected_notes2, result2)

    def test_validate_employee_name(self):
        with patch('builtins.input', side_effect=["Test Employee"]):
            expected_name = "Test Employee"
            fake_list = []
            result = validate_employee_name("Not In Database", fake_list)
            self.assertEqual(expected_name, result)
            test = Employee.get(Employee.name == result)
            test.delete_instance()

    def test_remaining_entries(self):
        employee_name = "Brian Peterson"
        query = (Time_Entry.select()
                            .join(Employee)
                            .where(Employee.name == employee_name))
        expected_result = len(query)
        result = remaining_entries(employee_name)
        self.assertEqual(expected_result, result)

    def test_get_date_range(self):
        with patch('builtins.input', side_effect=["01/01/2017", "01/01/2018"]):
            start = "01/01/2017"
            end = "01/01/2018"
            expected_start = datetime.datetime.strptime(start, '%d/%m/%Y')
            expected_end = datetime.datetime.strptime(end, '%d/%m/%Y')
            result1, result2 = get_date_range()
            self.assertEqual(expected_start, result1)
            self.assertEqual(expected_end, result2)

    def test_validate_date_eds(self):
        with patch('builtins.input', side_effect=["21/07/2018"]):
            expected_date = "21/07/2018"
            invalid_date = "2018/07/21"
            fake_list_of_entries = []
            result = validate_date_eds(invalid_date, fake_list_of_entries)
            self.assertEqual(expected_date, result)


if __name__ == '__main__':
    unittest.main()
