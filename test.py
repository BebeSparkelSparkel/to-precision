__author__ = 'William Rusnack github.com/BebeSparkelSparkel linkedin.com/in/williamrusnack williamrusnack@gmail.com'

import unittest
from to_precision import to_precision, auto_notation, std_notation, sci_notation, eng_notation, _place_dot, _number_profile

class TestToPrecision(unittest.TestCase):
  def test_auto(self):
    # Automatic conversion of input type to float
    self.assertEqual(
        to_precision("1.2", 2),
        '1.2'
      )

    # within limit
    self.assertEqual(
        to_precision(-552, 2, notation='auto', delimiter='e'),
        '-550'
      )

    self.assertEqual(
        to_precision(552, 2, notation='auto', delimiter='e'),
        '550'
      )

    # over limit
    self.assertEqual(
        to_precision(1001, 2, notation='auto', delimiter='e'),
        '1.0e3'
      )

    self.assertEqual(
        to_precision(-1001, 2, notation='auto', delimiter='e'),
        '-1.0e3'
      )

    self.assertEqual(
        to_precision(0.0009, 2, notation='auto', delimiter='e'),
        '9.0e-4'
      )

    self.assertEqual(
        to_precision(-0.0009, 2, notation='auto', delimiter='e'),
        '-9.0e-4'
      )

    # Auto limit
    self.assertEqual(
        to_precision(1234, 4, notation='auto', delimiter='e'),
        '1.234e3'
      )
    self.assertEqual(
        to_precision(1234, 4, notation='auto', delimiter='e', auto_limit=4),
        '1234'
      )

    self.assertEqual(
        to_precision(.001, 3, notation='auto', delimiter='e'),
        '1.00e-3'
      )
    self.assertEqual(
        to_precision(.001, 3, notation='auto', delimiter='e', auto_limit=4),
        '0.00100'
      )

    self.assertEqual(
        to_precision(12345, 5, notation='auto', delimiter='e', auto_limit=4),
        '1.2345e4'
      )
    self.assertEqual(
        to_precision(12345, 5, notation='auto', delimiter='e', auto_limit=5),
        '12345'
      )

    self.assertEqual(
        to_precision(.000123, 3, notation='auto', delimiter='e', auto_limit=4),
        '1.23e-4'
      )
    self.assertEqual(
        to_precision(.000123, 3, notation='auto', delimiter='e', auto_limit=5),
        '0.000123'
      )

   # preserve_integer
    self.assertEqual(
      to_precision(12345, 2, notation='auto', preserve_integer=False, auto_limit=5),
      '12000')
    self.assertEqual(
      to_precision(12345, 2, notation='auto', preserve_integer=True, auto_limit=5),
      '12345')

    # Zero stripping
    self.assertEqual(
      to_precision(12000000, 5, notation='auto', strip_zeros=False),
      '1.2000e7')
    self.assertEqual(
      to_precision(12000000, 5, notation='auto', strip_zeros=True),
      '1.2e7')
    self.assertEqual(
      to_precision(12000000, 5, notation='sci', strip_zeros=False),
      '1.2000e7')
    self.assertEqual(
      to_precision(12000000, 5, notation='sci', strip_zeros=True),
      '1.2e7')
    self.assertEqual(
      to_precision(12000000, 5, notation='eng', strip_zeros=False),
      '12.000e6')
    self.assertEqual(
      to_precision(12000000, 5, notation='eng', strip_zeros=True),
      '12e6')
    self.assertEqual(
      to_precision(12, 5, notation='std', strip_zeros=False),
      '12.000')
    self.assertEqual(
      to_precision(12, 5, notation='std', strip_zeros=True),
      '12')

  def test_multi(self):
    self.assertEqual(
        to_precision(500, 2, notation='std', delimiter='e'),
        '500'
      )

    self.assertEqual(
        to_precision(500, 2, notation='sci', delimiter='e'),
        '5.0e2'
      )

    self.assertEqual(
        to_precision(1100, 2, notation='eng', delimiter='e'),
        '1.1e3'
      )

class TestAutoNotation(unittest.TestCase):
  def test_multi(self):
    self.assertEqual(auto_notation(123, 4), '123.0')
    self.assertEqual(auto_notation(1234, 4), '1.234e3')

class TestEngNotation(unittest.TestCase):
  def test_multi(self):
    self.assertEqual(eng_notation(1, 1), '1e0')
    self.assertEqual(eng_notation("1", 1), '1e0') # type conversion
    self.assertEqual(eng_notation(1, 2), '1.0e0')
    self.assertEqual(eng_notation(10, 1), '10e0')

    self.assertEqual(eng_notation(123, 1), '100e0')
    self.assertEqual(eng_notation(123, 2), '120e0')  # round down
    self.assertEqual(eng_notation(-1260, 2), '-1.3e3')  # round up

    self.assertEqual(eng_notation(.123, 1), '100e-3')
    self.assertEqual(eng_notation(-.0123, 2), '-12e-3')
    self.assertEqual(eng_notation(-.0123, 3), '-12.3e-3')
    self.assertEqual(eng_notation(.126, 2), '130e-3')

    self.assertEqual(eng_notation(-123, 4), '-123.0e0')  # round down

    # sig zero
    self.assertEqual(eng_notation(10, 2), '10.e0')

