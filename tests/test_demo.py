import unittest


def xxx(self):
    print("xxx")

suite = unittest.TestSuite()


suite.addTest(xxx)

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)