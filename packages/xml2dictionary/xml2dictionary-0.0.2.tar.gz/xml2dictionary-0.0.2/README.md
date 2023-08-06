# xml2dictionary

xml2dictionary is a package that converts any xml to json (dict)

## Requirements

1. Python 3.8
2. Pipenv


## Installation


```sh
pip install xml2dictionary
```

## Usage

Example

```sh
from xml2dictionary import xml2dictionary
with open('tests/sample.xml', 'r') as f:
    m = f.read()

result = xml2dictionary(m)

OrderedDict([('breakfast_menu', OrderedDict([('food', [OrderedDict([('name', 'Belgian Waffles'), ('price', '$5.95'), ('description', 'Two of our famous Belgian Waffles with plenty of real maple syrup'), ('calories', '650')]), OrderedDict([('name', 'Strawberry Belgian Waffles'), ('price', '$7.95'), ('description', 'Light Belgian waffles covered with strawberries and whipped cream'), ('calories', '900')]), OrderedDict([('name', 'Berry-Berry Belgian Waffles'), ('price', '$8.95'), ('description', 'Light Belgian waffles covered with an assortment of fresh berries and whipped cream'), ('calories', '900')]), OrderedDict([('name', 'French Toast'), ('price', '$4.50'), ('description', 'Thick slices made from our homemade sourdough bread'), ('calories', '600')]), OrderedDict([('name', 'Homestyle Breakfast'), ('price', '$6.95'), ('description', 'Two eggs, bacon or sausage, toast, and our ever-popular hash browns'), ('calories', '950')])])]))])

```

## Functions


```sh
parse - parses xml string to dictionary
clear_signs - clears parsed xml from props with `sign` , shifts `shift` , escapes `scape`
json_to_xml - converts json to xml
xml2json - uses parse & clear_signs
```