class TestStdNotation(unittest.TestCase):
  def test_multi(self):
    self.assertEqual(std_notation(123, 1), '100')
    self.assertEqual(std_notation("123", 1), '100') # type conversion
    self.assertEqual(std_notation(123, 2), '120')  # round down
    self.assertEqual(std_notation(126, 2), '130')  # round up
    self.assertEqual(std_notation(1260, 2), '1300')  # round up

    self.assertEqual(std_notation(.123, 1), '0.1')
    self.assertEqual(std_notation(.0123, 2), '0.012')
    self.assertEqual(std_notation(.126, 2), '0.13')
    self.assertEqual(std_notation(.126, 4), '0.1260')

    self.assertEqual(std_notation(123, 3), '123')
    self.assertEqual(std_notation(123, 4), '123.0')  # round down

    # sig zero
    self.assertEqual(std_notation(10, 2), '10.')

  def test_values_less_than_1(self):
    # github.com/BebeSparkelSparkel/to-precision/issues/5
    self.assertEqual(std_notation(0.999999, 3), '1.00')
    self.assertEqual(std_notation(-0.999999, 3), '-1.00')

class TestSciNotation(unittest.TestCase):
  def test_multi(self):
    self.assertEqual(sci_notation(1, 1), '1e0')
    self.assertEqual(sci_notation("1", 1), '1e0')  # type conversion
    self.assertEqual(sci_notation(1, 2), '1.0e0')
    self.assertEqual(sci_notation(10, 1), '1e1')

    self.assertEqual(sci_notation(123, 1), '1e2')
    self.assertEqual(sci_notation(123, 2), '1.2e2')  # round down
    self.assertEqual(sci_notation(-126, 2), '-1.3e2')  # round up

    self.assertEqual(sci_notation(.123, 1), '1e-1')
    self.assertEqual(sci_notation(-.0123, 2), '-1.2e-2')
    self.assertEqual(sci_notation(.126, 2), '1.3e-1')

    self.assertEqual(sci_notation(123, 3), '1.23e2')
    self.assertEqual(sci_notation(-123, 4), '-1.230e2')  # round down

  def test_values_less_than_1(self):
    # github.com/BebeSparkelSparkel/to-precision/issues/5
    self.assertEqual(sci_notation(0.999999, 3), '1.00e0')
    self.assertEqual(sci_notation(-0.999999, 3), '-1.00e0')

class TestPlaceDot(unittest.TestCase):
  def test_all(self):
    self.assertEqual(_place_dot('123', 0, False), '123')
    self.assertEqual(_place_dot('120', 0, False), '120.')
    self.assertEqual(_place_dot('0', 0, False), '0')

    self.assertEqual(_place_dot('123', 2, False), '12300')

    self.assertEqual(_place_dot('123', -2, False), '1.23')
    self.assertEqual(_place_dot('123', -3, False), '0.123')
    self.assertEqual(_place_dot('123', -5, False), '0.00123')

    # Zero stripping
    self.assertEqual(_place_dot('123' ,  2, True),  '12300')
    self.assertEqual(_place_dot('100' , -1, True),  '10')
    self.assertEqual(_place_dot('1200', -2, False), '12.00')
    self.assertEqual(_place_dot('1200', -2, True),  '12')
    self.assertEqual(_place_dot('1200', -1, False), '120.0')
    self.assertEqual(_place_dot('1200', -1, True),  '120')

class TestNumberProfile(unittest.TestCase):
  def test_positive(self):
    self.assertEqual(
        _number_profile(123, 2),
        ('12', 1, False)
      )

    self.assertEqual(
        _number_profile(123, 3),
        ('123', 0, False)
      )

  def test_negative(self):
    self.assertEqual(
        _number_profile(-123, 3),
        ('123', 0, True)
      )

    self.assertEqual(
        _number_profile(-123, 1),
        ('1', 2, True)
      )

    self.assertEqual(
        _number_profile(-12.3, 2),
        ('12', 0, True)
      )

    self.assertEqual(
        _number_profile(-12.3, 3),
        ('123', -1, True)
      )

    self.assertEqual(
        _number_profile(-.123, 3),
        ('123', -3, True)
      )

    self.assertEqual(
        _number_profile(-.123, 2),
        ('12', -2, True)
      )

  def test_zeros(self):
    self.assertEqual(
        _number_profile(0, 1),
        ('0', 0, False)
      )

    self.assertEqual(
        _number_profile(0, 3),
        ('000', -2, False)
      )

  def test_round_up(self):
    self.assertEqual(
        _number_profile(-.126, 2),
        ('13', -2, True)
      )


if __name__ == '__main__':
  unittest.main()
