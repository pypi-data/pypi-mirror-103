# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cltools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cltools',
    'version': '0.5.0',
    'description': 'Set of decorators of to create transform a class into a command-line tool.',
    'long_description': 'cltools\n=======\n\nSet of decorators of  to create transform a class into a command-line tool\n\nImagine, you\'ve got a class you want to use from the command line, without having\nto explicitly parse the command line and make all the routing stuff.\n\nThat\'s what\'s ``cltools`` is doing by proving decorators on class and methods to make your\nclass runnable, and transform your method into commands.\n\n``cltools`` create command tools like git/hg/svn/apt-get/apt-cache/..., that means your\ntool will have commands\n\nsimple example :\n----------------\n\nImagine, you\'ve got a simple class that make tasks, and you want to make a command line tool\nwith that. Let\'s say, it\'s a calculator module ``calclib.py``:\n\n.. code:: python\n\n    #!/usr/bin/env python\n    \n    class Calc(object) :\n        def __init__(self) :\n            pass\n        def add(self, value1, value2) :\n            return value1+value2\n        def mult(self, value1, value2) :\n            return value1*value2\n\nThen, we will write a simple class and transform into a runnable tool:\n\n.. code:: python\n\n    #!/usr/bin/env python\n    \n    import sys\n    from calclib import Calc\n    from cltools import CLRunner\n    \n    @CLRunner.runnable()\n    class CalcTool(object) :\n        \'\'\'A simple command-line wrapper for calclib\'\'\'    \n        def __init__(self) :\n            self._calc = Calc()\n    \n    \n        def get_two_params(self, args) :\n            if len(args) != 2 :\n                # errorexit provided by CLRunnable parent\n                self.errorexit("Need two values VALUE1 and VALUE2 as arguments")\n            try :\n                value1 = int(args[0])\n            except Exception :\n                self.errorexit("Value [%s] should be a valid number" % (args[0],))\n            try :\n                value2 = int(args[1])\n            except Exception :\n                self.errorexit("Value [%s] should be a valid number" % (args[1],))\n            return value1, value2\n    \n        @CLRunner.command()\n        def add(self, args, kwargs) :\n            \'\'\'Add two values VALUE1 and VALUE2 given as parameters\'\'\'\n            value1, value2 = self.get_two_params(args)\n            value = self._calc.add(value1, value2)\n            self.status("Result : [%s]" % (value,))\n    \n        @CLRunner.command()\n        def mult(self, args, kwargs) :\n            \'\'\'Multiplie two values VALUE1 and VALUE2\'\'\'\n            value1, value2 = self.get_two_params(args)\n            value = self._calc.mult(value1, value2)\n            self.status("Result : [%s]" % (value,))\n    \n        @CLRunner.command()\n        def help(self, args=[], kwargs={}) :\n            \'\'\'Get this help\'\'\'\n            super().help()\n    \n    if __name__ == \'__main__\' :\n        calctool = CalcTool()\n        if not(calctool.run( sys.argv )) :\n            sys.exit(1)\n\nNow we can test our command line tool::\n\n    $ ./calc.py\n    Usage: calc.py COMMAND_NAME [OPTION] [VALUES]\n    A simple command-line wrapper for calclib\n\n    Commands:\n        add                  Add two values VALUE1 and VALUE2 given as parameters\n        help                 Get this help\n        mult                 Multiplie two values VALUE1 and VALUE2\n    \n    Error : Need a command name\n\n::\n    \n    $ ./calc.py add 4 17\n    Result : [21]\n\n::\n    \n    $ ./calc.py add 15 66 33\n    Error : Need two values VALUE1 and VALUE2 as arguments\n\nNote that the help is automatically generate based on commands declared in the class, \nand the online doc attached to the class and methods.\n',
    'author': 'Gissehel',
    'author_email': 'public-dev-cltools@gissehel.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gissehel/cltools',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
