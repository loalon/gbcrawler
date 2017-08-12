# GBcrawler

**GBcrawler** is a complete GenBank parser in Python 3 meant to be used by other applications.

Generates a Python object of GBcrawler class that stores all relevant information within a GenBank file.


## Table of Contents

[**Features**](#features)

[**Installation**](#installation)

[**Usage**](#usage)

[**Discrepancies**](#discrep)

[**Future features**](#future)

## Features

This script was made using the information from: 

  * NCBI-GenBank Flat File Release available at [NCBI](https://www.ncbi.nlm.nih.gov/genbank/)
  * Features table available at [INSDC](http://www.insdc.org/documents/feature-table).


## Installation

Python 3 is requiered.

Copy GBcrawler.py to the folder of your project and import it as explained in [**Usage**](#usage)


## Usage

To get the GenBank data, create an object with the GenBank filename as a parameter: 

```
import GBcrawler from GB crawler
GBobject = GBcrawler("tth1.gb")
```

The following data can be adquired using: attributes or methods

Attribute references:
  * `sequenceID` returns sequence identification
  * `sequenceLength` returns length of sequence
  * `strand` returns the strand type 
  * `moleculeType` returns molecule type
  * `division` returns divison code
  * `modDate` returns date
  * `definition` returns definition
  * `accession` returns accesion
  * `version` returns version
  * `referenceList` returns a list, each element is a reference
  * `comment` returns all the comments as a string
  * `featureList` returns a list of GBfeatues object
  * `sequenceList` returns the sequence as a list, (see methods to get the sequence as a string)
  * `baseCount` returns dictionary with nucleotide counts

Methods:
  * `getSequence()` returns sequence as a string

The featureList is composed of GBfeature objects and data can be adquired using the following attribute references:
  * `begin` returns sequence identification
  * `end` returns length of sequence
  * `type` returns the type of the feauture (gene, CDS, ...)
  * `qualifierDict` returns a Dictionary with keys and values for each qualifier

## Discrepancies

The last Flat File release 220.0 has a set of features that is different from the feature table in INSDC. The release indicates "Any discrepancy between the abbreviated feature table description of these release notes and the complete documentation on the Web
should be resolved in favor of the version at the above URL."

At the moment, both sets of features will be used to parse the GenBank files, until a large batch of GenBank files can be tested and check how many files uses the "non-standard" features


## Future features

  * export to FASTA
  * check features for mandatory qualifiers
  * faster performance
  * tag features by its locus_tag
  * use additional info for the features (beyond, between bases, etc)
  * create a Reference class to better reference data management
  * improve ACCESION to return a list
  * improve SOURCE parsing 

