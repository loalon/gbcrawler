# GBcrawler

GBcrawler is a complete GenBank parser in Python 3 meant to be used by other applications.

Generates a Python object of GBcrawler class that stores all relevant information within a GenBank file.

## Table of Contents

[**Features**](#features)

[**Installation**](#installation)
  * [**1 - Manual**](#option-1-download-and-install-manually)
  * [**2 - Release Archive Download**](#option-2-release-archive-download)

## Features

This script was made using the information from 

  * NCBI-GenBank Flat File Release available at [NCBI](https://www.ncbi.nlm.nih.gov/genbank/)
  * Features table available at [INSDC](http://www.insdc.org/documents/feature-table).



## Usage

Creating an object with the GenBank filename as a parameter

```
import GBcrawler from GB crawler
GBobject = GBcrawler("tth1.gb")
```

The following data can be adquired using:

attribute references:
  * sequenceID 
      returns sequence identification
  * sequenceLength 
    returns length of sequence
  * strand 

Methods:

  * getSequence() 
    returns sequence as a string

