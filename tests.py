import os
import unittest

from unittest.mock import patch

from classes.report import PdfReport
from classes.bill import Bill
from classes.flatmate import Flatmate
from utils.utils import input_handler


class TestInputHandler(unittest.TestCase):

    @patch('builtins.input', side_effect=["10"])
    def test_input_str(self, mock_input):
        return_val = input_handler(text="Text")
        self.assertEqual(return_val, "10")

    @patch('builtins.input', side_effect=["10"])
    def test_input_int(self, mock_input):
        return_val = input_handler(text="Text", return_type=int)
        self.assertEqual(return_val, 10)

    @patch('builtins.input', side_effect=["10"])
    def test_input_float(self, mock_input):
        return_val = input_handler(text="Text", return_type=float)
        self.assertEqual(return_val, 10.0)


class TestFlatmate(unittest.TestCase):

    def test_set_cost_for_flat(self):
        flatmate = Flatmate(name="Adam", days_in_house=10)
        flatmate.cost_for_flat = 120
        self.assertEqual(flatmate.cost_for_flat, 120)


class TestBill(unittest.TestCase):

    def test_split_by_two_flatmates(self):
        adam = Flatmate(name="Adam", days_in_house=30)
        eva = Flatmate(name="Eva", days_in_house=30)
        the_bill = Bill(amount=120, period="March 2020")
        bills = the_bill.split_by_flatmates(*(adam, eva))
        self.assertEqual(bills[adam.name], 60.0)
        self.assertEqual(bills[eva.name], 60.0)

    def test_split_by_three_flatmates(self):
        adam = Flatmate(name="Adam", days_in_house=30)
        eva = Flatmate(name="Eva", days_in_house=20)
        snake = Flatmate(name="Snake", days_in_house=10)
        the_bill = Bill(amount=120, period="March 2020")
        bills = the_bill.split_by_flatmates(*(adam, eva, snake))
        self.assertEqual(bills[adam.name], 60.0)
        self.assertEqual(bills[eva.name], 40.0)
        self.assertEqual(bills[snake.name], 20.0)


class TestPdfReporter(unittest.TestCase):

    def test_generate_and_check_exist(self):
        adam = Flatmate(name="Adam", days_in_house=30)
        eva = Flatmate(name="Eva", days_in_house=20)
        snake = Flatmate(name="Snake", days_in_house=10)
        flatmates = (adam, eva, snake)
        the_bill = Bill(amount=120, period="March 2020")
        bills = the_bill.split_by_flatmates(*flatmates)
        for name, bill in bills.items():
            for mate in flatmates:
                if mate.name == name:
                    mate.cost_for_flat = bill
                    print(f"{mate.name} pays {mate.cost_for_flat}")

        filename = f"{the_bill.period}.pdf"
        report = PdfReport(filename=filename)
        report.generate(bill=the_bill, flatmates=flatmates)
        self.assertTrue(os.path.isfile(filename))


if __name__ == "__main__":
    unittest.main()
