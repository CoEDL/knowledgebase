---
# Auto-Chunking Audio Files into Intonational Phrases
author: T. Mark Ellison
date: 2017-05-01
tags:
    - Segmentation
    - Intonational Phrase
    - Silence
    - PRAAT
categories:
    - Tips
---

[Eri Kashima](https://yammeringon.wordpress.com/) and I have found a neat way of chunking speech from the audio file, as a first step in transcription. Initial efforts using silence-detection in ELAN were not successful. Instead, we found that PRAAT's silence detection did the job quite well once the right parameters were chosen.

We use PRAAT's **Annotate &gt;&gt; To TextGrid (silences)...** option from the PRAAT file window. This option is available once you have loaded the *.wav* file. Our parameter settings are:

* **Minimum pitch** 70Hz
* **Silence threshold (dB):** -35
* **Minimum silent interval duration(s):** 0.25
* **Minimum sounding interval duration(s):** 0.1
* **Silent interval label:** (empty)
* **Sounding interval label:** \*\*\*

A detailed walkthrough - of chunking by PRAAT for a file normally explored in ELAN - can be seen on [Eri's blog page](https://yammeringon.wordpress.com/2017/05/01/elanpraat-machine-segmenting/) on the topic.