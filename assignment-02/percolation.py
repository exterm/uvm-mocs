
## from https://introcs.cs.princeton.edu/python/24percolation/percolation.py.html

#-----------------------------------------------------------------------
# percolation.py 
#-----------------------------------------------------------------------

import stdio

#-----------------------------------------------------------------------

# isOpen is a matrix that represents the open sites of a system.
# isFull is a partially completed matrix that represents the full sites
# of that system. Update isFull by marking every site of that system
# that is open and reachable from site (i, j).

def _flow(isOpen, isFull, i, j):
    n = len(isFull)
    if (i < 0) or (i >= n):
        return
    if (j < 0) or (j >= n):
        return
    if not isOpen[i][j]:
        return
    if isFull[i][j]:
        return
    isFull[i][j] = True
    _flow(isOpen, isFull, i+1, j  )  # Down.
    _flow(isOpen, isFull, i  , j+1)  # Right.
    _flow(isOpen, isFull, i  , j-1)  # Left.
    _flow(isOpen, isFull, i-1, j  )  # Up.

#-----------------------------------------------------------------------

# isOpen is a matrix that represents the open sites of a system.
# Compute and return a matrix that represents the full sites of
# that system.

def flow(isOpen):
    n = len(isOpen)
    isFull = create2D(n, n, False)
    for j in range(n):
        _flow(isOpen, isFull, 0, j)
    return isFull

#-----------------------------------------------------------------------

# isOpen is matrix that represents the open sites of a system. Return
# True if that system percolates, and False otherwise.

def percolates(isOpen):
    
    # Compute the full sites of the system.
    isFull = flow(isOpen)
    
    # If any site in the bottom row is full, then the system
    # percolates.
    n = len(isFull)
    for j in range(n):
        if isFull[n-1][j]:
            return True
    return False

#-----------------------------------------------------------------------

# Read from standard input a boolean matrix that represents the
# open sites of a system. Write to standard output a boolean
# matrix representing the full sites of the system. Then write
# True if the system percolates and False otherwise.

def main():
    isOpen = readBool2D()
    write2D(flow(isOpen))
    stdio.writeln(percolates(isOpen))

    #isOpen = readBool2D()
    #write2D(flow(isOpen))
    #draw(isOpen, False)
    #stddraw.setPenColor(stddraw.BLUE)
    #draw(flow(isOpen), True)
    #stdio.writeln(percolates(isOpen))
    #stddraw.show()

#-----------------------------------------------------------------------

# python percolation.py < test5.txt 
# 5 5
# 0 1 1 0 1 
# 0 0 1 1 1 
# 0 0 0 1 1 
# 0 0 0 0 1 
# 0 1 1 1 1 
# True

# python percolation.py < test8.txt 
# 8 8
# 0 0 1 1 1 0 0 0 
# 0 0 0 1 1 1 1 1 
# 0 0 0 0 0 1 1 0 
# 0 0 0 0 0 1 1 1 
# 0 0 0 0 0 1 1 0 
# 0 0 0 0 0 0 1 1 
# 0 0 0 0 1 1 1 1 
# 0 0 0 0 0 1 0 0 
# True

"""
py

The stdarray module defines functions related to creating, reading,
and writing one- and two-dimensional arrays.
"""

import stdio

#=======================================================================
# Array creation functions
#=======================================================================

def create1D(length, value=None):
    """
    Create and return a 1D array containing length elements, each
    initialized to value.
    """
    return [value] * length

#-----------------------------------------------------------------------

def create2D(rowCount, colCount, value=None):
    """
    Create and return a 2D array having rowCount rows and colCount
    columns, with each element initialized to value.
    """
    a = [None] * rowCount
    for row in range(rowCount):
        a[row] = [value] * colCount
    return a

#=======================================================================
# Array writing functions
#=======================================================================

def write1D(a):
    """
    Write array a to sys.stdout.  First write its length. bool objects
    are written as 0 and 1, not False and True.
    """
    length = len(a)
    stdio.writeln(length)
    for i in range(length):
        # stdio.writef('%9.5f ', a[i])
        element = a[i]
        if isinstance(element, bool):
            if element == True:
                stdio.write(1)
            else:
                stdio.write(0) 
        else:
            stdio.write(element)
        stdio.write(' ')
    stdio.writeln()

#-----------------------------------------------------------------------

def write2D(a):
    """
    Write two-dimensional array a to sys.stdout.  First write its
    dimensions. bool objects are written as 0 and 1, not False and True.
    """
    rowCount = len(a)
    colCount = len(a[0])
    stdio.writeln(str(rowCount) + ' ' + str(colCount))
    for row in range(rowCount):
        for col in range(colCount):
            #stdio.writef('%9.5f ', a[row][col])
            element = a[row][col]
            if isinstance(element, bool):
                if element == True:
                    stdio.write(1)
                else:
                    stdio.write(0)
            else:
                stdio.write(element)
            stdio.write(' ')
        stdio.writeln()

#=======================================================================
# Array reading functions
#=======================================================================

def readInt1D():
    """
    Read from sys.stdin and return an array of integers. An integer at
    the beginning of sys.stdin defines the array's length.
    """
    count = stdio.readInt()
    a = create1D(count, None)
    for i in range(count):
        a[i] = stdio.readInt()
    return a

#-----------------------------------------------------------------------

def readInt2D():
    """
    Read from sys.stdin and return a two-dimensional array of integers.
    Two integers at the beginning of sys.stdin define the array's
    dimensions.
    """
    rowCount = stdio.readInt()
    colCount = stdio.readInt()
    a = create2D(rowCount, colCount, 0)
    for row in range(rowCount):
        for col in range(colCount):
            a[row][col] = stdio.readInt()
    return a

#-----------------------------------------------------------------------

def readFloat1D():
    """
    Read from sys.stdin and return an array of floats. An integer at the
    beginning of sys.stdin defines the array's length.
    """
    count = stdio.readInt()
    a = create1D(count, None)
    for i in range(count):
        a[i] = stdio.readFloat()
    return a

#-----------------------------------------------------------------------

def readFloat2D():
    """
    Read from sys.stdin and return a two-dimensional array of floats.
    Two integers at the beginning of sys.stdin define the array's
    dimensions.
    """
    rowCount = stdio.readInt()
    colCount = stdio.readInt()
    a = create2D(rowCount, colCount, 0.0)
    for row in range(rowCount):
        for col in range(colCount):
            a[row][col] = stdio.readFloat()
    return a

#-----------------------------------------------------------------------

def readBool1D():
    """
    Read from sys.stdin and return an array of booleans. An integer at
    the beginning of sys.stdin defines the array's length.
    """
    count = stdio.readInt()
    a = create1D(count, None)
    for i in range(count):
        a[i] = stdio.readBool()
    return a

#-----------------------------------------------------------------------

def readBool2D():
    """
    Read from sys.stdin and return a two-dimensional array of booleans.
    Two integers at the beginning of sys.stdin define the array's
    dimensions.
    """
    rowCount = stdio.readInt()
    colCount = stdio.readInt()
    a = create2D(rowCount, colCount, False)
    for row in range(rowCount):
        for col in range(colCount):
            a[row][col] = stdio.readBool()
    return a


# Copyright © 2000–2015, Robert Sedgewick, Kevin Wayne, and Robert Dondero.
# Last updated: Fri Oct 20 20:45:16 EDT 2017. 

# Copyright © 2000–2015, Robert Sedgewick, Kevin Wayne, and Robert Dondero.
# Last updated: Fri Oct 20 20:45:16 EDT 2017.
