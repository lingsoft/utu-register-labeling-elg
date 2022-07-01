"""
Basic tokenizer
From keras-bert-ner by TurkuNLP. MIT license.
"""

import os
import sys
import unicodedata

punct_chars = set([
    chr(i) for i in range(sys.maxunicode)
    if (unicodedata.category(chr(i)).startswith('P') or
        ((i >= 33 and i <= 47) or (i >= 58 and i <= 64) or
         (i >= 91 and i <= 96) or (i >= 123 and i <= 126)))
])

translation_table = str.maketrans({ c: ' '+c+' ' for c in punct_chars })


def basic_tokenize(text):
    return text.translate(translation_table).split()
