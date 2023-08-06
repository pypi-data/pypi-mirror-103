|PyPI version| |DOI| |nlptasks| |Total alerts| |Language grade: Python|
|deepcode|

nlptasks
========

A collection of boilerplate code for various NLP tasks with standardized
input and output data types to make it easier to combine NLP tasks with
different libraries and models. The main focus lies on the **German**
language, multi-lingual models that covers German and its dialects. Only
rule-based algorithms or pre-trained models that do not require training
are used.

Please consult the `appendix <#appendix>`__ for `installation
instructions <#installation>`__.

Usage
=====

In the following

**Table of Contents**

-  `Sentence Boundary Disambiguation
   (SBD) <#sentence-boundary-disambiguation>`__
-  `Word Tokenization <#word-tokenization>`__
-  `Lemmatization <#lemmatization>`__
-  Part-of-Speech (PoS) Tagging

   -  `PoS tags to ID sequences <#pos-tagging---id-sequences>`__
   -  `PoS tags and Morphological Features to mask
      sequences <#pos-tagging---mask-sequences>`__

-  Named Entity Recognition (NER)

   -  `NER-tags to ID
      sequences <#named-entity-recognition---id-sequences>`__
   -  `NER-tags and Chunks to mask
      sequences <#named-entity-recognition---mask-sequences>`__

-  Dependency Relations

   -  `Parent Node ID and relation
      type <#dependency-relations---parents>`__
   -  `Children Nodes of a token <#dependency-relations---children>`__
   -  `Trees as mask indices <#dependency-relations---trees>`__

-  `Meta Information <#meta-information>`__

Sentence Boundary Disambiguation
--------------------------------

SBD is about splitting a text into sentences (Synonyms: sentence
splitting, sentence segmentation, or sentence boundary detection).

**Input:**

-  A list of M **documents** as string (data type: ``List[str]``)

**Output:**

-  A list of K **sentences** as string (data type: ``List[str]``)

**Usage:**

.. code:: py

   import nlptasks as nt
   import nlptasks.sbd
   docs = [
       "Die Kuh ist bunt. Die Bäuerin mäht die Wiese.", 
       "Ein anderes Dokument: Ganz super! Oder nicht?"]
   myfn = nt.sbd.factory(name="somajo")
   sents = myfn(docs)
   print(sents)

Example output:

::

   [
       'Die Kuh ist bunt.', 
       'Die Bäuerin mäht die Wiese.', 
       'Ein anderes Dokument: Ganz super!', 
       'Oder nicht?'
   ]

**Algorithms:**

