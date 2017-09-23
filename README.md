py-branfuck
===========

A simple interpreter for Brainfuck in pure Python without dependencies.

Testing
-------

First set up the virtual env:

    virtualenv .venv -p python3
    source .venv/bin/activate
    pip install -r requirements

Then, run the tests using `nosetest`:

    nosetests
