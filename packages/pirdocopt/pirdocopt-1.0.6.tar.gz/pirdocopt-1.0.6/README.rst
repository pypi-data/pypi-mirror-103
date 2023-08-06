``pirdocopt`` a helper for enhancing your command line project
==================================================================

API
============

.. code:: python

    from pirdocopt import docopt
    arguments = docopt(__doc__, version="", help_message=Ture, argv=[])

How to Install
========================
Use pip or easy_install:

.. code:: python

    pip install pirdocopt
    
Or just include ``docopt.py`` and ``docopt_util.py`` in you project folder and import the module ``import docopt from docopt``.

Testing
========
All test cases are included in ``examples`` folder

Usages
========
When you have a command-line python program which contains a docstring and want to show user all the usage patterns
and the options that provided by you program, you just need to call docopt.py:

.. code:: python

    """Perfect

       Usage:
         my_program.py ship new <name>
         my_program.py ship <name> move <x> <y> [--speed=<kn>]
         my_program.py ship shoot <x> <y>
         my_program.py mine (set|remove) <x> <y> [--moored | --drifting]
         my_program.py (-h | --help)
         my_program.py --version

       Options:
         -h --help  Show this screen.
         --version     Show version.
         --speed=<kn> -s KN  Speed in knots [default: 10].
         --moored      Moored (anchored) mine.
         --drifting    Drifting mine.
         
    """
    from pirdocopt import docopt
    
    if __name__ == '__main__':
        res = docopt(__doc__, version="", help_message=False, argv=['mine', 'set', '50', '200', '--moored'])
        print(res)
      
Docopot will turns all your usage pattern and options into a dictionary as the return value and standout the tidy JSON-like string:

.. code:: javascript

   res == {'ship': False, 'new': False, 'name': None, 
   'move': False, 'x': '50', 'y': '200', 'shoot': False, 'mine': True, 
   'set': True, 'remove': False, '--helping': False, '--sorted': False, 
   '--output': './test.txt', '--version': False, '--speed': 10, '--moored': True, 
   '--drifting': False, '--rr': False, '--aaa': 20, '--yyy': False}
    
    {'ship': False      'set': True                  '--drifting': False
     'new': False       'remove': False              '--rr': False
     'name': None       '--helping': False           '--aaa': None
     'move': False      '--sorted': False            '--yyy': False
     'x': '50'          '--output': './test.txt'
     'y': '200'         '--version': False
     'shoot': False     '--speed': 10
     'mine': True       '--moored': True}
     
Sample help message when ``help_message=True``::


     Perfect

     Version:
       test 2.0

     Usage:
       naval_fate.py ship new <name>
       naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
       naval_fate.py ship shoot <x> <y>
       naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
       naval_fate.py (-h | --help)
       naval_fate.py --version

     Options:
       -h --help --helping --haha -hhh --ooooo  Show this screen.
       --sorted  Show sorted.
       -o FILE --output=<file>  Speed in knots [default: ./test.txt].
       --version     Show version.
       --speed=<kn> -s KN  Speed in knots [default: 10].
       --moored      Moored (anchored) mine.
       --drifting    Drifting mine.
       --rr     Show version.
       --aaa=<file>      Moored (anchored) mine [default: 20].
       --yyy    Drifting mine.

Features
--------

- ``docopt`` will match the useage pattern specified by you in the docstring and show errors if user input a wrong pattern.
- ``<value>`` means the required value from usage arguments
- ``[--option]`` means a opotion
- For usage patterns ``docopt`` support ``(value1|value2)`` for required choices from user
  and ``[-option1 | --option2]`` for optional choices from user
- For options, ``docopt`` support multiple keywords for one option e.g. ``-h --help``
- For options that has an value, you can either use ``--option= <value>`` or ``--option VALUE``.
- For multiple keywords in options, the output dictionay will only display the detailest (longest) keyword.
- Show warnings if you program does not hava a docstring that meets the min case or
  your docstring does not includes a Usage pattern list or options list.
  
Formats
-----------------------

The cases for docstring:

