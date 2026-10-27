"""Dependency, address and carry-boundary checks for the logical example."""
import importlib.util
from itertools import permutations
from math import comb
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('address_model',
    Path(__file__).resolve().parents[1]/'examples/pccpu_address_model.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class AddressModelTests(unittest.TestCase):
    def test_controller_and_workers_have_distinct_addresses(self):
        addresses=[m.cell_address(r,c) for r in range(2) for c in range(3)]
        self.assertEqual(addresses,list(range(1000,1006)))
        self.assertEqual(m.AddressModel().memory[m.cell_address(1,1)]['kind'],'controller')
        with self.assertRaises(ValueError):m.cell_address(0,3)
        with self.assertRaises(ValueError):m.cell_address(-1,0)

    def test_consumer_waits_for_both_producers(self):
        model=m.AddressModel()
        with self.assertRaises(ValueError):model.read_value(1003)
        events=model.step((1002,1001,1000))
        self.assertEqual({e['worker'] for e in events},{'A','B'})
        self.assertEqual(model.memory[1002]['state'],'waiting')
        with self.assertRaises(ValueError):model.read_value(1003)
        model.step()
        self.assertEqual(model.read_value(1003),210)
        self.assertEqual(model.memory[1003]['mathematical_address'],(10,4))

    def test_all_worker_orders_preserve_results(self):
        for order in permutations((1000,1001,1002)):
            model=m.AddressModel(12,5)
            model.step(order);model.step(order)
            self.assertEqual(model.read_value(1003),comb(13,6))
            self.assertEqual(model.memory[1004]['event_counter'],3)
            self.assertEqual(model.memory[1004]['logical_round'],2)

    def test_completion_does_not_dispatch_twice(self):
        model=m.AddressModel();self.assertEqual(model.run(),210)
        prior=list(model.events)
        self.assertEqual(model.step(),[])
        self.assertEqual(model.run(),210)
        self.assertEqual(model.events,prior)

    def test_small_pascal_grid_against_independent_addition(self):
        row=[1,1]
        for n in range(1,30):
            next_row=[1]+[a+b for a,b in zip(row,row[1:])]+[1]
            for k in range(n):
                self.assertEqual(m.AddressModel(n,k).run(),next_row[k+1])
            row=next_row

    def test_row_product_keeps_value_but_may_require_carry(self):
        self.assertTrue(m.row_product(10,2,2)['carry_free'])
        self.assertFalse(m.row_product(10,3,2)['carry_free'])
        self.assertEqual(121*121,11**4)
        self.assertEqual(1331*121,11**5)
        self.assertFalse(m.row_product(3,1,2)['carry_free'])
        self.assertTrue(m.row_product(127,4,5)['carry_free'])
        self.assertFalse(m.row_product(127,5,5)['carry_free'])

    def test_invalid_requests_fail_before_execution(self):
        for n,k in [(0,0),(2,2),(3,-1),(True,0)]:
            with self.assertRaises(ValueError):m.AddressModel(n,k)
        model=m.AddressModel()
        with self.assertRaises(ValueError):model.step((1000,1000,1002))
        self.assertEqual(model.events,[])
        self.assertEqual(model.memory[1004]['logical_round'],0)

if __name__=='__main__':unittest.main()
