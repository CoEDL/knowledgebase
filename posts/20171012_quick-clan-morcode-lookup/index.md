---
# Quick CLAN morcode lookup
author: Sasha Wilmoth
date: 2017-10-12
tags:
    - Tutorial
    - CLAN
    - CHAT
    - Gurindji Kriol
    - Python
categories:
    - Scripts
---

## Introduction

Each utterance in the Gurindji Kriol corpus has a tier with morphological information for each token in the transcription tier. It looks like this (with the `\P` marking a pronominal subject):

```
*FSO:	kayirra _k tubala karrap . 
%mor:	adv:loc|kayirra&g=north case:all|_k&g=ALL
	pro|dubala&3DU&k=those_two\P v:tran|karrap&g=look_at .
%eng:	Those two are looking to the north.
```
Whereas the lexicon that all these codes are taken from looks like this:

```
...
_k {[scat case:all]} "_k&g" =ALL=
_k {[scat der:fact]} "_k&g" =FACT=
...
karrap {[scat v:tran]} "karrap&g" =look_at=
...
kayirra {[scat adv:loc]} "kayirra&g" =north=
...
tubala {[scat pro]} "dubala&3DU&k" =those_two=
...

```
As you can imagine, if you have to make any small corrections to the mor tier, it's incredibly fiddly and time-consuming to look up each morph in the lexicon and type out the code. The only other option is to run the MOR command again, which is even more undesirable.

So, I wrote a little interactive script (printMorCodes.py) that looks them up for you.

## Instructions
## Requirements
This script requires Python 2.x. It works on Mac and has not been tested on Windows

The script can be found [here](https://gitlab.com/swilmoth/morCodeLookup.py).

## Running the script
The command is:

```
morCodeLookup.py -l lexicon(s)
```

Gurindji Kriol uses two lexicon files, so the command I use is:

```
morCodeLookup.py -l /Users/swilmoth/Dropbox/appencoedlinternship/kri/lex/lex_gurindji.cut /Users/swilmoth/Dropbox/appencoedlinternship/kri/lex/lex_kriolgen.cut
```

The script has a little welcome message, and then you just type a sentence into the terminal and it looks up the codes for you.

If you type *kayirra _k tubala karrap*, it gives you:

 `adv:loc|kayirra&g=north case:all|_k&g=ALL^der:fact|_k&g=FACT pro|dubala&3DU&k=those_two v:tran|karrap&g=look_at`.

If you type *jei \_m gon Lajamanu \_ngkirri!* 'They went to Lajamanu!', you get:

`pro|dei&3PL/S&k=they suf|_m&TAM&k=PRS v:intran|gu&k=go^v:minor|gon&k=go n:prop|Lajamanu case:all|_jirri&g=ALL !`

I've tried to replicate CLAN's MOR command, so punctuation is handled in a similar way, homographs have all the options listed with a `^` and anything starting with a capital letter has `n:prop`. And if you type something that's not in the lexicon, you get something like:

`Not-in-lexicon:supercalifragilisticexpialidocious`

When you're done, simply type `exit`.

### Copying to clipboard
To save myself the step of highlighting the mor-codes and pressing command+C, I added an option so that when you type in *kayirra*, it not only prints `adv:loc|kayirra&g=north` to your terminal, it also copies the code to your clipboard. So you can quickly jump back to your transcript and paste it in. When you're entering the command for the script, just add `-c`.

### Setting up an alias
If this is something you want to use all the time, you can add an alias to your [bash profile](https://natelandau.com/my-mac-osx-bash_profile/) so you don't have to type the whole command and find the lexicon files each time. I open up my `~/.bashrc` file, and add this line:

```
alias lookup = 'morCodeLookup.py -l /Users/swilmoth/Dropbox/appencoedlinternship/kri/lex/lex_gurindji.cut /Users/swilmoth/Dropbox/appencoedlinternship/kri/lex/lex_kriolgen.cut'
```
Next time, the only command I need is `lookup`, or `lookup -c`.