+---------------+-----------------+---------------------+-------------+
| Factory       | Package         | Algorithm           | Notes       |
| ``name``      |                 |                     |             |
+===============+=================+=====================+=============+
| `             | ``de_core_      | Rule-based          | `           |
| `'spacy-de'`` | news_lg-2.3.0`` | tokenization        | 10.5281/zen |
|               |                 | followed by         | odo.1212303 |
|               |                 | Dependency Parsing  |  <https://d |
|               |                 | for SBD             | oi.org/10.5 |
|               |                 |                     | 281/zenodo. |
|               |                 |                     | 1212303>`__ |
+---------------+-----------------+---------------------+-------------+
| ``            | ``s             | Char-based Bi-LSTM  | `Qi et.     |
| 'stanza-de'`` | tanza==1.1.*``, | + 1D-CNN Dependency | al. (2018)  |
|               | ``de``          | Parser for          | <https://nl |
|               |                 | Tokenization, MWT   | p.stanford. |
|               |                 | and SBD             | edu/pubs/qi |
|               |                 |                     | 2018univers |
|               |                 |                     | al.pdf>`__, |
|               |                 |                     | `GitHub <ht |
|               |                 |                     | tps://githu |
|               |                 |                     | b.com/stanf |
|               |                 |                     | ordnlp/stan |
|               |                 |                     | za/tree/mas |
|               |                 |                     | ter/stanza/ |
|               |                 |                     | models>`__, |
|               |                 |                     | `10.18      |
|               |                 |                     | 653/v1/2020 |
|               |                 |                     | .acl-demos. |
|               |                 |                     | 14 <http:// |
|               |                 |                     | dx.doi.org/ |
|               |                 |                     | 10.18653/v1 |
|               |                 |                     | /2020.acl-d |
|               |                 |                     | emos.14>`__ |
+---------------+-----------------+---------------------+-------------+
| ``'nlt        | ``nltk==3.5``,  | Punkt Tokenizer,    | `Kiss and   |
| k-punkt-de'`` | ``german``      | rule-based          | Strunk      |
|               |                 |                     | (20         |
|               |                 |                     | 06) <https: |
|               |                 |                     | //www.aclwe |
|               |                 |                     | b.org/antho |
|               |                 |                     | logy/J06-40 |
|               |                 |                     | 03.pdf>`__, |
|               |                 |                     | `Source     |
|               |                 |                     | Code <http  |
|               |                 |                     | s://www.nlt |
|               |                 |                     | k.org/_modu |
|               |                 |                     | les/nltk/to |
|               |                 |                     | kenize/punk |
|               |                 |                     | t.html>`__, |
|               |                 |                     | `10.1162/co |
|               |                 |                     | li.2006.32. |
|               |                 |                     | 4.485 <http |
|               |                 |                     | ://dx.doi.o |
|               |                 |                     | rg/10.1162/ |
|               |                 |                     | coli.2006.3 |
|               |                 |                     | 2.4.485>`__ |
+---------------+-----------------+---------------------+-------------+
| ``            | ``S             | rule-based          | `Proisl and |
| 'somajo-de'`` | oMaJo==2.1.1``, |                     | Uhrig       |
|               | ``de_CMC``      |                     | (2016       |
|               |                 |                     | ) <http://a |
|               |                 |                     | clweb.org/a |
|               |                 |                     | nthology/W1 |
|               |                 |                     | 6-2607>`__, |
|               |                 |                     | `Git        |
|               |                 |                     | Hub <https: |
|               |                 |                     | //github.co |
|               |                 |                     | m/tsproisl/ |
|               |                 |                     | SoMaJo>`__, |
|               |                 |                     | `10.18653/  |
|               |                 |                     | v1/W16-2607 |
|               |                 |                     |  <http://dx |
|               |                 |                     | .doi.org/10 |
|               |                 |                     | .18653/v1/W |
|               |                 |                     | 16-2607>`__ |
+---------------+-----------------+---------------------+-------------+
| ``'spa        | `               | rule-based          | `           |
| cy-rule-de'`` | `spacy==2.3.0`` |                     | Sentencizer |
|               |                 |                     | class <http |
|               |                 |                     | s://spacy.i |
|               |                 |                     | o/api/sente |
|               |                 |                     | ncizer>`__, |
|               |                 |                     | `           |
|               |                 |                     | 10.5281/zen |
|               |                 |                     | odo.1212303 |
|               |                 |                     |  <https://d |
|               |                 |                     | oi.org/10.5 |
|               |                 |                     | 281/zenodo. |
|               |                 |                     | 1212303>`__ |
+---------------+-----------------+---------------------+-------------+

**Notes:**

-  Dependency parser based SBDs (e.g. ``'spacy'``, ``'stanza'``) are
   more suitable for documents with typos (e.g. ``','`` instead of
   ``'.'``, ``' .'`` instead of ``'. '``) or missing punctuation.
-  Rule-based based SBD algorithms (e.g. ``'nltk_punkt'``, ``'somajo'``,
   ``'spacy_rule'``) are more suitable for documents that can be assumed
   error free, i.e. it’s very likely that spelling and grammar rules are
   being followed by the author, e.g. newspaper articles, published
   books, reviewed articles.

Word Tokenization
-----------------

A word consists of one or multiples characters, and has a meaning.
Depending on the language, the rules for setting the **word boundaries**
have phonetic, orthographic, morphological, syntactic, semantic or other
reasons. In alphabetic languages like German, the space is usually used
to mark a word boundary. That’s why *whitespace tokenization*
(e.g. ``mystring.split(" ")``) is widespread quick hack among coders.

**Input:**

-  A list of K **sentences** as string (data type: ``List[str]``)

**Output:**

-  A list of K **token sequences** (data type: ``List[List[str]]``)

**Usage:**

.. code:: py

   import nlptasks as nt
   import nlptasks.token
   sentences = [
       "Die Kuh ist bunt.", 
       "Die Bäuerin mäht die Wiese."]
   myfn = nt.token.factory(name="stanza-de")
   sequences = myfn(sentences)
   print(sequences)

Example output

::

   [
       ['Die', 'Kuh', 'ist', 'bunt', '.'], 
       ['Die', 'Bäuerin', 'mäht', 'die', 'Wiese', '.']
   ]

**Algorithms:**

+---------------+-----------------+---------------------+-------------+
| Factory       | Package         | Algorithm           | Notes       |
| ``name``      |                 |                     |             |
+===============+=================+=====================+=============+
| `             | ``de_core_      | Rule-based          | `           |
| `'spacy-de'`` | news_lg-2.3.0`` | tokenization        | Docs <https |
|               |                 |                     | ://spacy.io |
|               |                 |                     | /usage/ling |
|               |                 |                     | uistic-feat |
|               |                 |                     | ures#tokeni |
|               |                 |                     | zation>`__, |
|               |                 |                     | `           |
|               |                 |                     | 10.5281/zen |
|               |                 |                     | odo.1212303 |
|               |                 |                     |  <https://d |
|               |                 |                     | oi.org/10.5 |
|               |                 |                     | 281/zenodo. |
|               |                 |                     | 1212303>`__ |
+---------------+-----------------+---------------------+-------------+
| ``            | ``s             | Char-based Bi-LSTM  | `Qi et.     |
| 'stanza-de'`` | tanza==1.1.*``, | + 1D-CNN Dependency | al. (2018)  |
|               | ``de``          | Parser for          | <https://nl |
|               |                 | Tokenization, MWT   | p.stanford. |
|               |                 | and SBD             | edu/pubs/qi |
|               |                 |                     | 2018univers |
|               |                 |                     | al.pdf>`__, |
|               |                 |                     | `GitHub <ht |
|               |                 |                     | tps://githu |
|               |                 |                     | b.com/stanf |
|               |                 |                     | ordnlp/stan |
|               |                 |                     | za/tree/mas |
|               |                 |                     | ter/stanza/ |
|               |                 |                     | models>`__, |
|               |                 |                     | `10.18      |
|               |                 |                     | 653/v1/2020 |
|               |                 |                     | .acl-demos. |
|               |                 |                     | 14 <http:// |
|               |                 |                     | dx.doi.org/ |
|               |                 |                     | 10.18653/v1 |
|               |                 |                     | /2020.acl-d |
|               |                 |                     | emos.14>`__ |
+---------------+-----------------+---------------------+-------------+

Lemmatization
-------------

A lemma is the basic form or canonical form of a **set of words**
(e.g. a lemma and its flexions). In dictionaries, lemmata are used as
**headwords**, and thus, referred to as citation form or dictionary
form.

**Input:**

-  A list of **token sequences** (data type: ``List[List[str]]``)

**Outputs:**

-  A list of **ID sequences** (data type: ``List[List[int]]``)
-  Vocabulary with ``ID:Lemma`` mapping (data type: ``List[str]``)

**Usage:**

.. code:: py

   import nlptasks as nt
   import nlptasks.lemma
   sequences = [
       ['Die', 'Kuh', 'ist', 'bunt', '.'], 
       ['Die', 'Bäuerin', 'mäht', 'die', 'Wiese', '.']
   ]
   myfn = nt.lemma.factory(name="spacy")
   idseqs, VOCAB = myfn(sequences, min_occurrences=0)
   print(idseqs)
   print(VOCAB)

Example output

::

   [[5, 2, 7, 4, 0], [5, 1, 6, 5, 3, 0]]
   ['.', 'Bäuerin', 'Kuh', 'Wiese', 'bunt', 'der', 'mähen', 'sein', '[UNK]']

**Algorithms:**

+---------------+-----------------+---------------------+-------------+
| Factory       | Package         | Algorithm           | Notes       |
| ``name``      |                 |                     |             |
+===============+=================+=====================+=============+
| `             | ``de_core_      | Rule-based          | `           |
| `'spacy-de'`` | news_lg-2.3.0`` | tokenization        | Docs <https |
|               |                 |                     | ://spacy.io |
|               |                 |                     | /usage/ling |
|               |                 |                     | uistic-feat |
|               |                 |                     | ures#tokeni |
|               |                 |                     | zation>`__, |
|               |                 |                     | `           |
|               |                 |                     | 10.5281/zen |
|               |                 |                     | odo.1212303 |
|               |                 |                     |  <https://d |
|               |                 |                     | oi.org/10.5 |
|               |                 |                     | 281/zenodo. |
|               |                 |                     | 1212303>`__ |
+---------------+-----------------+---------------------+-------------+
| ``            | ``s             | n.a.                | `Qi et.     |
| 'stanza-de'`` | tanza==1.1.*``, |                     | al. (2018), |
|               | ``de``          |                     | Ch.         |
|               |                 |                     | 2.3         |
|               |                 |                     | <https://nl |
|               |                 |                     | p.stanford. |
|               |                 |                     | edu/pubs/qi |
|               |                 |                     | 2018univers |
|               |                 |                     | al.pdf>`__, |
|               |                 |                     | `GitHub <ht |
|               |                 |                     | tps://githu |
|               |                 |                     | b.com/stanf |
|               |                 |                     | ordnlp/stan |
|               |                 |                     | za/tree/mas |
|               |                 |                     | ter/stanza/ |
|               |                 |                     | models>`__, |
|               |                 |                     | `10.18      |
|               |                 |                     | 653/v1/2020 |
|               |                 |                     | .acl-demos. |
|               |                 |                     | 14 <http:// |
|               |                 |                     | dx.doi.org/ |
|               |                 |                     | 10.18653/v1 |
|               |                 |                     | /2020.acl-d |
|               |                 |                     | emos.14>`__ |
+---------------+-----------------+---------------------+-------------+

PoS-Tagging - ID Sequences
--------------------------

With PoS tagging (Part-of-Speech) every word in a sentence is assigned a
grammatical attribute. The list of grammatical attributes is called
**tagset**.

The routines ``nlptasks.pos`` will run a PoS tagger on each word token
of a sequences, and return ID sequences, whereas the IDs map to the PoS
tagset.

**Input:**

-  A list of **token sequences** (data type: ``List[List[str]]``)

**Outputs:**

-  A list of **ID sequences** (data type: ``List[List[int]]``)
-  Vocabulary with ``ID:postag`` mapping, i.e. the “tag set” (data type:
   ``List[str]``)

**Usage:**

.. code:: py

   import nlptasks as nt
   import nlptasks.pos
   sequences = [
       ['Die', 'Kuh', 'ist', 'bunt', '.'], 
       ['Die', 'Bäuerin', 'mäht', 'die', 'Wiese', '.']
   ]
   myfn = nt.pos.factory(name="spacy")
   idseqs, TAGSET = myfn(sequences, maxlen=4)
   print(idseqs)

Example output

::

   [[19, 41, 4, 2], [48, 10, 19, 2]]

**Algorithms:**

+---------------+-----------------+---------------------+-------------+
| Factory       | Package         | Algorithm           | Notes       |
| ``name``      |                 |                     |             |
+===============+=================+=====================+=============+
| `             | ``de_core_      | multi-task CNN      | `Docs <http |
| `'spacy-de'`` | news_lg-2.3.0`` |                     | s://spacy.i |
|               |                 |                     | o/usage/lin |
|               |                 |                     | guistic-fea |
|               |                 |                     | tures#pos-t |
|               |                 |                     | agging>`__, |
|               |                 |                     | `           |
|               |                 |                     | 10.5281/zen |
|               |                 |                     | odo.1212303 |
|               |                 |                     |  <https://d |
|               |                 |                     | oi.org/10.5 |
|               |                 |                     | 281/zenodo. |
|               |                 |                     | 1212303>`__ |
+---------------+-----------------+---------------------+-------------+
| ``            | ``s             | Bi-LSTM with a)     | `Qi et.     |
| 'stanza-de'`` | tanza==1.1.*``, | word2vec, b) own    | al. (2018), |
|               | ``de``          | embedding layer, c) | Ch.         |
|               |                 | char-based          | 2.2         |
|               |                 | embedding as input  | <https://nl |
|               |                 |                     | p.stanford. |
|               |                 |                     | edu/pubs/qi |
|               |                 |                     | 2018univers |
|               |                 |                     | al.pdf>`__, |
|               |                 |                     | `GitHub <ht |
|               |                 |                     | tps://githu |
|               |                 |                     | b.com/stanf |
|               |                 |                     | ordnlp/stan |
|               |                 |                     | za/tree/mas |
|               |                 |                     | ter/stanza/ |
|               |                 |                     | models>`__, |
|               |                 |                     | `10.18      |
|               |                 |                     | 653/v1/2020 |
|               |                 |                     | .acl-demos. |
|               |                 |                     | 14 <http:// |
|               |                 |                     | dx.doi.org/ |
|               |                 |                     | 10.18653/v1 |
|               |                 |                     | /2020.acl-d |
|               |                 |                     | emos.14>`__ |
+---------------+-----------------+---------------------+-------------+
| `             | ``              |                     | `Docs <h    |
| `'flair-de'`` | flair==0.6.*``, |                     | ttps://gith |
|               | ``de-pos-u      |                     | ub.com/flai |
|               | d-hdt-v0.5.pt`` |                     | rNLP/flair/ |
|               |                 |                     | blob/master |
|               |                 |                     | /resources/ |
|               |                 |                     | docs/TUTORI |
|               |                 |                     | AL_2_TAGGIN |
|               |                 |                     | G.md#german |
|               |                 |                     | -models>`__ |
+---------------+-----------------+---------------------+-------------+
| ``'s          | ``1.7.1``       | Perceptron          | `Proisl     |
| omeweta-de'`` |                 |                     | (20         |
|               |                 |                     | 18) <http:/ |
|               |                 |                     | /www.lrec-c |
|               |                 |                     | onf.org/pro |
|               |                 |                     | ceedings/lr |
|               |                 |                     | ec2018/pdf/ |
|               |                 |                     | 49.pdf>`__, |
|               |                 |                     | `Docs <ht   |
|               |                 |                     | tps://githu |
|               |                 |                     | b.com/tspro |
|               |                 |                     | isl/SoMeWeT |
|               |                 |                     | a#usage>`__ |
+---------------+-----------------+---------------------+-------------+
| ``'somew      | ``1.7.1``       | Perceptron          | `Proisl     |
| eta-web-de'`` |                 |                     | (20         |
|               |                 |                     | 18) <http:/ |
|               |                 |                     | /www.lrec-c |
|               |                 |                     | onf.org/pro |
|               |                 |                     | ceedings/lr |
|               |                 |                     | ec2018/pdf/ |
|               |                 |                     | 49.pdf>`__, |
|               |                 |                     | `Docs <ht   |
|               |                 |                     | tps://githu |
|               |                 |                     | b.com/tspro |
|               |                 |                     | isl/SoMeWeT |
|               |                 |                     | a#usage>`__ |
+---------------+-----------------+---------------------+-------------+

