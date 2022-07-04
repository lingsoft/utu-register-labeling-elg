import os
import sys
import unicodedata


registers = {
        "HI": "How-to/Instructions",
        "ID": "Interactive discussion",
        "IN": "Informational description",
        "IP": "Informational persuasion",
        "LY": "Lyrical",
        "NA": "Narrative",
        "OP": "Opinion",
        "SP": "Spoken",
        "av": "Advice",
        "ds": "Description with intent to sell",
        "dtp": "Description of a thing or a person",
        "ed": "News & opinion blog or editorial",
        "en": "Encyclopedia article",
        "fi": "FAQ",
        "it": "Interview",
        "lt": "Legal terms and conditions",
        "nb": "Narrative blog",
        "ne": "News report",
        "ob": "Opinion blog",
        "ra": "Research article",
        "re": "Recipe",
        "rs": "Religious blog / sermon",
        "rv": "Review",
        "sr": "Sports report"
}

punct_chars = set([
    chr(i) for i in range(sys.maxunicode)
    if (unicodedata.category(chr(i)).startswith('P') or
        ((i >= 33 and i <= 47) or (i >= 58 and i <= 64) or
         (i >= 91 and i <= 96) or (i >= 123 and i <= 126)))
])

translation_table = str.maketrans({ c: ' '+c+' ' for c in punct_chars })


# Basic tokenizer from keras-bert-ner by TurkuNLP. MIT license.
def basic_tokenize(text):
    return text.translate(translation_table).split()


def full_register_name(label):
    if label in registers:
        return label, registers[label]
    else:
        return label, "Unknown"
