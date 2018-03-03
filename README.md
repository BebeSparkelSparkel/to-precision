# to_precision
Formatting floating point numbers to standard, scientific, or engineering notation with a specified number of significant digits.

[![Build Status](https://travis-ci.org/BebeSparkelSparkel/to-precision.svg?branch=master)](https://travis-ci.org/BebeSparkelSparkel/to-precision)

Created by:  
**William Rusnack**
[GitHub](github.com/BebeSparkelSparkel)
[LinkedIn](linkedin.com/in/williamrusnack/)
[Email](williamrusnack@gmail.com)  
**Eric Moyer**
[GitHub](github.com/epmoyer)
[Email](eric@lemoncrab.com)  
**Randle Taylor**
[GitHub](github.com/randlet)

## Use Latest Release
https://github.com/BebeSparkelSparkel/to-precision/releases/tag/0.0.0

## Install

    pip install git+"link to latest release"

### standard notation
to_precision.**std_notation**(value, precision)

standard notation (US version). http://www.mathsisfun.com/definitions/standard-notation.html

returns a string of value with the proper precision

ex:

    >>> std_notation(5, 2)
    '5.0'
    >>> std_notation(5.36, 2)
    '5.4'
    >>> std_notation(5360, 2)
    '5400'
    >>> std_notation(0.05363, 3)
    '0.0536'

### scientific notation
to_precision.**sci_notation**(value, precision, delimiter='e'):

scientific notation. https://www.mathsisfun.com/numbers/scientific-notation.html

returns a string of value with the proper precision and 10s exponent
delimiter is placed between the decimal value and 10s exponent

ex:

    >>> sci_notation(123, 1, 'E')
    '1E2'
    >>> sci_notation(123, 3, 'E')
    '1.23E2'
    >>> sci_notation(.126, 2, 'E')
    '1.3E-1'

### engineering notation
to_precision.**eng_notation**(value, precision, delimiter='e')

engineering notation. http://www.mathsisfun.com/definitions/engineering-notation.html

returns a string of value with the proper precision and 10s exponent that is divisible by 3
delimiter is placed between the decimal value and 10s exponent

ex:

    >>> eng_notation(123, 1, 'E')
    '100E0'
    >>> eng_notation(1230, 3, 'E')
    '1.23E3'
    >>> eng_notation(.126, 2, 'E')
    '120E-3'

### auto notation
to_precision.**auto_notation**(value, precision, delimiter='e')

Automatically selects between standard notation (US version) and scientific notation.
Values in the range 0.001 < abs(value) < 1000 return standard notation.

http://www.mathsisfun.com/definitions/standard-notation.html
https://www.mathsisfun.com/numbers/scientific-notation.html

returns a string of value with the proper precision

ex:

    >>> auto_notation(123, 4)
    '123.4'
    >>> std_notation(1234, 4)
    '1.234e3'

### to_precision
to_precision.**to_precision**(value, precision, notation='auto', delimiter='e', auto_limit=3, strip_zeros=False, preserve=False)  

Converts a value to the specified notation and precision
value - any type that can be converted to a float
precision - integer that is greater than zero
notation - string

* value
    * The number to convert
* precision
    * The digits of precision
* notation
    * 'auto' - selects standard notation when abs(power) < auto_limit else returns scientific notation.
    * 'sci' or 'scientific' - returns scientific notation. https://www.mathsisfun.com/numbers/scientific-notation.html
    * 'eng' or 'engineering' - returns engineering notation. http://www.mathsisfun.com/definitions/engineering-notation.html
    * 'std' or 'standard' - returns standard notation. http://www.mathsisfun.com/definitions/standard-notation.html
* delimiter
    * Text that is placed between the decimal value and 10s exponent
* auto_limit
    * Integer. When abs(power) exceeds this limit, 'auto'
    mode will return scientific notation. The default (3) will cause 'auto' mode to return scientific notation for 0.001 < abs(value) < 1000
* strip_zeros
    * If true, trailing decimal zeros will be removed.
* preserve_integer
    * If true, 'std' will preserve all digits when returning
    values that have no decimal component.

## Implicit vs. Explicit precision

Consider the following data set:

    A                 B              C              D              
    ----------------  -------------  -------------  -------------  
    1.00000000000     0.98765432100  0.08700000000  0.00000000234  
    1.20000000000     1.40000000000  1.00000000000  0.00000000002  
    1234.00000000000  1.23450000000  0.02345678000  0.00000000000 

In a scientific or engineering context, one typically indicates precision *explicitly* by showing all significant digits.  This can be accomplished using `to_pecision()` with its default arguments.

Using `to_precision(x, 3)` to render the example data set yields:

    A       B      C       D         
    ------  -----  ------  --------  
    1.00    0.988  0.0870  2.34e-9   
    1.20    1.40   1.00    2.00e-11  
    1.23e3  1.23   0.0235  0.00

In a business or informal context one may wish to *implicitly* specify precision, and render results in their simplest, least cluttered form given that precision.  This can be accomplished by invoking the `strip_zeros` and `preserve_integer` arguments.  Additionally, `auto_limit` can be used to control the threshold at which scientific notation is adopted.

Using `to_precision(x, 3, auto_limit=4, strip_zeros=True, preserve_integer=True)` to render the example data set yields:

    A     B      C       D        
    ----  -----  ------  -------  
    1     0.988  0.087   2.34e-9  
    1.2   1.4    1       2e-11    
    1234  1.23   0.0235  0 

## Decimal Notation

to-precision uses decimal notation to indicate precision in cases where the result:

* Is an integer
* Ends with one or more zeros
* All ending zeros are significant

See: https://en.wikipedia.org/wiki/Significant_figures#Significant_figures_rules_explained

For examlple:

    >>> to_precision(120, 2)
    '120'                      # Zero is not significant
    >>> to_precision(120, 3)
    '120.'                     # Zero is significant
    >>> to_precision(100, 2)
    '100'                      # First zero is significant but second is not
    >>>


## Demonstration

The script `demonstration.py` demonstrates the behavior of the various options...

    $./demonstration.py 
    Default (Auto Notation):
        to_precision(value, precision)

        value         precision=1    precision=2    precision=3    precision=4    precision=5
        ------------  -------------  -------------  -------------  -------------  -------------
        0             0              0.0            0.00           0.000          0.0000
        1             1              1.0            1.00           1.000          1.0000
        10            10             10.            10.0           10.00          10.000                                           
        ...
        (many cases)
        ...
        0.000123456  0.0001         0.00012        0.000123       0.0001235      0.00012346
        0.001234567  0.001          0.0012         0.00123        0.001235       0.0012346
        0.012345678  0.01           0.012          0.0123         0.01235        0.012346
        0.123456789  0.1            0.12           0.123          0.1235         0.12346
                  
                                                                                                                                  