PoS-Tagging - Mask Sequences
----------------------------

The PoS tagger returns UPOS and UD feats (v2) for a token,
e.g. ``"DET"`` and
``"Case=Gen|Definite=Def|Gender=Neut|Number=Sing|PronType=Art"``. All
information are boolean encoded, i.e. one token (column) can have one or
more 1s.

**Input:**

-  A list of **token sequences** (data type: ``List[List[str]]``)

**Outputs:**

-  A list of **index pairs of a logical matrix** (data type:
   ``List[List[Tuple[int, int]]]``)
-  A list with with original sequence length
-  Combined UPOS and UD feats Scheme

**Usage:**

.. code:: py

   import nlptasks as nt
   import nlptasks.pos2
   sequences = [
       ['Die', 'Frau', 'arbeit', 'in', 'der', 'UN', '.'], 
       ['Angela', 'Merkel', 'mäht', 'die', 'Wiese', '.']
   ]
   myfn = nt.pos2.factory(name="stanza-de")
   maskseqs, seqlen, SCHEME = myfn(sequences)
   print(maskseqs)
   print(seqlen)
   print(SCHEME)

Example output

::

   [
       [
           (5, 0), (112, 0), (115, 0), (41, 0), (77, 0), (17, 0), (7, 1),
           ...
           (11, 5), (100, 5), (41, 5), (77, 5), (12, 6)
       ],
       [
           (11, 0), (112, 0), (41, 0), (77, 0), (11, 1), (112, 1), (41, 1), 
           ... 
           (17, 3), (7, 4), (110, 4), (41, 4), (77, 4), (12, 5)]
       ]
   [7, 6]
   ['ADJ', 'ADP', ... 'VERB', 'X', 'PronType=Art', ..., 'Clusivity=In']

