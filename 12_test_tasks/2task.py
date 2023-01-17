"""
Task 2. Python

myDict = {"fruit" : ["apple", "blueberry", "pineapple"], "vegetable" : ["broccoli", "potato", "tomato"]}

a = ["maya", "apple", "potato", "blueberry", "laptop", "icecream", "tomato", "candy"]

There is a list a with a different set of words.
There is also a myDict dictionary with categories fruit and vegetables.

The task is to replace all vegetables and fruits in the list with alternative ones from the dictionary
(according to their belonging to a certain category).

Moreover, a fruit / vegetable cannot be replaced with the same one
(for example, if you replace apple with apple, this will not be correct).

For example, the list ['apple', 'tomato', 'car'] should be replaced with something like ['blueberry', 'potato', 'car'].

Please note that car has not been replaced by anything, because it does not belong to any of the myDict categories.


"""
import random

myDict = {"fruit" : ["apple", "blueberry", "pineapple"], "vegetable" : ["broccoli", "potato", "tomato"]}
a = ["maya", "apple", "potato", "blueberry", "laptop", "icecream", "tomato", "candy", 'pineapple', 'apple']

output = []

for item in a:
    nonfind = ''
    for key in myDict:
        if item in myDict[key]:
            new_values = myDict[key].copy()
            new_values.remove(item)
            new_i = random.choice(new_values)
            output.append(new_i)
            if nonfind == item:
                nonfind = ''
            break
        else:
            nonfind = item
    if nonfind != '':
        output.append(nonfind)
        nonfind=''


for i in output:
    print(i)

