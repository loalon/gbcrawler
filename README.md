# GBcrawler

## Overview

GBcrawler is a complete GenBank parser in Python meant to be used by other applications.

Generates a Python object of GBcrawler class that stores all relevant information within a GenBank file.

## Usage

Creating an object with the GenBank filename as a parameter

'''
GBobject = GBcrawler("tth1.gb")
'''

The following data can be adquired using:

attribute references:
	sequenceID returns sequence identification
	sequenceLength returns length of sequence
	strand 
	
	
Methods:

  * getSequence() returns sequence as a string