**Algorithms:**

+---------------+-----------------+---------------------+-------------+
| Factory       | Package         | Algorithm           | Notes       |
| ``name``      |                 |                     |             |
+===============+=================+=====================+=============+
| ``            | ``s             | Bi-LSTM with a)     | `Qi et.     |
| 'stanza-de'`` | tanza==1.1.*``, | word2vec, b) own    | al. (2018), |
|               | ``de``          | embedding layer, c) | Ch.         |
|               |                 | char-based          | 2.2         |
|               |                 | embedding as input  | <https://nl |
|               |                 |                     | p.stanford. |
|               |                 |                     | edu/pubs/qi |
|               |                 |                     | 2018univers |
|               |                 |                     | al.pdf>`__, |
|               |                 |                     | `GitHub <ht |
|               |                 |                     | tps://githu |
|               |                 |                     | b.com/stanf |
|               |                 |                     | ordnlp/stan |
|               |                 |                     | za/tree/mas |
|               |                 |                     | ter/stanza/ |
|               |                 |                     | models>`__, |
|               |                 |                     | `10.18      |
|               |                 |                     | 653/v1/2020 |
|               |                 |                     | .acl-demos. |
|               |                 |                     | 14 <http:// |
|               |                 |                     | dx.doi.org/ |
|               |                 |                     | 10.18653/v1 |
|               |                 |                     | /2020.acl-d |
|               |                 |                     | emos.14>`__ |
+---------------+-----------------+---------------------+-------------+

