# Importing required libraries for the package.
import struct

# Architecture function, returns the computer's architecture.
def architecture():
    bytesize = struct.calcsize('P')
    return bytesize * 8