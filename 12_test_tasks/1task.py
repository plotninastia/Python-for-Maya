"""
Task 2. Python

Find a word with maximum length. a function should take any number of arguments
"""

def findMaxWord(*args):
    return max(*args, key=len)


def main():
    print(findMaxWord('ala', 'ma', 'kota', 'laka', 'edr', 'ghyf'))


if __name__ == '__main__':
    main()