Named Entity Recognition - ID Sequences
---------------------------------------

The NE-tags without prefix (e.g. ``LOC``, ``PER``) are mapped with IDs,
i.e. ``int``.

**Input:**

-  A list of **token sequences** (data type: ``List[List[str]]``)

**Outputs:**

-  A list of **ID sequences** (data type: ``List[List[int]]``)
-  Vocabulary with ``ID:nerscheme`` mapping (data type: ``List[str]``)

**Usage:**

.. code:: py

   import nlptasks as nt
   import nlptasks.ner
   sequences = [
       ['Die', 'Frau', 'arbeit', 'in', 'der', 'UN', '.'], 
       ['Angela', 'Merkel', 'mäht', 'die', 'Wiese', '.']
   ]
   myfn = nt.ner.factory(name="spacy-de")
   idseqs, SCHEME = myfn(sequences)
   print(idseqs)
   print(SCHEME)

Example output

::

   [[4, 4, 4, 4, 4, 2, 4], [0, 0, 4, 4, 4, 4]]
   ['PER', 'LOC', 'ORG', 'MISC', '[UNK]']

**Algorithms:**

+---------------+-----------------+---------------------+-------------+
| Factory       | Package         | Algorithm           | Notes       |
| ``name``      |                 |                     |             |
+===============+=================+=====================+=============+
| ``'f          | ``              |                     | `Do         |
| lair-multi'`` | flair==0.6.*``, |                     | cs <https:/ |
|               | ``qua           |                     | /github.com |
|               | dner-large.pt`` |                     | /flairNLP/f |
|               |                 |                     | lair/blob/m |
|               |                 |                     | aster/resou |
|               |                 |                     | rces/docs/T |
|               |                 |                     | UTORIAL_2_T |
|               |                 |                     | AGGING.md#m |
|               |                 |                     | ultilingual |
|               |                 |                     | -models>`__ |
+---------------+-----------------+---------------------+-------------+
| `             | ``de_core_      | multi-task CNN      | `Do         |
| `'spacy-de'`` | news_lg-2.3.0`` |                     | cs <https:/ |
|               |                 |                     | /spacy.io/u |
|               |                 |                     | sage/lingui |
|               |                 |                     | stic-featur |
|               |                 |                     | es#named-en |
|               |                 |                     | tities>`__, |
|               |                 |                     | `           |
|               |                 |                     | 10.5281/zen |
|               |                 |                     | odo.1212303 |
|               |                 |                     |  <https://d |
|               |                 |                     | oi.org/10.5 |
|               |                 |                     | 281/zenodo. |
|               |                 |                     | 1212303>`__ |
+---------------+-----------------+---------------------+-------------+
| ``            | ``s             | n.a.                | `Do         |
| 'stanza-de'`` | tanza==1.1.*``, |                     | cs <https:/ |
|               | ``de``          |                     | /stanfordnl |
|               |                 |                     | p.github.io |
|               |                 |                     | /stanza/ava |
|               |                 |                     | ilable_mode |
|               |                 |                     | ls.html#ava |
|               |                 |                     | ilable-ner- |
|               |                 |                     | models>`__, |
|               |                 |                     | `GitHub <ht |
|               |                 |                     | tps://githu |
|               |                 |                     | b.com/stanf |
|               |                 |                     | ordnlp/stan |
|               |                 |                     | za/tree/mas |
|               |                 |                     | ter/stanza/ |
|               |                 |                     | models>`__, |
|               |                 |                     | `10.18      |
|               |                 |                     | 653/v1/2020 |
|               |                 |                     | .acl-demos. |
|               |                 |                     | 14 <http:// |
|               |                 |                     | dx.doi.org/ |
|               |                 |                     | 10.18653/v1 |
|               |                 |                     | /2020.acl-d |
|               |                 |                     | emos.14>`__ |
+---------------+-----------------+---------------------+-------------+

Named Entity Recognition - Mask Sequences
-----------------------------------------

The NER tagger will return NE-tags with IOB-prefix, e.g. ``E-LOC``. Both
information are boolean encoded, i.e. one token (column) can have one or
two 1s.

**Input:**

-  A list of **token sequences** (data type: ``List[List[str]]``)

**Outputs:**

-  A list of **index pairs of a logical matrix** (data type:
   ``List[List[Tuple[int, int]]]``)
-  A list with with original sequence length
-  NER-Scheme tags

**Usage:**

.. code:: py

   import nlptasks as nt
   import nlptasks.ner2
   sequences = [
       ['Die', 'Frau', 'arbeit', 'in', 'der', 'UN', '.'], 
       ['Angela', 'Merkel', 'mäht', 'die', 'Wiese', '.']
   ]
   myfn = nt.ner2.factory(name="flair-multi")
   maskseqs, seqlen, SCHEME = myfn(sequences)
   print(maskseqs)
   print(seqlen)
   print(SCHEME)

Example output

::

   [
       [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (8, 5), (2, 5), (6, 6)], 
       [(4, 0), (0, 0), (7, 1), (0, 1), (6, 2), (6, 3), (6, 4), (6, 5)]
   ]
   ['PER', 'LOC', 'ORG', 'MISC', 'B', 'I', 'O', 'E', 'S']

**Algorithms:**

+-----------------+-----------------+-----------+-----------------+
| Factory         | Package         | Algorithm | Notes           |
| ``name``        |                 |           |                 |
+=================+=================+===========+=================+
| ``              | ``              |           | `Docs <h        |
| 'flair-multi'`` | flair==0.6.*``, |           | ttps://github.c |
|                 | ``qua           |           | om/flairNLP/fla |
|                 | dner-large.pt`` |           | ir/blob/master/ |
|                 |                 |           | resources/docs/ |
|                 |                 |           | TUTORIAL_2_TAGG |
|                 |                 |           | ING.md#multilin |
|                 |                 |           | gual-models>`__ |
+-----------------+-----------------+-----------+-----------------+

Dependency Relations - Parents
------------------------------

In CoNLL-U, spacy, stanza, etc. the ``head`` attribute refers to the
parent node of a token, i.e. it’s an adjacency list.

**Input:**

-  A list of **token sequences** (data type: ``List[List[str]]``)

**Outputs:**

-  A list of **index pairs of an adjacency matrix** (data type:
   ``List[List[Tuple[int, int]]]``) for parent relation to a token
-  A list with with original sequence length

**Usage:**

.. code:: py

   import nlptasks as nt
   import nlptasks.dephead
   sequences = [
       ['Die', 'Kuh', 'ist', 'bunt', '.'], 
       ['Die', 'Bäuerin', 'mäht', 'die', 'Wiese', '.']
   ]
   myfn = nt.dephead.factory("stanza-de")
   maskseqs, seqlens = myfn(
       sequences, maxlen=4, padding='pre', truncating='pre')
   print(maskseqs)
   print(seqlens)

Example output

::

   [
       [
           (45, 0), (46, 1), (46, 2), (46, 3), (46, 4),
           (19, 0), (36, 1), (43, 2), (27, 3), (32, 4)
       ],
       [
           (45, 0), (46, 1), (46, 2), (48, 3), (46, 4), (46, 5),
           (19, 0), (36, 1), (43, 2), (19, 3), (21, 4), (32, 5)
       ]
   ]
   [5, 6]

**Algorithms:**

+---------------+-----------------+---------------------+-------------+
| Factory       | Package         | Algorithm           | Notes       |
| ``name``      |                 |                     |             |
+===============+=================+=====================+=============+
| `             | ``de_core_      | multi-task CNN      | `Docs       |
| `'spacy-de'`` | news_lg-2.3.0`` |                     |  <https://s |
|               |                 |                     | pacy.io/usa |
|               |                 |                     | ge/linguist |
|               |                 |                     | ic-features |
|               |                 |                     | #dependency |
|               |                 |                     | -parse>`__, |
|               |                 |                     | `           |
|               |                 |                     | 10.5281/zen |
|               |                 |                     | odo.1212303 |
|               |                 |                     |  <https://d |
|               |                 |                     | oi.org/10.5 |
|               |                 |                     | 281/zenodo. |
|               |                 |                     | 1212303>`__ |
+---------------+-----------------+---------------------+-------------+
| ``            | ``s             | n.a.                | `Do         |
| 'stanza-de'`` | tanza==1.1.*``, |                     | cs <https:/ |
|               | ``de``          |                     | /stanfordnl |
|               |                 |                     | p.github.io |
|               |                 |                     | /stanza/ava |
|               |                 |                     | ilable_mode |
|               |                 |                     | ls.html#ava |
|               |                 |                     | ilable-ner- |
|               |                 |                     | models>`__, |
|               |                 |                     | `GitHub <ht |
|               |                 |                     | tps://githu |
|               |                 |                     | b.com/stanf |
|               |                 |                     | ordnlp/stan |
|               |                 |                     | za/tree/mas |
|               |                 |                     | ter/stanza/ |
|               |                 |                     | models>`__, |
|               |                 |                     | `10.18      |
|               |                 |                     | 653/v1/2020 |
|               |                 |                     | .acl-demos. |
|               |                 |                     | 14 <http:// |
|               |                 |                     | dx.doi.org/ |
|               |                 |                     | 10.18653/v1 |
|               |                 |                     | /2020.acl-d |
|               |                 |                     | emos.14>`__ |
+---------------+-----------------+---------------------+-------------+

Dependency Relations - Children
-------------------------------

**Input**

-  A list of **token sequences** (data type: ``List[List[str]]``)

**Outputs**

-  A list of **index pairs of an adjacency matrix** (data type:
   ``List[List[Tuple[int, int]]]``) for children relations to a token.
-  A list with with original sequence length

**Usage:**

.. code:: py

   import nlptasks as nt
   import nlptasks.depchild
   sequences = [
       ['Die', 'Kuh', 'ist', 'bunt', '.'], 
       ['Die', 'Bäuerin', 'mäht', 'die', 'Wiese', '.']
   ]
   myfn = nt.depchild.factory("spacy-de")
   maskseqs, seqlens = myfn(
       sequences, maxlen=4, padding='pre', truncating='pre')
   print(maskseqs)
   print(seqlens)

Example output

::

   [
       [(0, 1), (1, 2), (3, 2), (4, 2)], 
       [(0, 1), (1, 2), (4, 2), (5, 2), (3, 4)]
   ]
   [5, 6]

**Algorithms:**

+---------------+-----------------+---------------------+-------------+
| Factory       | Package         | Algorithm           | Notes       |
| ``name``      |                 |                     |             |
+===============+=================+=====================+=============+
| `             | ``de_core_      | multi-task CNN      | `Docs       |
| `'spacy-de'`` | news_lg-2.3.0`` |                     |  <https://s |
|               |                 |                     | pacy.io/usa |
|               |                 |                     | ge/linguist |
|               |                 |                     | ic-features |
|               |                 |                     | #dependency |
|               |                 |                     | -parse>`__, |
|               |                 |                     | `           |
|               |                 |                     | 10.5281/zen |
|               |                 |                     | odo.1212303 |
|               |                 |                     |  <https://d |
|               |                 |                     | oi.org/10.5 |
|               |                 |                     | 281/zenodo. |
|               |                 |                     | 1212303>`__ |
+---------------+-----------------+---------------------+-------------+

Dependency Relations - Trees
----------------------------

Most **syntax dependency parsers** return tree representations, usually
adjacency list based tree. The ``nlptasks.deptree`` submodule uses the
``treesimi`` package (DOI:
`10.5281/zenodo.4321304 <http://doi.org/10.5281/zenodo.4321304>`__) to
extract subtrees and other tree patterns, which are indexed for a mask
vector.

