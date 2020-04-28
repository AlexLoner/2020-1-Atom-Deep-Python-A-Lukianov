import unittest
from orm_base import MyBase
from tables import Tables
from entities import Customer


class Test(unittest.TestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test_create_get(self):
        base = Tables(MyBase('data_1'))
        my_customer =  Customer(name="Alex", fullname="Loner", email="some@gmail.com", birthday="1995-11-21")
        base.create(my_customer)
        self.assertEqual('<Customer :: 1_Alex_Loner_some@gmail.com_1995-11-21)>', str(base.get(1)))

    # ------------------------------------------------------------------------------------------------------------------
    def test_all(self):
        base = Tables(MyBase('data_2'))
        for _ in range(5):
            base.create(Customer())
        self.assertEqual(5, len(base.all()))

    # ------------------------------------------------------------------------------------------------------------------
    def test_update(self):
        base = Tables(MyBase('data_3'))
        for _ in range(5):
            base.create(Customer(name="Tom"))
        check = str(base.get(2))
        base.update((Customer.id == 2,), Customer.name, "Alex")
        self.assertEqual(check.replace("Tom", "Alex"), str(base.get(2)))

    # ------------------------------------------------------------------------------------------------------------------
    def test_delete(self):
        base = Tables(MyBase('data_4'))
        for _ in range(5):
            base.create(Customer())
        base.delete((Customer.id == 1,))
        self.assertEqual(4, len(base.all()))
