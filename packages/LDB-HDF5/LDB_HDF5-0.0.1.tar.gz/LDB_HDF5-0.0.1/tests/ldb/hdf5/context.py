from __future__ import absolute_import

import unittest

from ldb.hdf5.context import CountingContextManager

class TestClass(CountingContextManager):
    def __init__(self, enter_returns, intercept_exception):
        super(TestClass, self).__init__()
        self.enter_returns = enter_returns
        self.intercept_exception = intercept_exception
        self.entered = False
        self.exited = False

    def _initial_context_enter(self):
        self.entered = True

        if self.enter_returns is not None:
            return self.enter_returns

    def _final_context_exit(self, exc_type, exc_value, traceback):
        self.exited = True
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.traceback = traceback
        return self.intercept_exception


class CountingContextManagerTestCase(unittest.TestCase):
    def testEnterExit(self):
        test_inst = TestClass(None, False)
        self.assertFalse(test_inst.entered)
        self.assertFalse(test_inst.exited)
        with test_inst as test_inst_b:
            self.assertEqual(test_inst, test_inst_b)
            self.assertTrue(test_inst.entered)
            self.assertFalse(test_inst.exited)
            with test_inst_b:
                self.assertFalse(test_inst.exited)
            self.assertFalse(test_inst.exited)
        self.assertTrue(test_inst.exited)

    def testEnterReturn(self):
        test_inst = TestClass(1, False)
        with test_inst as test_inst_b:
            self.assertEqual(test_inst_b, 1)

    def testException(self):
        test_inst = TestClass(None, False)
        with self.assertRaises(Exception):
            with test_inst:
                raise Exception("Asdf")
        self.assertEqual(test_inst.exc_type, Exception)
        self.assertEqual(test_inst.exc_value.args[0], "Asdf")
        self.assertNotEqual(test_inst.traceback, None)

        test_inst_2 = TestClass(None, True)
        with test_inst_2:
            raise Exception

    def testBareContextManager(self):
        test_inst = CountingContextManager()

        with test_inst:
            pass