**Input:**

-  A list of **token sequences** (data type: ``List[List[str]]``)

**Outputs:**

-  For each sentences, a list of mask indices (data type:
   ``List[List[int]]``)
-  Vocabulary with ``ID:Hash`` mapping (data type: ``List[str]``)

**Usage:**

.. code:: py

   import nlptasks as nt
   import nlptasks.deptree
   sequences = [
       ['Die', 'Kuh', 'ist', 'bunt', '.'], 
       ['Die', 'Bäuerin', 'mäht', 'die', 'Wiese', ',', 'aber', 'mit', 'Extra', '.']
   ]
   myfn = nt.deptree.factory("stanza-de")
   indices, VOCAB = myfn(sequences)
   print(indices)

   masked, _ = myfn(sequences, VOCAB=VOCAB, return_mask=True)
   print(masked)

**Example output**

Each index represents a specific tree or subtree pattern that you can
find inside a dependency tree.

::

   [
       [0, 1, 2, 3, 4], 
       [5, 1, 2, 6, 7, 4, 8, 9]
   ]

   [
       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
       [0, 1, 1, 0, 1, 1, 1, 1, 1, 1]
   ]

**Algorithms:**

+---------------+-----------------+---------------------+-------------+
| Factory       | Package         | Algorithm           | Notes       |
| ``name``      |                 |                     |             |
+===============+=================+=====================+=============+
| `             | ``de_core_      | multi-task CNN      | `Docs       |
| `'spacy-de'`` | news_lg-2.3.0`` |                     |  <https://s |
|               |                 |                     | pacy.io/usa |
|               |                 |                     | ge/linguist |
|               |                 |                     | ic-features |
|               |                 |                     | #dependency |
|               |                 |                     | -parse>`__, |
|               |                 |                     | `           |
|               |                 |                     | 10.5281/zen |
|               |                 |                     | odo.1212303 |
|               |                 |                     |  <https://d |
|               |                 |                     | oi.org/10.5 |
|               |                 |                     | 281/zenodo. |
|               |                 |                     | 1212303>`__ |
+---------------+-----------------+---------------------+-------------+
| ``            | ``s             | n.a.                | `Do         |
| 'stanza-de'`` | tanza==1.1.*``, |                     | cs <https:/ |
|               | ``de``          |                     | /stanfordnl |
|               |                 |                     | p.github.io |
|               |                 |                     | /stanza/ava |
|               |                 |                     | ilable_mode |
|               |                 |                     | ls.html#ava |
|               |                 |                     | ilable-ner- |
|               |                 |                     | models>`__, |
|               |                 |                     | `GitHub <ht |
|               |                 |                     | tps://githu |
|               |                 |                     | b.com/stanf |
|               |                 |                     | ordnlp/stan |
|               |                 |                     | za/tree/mas |
|               |                 |                     | ter/stanza/ |
|               |                 |                     | models>`__, |
|               |                 |                     | `10.18      |
|               |                 |                     | 653/v1/2020 |
|               |                 |                     | .acl-demos. |
|               |                 |                     | 14 <http:// |
|               |                 |                     | dx.doi.org/ |
|               |                 |                     | 10.18653/v1 |
|               |                 |                     | /2020.acl-d |
|               |                 |                     | emos.14>`__ |
+---------------+-----------------+---------------------+-------------+

