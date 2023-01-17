"""
Task 3. Python

Find elements which meet following conditions:
- first letter should be in upper case. '_' should follow it
- one of the following words should be in a middle: 'car', 'bus' or 'truck'
- should ends with '_' and with any three number
"""

import re

def regular_expr(line):
    # expr = re.compile("^[A-Z]_.*\Z")
    # expr = re.compile("^[A-Z]_.*(car|bus|truck){1}.*\Z")
    expr = re.compile("^[A-Z]_.*(car|bus|truck){1}.*_[0-9]{3}\Z")

    if expr.match(line):
        return True
    else:
        return False


def main():
    print(regular_expr('A_super_bus_driver_001'))
    print(regular_expr('B_sport_car_091'))


if __name__ == '__main__':
    main()