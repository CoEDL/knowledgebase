---
permalink: quick-glossing-in-CLAN
title: Quick automatic glossing in CLAN
author: Sasha Wilmoth, Simon Hammond, Hannah Sarvasy
date: 2017-05-30
tags:
    - Glossing
    - CLAN
    - Python
    - Appen
categories:
    - Scripts 
---

# Introduction
Hannah Sarvasy is conducting a longitudinal study of five children acquiring the Papuan language Nungon in a remote village of Papua New Guinea. This entails monthly recordings of the target children that are conducted and transcribed by four Nungon-speaking assistants in the village. The corpus will total 104 hours of transcribed natural speech recordings. Hannah's task is to add interlinear morpheme-by-morpheme parses and glossing and free English translations to the Nungon transcriptions, which are in the CHAT format. The glossing is to be done 

CLAN's built-in MOR program is an effective tool for glossing if you've already transcribed your data with morpheme boundaries, and you have a lexicon in .cut format.

However, Hannah had some slightly different needs, and I figured we could write a simple script that could correct spelling on the transcription tier, add a pre-determined parse, and add a gloss.

This script, glossFile.py is not an automatic parser - it simply takes the words you feed it, and makes no guesses about their structure.

It might be useful for you if you want to do a rough automatic pass before checking through your glossing manually, and you don't already have a large lexicon or parser set up. It was also designed to suit our particular circumstances, as the data had a lot of variation in spelling and spacing, and many repeated words (so we could cover a lot of ground without a parser).

# Instructions
## Requirements
glossFile.py can be found here [here](https://gitlab.com/swilmoth/glossFile.py/). You will need a GitLab account to request access.

glossFile.py requires Python 2.7, and does not currently work with Python 3. It works on Mac, and has not been tested on Windows.

## Step 1: Create a lexicon
Compile a list of words in your data, sorted by frequency. You can use CLAN's FREQ command to do this.

I also made a pre-populated lexicon based on some files that had already been manually glossed.

I then sent all the remaining words to Hannah, sorted by frequency, in the following format:

Word | Spelling Correction | %gls | %xcod | Frequency
---|---|---|---|---|
no | no | no |  | 1500
ma | ma | ma |  | 772
oro | oro | oro |  | 752
dek | dek | dek |  | 543
ho | ho | ho |  | 520
diyogo | diyogo | diyogo |  | 230
nano | nano | nano |  | 200
awa | awa | awa |  | 187
hewam | hewam | hewam |  | 175
arap | arap | arap |  | 174
Lisa | Lisa | Lisa |  | 169
dec | dec | dec |  | 167
bop | bop | bop |  | 165
gon | gon | gon |  | 162
to | to | to |  | 155
mai | mai | mai |  | 151

Hannah then checked through this list, and for each entry:

1. Made a correction in the second column if necessary
    * In order to reduce the manual effort of entering glossing for misspelled words multiple times, the third and fourth columns are ignored if there is a spelling correction.
    * Corrected words are then glossed according to the correctly-spelled entry (which already existed in most cases).
2. Added the appropriate morpheme boundaries
    * This example shows the most frequent items, which happened to include a lot of suffixes and clitics. If a `-` or `=` is added in the third column, the transcription tier is corrected to reflect this, and a space is removed.
3. Added a gloss for the whole word.

**Note:**

* Multiple entries for homophones are fine, and will be separated with a # symbol in both the %gls and %xcod tiers for manual disambiguation.
* If a word is not found in the lexicon, it is just printed as is on all tiers in the output.
* If a 'word' is not a morpheme at all, but should just be connected to the previous word, a full stop can be added in the third column. E.g. `.kak` tells the script that the word `kak` is actually a part of the previous word.



Word | Spelling Correction | %gls | %xcod | Comments
---|---|---|---|---|
no | no | -no | -3sg.poss|This means that `example no` will become `exampleno`/`example-no`/`example-3sg.poss` on the three tiers.
ma | ma | =ma | =rel|
oro | oro | oro | adv^well|
dek | dek | =dek | =loc|
ho | ho | =ho | =foc|
diyogo | diyogo | diyogo | q^how|
nano | nanno | nano | |The script only looks at the second column and ignores the rest.
awa | aawa | awa | |
hewam | hewam | hewam | n^tree.kangaroo|
arap | arap | arap | n^mammal|
Lisa | Lisa | Lisa | n^name|
dec | dec | =dec | |
bop | boop | bop | |
gon | gon | =gon | =restr|
to | to | =to | =foc|
mai | mai | =ma-i | =rel-top|


## Step 2: Run the script


Once you have a 4-column lexicon file (we can discard the frequency column), the command is:

```
python glossFile.py [-h] lexicon input.cha > output.cha
```

This will turn a passage like this (from 09_septemba_niumen.cha):

```
*CHI:	biksa yandinga itdok.
%com:	dogu digu yandinga itdok.
*MOT:	opmu menon ngo nungon to duwonga itdok ngo.
*MOT:	ngo ngo.
*CHI:	nnn nandumau.

```

into this:

```
*CHI:	biksa yandinga itdok.
%gls:	biksa yandinga it-do-k
%xcod:	tpn^picture yandinga v^be-rp-3sg
%eng:
%com:	dogu digu yandinga itdok.
*MOT:	opmu menon ngo nungonto duwonga itdok ngo.
%gls:	opmou menon ngo nungon=to duwo-nga it-do-k ngo
%xcod:	adj^small menon d^prox q^what=foc v^sleep-mv.ss v^be-rp-3sg d^prox
%eng:
*MOT:	ngo ngo.
%gls:	ngo ngo
%xcod:	d^prox d^prox
%eng:
*CHI:	nnn nandumau.
%gls:	nn nandu=ma au#nandu=ma-u
%xcod:	ij n^non.specific=rel adj^other#n^non.specific=rel-top
%eng:
```

**Note**:

* *oe ho* is corrected to *oeho*,
* *yandinga* and *menon* are just printed as is (they weren't in the lexicon),
* *nandumau* has a couple of options to choose from, *nandu=ma au* (n^non.specific=rel adj^other) or *nandu=ma-u* (n^non.specific=rel-top)


## Acknowledgements
glossFile.py was written by Simon Hammond thanks to Appen's partnership with CoEDL.

All Nungon data shown here was collected by Hannah Sarvasy, and transcribed by Nungon-speaking assistants.