Meta Information
----------------

In order to retrieve the model’s meta information, call

.. code:: py

   import nlptasks as nt
   import nlptasks.meta
   modelmeta = nt.meta.get(name='nltk-punkt-de', module='sbd')
   print(modelmeta)

The meta information could be stored next the annotated text data for
various database management purposes (e.g. reproducibility, detect
changed results due to version changes, compliance with license
conditions, etc.)

.. code:: sh

   {
       'pypi': {
           'name': 'nltk', 'version': '3.5', 'licence': 'Apache-2',
           'isbn': '9780596516499'}, 
       'model': {
           'name': 'punkt', 'file': 'nltk_data/tokenizers/punkt/PY3/german.pickle',
           'modified': '2013-08-23T04:10:02', 'licence': 'Apache-2',
           'doi': '10.1162/coli.2006.32.4.485'}
   }

Appendix
========

Installation
------------

The ``nlptasks`` package is available on the `PyPi
server <https://pypi.org/project/nlptasks/>`__

.. code:: sh

   pip install nlptasks>=0.3.0

Install a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   python3.6 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements-dev.txt
   pip install -r requirements.txt
   python scripts/nlptasks_downloader.py
   bash download_testdata.sh

(If your git repo is stored in a folder with whitespaces, then don’t use
the subfolder ``.venv``. Use an absolute path without whitespaces.)

