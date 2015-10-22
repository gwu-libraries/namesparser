# namesparser

[![Build status](https://travis-ci.org/gwu-libraries/namesparser.svg)]

Complement to [nameparser](https://github.com/derek73/python-nameparser) for parsing lists of names.
Namesparser handles initials and variable name ordering.

Examples of lists of names:

* Oliver Boliver Butt and Zanzibar Buck-Buck McFate and Bodkin Van Horn
* OB Butt, ZBB McFate and B Van Horn
* Butt, Oliver Boliver, Zanzibar Buck-Buck McFate, and Bodkin Van Horn
* Butt O.B., McFate Z.B.B. and Van Horn B.

(Names courtesy of Dr. Seuss's [Too Many Daves](http://www.poetryfoundation.org/poem/171612).)

## Usage
    >>> from namesparser import HumanNames
    >>> names = HumanNames("Oliver Boliver Butt and Zanzibar Buck-Buck McFate and Bodkin Van Horn")
    >>> str(names)
    'Oliver Boliver Butt and Zanzibar Buck-Buck McFate and Bodkin Van Horn'
    >>> names.human_names
    [<HumanName : [
        title: '' 
        first: 'Oliver' 
        middle: 'Boliver' 
        last: 'Butt' 
        suffix: ''
        nickname: ''
    ]>, <HumanName : [
        title: '' 
        first: 'Zanzibar' 
        middle: 'Buck-Buck' 
        last: 'McFate' 
        suffix: ''
        nickname: ''
    ]>, <HumanName : [
        title: '' 
        first: 'Bodkin' 
        middle: '' 
        last: 'Van Horn' 
        suffix: ''
        nickname: ''
    ]>]
    >>> names.name_strings
    ['Oliver Boliver Butt', 'Zanzibar Buck-Buck McFate', 'Bodkin Van Horn']
    >>> names = HumanNames("OB Butt, ZBB McFate and B Van Horn")
    >>> str(names)
    'OB Butt and ZBB McFate and B Van Horn'
    >>> names = HumanNames("Butt, Oliver Boliver, Zanzibar Buck-Buck McFate, and Bodkin Van Horn")
    >>> str(names)
    'Oliver Boliver Butt and Zanzibar Buck-Buck McFate and Bodkin Van Horn'
    >>> names = HumanNames("Butt O.B., McFate Z.B.B. and Van Horn B.")
    >>> str(names)
    'O.B. Butt and Z.B.B. McFate and B. Van Horn'


## Install
    pip install namesparser

## Tests

    python -m unittest discover
