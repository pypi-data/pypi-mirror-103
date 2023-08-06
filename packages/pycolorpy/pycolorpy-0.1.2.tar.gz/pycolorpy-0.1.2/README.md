# pycolorpy

Adds typographical emphasis and text / background color for strings in python.

## Installation

```bash
pip install pycolorpy
```

## Usage

```python
from pycolorpy import black, red, green, yellow, blue, magenta, cyan, white

example_string = yellow('Hello ', options=['blink'], background='red') + magenta('World', options=['underline', 'italic'], background='green') + cyan('!')
print(example_string)
```

## Available options

* bright
* dark
* italic
* underline
* blink
* selected

## Available background colors

* black
* red
* green
* yellow
* blue
* magenta
* cyan
* white
