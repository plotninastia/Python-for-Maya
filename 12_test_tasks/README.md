Here are tasks from the test.


Task 1. Python
Find a word with maximum length. a function should take any number of arguments.

---

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

---

Task 3. Python

Find elements which meet following conditions:
- first letter should be in upper case. '_' should follow it
- one of the following words should be in a middle: 'car', 'bus' or 'truck'
- should ends with '_' and with any three number

---

Task 4. Maya

There is a certain hierarchy of objects in Outliner.

The objects group called 'objects' is hidden (respectively, all objects inside too).

All locators (loc_inst_##) are located somewhere in the scene, have different coordinates, rotation, scales.

The task is to replace these locators with objects from the objects group. Objects in this group must be
randomly selected for each locator.

The replacement must occur either with copies of objects from the group (the originals remain in the hidden group),
or by the originals themselves (at the same time, the number of locators and objects must match - you will need to check this).
Note that locators can either be at the root of the Outliner or in a group.

---

Task 5. Maya

There is some geometric surface in the scene.

Write a script which will position other selected objects (spheres or locators, etc)
on the surface of the current object at random positions.

If objects, when placed on the surface, intersect with the surface, this is ok.

---

Task 6. UI

Create a window which has two custom widgets.
These two widgets must be instances of the same class.

They should stand out against the background of the dialog box (change bg color of them).

When user clicks on one widget, the other widget should change color to a random one.
