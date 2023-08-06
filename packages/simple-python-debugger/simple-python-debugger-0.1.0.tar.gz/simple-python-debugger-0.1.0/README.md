# Simple-Python-Debugger
Simple Debugger Package for python.

## Example
### Code
```
from simple_python_debugger import debug


@debug
def binary_search(list_, value):
    list_size = len(list_) - 1

    index0 = 0
    indexn = list_size
    while index0 <= indexn:
        middle = (index0 + indexn) // 2

        if list_[middle] == value:
            return middle

        if value > list_[middle]:
            index0 = middle + 1
        else:
            index0 = middle - 1

    if index0 > indexn:
        return None


binary_search([x for x in range(10)], 7)
```
### Output
```
binary_search(args: ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 7) kwargs: {}) -> 7
Time of Execution: 0.00
```
