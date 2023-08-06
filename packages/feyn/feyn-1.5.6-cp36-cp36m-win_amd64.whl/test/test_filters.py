import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

import feyn
import _feyn

class TestFilters(unittest.TestCase):

    def test_excludefunction(self):
        with self.subTest("Can use function name"):
            f = feyn.filters.ExcludeFunctions("gaussian")

            excluded = set(_feyn.get_specs()).difference(f.specs)
            self.assertTrue(excluded)
            for spec in excluded:
                self.assertTrue(spec.startswith("cell:gaussian"))


        with self.subTest("Can use function name list"):
            f = feyn.filters.ExcludeFunctions(["gaussian", "multiply"])

            excluded = set(_feyn.get_specs()).difference(f.specs)

            self.assertTrue(excluded)
            for spec in excluded:
                self.assertTrue(spec.startswith("cell:gaussian") or spec.startswith("cell:multiply") )


    def test_functions(self):
        with self.subTest("Can use function name"):
            f = feyn.filters.Functions("add")

            for spec in f.specs:
                self.assertTrue(spec.startswith("cell:add") or spec.startswith("in:") or spec.startswith("out:"))



        with self.subTest("Can use function name list"):
            f = feyn.filters.Functions(["add","multiply"])

            for spec in f.specs:
                self.assertTrue(spec.startswith("cell:add") or spec.startswith("cell:multiply") or spec.startswith("in:") or spec.startswith("out:"))

