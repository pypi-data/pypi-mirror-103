Left-pad for Python
===================

Installation:

    pip install smarty-left-pad

Usage

```
    from smarty_left_pad.left_pad import left_pad

    >>>left_pad('input', 10, '-')
    -----input
```

This package uses doctest for testing, run :code:`doctest left_pad.py` to run the tests.

Example of run log:

```python
(personal386) $ pwd
/smarty-left-pad/pad_on_left
(personal386) $ python -m doctest left_pad.py -v
Trying:
    left_pad('foo', 5)
Expecting:
    '  foo'
ok
Trying:
    left_pad('foobar', 6)
Expecting:
    'foobar'
ok
Trying:
    left_pad('toolong', 2)
Expecting:
    'toolong'
ok
Trying:
    left_pad(1, 2, '0')
Expecting:
    '01'
ok
Trying:
    left_pad(17, 5, 0)
Expecting:
    '00017'
ok
1 items had no tests:
    left_pad
1 items passed all tests:
   5 tests in left_pad.left_pad
5 tests in 2 items.
5 passed and 0 failed.
Test passed.
(personal386) $
```

In case of a failure:

```python
Failed example:
    left_pad('foo', 5)
Expected:
    '  fooN'
Got:
    '  foo'
```
