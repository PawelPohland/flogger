import unittest
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parents[0])

loader = unittest.TestLoader()
tests = loader.discover('.')
test_runner = unittest.runner.TextTestRunner()

if __name__ == "__main__":
    test_runner.run(tests)
