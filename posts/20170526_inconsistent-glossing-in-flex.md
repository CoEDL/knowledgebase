---
permalink: inconsistent-glossing-in-flex
title: Finding and correcting glossing inconsistencies
author: Sasha Wilmoth
date: 2017-05-26
tags:
    - Glossing
    - Flex
    - Python
    - Appen
categories:
    - Tutorials
---

# Introduction
The analysis of a language's grammar can evolve over time. So too can glossing preferences. How can one ensure that an entire corpus is glossed consistently, as the lexicon is continually updated?

This post introduces a simple process for finding glossing inconsistencies in flextexts, and then automatically making changes across a corpus.

1. inconsistentGlosses.py finds glossing inconsistencies, and compares them to the most up-to-date lexicon.
2. The user manually corrects the output to reflect the preferred gloss.
3. updateGlosses.py automatically applies these changes across a corpus.

This process is designed to be iterative, with a bit of back and forth between running inconsistentGlosses.py, updating the lexicon, and fixing individual examples in context.

## Requirements
inconsistentGlosses.py and updateGlosses.py require Python 2.7, and do not currently work with Python 3. They work on Mac, and have not been tested on Windows.

Both scripts can be found [here](https://gitlab.com/swilmoth/inconsistentGlosses.py).

# inconsistentGlosses.py

## Input
inconsistentGlosses.py takes two arguments: a Flex lexicon, and a directory containing .flextext files. It looks in all subdirectories.

The command is:

```
inconsistentGlosses.py [-h] YourFlexLexicon /path/to/your/corpus/ [-v] > output [2> ErrorReport]
```
`-h` is a help message, `-v` is a verbose option that prints which files the invalid glosses were found in.

## Output
The script looks for morphs with glosses that aren't in the lexicon, and outputs a table which can be copied into a spreadsheet. This is the non-verbose output:

Morph | Original gloss | Gloss to correct | Frequency | In lexicon | Comments
 |  |  |  |  |  | 
-nku  | 3DAUC.DO | 3DAUC.DO | 18 | ✗ | Consider: 3PAUC.DO
 |  |  |  |  |  | 
-wanku  | COM | COM | 32 | ✓ | 
 | also | also | 1 | ✗ | Consider: COM
 |  |  |  |  |  | 
Dawun  | MISSING GLOSS | MISSING GLOSS | 3 | ✗ | Variant of dawun. There is no gloss for Dawun or dawun in the lexicon.
 |  |  |  |  |  | 
batbat  | right | right | 2 | ✗ | There is no gloss for batbat in the lexicon.
 |  |  |  |  |  | 
batj  | bring | bring | 74 | ✓ | 
 | watch | watch | 14 | ✓ | 
 | cook | cook | 2 | ✓ | 
 | take/bring | take/bring | 1 | ✗ | Consider: cook, bring, have.something.caught.in.one's.throat, watch, submerge
 ...|
 
The script also reports some stats to your terminal, as well as any morphs it finds that aren't in the lexicon. You can save this with ```2> ErrorReport.txt``` if you want to. For the Murrinhpatha data, the error report looks like this (if the verbose option is switched on, there's another column with file names):

**118 flextext files analysed**

**95 morphs with inconsistent glosses**

**15 morphs missing from lexicon**


Morph not in lexicon | Gloss in text | Frequency | Comments 
 |  |  | 
-dhangunu | source | 4  | 
-n | 3PL.DO | 10  | Allophone: -pun is citation form 
-pirra | 3PL.IO | 5  | Allophone: -wirra is citation form 
-rru | 3PAUC.IO | 6  | Allophone: -pirru is citation form 
-wayida | reason | 1  | 
=ka | =TOP | 35  | 
...|


We can then add all the missing morphs to the lexicon (or correct errors), add glosses to the lexicon where they were missing, and check glosses in context where necessary. If we run the script again, the output will be a bit smaller (e.g. *batbat* no longers show up because we've added 'right' as the gloss in the lexicon). Then we can correct the third column like so:

Morph | Original gloss | Gloss to correct | Frequency | In lexicon | Comments
 |  |  |  |  |  | 
-nku  | 3DAUC.DO | **3PAUC.DO** | 18 | ✗ | Consider: 3PAUC.DO
 |  |  |  |  |  | 
-wanku  | COM | COM | 32 | ✓ | 
 | also | **COM** | 1 | ✗ | Consider: COM
 |  |  |  |  |  | 
Dawun  | MISSING GLOSS | **Darwin** | 3 | ✗ | Variant of dawun. Consider: Darwin.
 |  |  |  |  |  | 
batj  | bring | bring | 74 | ✓ | 
 | watch | watch | 14 |  ✓ | 
 | cook | cook | 2 | ✓ | 
 | take/bring | **bring** | 1 | ✗ | Consider: cook, bring, have.something.caught.in.one's.throat, watch, submerge
 ...|
 
 This file becomes the input for updateGlosses.py, so we can make these changes across all the files automatically.

# updateGlosses.py
To update your lexicon:

```
updateGlosses.py [-h] CorrectionsFile /path/to/your/corpus/
```

The script creates a new directory called UpdatedFlextexts in your current working directory, and makes new copies of any flextext files containing incorrect glosses.

**Note:** Flex might object when you try and open the new files. If this happens, make sure the new glosses match the latest version of the lexicon. There may be an occasional problem when a gloss was missing in the original file.

# Acknowledgements
Thanks to Rachel Nordlinger and John Mansfield for the Murrinhpatha data, and Jason Johnston (with the support of Appen) for Python help.