.. code:: python

    # Minimum case
    """Usage: my_program.py

    """

    # Docstring with program name, usage pattern, and options table
    """Perfect # Program name in the first line
      # Must separae each section with a newline
      Usage:
        my_program.py --help
        ...
      # Must separae each section with a newline
      Options:
        -h --help Show this screen.
        ...

    """

    # Docstring with, usage pattern, and options table
    """
      Usage:
        my_program.py --help
        ...

      Options:
        -h --help Show this screen.
        ...

    """

    """Usage:
        my_program.py --help
        ...

      Options:
        -h --help Show this screen.
        ...

    """

    """Usage:
        my_program.py --help
        ...

        -h --help Show this screen.
        ...

    """

The different cases for usage patterns::

    my_program.py   #GOOD a pattern that has no parameter and arguments.
    my_program.py ship   #GOOD a pattern that has one required parameter.
    my_program.py <value>     #GOOD a pattern that has one required user input value.
    my_program.py <value> my_program.py ship    #BAD every pattern will start from a new line.

    my_program.py  (value1 | value2)    #GOOD a pattern that contains a choosable required arugment.
    my_program.py  [-option1 | --option2]    #GOOD a pattern that contains a choosable optional arugment.
    my_program.py  a1 | a2    #BAD mutual choices will either inside a bracket or a round parenthese.
    
The different cases for options table::


     Options:
       --help show help message #GOOD a line that starts with '--' will be considered as an option.
       -h short for show help message #GOOD  a line that starts with '-' will be considered as an option.
     Options: --help show help message #BAD program will ignore the lines that
                                            not start with double dash or single dash in options table.

     Options:
       --input=<file> user input file   #GOOD an options that must contain a value.
       -i=<file> user input file   #GOOD an options that must contain a value.
       --speed KN user input speed in integer   #GOOD KN will consider as the required value for speed.
       -s KN user input speed in integer    #GOOD KN will consider as the required value for speed.
       -s KN -i=<file>   #BAD these two keyword will consider as two different keyword or an option

     Options:
       --speed=<kn> -s KN user input speed    #GOOD mulitple keyword for an option.
       --speed=<kn> -s KN user input speed [default: 10]    #GOOD to provide a default value for such option.


Required and Optional Parameters
----------------------------------

- ``__doc__`` is a required parameter for ``docopt`` to receive the docstring from you program.
- ``version=""`` is a optional parameter that you can specify you program version in string and display to user
- ``help_message=False`` is a optional parameter that default is set to ``Ture``. It allows ``docopt`` to standard output your docstring and the version specified by you right after the program is executed.
- ``argv=[]`` is also a optional parameter in which you can put an array of default arguments (must match your docstring usage pattern).

Comparasion Table
---------------------------

    +---------------------------------------------------+-----------+---------+----------+-------+--------+
    | Features                                          | pirdocopt |  getopt | optparse | click | docopt |
    +===================================================+===========+=========+==========+=======+========+
    | Parse usage partterns and options in docstring    |   True    |  False  |  False   | False |  True  | 
    +---------------------------------------------------+-----------+---------+----------+-------+--------+
    | Support default arguments from programmer         |   True    |  False  |  False   | False |  True  |
    +---------------------------------------------------+-----------+---------+----------+-------+--------+
    | Support default values in options docstring       |   True    |  True   |  True    | True  |  True  | 
    +---------------------------------------------------+-----------+---------+----------+-------+--------+
    | Enabling help message displaying when executes    |   True    |  False  |  False   | False |  True  |
    +---------------------------------------------------+-----------+---------+----------+-------+--------+
    | Enabling help message printing when executes      |   True    |  False  |  False   | False |  True  |
    +---------------------------------------------------+-----------+---------+----------+-------+--------+
    | Program version specifying                        |   True    |  False  |  False   | False |  false |
    +---------------------------------------------------+-----------+---------+----------+-------+--------+
    | Exception for incorrect  user arugment pattern    |   True    |  Flase  |   False  | False |  True  |
    +---------------------------------------------------+-----------+---------+----------+-------+--------+
          
Support
-------

If you are having issues, please let us know.
We have a mailing list located at: cl19x@my.fsu.edu or ktw16b@my.fsu.edu


License
-------

The project is licensed under the MIT license.

