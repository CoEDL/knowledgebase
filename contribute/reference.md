---
title: Reference
date: 2017-04-24
author: Nay San
categories:
    - Contribute
---

A reference manual and style guide for writing CoEDL Knowledge Base posts.

<!--more-->

## File structure

Create a folder named with `date_post_title` in `posts`. Save your markdown file as `index.md` in that folder, along with any images you use.  This will enable images to show while writing with MacDown as well as when the content is published. The image code is simply `![Alt Text](filename.png)`.

```tree

└── posts
    ├── 20170501_a-post-without-images
    │   └── index.md
    │
    └── 20170509_a-post-with-images
        ├── image_1.png
        ├── image_2.png
        └── index.md
  
```


## Naming

Please use kebab-case for permalinks e.g., 

    permalink: my-post-title

and ensure the post's folder is named with DATE_permalink e.g., 

    20170901_my-post-title



## Interlinear glossing

In Markdown posts, you can enter glosses in the following manner (gloss texts separated by line breaks, using brackets `{ .. }` to group things together where necessary):

```
{{%/* gloss */%}}
Die Umgangssprache ist ein Teil des menschlichen Organismus und nicht weniger kompliziert als dieser.

/di: ʊmgaŋsʃpra:xə ɪst aɪn taɪl dɛs mɛnʃlɪçən ɔrganɪsmʊs ʊnt nɪçt ve:nɪgɐ kɔmpli:tsi:rt als di:zɐ/

DET.NOM.F.SG {colloquial language} be.3SG.PRS DET.NOM.M.SG part DET.GEN.M.SG human-ADJ-AGR.GEN.M.SG organism and NEG less-CMPR complicated CMPR DET-AGR.M.SG

the {colloquial language} is a part {of the} human organism and not less complicated than it

'Colloquial language is a part of the human organism and is not less complicated than it.' — Wittgenstein, Tractatus Logico-Philosophicus, 4.002
{{%/* /gloss */%}}
```

which will render as

{{% gloss %}}
Die Umgangssprache ist ein Teil des menschlichen Organismus und nicht weniger kompliziert als dieser.

/di: ʊmgaŋsʃpra:xə ɪst aɪn taɪl dɛs mɛnʃlɪçən ɔrganɪsmʊs ʊnt nɪçt ve:nɪgɐ kɔmpli:tsi:rt als di:zɐ/

DET.NOM.F.SG {colloquial language} be.3SG.PRS DET.NOM.M.SG part DET.GEN.M.SG human-ADJ-AGR.GEN.M.SG organism and NEG less-CMPR complicated CMPR DET-AGR.M.SG

the {colloquial language} is a part {of the} human organism and not less complicated than it

'Colloquial language is a part of the human organism and is not less complicated than it.' — Wittgenstein, Tractatus Logico-Philosophicus, 4.002
{{% /gloss %}}

Example taken from [Leipzig.js page](http://bdchauvette.net/leipzig.js/) (the codes that renders the glosses), with an additional IPA line.
