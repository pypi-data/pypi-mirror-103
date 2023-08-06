[![PyPI version shields.io](https://img.shields.io/pypi/v/matrix-py.svg)](https://pypi.python.org/pypi/matrix-py/)
[![PyPI license](https://img.shields.io/pypi/l/matrix-py.svg)](https://pypi.python.org/pypi/matrix-py/)
[![Updated Badge](https://badges.pufler.dev/updated/FaresAhmedb/matrix-py)](https://badges.pufler.dev)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/480bf6060f5a49938991f62a368f8859)](https://www.codacy.com/gh/FaresAhmedb/matrix-py/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=FaresAhmedb/matrix-py&amp;utm_campaign=Badge_Grade)
[![codebeat badge](https://codebeat.co/badges/b51ca73f-6ba1-443f-ae4d-fd9f541176b2)](https://codebeat.co/projects/github-com-faresahmedb-matrix-py-main)

# matrix-py
matrix-py Module is a python module to:

  - Add Matrices :heavy_check_mark:

  - Substract Matrices :heavy_check_mark:

  - Multiply Matrices :heavy_check_mark:

  - Transpose Matrices :heavy_check_mark:

and many other things will come on 1.0 (if the project is still live)

Works with Python3+ 

---

# Installation
As far as I'm concerned it should work on any python3 version but it's always good to have the latest version since it will be the one I am sure it works on

## Using PyPI
```bash
pip install matrix-py
```

## Manule Installation
```bash
git clone https://github.com/FaresAhmedb/matrix-py.git
cd matrix-py && python setup.py install --user
```

Now Try it! 
```bash
$ matrixpy -h
```
On Windows
```powershell
> python -m matrixpy -h
```

The ouput should be something like this:
```
usage: __main__.py [-h] [-v] [-s] [-t] [-ma] [-op] [-mb] [-i]

Matrix Minuplation module to add, substract, multiply matrices.

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      show program's version number and exit
  -s , --size        Size of A Matrix
  -t , --transpose   Transpose of A Matrix (-t "[[1, 2, 3], [4, 5, 6]]")
  -ma , --matrixa    Matrix A (.. -ma "[[1, 2, 3], [4, 5, 6]]")
  -op , --operator   Operator (.. -op "+", "-", "*")
  -mb , --matrixb    Matrix B (.. -mb "[[1, 2, 3], [4, 5, 6]]")
  -i , --int         Integer (.. -i 69)

Usage: .. -ma "[[1, 2, 3], [4, 5, 6]]" -op "+" -mb "[[7, 8, 9], [10, 11, 12]]"
```

# Usage
HEADS UP! :warning:: UPDATE 0.3 HAS OTHER STUFF SO USE help(Matrix) UNTIL I ADD THE NEW STUFF
## - The Module
Sample code:
```python


from matrixpy import Matrix

A = Matrix([ [1, 2, 3], [4, 5, 6] ])   # List -> Matrix Object
B = Matrix([ [1, 4], [2, 5], [3, 6] ]) # List -> Matrix Object

# Print the multiply of Matrix A * Matrix B
print(A * B)
# Ouput:
# 14 32
# 32 77
# (2x2)

# Print the addition of the negative Matrix A + Matrix B transposed
print(-A + B.transpose()) 
# Ouput:
# 0 0 0
# 0 0 0
# (2x3)

# 0.1% solved this
C = (+A.transpose() - -B) - (B * 3) + (A.transpose() * 5)
print(C)
# Output:
# 4 16
# 8 20
# 12 24
# (3x2)

# Convert the Matrix to a list if you want to manipulate the matrices yourself
C = C.tolist()
print(type(C))
# Output:
# <class 'list'>
```

## - The Command Line Interface (CLI)
NOTE :warning:: On Windows NT all the command  below are done like this:
```
python -m matrixpy
```

The CLI is limited at the moment by one  operation at a time (eg. You can't add 3 matrices) duo to the limitations of argparse 

To get the size of a matrix
```bash
$ matrixpy -s '[[1, 2, 3], [4, 5, 6]]'
1 2 3
4 5 6
(2x3)
```
Your matrix is [[1, 2, 3], [4, 5, 6]] \
To get the transpose of a matrix
```bash
$ matrixpy -t '[[1, 2, 3], [4, 5, 6]]'
1 4
2 5
3 6
(3x2)
```
To add 2 matrices to each other or add a matrix to an integer:
```bash
$ matrixpy -ma '[[1, 2, 3], [4, 5, 6]]' -op '+' -mb '[[1, 2, 3], [4, 5, 6]]'
2 4 6
8 10 12
(2x3)

$ matrixpy -ma '[[1, 2, 3], [4, 5, 6]]' -op '+' -i 2
3 4 5
6 7 8
(2x3)
```
to substract or multiply matrices just change the '+' to '-' or '*' \
and for a list of the all avillable options
```
$ matrixpy --help
```
---

## Alpha Noitce
The Module is right now in Alpha so there's a big chance there's
some bugs so please consider reporting them.

All Contributions are welcomed so consider looking at the source
code on src/matrixpy

## Why, Why publishing this simple module?
Yes I know it's a simple module that doesn't do everything it's excpected to do \
and to be honest I didn't really want to put it on my github as my "FIRST" project \
nope it is not. I code most of the time without remote repositories for \
fun and personal programs (this one was) that I want and don't think anyone would be \
intersted in (eg. I created CLH-Bash the game in python for the sake of hating JavaScript) \
but this project is different I have learnt a LOT of things while creating this module from \
knowing classes better to writing a more readable code to how to package a module and even some algorithms \
that I used and was very inspiring to me so I wanted to share my little creation with the world!

## License &copy;
matrix-py module to add, substract, multiply matrices.
Copyright (C) 2021 Fares Ahmed

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