Python commands
~~~~~~~~~~~~~~~

-  Jupyter for the examples: ``jupyter lab``
-  Check syntax:
   ``flake8 --ignore=F401 --exclude=.venv,data,.github,.pytest_cache,__pycache__``
   or
   ``flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')``
-  Run Unit Tests: ``pytest`` or ``py.test --profile``

Some unit test are excluded from pytest due to troubles (e.g. memory,
timeout) to run these with CI tools (e.g. Github Actions). You can these
manually as follows

.. code:: sh

   # run all files "test/test_*.py"
   py.test --profile
   # excluded unit tests
   py.test test/excluded_pos.py --profile

Publish

.. code:: sh

   pandoc README.md --from markdown --to rst -s -o README.rst
   python setup.py sdist 
   twine upload -r pypi dist/*

Clean up
~~~~~~~~

::

   find . -type f -name "*.pyc" | xargs rm
   find . -type d -name "__pycache__" | xargs rm -r
   rm -r .pytest_cache
   rm -r .venv

Support
~~~~~~~

Please `open an issue <https://github.com/ulf1/nlptasks/issues/new>`__
for support.

Contributing
~~~~~~~~~~~~

Please contribute using `Github
Flow <https://guides.github.com/introduction/flow/>`__. Create a branch,
add commits, and `open a pull
request <https://github.com/ulf1/nlptasks/compare/>`__.

.. |PyPI version| image:: https://badge.fury.io/py/nlptasks.svg
   :target: https://badge.fury.io/py/nlptasks
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4284804.svg
   :target: https://doi.org/10.5281/zenodo.4284804
.. |nlptasks| image:: https://snyk.io/advisor/python/nlptasks/badge.svg
   :target: https://snyk.io/advisor/python/nlptasks
.. |Total alerts| image:: https://img.shields.io/lgtm/alerts/g/ulf1/nlptasks.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/nlptasks/alerts/
.. |Language grade: Python| image:: https://img.shields.io/lgtm/grade/python/g/ulf1/nlptasks.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/nlptasks/context:python
.. |deepcode| image:: https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6InVsZjEiLCJyZXBvMSI6Im5scHRhc2tzIiwiaW5jbHVkZUxpbnQiOmZhbHNlLCJhdXRob3JJZCI6Mjk0NTIsImlhdCI6MTYxOTUzODU2MX0.paACl8jVYem_lr7ouSTsCiQR8mg8GD1dDVHRF-Fr-04
   :target: https://www.deepcode.ai/app/gh/ulf1/nlptasks/_/dashboard?utm_content=gh%2Fulf1%2Fnlptasks
